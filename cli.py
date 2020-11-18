"""
    Detect the impostor at game start
    https://github.com/lesander/amongus-impostor-detector

    Requires Wireshark/tshark amongus protocol to be installed:
    https://github.com/cybershard/wireshark-amongus
"""

import argparse
from sys import exit
from detector import Detector

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("method", default="live", help="inspect a live interface or analyze a pcap file [live/file]")
parser.add_argument("input", default="eth0", help="interface name or file path location")
parser.add_argument("--verbose", "-v", action='store_true', help="show print output from Detector class")
args = parser.parse_args()

detector = Detector(debug=bool(args.verbose))

if args.method == 'live':
    detector.start_live_capture(interface=args.input)
elif args.method == 'file':
    detector.start_file_capture(filepath=args.input)
else:
    print(f"Unknown method {args.method}")
    exit(1)

print(detector.get_impostors())
