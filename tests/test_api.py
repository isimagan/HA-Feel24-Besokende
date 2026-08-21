"""Tests for the Feel24 Membro/iBooking API contract."""

import importlib.util
from pathlib import Path
import sys
import unittest

API_PATH = (
    Path(__file__).parents[1]
    / "custom_components"
    / "feel24_visitors"
    / "api.py"
)
SPEC = importlib.util.spec_from_file_location("feel24_api", API_PATH)
assert SPEC and SPEC.loader
API_MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = API_MODULE
SPEC.loader.exec_module(API_MODULE)

Feel24Api = API_MODULE.Feel24Api
Feel24AuthenticationError = API_MODULE.Feel24AuthenticationError


class FakeResponse:
    """Minimal aiohttp response context manager."""

    def __init__(self, status: int, payload: object) -> None:
        """Initialize a queued response."""
        self.status = status
        self._payload = payload

    async def __aenter__(self):
        """Enter the response context."""
        return self

    async def __aexit__(self, *_args):
        """Exit the response context."""

    async def json(self, *, content_type=None):
        """Return the queued JSON payload."""
        return self._payload


class FakeSession:
    """Queue responses and record API requests."""

    def __init__(self, *responses: FakeResponse) -> None:
        """Initialize a fake session."""
        self.responses = list(responses)
        self.requests: list[tuple[str, str, dict[str, object]]] = []

    def request(self, method: str, url: str, **kwargs):
        """Record a request and return the next response."""
        self.requests.append((method, url, kwargs))
        return self.responses.pop(0)


class Feel24ApiTests(unittest.IsolatedAsyncioTestCase):
    """Verify login and presence request formats."""

    async def test_start_authentication(self) -> None:
        """A phone login creates an iBooking auth challenge."""
        session = FakeSession(
            FakeResponse(200, {"id": "challenge-id", "token": "challenge"})
        )

        challenge = await Feel24Api(session).async_start_authentication(
            "+4799999999"
        )

        self.assertEqual(challenge.id, "challenge-id")
        method, url, request = session.requests[0]
        self.assertEqual(method, "POST")
        self.assertTrue(url.endswith("/v1/auth_challenges"))
        self.assertEqual(request["params"], {"company_id": "1405"})
        self.assertEqual(request["json"], {"phone": "+4799999999"})

    async def test_complete_authentication(self) -> None:
        """The code exchange returns the token and Feel24 user ID."""
        session = FakeSession(
            FakeResponse(
                200,
                {
                    "users": [
                        {"id": 42, "company_id": 1405},
                        {"id": 84, "company_id": 9999},
                    ],
                    "companies": [{"id": 1405}],
                },
            ),
            FakeResponse(200, {"token": "member-token"}),
        )
        challenge = API_MODULE.Feel24AuthChallenge(
            "challenge-id", "challenge-token"
        )

        credentials = await Feel24Api(
            session
        ).async_complete_authentication(challenge, "123456")

        self.assertEqual(credentials.token, "member-token")
        self.assertEqual(credentials.user_id, 42)

        method, url, request = session.requests[0]
        self.assertEqual(method, "PATCH")
        self.assertTrue(url.endswith("/v1/auth_challenges/challenge-id"))
        self.assertEqual(
            request["json"],
            {"token": "challenge-token", "code": "123456"},
        )
        self.assertEqual(request["params"]["include_companies"], "1")

        method, url, request = session.requests[1]
        self.assertEqual(method, "POST")
        self.assertTrue(url.endswith("/v1/auth_challenges/authenticate"))
        self.assertEqual(
            request["json"],
            {"auth_token": "challenge-token", "for_admin": False},
        )
        self.assertEqual(
            request["headers"]["X-iBooking-Company-id"], "1405"
        )

    async def test_fetch_visitor_count(self) -> None:
        """The presence endpoint supplies current_sum for the sensor."""
        session = FakeSession(FakeResponse(200, {"current_sum": "17"}))

        count = await Feel24Api(session).async_get_visitor_count(
            2713, "member-token", 42
        )

        self.assertEqual(count, 17)
        method, url, request = session.requests[0]
        self.assertEqual(method, "GET")
        self.assertTrue(url.endswith("/v1/presence"))
        self.assertEqual(request["params"], {"studio_id": "2713"})
        self.assertEqual(
            request["headers"]["X-iBooking-Token"], "member-token"
        )
        self.assertEqual(request["headers"]["X-iBooking-User-Id"], "42")

    async def test_presence_authentication_error(self) -> None:
        """Rejected stored credentials trigger Home Assistant reauth."""
        session = FakeSession(
            FakeResponse(
                401,
                {"error": {"code": "no_auth", "message": "Invalid token"}},
            )
        )

        with self.assertRaises(Feel24AuthenticationError):
            await Feel24Api(session).async_get_visitor_count(
                2713, "expired-token", 42
            )


if __name__ == "__main__":
    unittest.main()
