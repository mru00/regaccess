import serial
import struct

__doc__ = """
generated interface file for serial communication with avr controller
based on the xml register definitions
"""

% for k,v in opcodes.items():
OPCODE_${v} = ${k}
% endfor

% for k,v in statuscodes.items():
STATUSCODE_${v} = ${k}
% endfor


class RegConnection():
    def __init__(self):
        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=38400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )

        self.ser.open()
        self.ser.isOpen()


    def status_to_string(self, status):
% for k,v in statuscodes.items():
        if status == STATUSCODE_${v}: return "${v} [${k}]"
% endfor
        return "unkown status code [%d]" % status
        
    def _read_byte_register(self, id):
        self.ser.flushInput()
	self.ser.write(struct.pack("=BB", OPCODE_READ_BYTE, id))
        ( status, b ) = struct.unpack("=BB", self.ser.read(2))
        assert status == 0, self.status_to_string(status)
        return b

    def _write_byte_register(self, id, value):
        self.ser.flushInput()
	self.ser.write(struct.pack("=BBB", OPCODE_WRITE_BYTE, id, value))
        ( status, ) = struct.unpack("=B", self.ser.read(1))
        assert status == 0, self.status_to_string(status)

    def _read_float_register(self, id):
        self.ser.flushInput()
	self.ser.write(struct.pack("=BB", OPCODE_READ_FLOAT, id))
        ( status, f ) = struct.unpack("=Bf", self.ser.read(5))
        assert status == 0, self.status_to_string(status)
        return f

    def _write_float_register(self, id, value):
        self.ser.flushInput()
	self.ser.write(struct.pack("=BBf", OPCODE_WRITE_FLOAT, id, value))
        ( status, ) = struct.unpack("=B", self.ser.read(1))
        assert status == 0, self.status_to_string(status)


    def _read_short_register(self, id):
        self.ser.flushInput()
	self.ser.write(struct.pack("=BB", OPCODE_READ_SHORT, id))
        ( status, s ) = struct.unpack("=BH", self.ser.read(struct.calcsize("=BH")))
        assert status == 0, self.status_to_string(status)
        return s 

    def _write_short_register(self, id, value):
        self.ser.flushInput()
	self.ser.write(struct.pack("=BBH", OPCODE_WRITE_SHORT, id, value))
        (status,) = struct.unpack("=B", self.ser.read(1))
        assert status == 0, self.status_to_string(status)

    def read_all(self):
        fields = {}
% for type in files:
% for r in filter(lambda entry: entry.read, files[type]):
        fields["${r.name}"] = self.get_${r.name}()
% endfor
% endfor
        return fields



% for type in files:
% for r in files[type]:

% if r.read:
    def get_${r.name}(self):
        return self._read_${type}_register(${r.id})
% endif
% if r.write:
    def set_${r.name}(self, value):
        self._write_${type}_register(${r.id}, value)
% endif
% endfor
% endfor
