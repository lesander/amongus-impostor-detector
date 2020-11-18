# Among Us Impostor(s) Detector

## Installing
This Python 3 module requires [Wireshark or tshark](https://www.wireshark.org/) to be
installed on the system with the following Lua plugin installed:
https://github.com/cybershard/wireshark-amongus.

After Wireshark and the Lua plugin are installed, clone this repository and
install pyshark with pip.
```shell
git clone https://github.com/lesander/amongus-impostor-detector.git
cd amongus-impostor-detector/
pip install -r requirements.txt
```

## Usage
This module ships with a simple command line interface. See the below
examples for reference.

Use `tshark -D` to find the interface you want to listen to. Note that
on Windows, interface names **do not** need to be escaped using `\\` or quotes.

```shell
# listen to live interface eth0
python cli.py --method=live input=eth0

# parse given pcap file
python cli.py --method=file input=path/to/file.pcapng

# use verbose option for quicker results in live capture
python cli.py --method=live --input=eth0 --verbose

# listen to a live windows adapter
python cli.py --method=live --input=\Device\ABC_{12345678-1234-5678-1234-123456789012} --verbose
```

This module can also be used programmatically.

```python
from detector import Detector
detector = Detector()

# start live capture on interface eth0
detector.start_live_capture(interface='eth0')

# parse given pcap file
detector.start_file_capture(filepath='path/to/file.pcapng')

# get found impostor(s)
print(detector.get_impostors())
```
