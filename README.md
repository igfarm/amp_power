
# Power Amp Control for CamillaDSP and RasperyPi using Kasa SmartPulg

This project contains a small script to control the AC power of an audio power amplifier using an Kasa smart plug when connected to CamillaDSP on a RasperyPi. The "RPi4 + CamillaDSP Tutorial" setup is descirbed in [this thread](https://www.audiosciencereview.com/forum/index.php?threads/rpi4-camilladsp-tutorial.29656/) of the Audio Science Review website.

The script can use any of the plugs from that the [python-kasa](https://github.com/python-kasa/python-kasa) can control. In my case I used the [HS103 device](https://www.amazon.com/TP-Link-Kasa-Smart-Wifi-Plug/dp/B07RCNB2L3).

The script looks for the status of the playback device on the linux process information pseudo-file system:
```
$ head /proc/asound/card2/stream0
MOTU M4 at usb-0000:01:00.0-1.3, high speed : USB Audio

Playback:
  Status: Stop
  Interface 1
  ...
```
and checks the stream for a `Stop` or `Running` status and uses that to turn the smart plug on or off.

To use, first make sure you install the `python-kasa` library as per the instruction and can control the device from the command line. A good article on who to do this is [here](https://medium.com/geekculture/use-raspberry-pi-and-tp-link-kasa-to-automate-your-devices-9f936a6243c1).

Then clone the library, modify as required and:

```
cd camiladsp
git clone git@github.com:igfarm/amp_power.git
cd amp_power
```

Test the script
```
python3 amp_power.py
```

After you are satisfied it works, install it as a service. To do this update `amp_power.service` to point to the correct path and then:

```
sudo cp amp_power.service /lib/systemd/system/
sudo systemctl enable amp_power.service
sudo systemctl daemon-reload
sudo systemctl start amp_power.service
```

