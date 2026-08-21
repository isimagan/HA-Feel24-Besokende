"""Async client for the Membro/iBooking API used by Feel24."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import json
from typing import Any

API_BASE_URL = "https://api.ibooking.no/v1/"
COMPANY_ID = 1405
REQUEST_TIMEOUT = 20
USER_AGENT = "HomeAssistant-Feel24Visitors"


class Feel24ApiError(Exception):
    """Base error returned by the Feel24 API."""

    def __init__(self, message: str, status: int | None = None) -> None:
        """Initialize an API error."""
        super().__init__(message)
        self.status = status


class Feel24AuthenticationError(Feel24ApiError):
    """Raised when stored member credentials are rejected."""


class Feel24InvalidPhoneError(Feel24ApiError):
    """Raised when no login challenge can be started for a phone number."""


class Feel24InvalidCodeError(Feel24ApiError):
    """Raised when a login code is rejected."""


class Feel24RateLimitError(Feel24ApiError):
    """Raised when iBooking asks the client to slow down."""


@dataclass(frozen=True, slots=True)
class Feel24AuthChallenge:
    """An in-progress phone login challenge."""

    id: str
    token: str


@dataclass(frozen=True, slots=True)
class Feel24Credentials:
    """Credentials needed for authenticated Feel24 requests."""

    token: str
    user_id: int


class Feel24Api:
    """Talk to the supported API endpoints used by the Feel24 app."""

    def __init__(self, session: Any) -> None:
        """Initialize the API client with Home Assistant's HTTP session."""
        self._session = session

    async def async_start_authentication(
        self, phone: str
    ) -> Feel24AuthChallenge:
        """Start a phone login and request a one-time code."""
        try:
            payload = await self._async_request(
                "POST",
                "auth_challenges",
                params={"company_id": str(COMPANY_ID)},
                json_body={"phone": phone},
            )
        except Feel24RateLimitError:
            raise
        except Feel24ApiError as err:
            if err.status is not None and 400 <= err.status < 500:
                raise Feel24InvalidPhoneError(str(err), err.status) from err
            raise

        challenge_id = payload.get("id")
        challenge_token = payload.get("token")
        if not isinstance(challenge_id, str) or not isinstance(
            challenge_token, str
        ):
            raise Feel24ApiError("The login challenge response was incomplete")

        return Feel24AuthChallenge(challenge_id, challenge_token)

    async def async_complete_authentication(
        self, challenge: Feel24AuthChallenge, code: str
    ) -> Feel24Credentials:
        """Complete a phone challenge and obtain a member token."""
        try:
            payload = await self._async_request(
                "PATCH",
                f"auth_challenges/{challenge.id}",
                params={
                    "include_companies": "1",
                    "for_admin": "0",
                    "company_id": str(COMPANY_ID),
                },
                json_body={"token": challenge.token, "code": code},
            )
        except Feel24RateLimitError:
            raise
        except Feel24ApiError as err:
            if err.status is not None and 400 <= err.status < 500:
                raise Feel24InvalidCodeError(str(err), err.status) from err
            raise

        user_id = _find_feel24_user_id(payload.get("users"))
        if user_id is None:
            raise Feel24ApiError(
                "No Feel24 member was returned for this login"
            )

        token_payload = await self._async_request(
            "POST",
            "auth_challenges/authenticate",
            headers={"X-iBooking-Company-id": str(COMPANY_ID)},
            json_body={
                "auth_token": challenge.token,
                "for_admin": False,
            },
        )
        member_token = token_payload.get("token")
        if not isinstance(member_token, str) or not member_token:
            raise Feel24ApiError("The member token response was incomplete")

        return Feel24Credentials(member_token, user_id)

    async def async_get_visitor_count(
        self, studio_id: int, token: str, user_id: int
    ) -> int:
        """Return the current visitor count for a Feel24 studio."""
        try:
            payload = await self._async_request(
                "GET",
                "presence",
                params={"studio_id": str(studio_id)},
                headers={
                    "X-iBooking-Token": token,
                    "X-iBooking-Company-Id": str(COMPANY_ID),
                    "X-iBooking-User-Id": str(user_id),
                },
            )
        except Feel24ApiError as err:
            if err.status in (401, 403):
                raise Feel24AuthenticationError(str(err), err.status) from err
            raise

        current_sum = _as_int(payload.get("current_sum"))
        if current_sum is None or current_sum < 0:
            raise Feel24ApiError(
                "The visitor response did not contain a valid current_sum"
            )
        return current_sum

    async def _async_request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make one API request and return a JSON object."""
        request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-iBooking-UserAgent": USER_AGENT,
            **(headers or {}),
        }

        async with asyncio.timeout(REQUEST_TIMEOUT):
            async with self._session.request(
                method,
                f"{API_BASE_URL}{path}",
                params=params,
                headers=request_headers,
                json=json_body,
            ) as response:
                try:
                    payload = await response.json(content_type=None)
                except (json.JSONDecodeError, ValueError, TypeError) as err:
                    raise Feel24ApiError(
                        "The Feel24 API returned an invalid response",
                        response.status,
                    ) from err

                if response.status == 429:
                    raise Feel24RateLimitError(
                        _error_message(payload), response.status
                    )
                if response.status >= 400:
                    raise Feel24ApiError(
                        _error_message(payload), response.status
                    )
                if not isinstance(payload, dict):
                    raise Feel24ApiError(
                        "The Feel24 API returned an unexpected response",
                        response.status,
                    )

        return payload


def _find_feel24_user_id(value: Any) -> int | None:
    """Find the member user that belongs to Feel24's company."""
    if not isinstance(value, list):
        return None

    valid_user_ids: list[int] = []
    for user in value:
        if not isinstance(user, dict):
            continue

        user_id = _as_int(user.get("id"))
        if user_id is None:
            continue
        valid_user_ids.append(user_id)

        company_id = _as_int(user.get("company_id"))
        if company_id is None and isinstance(user.get("company"), dict):
            company_id = _as_int(user["company"].get("id"))
        if company_id == COMPANY_ID:
            return user_id

    return valid_user_ids[0] if len(valid_user_ids) == 1 else None


def _as_int(value: Any) -> int | None:
    """Convert API integer values without accepting booleans."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    return None


def _error_message(payload: Any) -> str:
    """Extract a useful but non-secret error message from an API response."""
    if isinstance(payload, dict):
        error = payload.get("error")
        if isinstance(error, dict) and isinstance(error.get("message"), str):
            return error["message"]
        if isinstance(payload.get("message"), str):
            return payload["message"]
    return "The Feel24 API rejected the request"
