#include <avr/eeprom.h>

#include "common.h"

#define EEPROM_VALID_MASK 0xA5

% for k,v in opcodes.items():
#define REG_OP_${v} ${k}
% endfor

% for k,v in statuscodes.items():
#define REG_ST_${v}  ${k}
% endfor


// ----------------------- file definitions

% for type in files:
typedef struct {
% for r in files[type]:
  ${type} ${r.name};     // ${r.doc}
% endfor
} reg_${type}_t;

% endfor

// register in memory layout
typedef struct  {
% for type in files:
  reg_${type}_t reg_${type};
%endfor
} reg_file_t;

volatile reg_file_t reg_file;


// persistance of variables: eeprom layout

typedef struct {
% for type in files:
% for r in filter(lambda entry: entry.persist, files[type]):
  ${type} pers_${type}_${r.name};
% endfor
% endfor
} reg_file_persist_t;


reg_file_persist_t reg_persist_eeprom EEMEM;
uint8_t ee_valid_configuration EEMEM;


extern void regfile_init(void) {
% for type in files:
% for r in filter(lambda entry: entry.default, files[type]):
  reg_file.reg_${type}.${r.name} = ${r.default};
% endfor
% endfor
	
  if ( eeprom_read_byte(&ee_valid_configuration) == EEPROM_VALID_MASK) {
	  
% for type in files:
% for r in filter(lambda entry: entry.persist, files[type]):
    eeprom_read_block ((void *) &reg_file.reg_${type}.${r.name}, 
					   (const void *) &reg_persist_eeprom.pers_${type}_${r.name}, 
					   sizeof(${type}));
% endfor
% endfor
  }
  else {
% for type in files:
% for r in filter(lambda entry: entry.persist, files[type]):
    eeprom_write_block( (const void*) &reg_file.reg_${type}.${r.name}, 
						&reg_persist_eeprom.pers_${type}_${r.name}, 
						sizeof(${type}));
% endfor
% endfor
    eeprom_write_byte(&ee_valid_configuration, EEPROM_VALID_MASK);
  }
}



// ----------------------- file accessors

% for type in files:
% for r in files[type]:

extern ${type} get_${r.name}(void) { return reg_file.reg_${type}.${r.name}; }
extern void  set_${r.name}(const ${type} f) {   
  reg_file.reg_${type}.${r.name} = f; 
% if r.persist:
  eeprom_write_block( (const void*) &reg_file.reg_${type}.${r.name}, 
					  &reg_persist_eeprom.pers_${type}_${r.name}, 
					  sizeof(${type}));  
% endif
}
% endfor
% endfor

% for type in files:
static byte read_${type}_register(const byte id, ${type}* value)  {
  switch(id) {
% for r in filter(lambda entry: entry.read, files[type]):
  case ${r.id}: *value = get_${r.name}(); return REG_ST_OK; break;
% endfor
% for r in filter(lambda entry: not entry.read, files[type]):
  case ${r.id}: return REG_ST_NO_ACCESS; break;
% endfor
  }
  return REG_ST_NO_SUCH_REGISTER;
}

static byte write_${type}_register(const byte id, const ${type} value)  {
  switch(id) {
% for r in filter(lambda entry: entry.write, files[type]):
  case ${r.id}: set_${r.name}(value); return REG_ST_OK; break;
% endfor
% for r in filter(lambda entry: not entry.write, files[type]):
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
  union { char b[2]; float f; } v;
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

extern void receive_reg(const uint8_t ch) {

  byte id = 0;
  byte status = 0;
  union {
	float f;
	byte b;
	short s;
  } v;

  switch(ch) {
  case REG_OP_PING:
	send_byte(REG_ST_PONG);
	break;
  case REG_OP_READ_BYTE:
	id = receive_byte();
	status = read_byte_register(id, &v.b);
	send_byte(status);
	if ( REG_ST_OK == status ) send_byte(v.b);
	break;
  case REG_OP_WRITE_BYTE:
	id = receive_byte();
	v.b = receive_byte();
	status = write_byte_register(id, v.b);
	send_byte(status);
	break;
  case REG_OP_READ_FLOAT:
	id = receive_byte();
	status = read_float_register(id, &v.f);
	send_byte(status);
	if ( REG_ST_OK == status ) send_float(v.f);
	break;
  case REG_OP_WRITE_FLOAT:
	id = receive_byte();
	v.f = receive_float();
	status = write_float_register(id, v.f);
	send_byte(status);
	break;
  case REG_OP_READ_SHORT:
	id = receive_byte();
	read_short_register(id, &v.s);
	send_byte(status);
	if ( REG_ST_OK == status ) send_short(v.s);
	break;
  case REG_OP_WRITE_SHORT:
	id = receive_byte();
	v.s = receive_short();
	status = write_short_register(id, v.s);
	send_byte(status);
	break;
  case REG_OP_SPECIAL:
	send_byte(REG_ST_NOT_IMPLEMENTED);
	break;
  default:
	send_byte(REG_ST_INVALID_OPCODE);
  }
}


