<%!
def gen_actual_params(fu):
    return ",".join( map(lambda p: ('&' if p.direction=='out' else '') + p.name, fu))

def gen_formal_params(fu):
    if len(fu) == 0:
        return "void"
    return ",".join( map(lambda p: p.type + " " + ('*' if p.direction=='out' else '') + p.name, fu))
%><%
init_values = {}
for fi in files:
  init_values[fi.type] = fi.init
%>\
#include <avr/eeprom.h>

#include "common.h"

#define EEPROM_VALID_MASK 0xA5

enum {
% for o in opcodes:
REG_OP_${o},
% endfor
};

% for k,v in statuscodes.items():
#define REG_ST_${v}  ${k}
% endfor

byte ping(void) { return 0; }

byte get_fw_version(void) { return 0; }
byte get_if_version(byte* version) { return ${if_version}; }


// ----------------------- file definitions

// register in memory layout
typedef struct {
% for fi in files:
% for r in fi.entries:
  ${fi.type} ${r.name};     // ${r.doc}
% endfor
% endfor
} reg_file_t;

volatile reg_file_t reg_file;


// persistance of variables: eeprom layout

typedef struct {
% for fi in files:
% for r in filter(lambda entry: entry.persist, fi.entries):
  ${fi.type} ${r.name};
% endfor
% endfor
} reg_file_persist_t;


reg_file_persist_t reg_persist_eeprom EEMEM;
uint8_t ee_valid_configuration EEMEM;


static void __attribute__((constructor))
regfile_autoinit(void) 
{
% for fi in files:
% for r in filter(lambda entry: entry.default, fi.entries):
  reg_file.${r.name} = ${r.default};
% endfor
% endfor
	
  if ( eeprom_read_byte(&ee_valid_configuration) == EEPROM_VALID_MASK) {
	  
% for fi in files:
% for r in filter(lambda entry: entry.persist, fi.entries):
    eeprom_read_block ((void *) &reg_file.${r.name}, 
					   (const void *) &reg_persist_eeprom.${r.name}, 
					   sizeof(${fi.type}));
% endfor
% endfor
  }
  else {
% for fi in files:
% for r in filter(lambda entry: entry.persist, fi.entries):
    eeprom_write_block( (const void*) &reg_file.${r.name}, 
						&reg_persist_eeprom.${r.name}, 
						sizeof(${fi.type}));
% endfor
% endfor
    eeprom_write_byte(&ee_valid_configuration, EEPROM_VALID_MASK);
  }
}



// ----------------------- file accessors

% for fi in files:
% for r in fi.entries:

extern ${fi.type} get_${r.name}(void) { return reg_file.${r.name}; }
extern void  set_${r.name}(const ${fi.type} v) {   
  reg_file.${r.name} = v; 
% if r.persist:
  eeprom_write_block( (const void*) &reg_file.${r.name}, 
					  &reg_persist_eeprom.${r.name}, 
					  sizeof(${fi.type}));  
% endif
}
% endfor
% endfor

% for fi in filter(lambda f: len(f.entries) > 0, files):
static byte read_${fi.type}_register(const byte id, ${fi.type}* value)  {
  switch(id) {
% for r in filter(lambda entry: entry.read, fi.entries):
  case ${r.id}: *value = get_${r.name}(); return REG_ST_OK; break;
% endfor
% for r in filter(lambda entry: not entry.read, fi.entries):
  case ${r.id}: return REG_ST_NO_ACCESS; break;
% endfor
  }
  return REG_ST_NO_SUCH_REGISTER;
}

static byte write_${fi.type}_register(const byte id, const ${fi.type} value)  {
  switch(id) {
% for r in filter(lambda entry: entry.write, fi.entries):
  case ${r.id}: set_${r.name}(value); return REG_ST_OK; break;
% endfor
% for r in filter(lambda entry: not entry.write, fi.entries):
  case ${r.id}: return REG_ST_NO_ACCESS; break;
% endfor
  }
  return REG_ST_NO_SUCH_REGISTER;
}

% endfor



// ----------------------- serial comm accessors


static byte receive_byte(void) {
  unsigned int v;
  while ( (v=uart_getc()) & UART_NO_DATA );
  return (byte) v&0xff;
}

static float receive_float(void) {
  union { char b[4]; float f; } v;
  v.b[0] = receive_byte();
  v.b[1] = receive_byte();
  v.b[2] = receive_byte();
  v.b[3] = receive_byte();
  return v.f;
}

static short receive_short(void) {
  union { char b[2]; short f; } v;
  v.b[0] = receive_byte();
  v.b[1] = receive_byte();
  return v.f;
}

static short receive_ushort(void) {
  union { char b[2]; ushort f; } v;
  v.b[0] = receive_byte();
  v.b[1] = receive_byte();
  return v.f;
}

static void send_byte(const byte value) {
  uart_putc(value);
}

static void send_float(const float value) {
  union { char b[4]; float f; } v;
  v.f = value;

  send_byte( v.b[0] );
  send_byte( v.b[1] );
  send_byte( v.b[2] );
  send_byte( v.b[3] );
}

static void send_short(const short value) {
  union { char b[2]; short f; } v;
  v.f = value;

  send_byte( v.b[0] );
  send_byte( v.b[1] );
}

static void send_ushort(const short value) {
  union { char b[2]; ushort f; } v;
  v.f = value;

  send_byte( v.b[0] );
  send_byte( v.b[1] );
}

extern void on_receive_byte(const uint8_t ch) {

  byte status = 0;

  switch(ch) {
% for fu in fus:
  case REG_OP_${fu.name}: {
% for p in filter(lambda p: p.direction=="in", fu.params):
	  ${p.type} ${p.name} = receive_${p.type}();
% endfor
% for p in filter(lambda p: p.direction=="out", fu.params):
	  ${p.type} ${p.name} = ${init_values[p.type]};
% endfor

      status = ${fu.name}(${gen_actual_params(fu.params)});

	  send_byte(status);
% if len(filter(lambda p: p.direction=="out", fu.params)) > 0:
	  if ( REG_ST_OK == status ) {
% for p in filter(lambda p: p.direction=="out", fu.params):
	    send_${p.type}(${p.name});
% endfor
	  }
% endif
	}
    break;
% endfor

  default:
	send_byte(REG_ST_INVALID_OPCODE);
  }
}

