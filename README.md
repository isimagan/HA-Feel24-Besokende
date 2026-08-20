<p align="center">
  <img src="brand/icon.png" alt="Feel24 logo" width="320">
</p>

# HA Feel24 Visitors

Home Assistant custom integration for visitor data from Feel24.

## Installation with HACS

HACS can only install from a public GitHub repository. When the integration is
ready for testers:

1. Make this repository public.
2. In HACS, open **Custom repositories**.
3. Add `https://github.com/isimagan/HA-Feel24-Visitors` as an **Integration**.
4. Download **HA Feel24 Visitors** and restart Home Assistant.
5. Open **Settings → Devices & services → Add integration** and select
   **Feel24 Visitors**.

## Configuration

The setup wizard lets you search for a Feel24 gym by typing in the gym field.
Choose one of the suggestions, or leave the optional field empty. An unknown
gym name cannot be submitted. Leaving the field empty creates a
`select.feel24_chosen_gym` entity so the active gym can be changed later.

The integration creates `sensor.feel24_visitors` with the unit `besøkende`.
The entity uses the Feel24 logo as its entity picture. Its state will contain
the current visitor count once the Feel24 visitor-data endpoint has been
verified and connected.

## Development

Integration files belong in `custom_components/feel24_visitors/`. Keep the
integration version in `manifest.json` in sync with GitHub release tags.
Retrieving live visitor counts is the next development milestone.

## License

MIT
