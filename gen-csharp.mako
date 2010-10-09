using System.IO.Ports;

namespace AVRConnector {
  public class AVRConnection {
	private SerialPort port;

	enum Opcodes {
% for o in opcodes:
	${",".join(map(lambda o: "OPCODE_FN_" +o, opcodes))}
% endfor
	};


	enum Statuscodes {
% for k,v in statuscodes.items():
STATUSCODE_${v} = ${k},
% endfor
	};

	private String get_status_string(int code) {
	  switch(code) {
% for k,v in statuscodes.items():
	  case STATUSCODE_${v} : return "${v} [${k}]"; break;
% endfor
	  }
	  return "unknown code";
	}

	public AVRConnection() {
	  port = new SerialPort();
	  port.BaudRate = 38400;
	  port.StopBits = 1;
	  port.ReadTimeout = 500;
	  port.Open();
	}

	
  }
}
    





public class ConnectionException : Exception:
    def __init__(self, code):
        self.code = code

    def __str__(self):
        global status_names
        if self.code in status_names.keys():
            return status_names[self.code]
        return "unknown status code [%d]" % self.code


	  public void read_all() {
        fields = {}
% for fi in files:
% for r in filter(lambda entry: entry.read, fi.entries):
        fields["${r.name}"] = self.get_${r.name}()
% endfor
% endfor
        return fields
		}
% for fi in files:
% for r in fi.entries:
% if r.read:
     public ${fi.type} get_${r.name}() {
        return read_${fi.type}_register(${r.id})
	}
% endif
% if r.write:
     public void set_${r.name}(value) {
        write_${fi.type}_register(${r.id}, value)
	 }

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
public void ${fu.name}(${", ".join( map(lambda p: p.name, filter( lambda p: p.direction=="in", fu.params)))}) {

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
		}

% endfor
