import snap7

import snap7
import logging

class Plc:
    def __init__(self, ip='192.168.1.15', rack=0, slot=1):
        """
        Initializes the PLC connection.

        :param ip: IP address of the PLC
        :param rack: Rack number
        :param slot: Slot number
        """
        self.plc = snap7.client.Client()
        try:
            self.plc.connect(ip, rack, slot)
            logging.info("Connected to PLC")
        except snap7.snap7exceptions.Snap7Exception as e:
            logging.error(f"Error connecting to PLC: {e}")

    def write_input(self, plc_byte, plc_bit, new_value):
        """
        Writes a boolean value to the PLC input.

        :param plc_byte: Byte address
        :param plc_bit: Bit address
        :param new_value: Boolean value to write
        """
        try:
            data = self.plc.read_area(snap7.types.Areas.PE, 0, plc_byte, 1)
            snap7.util.set_bool(data, 0, plc_bit, new_value)
            self.plc.write_area(snap7.types.Areas.PE, 0, plc_byte, data)
            logging.info(f"Input written: byte={plc_byte}, bit={plc_bit}, value={new_value}")
        except snap7.snap7exceptions.Snap7Exception as e:
            logging.error(f"Error writing input to PLC: {e}")

    def read_output(self, plc_byte, plc_bit):
        """
        Reads a boolean value from the PLC output.

        :param plc_byte: Byte address
        :param plc_bit: Bit address
        :return: Boolean value read
        """
        try:
            data = self.plc.read_area(snap7.types.Areas.PA, 0, plc_byte, 1)
            value = snap7.util.get_bool(data, 0, plc_bit)
            logging.info(f"Output read: byte={plc_byte}, bit={plc_bit}, value={value}")
            return value
        except snap7.snap7exceptions.Snap7Exception as e:
            logging.error(f"Error reading output from PLC: {e}")
            return None

    def disconnect(self):
        """
        Closes the PLC connection.
        """
        self.plc.disconnect()
        logging.info("Disconnected from PLC")
        