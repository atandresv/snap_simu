import snap7
import logging
import re

class Plc:
    def __init__(self, ip='192.168.1.15', rack=0, slot=1):
        """
        Initializes the PLC connection.

        :param ip: IP address of the PLC
        :param rack: Rack number
        :param slot: Slot number
        """
        self.plc = snap7.client.Client()
        self.ip = ip
        self.rack = rack
        self.slot = slot
        
        if not self._validate_ip(ip):
            logging.error(f"Invalid IP address: {ip}")
            return
            
        try:
            self.plc.connect(ip, rack, slot)
            if self.plc.get_connected():
                logging.info(f"Connected to PLC at IP {ip}, rack {rack}, slot {slot}")
            else:
                logging.error("Failed to connect to PLC")
        except Exception as e:
            logging.error(f"Error connecting to PLC: {e}")
        
    @staticmethod
    def _validate_ip(ip):
        """
        Validates the IP address format.

        :param ip: IP address to validate
        :return: True if valid, False otherwise
        """
        pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if pattern.match(ip):
            return all(0 <= int(num) <= 255 for num in ip.split('.'))
        return False
        
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
        except Exception as e:
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
        except Exception as e:
            logging.error(f"Error reading output from PLC: {e}")
            return None

    def write_analog_input(self, start_byte, value, size=2):
        """
        Writes an analog value to the PLC input.

        :param start_byte: Byte address
        :param value: The analog value to write
        :param size: Write area size in bytes (2 or 4)
        :return: None
        """
        try:
            data = bytearray(size)
            
            if size == 2:
                snap7.util.set_int(data, 0, value)
            elif size == 4:
                snap7.util.set_dint(data, 0, value)
            else:
                logging.error(f"Invalid size: {size}. Size must be 2 or 4 bytes.")
                return
        
            self.plc.write_area(snap7.types.Areas.PE, 0, start_byte, data)
            logging.info(f"Analog input written: byte={start_byte}, size={size}, value={value}")
        except Exception as e:
            logging.error(f"Error writing analog input to PLC: {e}")

    def read_analog_output(self, start_byte, size=2):
        """
        Reads an analog value from the PLC output.

        :param start_byte: Byte address
        :param size: read area size in bytes (2 or 4)
        :return: analog value read
        """
        try:
            data = self.plc.read_area(snap7.types.Areas.PA, 0, start_byte, size)
            if size == 2:
                value = snap7.util.get_int(data, 0)
            elif size == 4:
                value = snap7.util.get_dint(data, 0)
            else:
                logging.error(f"Invalid size: {size}. Size must be 2 or 4 bytes.")
                return None

            logging.info(f"Analog output read: byte={start_byte}, size={size}, value={value}")
            return value
        except Exception as e:
            logging.error(f"Error reading analog output from PLC: {e}")
            return None

    def disconnect(self):
        """
        Closes the PLC connection.
        """
        try:
            self.plc.disconnect()
            logging.info("Disconnected from PLC")
        except Exception as e:
            logging.error(f"Error disconnecting from PLC: {e}")
