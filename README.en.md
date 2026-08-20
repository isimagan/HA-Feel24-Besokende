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

When the field is left empty, `select.feel24_chosen_gym` is created so the
active gym can be changed later in Home Assistant.

## Entities

| Entity | Icon | Description |
| --- | --- | --- |
| `sensor.feel24_visitors` | `mdi:shoe-sneaker` | Number of visitors at the selected gym. The entity uses the green Feel24 symbol as its entity picture and the unit `besøkende`. |
| `select.feel24_chosen_gym` | `mdi:weight-lifter` | Selects the gym that controls the visitor sensor. It is only created when the setup wizard is completed without a selected gym. |

## Development

Integration files are located in `custom_components/feel24_visitors/`. The
next development milestone is connecting the sensor to a verified source of
live visitor data.

Keep the version in `manifest.json` synchronized with GitHub releases.

## License

MIT
