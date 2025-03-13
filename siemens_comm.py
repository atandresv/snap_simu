import snap7

class Plc:
    def __init__(self):
        self.plc = snap7.client.Client()
        self.plc.connect('192.168.1.15', 0, 1)

    def write_input(self, plc_byte, plc_bit, new_value):
        data = self.plc.read_area(snap7.types.Areas.PE, 0, plc_byte, 1)
        snap7.util.set_bool(data, 0, plc_bit, new_value)
        self.plc.write_area(snap7.types.Areas.PE, 0, plc_byte, data)
    
    def read_output(self, plc_byte, plc_bit):
        data = self.plc.read_area(snap7.types.Areas.PA, 0, plc_byte, 1)
        return snap7.util.get_bool(data,0,plc_bit)
        