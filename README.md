# HA Feel24 Visitors

Home Assistant custom integration for visitor data from Feel24.

> [!IMPORTANT]
> The repository currently contains the HACS-ready project structure. The
> visitor data source and Home Assistant entities still need to be implemented
> before the first release.

## Installation with HACS

HACS can only install from a public GitHub repository. When the integration is
ready for testers:

1. Make this repository public.
2. In HACS, open **Custom repositories**.
3. Add `https://github.com/isimagan/HA-Feel24-Visitors` as an **Integration**.
4. Download **HA Feel24 Visitors** and restart Home Assistant.

## Development

Integration files belong in `custom_components/feel24_visitors/`. Keep the
integration version in `manifest.json` in sync with GitHub release tags.

## License

MIT
