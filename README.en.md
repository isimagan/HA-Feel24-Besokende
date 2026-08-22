![Feel24 logo](https://raw.githubusercontent.com/isimagan/HA-Feel24-Visitors/master/brand/logo.png)

[Norsk](https://github.com/isimagan/HA-Feel24-Visitors/blob/master/README.md) | **English**

# HA Feel24 Visitors

An unofficial Home Assistant integration for Feel24.

The integration includes a configuration flow where you can search for and
select a Feel24 gym. Only gyms from the built-in list can be selected. Sensors
and visitor-count retrieval will be added in a later version.

## Add to HACS using the link

The repository is not listed in the HACS catalogue. Add it manually:

1. Open HACS and select **Custom repositories**.
2. Add `https://github.com/isimagan/HA-Feel24-Visitors`.
3. Select **Integration** as the category.
4. Select **Add**.

## Configuration

1. Install the integration through HACS and restart Home Assistant.
2. Open **Settings → Devices & services**.
3. Select **Add integration** and search for **Feel24 Visitors**.
4. Start typing the name of your gym, then select it from the list.

The location ID is stored automatically. There are no other settings yet.

Only users who have the GitHub link and add it as a custom repository will
find the repository in HACS. It has not been submitted to the default HACS
repository list.

## Status

- Configuration flow with searchable gym selection
- Norwegian and English interface
- No sensors yet

This is an unofficial community project and is not developed, endorsed, or
supported by Feel24.

## License

MIT
