# amp_power

This project contains a small utility to control the AC power of an audio power amplifier using an smart plug when connected to CamillaDSP on a RasperyPi as descirbed in [this thread](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/) of the Audio Science Review website.

It can use any of the plugs from that the [python-kasa](https://github.com/python-kasa/python-kasa) can control. In my case I used the [HS103 device](https://www.amazon.com/TP-Link-Kasa-Smart-Wifi-Plug/dp/B07RCNB2L3).

The script looks at the file the status of the playback device:
```
$ head /proc/asound/card2/stream0
MOTU M4 at usb-0000:01:00.0-1.3, high speed : USB Audio

Playback:
  Status: Stop
  Interface 1
  ...
```
And checks the stream for a Stop or Running state and uses that to turn the Smart plug on or off.

To use, first make sure you install the  python-kasa library as per the instruction and can control the device from the command line.

The clone the library, modify as required and 

```
cd camiladsp
git clone git@github.com:igfarm/amp_power.git
cd amp_power
```

Test the script
```
python3 amp_power.py
```

After to are satisfied it works, you can install it as a srvice. To do this update amp_power.service to point to the correct path and then:

```
sudo cp amp_power.service /lib/systemd/system/
sudo systemctl enable amp_power.service
sudo systemctl daemon-reload
sudo systemctl start amp_power.service
```
