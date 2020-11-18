"""
    Detect the impostor at game start
    https://github.com/lesander/amongus-impostor-detector

    Requires Wireshark/tshark amongus protocol to be installed:
    https://github.com/cybershard/wireshark-amongus
"""

import pyshark

class Detector:

    def __init__(self, debug=False):
        self.debug = debug
        self.impostors = []
        self.max_impostors = 4

    def start_live_capture(self, interface):
        capture = pyshark.LiveCapture(interface=interface, display_filter='amongus')
        for packet in capture.sniff_continuously():
            if self.handle_packet(packet):
                capture.close()
                break

    def start_file_capture(self, filepath):
        capture = pyshark.FileCapture(filepath, display_filter='amongus')
        for packet in capture:
            if self.handle_packet(packet):
                capture.close()
                break

    def handle_packet(self, packet):
        if hasattr(packet.amongus, 'game_data'):
            data = packet.amongus._get_all_fields_with_alternates()
            field_count = 0
            for field in data:

                if 'Impostor Count' in str(field) and int(field.showname_value) != self.max_impostors:
                    if self.debug:
                        print(f"This game will have {field.showname_value} impostor(s).")
                    self.max_impostors = int(field.showname_value)

                if 'Impostor: 2' in str(field):
                    # The PlayerName string is 5 fields back in an UpdateGameData player array.
                    impostor = data[field_count-5].showname_value
                    if self.debug:
                        print(f"Found an impostor: {impostor}")
                    if impostor not in self.impostors:
                        self.impostors.append(impostor)
                field_count += 1

            if len(self.impostors) >= self.max_impostors:
                return True

    def get_impostors(self):
        return self.impostors
