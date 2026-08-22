![Feel24 logo](https://raw.githubusercontent.com/isimagan/HA-Feel24-Visitors/master/brand/logo.png)

[Norsk](https://github.com/isimagan/HA-Feel24-Visitors/blob/master/README.md) | **English**

# HA Feel24 Visitors

An unofficial Home Assistant integration for Feel24.

The integration includes a configuration flow where you can search for and
select a Feel24 gym. Only gyms from the built-in list can be selected. It then
creates a sensor showing how many people are currently training at the gym.

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

## Sensor

For a gym named **Feel24 Billingstad**, the integration normally creates:

```text
sensor.feel24_billingstad_visitors
```

The sensor:

- shows the current number of registered gym visitors
- uses the unit `visitors`
- uses the `mdi:shoe-sneaker` icon and the Feel24 entity picture
- includes the `center_id` attribute
- updates every five minutes

Each gym is also registered as a Home Assistant device. This gives the gym its
own device page containing the sensor instead of only a loose entity listing.

Only users who have the GitHub link and add it as a custom repository will
find the repository in HACS. It has not been submitted to the default HACS
repository list.

## Status

- Configuration flow with searchable gym selection
- Norwegian and English interface
- Current visitor-count sensor
- A device page for every configured gym

This is an unofficial community project and is not developed, endorsed, or
supported by Feel24.

## License

MIT
