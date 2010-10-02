import serial
import struct

__doc__ = """
generated interface file for serial communication with avr controller
based on the xml register definitions
"""

OPCODE_FN_write_float_register,OPCODE_FN_write_short_register,OPCODE_FN_read_float_register,OPCODE_FN_read_short_register,OPCODE_FN_set_led,OPCODE_FN_get_if_version,OPCODE_FN_ping,OPCODE_FN_ln5623_set_output = range(8)

STATUSCODE_FAIL = 1
STATUSCODE_OK = 0
STATUSCODE_NO_ACCESS = 3
STATUSCODE_NO_SUCH_REGISTER = 2
STATUSCODE_NOT_IMPLEMENTED = 5
STATUSCODE_INVALID_OPCODE = 4
STATUSCODE_PONG = 6

status_names = {
STATUSCODE_FAIL : 'FAIL [1]',
STATUSCODE_OK : 'OK [0]',
STATUSCODE_NO_ACCESS : 'NO_ACCESS [3]',
STATUSCODE_NO_SUCH_REGISTER : 'NO_SUCH_REGISTER [2]',
STATUSCODE_NOT_IMPLEMENTED : 'NOT_IMPLEMENTED [5]',
STATUSCODE_INVALID_OPCODE : 'INVALID_OPCODE [4]',
STATUSCODE_PONG : 'PONG [6]',
}

class ConnectionException(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        global status_names
        if self.code in status_names.keys():
            return status_names[self.code]
        return "unknown status code [%d]" % self.code

class RegConnection():
    def __init__(self):
        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=38400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
            )

        self.ser.open()
        self.ser.isOpen()        

    def read_all(self):
        fields = {}
        fields["kp"] = self.get_kp()
        fields["ki"] = self.get_ki()
        fields["kd"] = self.get_kd()
        fields["abgas_v1190"] = self.get_abgas_v1190()
        fields["abgas_amp_gain"] = self.get_abgas_amp_gain()
        fields["vorlauf_v1190"] = self.get_vorlauf_v1190()
        fields["vorlauf_amp_gain"] = self.get_vorlauf_amp_gain()
        fields["temp_vorlauf"] = self.get_temp_vorlauf()
        fields["temp_abgas"] = self.get_temp_abgas()
        fields["temp_ambient"] = self.get_temp_ambient()
        fields["controller_output"] = self.get_controller_output()
        return fields

    def get_kp(self):
        return self.read_float_register(0)
    def set_kp(self, value):
        self.write_float_register(0, value)

    def get_ki(self):
        return self.read_float_register(1)
    def set_ki(self, value):
        self.write_float_register(1, value)

    def get_kd(self):
        return self.read_float_register(2)
    def set_kd(self, value):
        self.write_float_register(2, value)

    def get_abgas_v1190(self):
        return self.read_float_register(3)
    def set_abgas_v1190(self, value):
        self.write_float_register(3, value)

    def get_abgas_amp_gain(self):
        return self.read_float_register(4)
    def set_abgas_amp_gain(self, value):
        self.write_float_register(4, value)

    def get_vorlauf_v1190(self):
        return self.read_float_register(5)
    def set_vorlauf_v1190(self, value):
        self.write_float_register(5, value)

    def get_vorlauf_amp_gain(self):
        return self.read_float_register(6)
    def set_vorlauf_amp_gain(self, value):
        self.write_float_register(6, value)

    def get_temp_vorlauf(self):
        return self.read_short_register(0)
    def get_temp_abgas(self):
        return self.read_short_register(1)
    def get_temp_ambient(self):
        return self.read_short_register(2)
    def get_controller_output(self):
        return self.read_short_register(3)


    def write_float_register(self, id, value):

        self.ser.flushInput()
	self.ser.write(struct.pack("=B", OPCODE_FN_write_float_register))
	self.ser.write(struct.pack("=B", id))
	self.ser.write(struct.pack("=f", value))

        ( status, ) = struct.unpack("=B", self.ser.read(1))
        if status != STATUSCODE_OK: 
            raise ConnectionException(status)
        return 

    def write_short_register(self, id, value):

        self.ser.flushInput()
	self.ser.write(struct.pack("=B", OPCODE_FN_write_short_register))
	self.ser.write(struct.pack("=B", id))
	self.ser.write(struct.pack("=h", value))

        ( status, ) = struct.unpack("=B", self.ser.read(1))
        if status != STATUSCODE_OK: 
            raise ConnectionException(status)
        return 

    def read_float_register(self, id):

        self.ser.flushInput()
	self.ser.write(struct.pack("=B", OPCODE_FN_read_float_register))
	self.ser.write(struct.pack("=B", id))

        ( status, ) = struct.unpack("=B", self.ser.read(1))
        if status != STATUSCODE_OK: 
            raise ConnectionException(status)
        ( value, ) = struct.unpack("=f", self.ser.read(4));
        return value

    def read_short_register(self, id):

        self.ser.flushInput()
	self.ser.write(struct.pack("=B", OPCODE_FN_read_short_register))
	self.ser.write(struct.pack("=B", id))

        ( status, ) = struct.unpack("=B", self.ser.read(1))
        if status != STATUSCODE_OK: 
            raise ConnectionException(status)
        ( value, ) = struct.unpack("=h", self.ser.read(2));
        return value

    def set_led(self, on):

        self.ser.flushInput()
	self.ser.write(struct.pack("=B", OPCODE_FN_set_led))
	self.ser.write(struct.pack("=B", on))

        ( status, ) = struct.unpack("=B", self.ser.read(1))
        if status != STATUSCODE_OK: 
            raise ConnectionException(status)
        return 

    def get_if_version(self, ):

        self.ser.flushInput()
	self.ser.write(struct.pack("=B", OPCODE_FN_get_if_version))

        ( status, ) = struct.unpack("=B", self.ser.read(1))
        if status != STATUSCODE_OK: 
            raise ConnectionException(status)
        ( version, ) = struct.unpack("=B", self.ser.read(1));
        return version

    def ping(self, ):

        self.ser.flushInput()
	self.ser.write(struct.pack("=B", OPCODE_FN_ping))

        ( status, ) = struct.unpack("=B", self.ser.read(1))
        if status != STATUSCODE_OK: 
            raise ConnectionException(status)
        return 

    def ln5623_set_output(self, value, dp):

        self.ser.flushInput()
	self.ser.write(struct.pack("=B", OPCODE_FN_ln5623_set_output))
	self.ser.write(struct.pack("=H", value))
	self.ser.write(struct.pack("=B", dp))

        ( status, ) = struct.unpack("=B", self.ser.read(1))
        if status != STATUSCODE_OK: 
            raise ConnectionException(status)
        return 


