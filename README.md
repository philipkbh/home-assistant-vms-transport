# Transport widgets for Home Assistant for Verkehrsverbund Mittelsachsen (VMS) 

Custom sensor component and lovelace card that displays upcoming departures from your defined public transport stops for Verkehrsverbund Mittelsachsen (VMS).

This repository contains only the integration, the Lovelace card itself is found here: https://github.com/philipkbh/lovelace-vms-transport-card.

You need to install them both. Preferably through HACS. I have separated two repositories to make installation through it more convenient.

## 💿 Installation

The component consists of two parts:

1. A sensor, which tracks departures via VVO Public API every 90 seconds
2. A widget (card) for the lovelace dashboard, which displays upcoming transport in a nice way. It has its own [separate repository](https://github.com/philipkbh/lovelace-vms-transport-card) with installation instructions.

### Install the sensor component
#### Install the sensor component via HACS

**1.** Add this [repository](https://github.com/philipkbh/home-assistant-vms-transport) as a custom repository in HACS in the category **integration**.

**2.** Add `Verkehrsverbund Mittelsachsen (VMS) transport` as a new integration under `Settings` -> `Devices & services`  .

**3.** Search for your stop (it will provide up to 15 stops that match your query).

**4.** Select the stop you are looking for.

**5.** Enter further details about the type of transport and walking time you require.


#### Install the sensor component manually

##### How do I find my `stop_id`?

Unfortunately, I didn't have time to figure out a proper user-friendly approach of adding new components to Home Assistant, so you will have to do some routine work of finding the IDs of the nearest transport stops to you. Sorry about that :)

Simply use this URL: `https://webapi.vvo-online.de/tr/pointfinder?format=JSON&query=%27Zentralhaltestelle%20Chemnitz%27`

Replace `Zentralhaltestelle Chemnitz` with the name of your own stop.

```json
{
  "PointStatus": "Identified",
  "Status": {
    "Code": "Ok"
  },
  "Points": [
    "36030131||Chemnitz|Zentralhaltestelle|5633297|4565081|0||"
  ],
  "ExpirationTime": "/Date(1710001564549+0100)/"
}
```

Copy the first 8-digit number of the stop you want to display in Home Assistant.
In this case it's `36030131`.

##### Install the sensor component

**1.** Copy the whole [vms_transport](./custom_components/) directory to the `custom_components` folder of your Home Assistant installation. If you can't find the `custom_components` directory at the same level with your `configuration.yml` — simply create it yourself and put `vms_transport` there.

**2.** Go to Home Assistant web interface -> `Developer Tools` -> `Check configuration` -> `Restart` and click on the `Restart Home Assistant` button. It will reload all components in the system.

**3.** Now you can add your new custom sensor to the corresponding section in the `configuration.yml` file.

```yaml
sensor:
  - platform: vms_transport
    departures:
      - name: "Zentralhaltestelle Chemnitz" # Free-form name, only for display purposes
        stop_id: 36030131                   # Actual Stop ID for the API
      - name: "Hauptbahnhof Chemnitz"       # You can add more that one stop to track
        stop_id: 36030062
        # walking_time: 5                   # Optional parameter with value in minutes that hides transport closer than N minutes
        # IntercityBus = false              # Optional parameter to hide Intercity Bus if `false` (default is true -> shown)
        # PlusBus = false                   # Optional parameter to hide Regio Bus if `false` (default is true -> shown)
        # SuburbanRailway = false           # Optional parameter to hide Suburban Train if `false` (default is true -> shown)
        # Train = false                     # Optional parameter to hide Train if `false` (default is true -> shown)
        # Tram = false                      # Optional parameter to hide Tram if `false` (default is true -> shown)
```

**4.** Restart Home Assistant core again and you should now see two new entities (however, it may take some time for them to fetch new data). If you don't see anything new — check the **logs** (`Settings` -> `System` -> `Logs`). Some error should pop up there.

### Add the lovelace card

Go to [lovelace-vms-transport-card](https://github.com/philipkbh/lovelace-vms-transport-card) repo and follow installation instructions there.

## 👩‍💻 Technical details

This sensor uses VVO Public API to fetch all transport information.

- API docs: https://github.com/kiliankoe/vvo

The component updates every 60-90 seconds, but it makes a separate request for each stop.

The VVO API is a bit unstable (as you can guess), so sometimes it gives random 503 or Timeout errors. This is normal. I haven't found how to overcome this, but it doesn't cause any problems other than warning messages in the logs.

After fetching the API, it creates one entity for each stop and writes 10 upcoming departures into `attributes.departures`. The entity state is not really used anywhere, it just shows the next departure in a human-readable format. If you have any ideas how to use it better — welcome to Github Issues.

## ❤️ Contributions

Contributions are welcome. Feel free to [open a PR](https://github.com/philipkbh/home-assistant-vms-transport/pulls) and send it to review. If you are unsure, [open an Issue](https://github.com/philipkbh/home-assistant-vms-transport/issues) and ask for advice.

## 🐛 Bug reports and feature requests

Since this is my small hobby project, I cannot guarantee you a 100% support or any help with configuring your dashboards. I hope for your understanding.

- **If you find a bug** - open [an Issue](https://github.com/VDenisyuk/home-assistant-transport/issues) and describe the exact steps to reproduce it. Attach screenshots, copy all logs and other details to help me find the problem.

## Credits

This module is a fork of [vas3k repo](https://github.com/vas3k/home-assistant-berlin-transport) made for Berlin and [VDenisyuk](https://github.com/VDenisyuk/home-assistant-transport) made for Dresden (DVB) and VVO.

## 👮‍♀️ License

- [MIT](./LICENSE.md)
