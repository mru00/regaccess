import serial
import struct

__doc__ = """
generated interface file for serial communication with avr controller
based on the xml register definitions
"""

${",".join(map(lambda o: "OPCODE_FN_" +o, opcodes))} = range(${len(opcodes)})

% for k,v in statuscodes.items():
STATUSCODE_${v} = ${k}
% endfor

status_names = {
% for k,v in statuscodes.items():
STATUSCODE_${v} : '${v} [${k}]',
% endfor
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
% for fi in files:
% for r in filter(lambda entry: entry.read, fi.entries):
        fields["${r.name}"] = self.get_${r.name}()
% endfor
% endfor
        return fields

% for fi in files:
% for r in fi.entries:
% if r.read:
    def get_${r.name}(self):
        return self.read_${fi.type}_register(${r.id})
% endif
% if r.write:
    def set_${r.name}(self, value):
        self.write_${fi.type}_register(${r.id}, value)

% endif
% endfor
% endfor

<%!
type_map = { 'float':  'f', 
             'short':  'h',
             'ushort': 'H',
             'byte':   'B' }
size_map= { 'float':  4,
            'short':  2,
            'ushort': 2,
            'byte':   1 }
%>
% for fu in fus:
    def ${fu.name}(self, ${", ".join( map(lambda p: p.name, filter( lambda p: p.direction=="in", fu.params)))}):

        self.ser.flushInput()
	self.ser.write(struct.pack("=B", OPCODE_FN_${fu.name}))
% for p in filter(lambda p: p.direction=="in", fu.params):
	self.ser.write(struct.pack("=${type_map[p.type]}", ${p.name}))
% endfor

        ( status, ) = struct.unpack("=B", self.ser.read(1))
        if status != STATUSCODE_OK: 
            raise ConnectionException(status)
% for p in filter(lambda p: p.direction=="out", fu.params):
        ( ${p.name}, ) = struct.unpack("=${type_map[p.type]}", self.ser.read(${size_map[p.type]}));
% endfor
        return ${",".join(map(lambda p: p.name,filter( lambda p: p.direction=="out", fu.params)))}

% endfor
