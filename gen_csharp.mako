using System;
using System.IO.Ports;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.Serialization;


namespace AVRConnector {

  public class ConnectionException : Exception, ISerializable {
	public ConnectionException(int code) : base(to_msg(code)) {
	}

	private static string to_msg(int code) {
	  switch(code) {
% for k,v in statuscodes.items():
	  case STATUSCODE_${v} : return "${v} [${k}]"; 
% endfor
	  default:
		return "unknown code"; 
	  }
	}

% for k,v in statuscodes.items():
	private const int STATUSCODE_${v} = ${k};
% endfor

  }

  public class AVRConnection {
	private SerialPort port;

% for k,v in zip(opcodes, range(len(opcodes))):
	private const int OPCODE_FN_${k} = ${v};
% endfor


% for k,v in statuscodes.items():
	private const int STATUSCODE_${v} = ${k};
% endfor

	public AVRConnection() {
	  port = new SerialPort();
	  port.BaudRate = 38400;
	  port.StopBits = StopBits.One;
	  port.ReadTimeout = 500;
	  port.Open();
	}

	  public Dictionary<string, object> read_all() {
		Dictionary<string, object> fields = new Dictionary<string, object>();

% for fi in files:
% for r in filter(lambda entry: entry.read, fi.entries):
        fields["${r.name}"] = get_${r.name}();
% endfor
% endfor
	    return fields;
	  }
% for fi in files:
% for r in fi.entries:
% if r.read:
     public ${fi.type} get_${r.name}() {
		${fi.type} value;
        read_${fi.type}_register(${r.id}, out value);
		return value;
	}
% endif
% if r.write:
     public void set_${r.name}(${fi.type} value) {
        write_${fi.type}_register(${r.id}, value);
	 }

% endif
% endfor
% endfor

<%!
write_map = { 'float':  'WriteFloat', 
             'short':  'WriteShort',
             'ushort': 'WriteUShort',
             'byte':   'WriteByte' }
read_map = { 'float':  'ReadFloat', 
             'short':  'ReadShort',
             'ushort': 'ReadUShort',
             'byte':   'ReadByte' }
size_map= { 'float':  4,
            'short':  2,
            'ushort': 2,
            'byte':   1 }
%>


  public void WriteByte(byte b) {
	Byte[] x = new Byte[1];
	x[0] = b;
	port.Write(x, 0, 1);
  }

  public void WriteShort(short b) {
	//
  }

  public void WriteUShort(ushort b) {
	//
  }

  public void WriteFloat(float b) {
	//	Byte[] x = new Byte[4];
	//	x[0] = b;
	//	port.Write(x, 0, 1);
	//tbd
  }


  public byte ReadByte() {
	Byte[] x = new Byte[1];
	port.Read(x, 0, 1);
	return x[0];
  }

  public short ReadShort() {
	return 0;
  }

  public ushort ReadUShort() {
	return 0;
  }

  public float ReadFloat() {
	return 0.0f;
  }



% for fu in fus:
  public void ${fu.name}(${", ".join( map(lambda p: "%s %s" %(p.type, p.name), filter( lambda p: p.direction=="in", fu.params)) + map(lambda p: "out %s %s" %(p.type, p.name), filter( lambda p: p.direction=="out", fu.params)) )}) {

	port.DiscardInBuffer();
	port.DiscardOutBuffer();

	WriteByte(OPCODE_FN_${fu.name});
% for p in filter(lambda p: p.direction=="in", fu.params):
	${write_map[p.type]}(${p.name});
% endfor

	int status = ReadByte();
    if (status != STATUSCODE_OK) 
	  throw new ConnectionException(status);
% for p in filter(lambda p: p.direction=="out", fu.params):
    ${p.name} = ${read_map[p.type]}();
% endfor
  }

% endfor

 }
}

