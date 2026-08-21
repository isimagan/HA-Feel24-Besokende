![Feel24 logo](https://raw.githubusercontent.com/isimagan/HA-Feel24-Visitors/master/brand/logo.png)

[Norsk](https://github.com/isimagan/HA-Feel24-Visitors/blob/master/README.md) | **English**

# HA Feel24 Visitors

A custom Home Assistant integration for visitor data from Feel24.

This is an unofficial community project and is not developed or supported by
Feel24.

## Installation with HACS

The repository is not listed in the HACS catalogue. Install it by adding it as
a custom repository:

1. Open HACS and select **Custom repositories**.
2. Add `https://github.com/isimagan/HA-Feel24-Visitors`.
3. Select **Integration** as the category.
4. Download **HA Feel24 Visitors** and restart Home Assistant.
5. Open **Settings → Devices & services → Add integration** and select
   **Feel24 Visitors**.

## Configuration

In the configuration wizard, start typing the name of a Feel24 gym to filter
the list of suggestions. Select a suggestion or leave the optional field
empty. An unknown gym name produces an error and cannot be saved.

The first setup asks for the phone number registered with Feel24. The wizard
requests a one-time SMS code from Feel24/iBooking and asks for that code in the
next step. The integration stores the resulting member token and uses it to
fetch the real visitor count. The one-time code is not stored.

After upgrading from version 0.2, Home Assistant requests reauthentication for
the existing entry. Complete the phone and code steps once to activate the
visitor sensor.

Run the wizard more than once to add multiple gyms. Each selected gym gets its
own config entry, device page, and visitor sensor. The same gym cannot be added
twice. New gym entries reuse the existing login, so another SMS code is
normally not needed.

When the field is left empty, `select.feel24_chosen_gym` is created so the
active gym can be changed later in Home Assistant.

## Entities

| Entity | Icon | Description |
| --- | --- | --- |
| `sensor.feel24_visitors` | `mdi:shoe-sneaker` | Number of visitors at the selected gym. The entity uses the green Feel24 symbol as its entity picture and the unit `besøkende`. The `gym` and `gym_id` attributes expose the gym name and iBooking ID. |
| `select.feel24_chosen_gym` | `mdi:weight-lifter` | Selects the gym that controls the visitor sensor. It is only created when the setup wizard is completed without a selected gym. |

The value `0` is a valid, available measurement and means that no visitors are
currently registered at the gym. The sensor only becomes `unavailable` when
the integration cannot retrieve a confirmed value.

Home Assistant may add a suffix to an entity ID when multiple visitor sensors
have the same name. Each sensor appears on its own device page in the
integration.

## Development

Integration files are located in `custom_components/feel24_visitors/`. The
integration uses the same authenticated Membro/iBooking flow and `presence`
endpoint as the Feel24 app. Home Assistant requests reauthentication if the
stored token is invalid or expires.

Keep the version in `manifest.json` synchronized with GitHub releases.

## License

MIT
