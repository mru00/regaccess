from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1286040802.5921891
_template_filename='gen_avr_impl.mako'
_template_uri='gen_avr_impl.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


# SOURCE LINE 1

def gen_actual_params(fu):
    return ",".join( map(lambda p: ('&' if p.direction=='out' else '') + p.name, fu))

def gen_formal_params(fu):
    if len(fu) == 0:
        return "void"
    return ",".join( map(lambda p: p.type + " " + ('*' if p.direction=='out' else '') + p.name, fu))


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        files = context.get('files', UNDEFINED)
        opcodes = context.get('opcodes', UNDEFINED)
        fus = context.get('fus', UNDEFINED)
        statuscodes = context.get('statuscodes', UNDEFINED)
        f = context.get('f', UNDEFINED)
        len = context.get('len', UNDEFINED)
        filter = context.get('filter', UNDEFINED)
        if_version = context.get('if_version', UNDEFINED)
        entry = context.get('entry', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 9

        init_values = {}
        for fi in files:
          init_values[fi.type] = fi.init
        
        
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin()[__M_key]) for __M_key in ['fi','init_values'] if __M_key in __M_locals_builtin()]))
        # SOURCE LINE 13
        __M_writer(u'')
        # SOURCE LINE 14
        __M_writer(u'#include <avr/eeprom.h>\n\n#include "common.h"\n\n#define EEPROM_VALID_MASK 0xA5\n\nenum {\n')
        # SOURCE LINE 21
        for o in opcodes:
            # SOURCE LINE 22
            __M_writer(u'REG_OP_')
            __M_writer(unicode(o))
            __M_writer(u',\n')
        # SOURCE LINE 24
        __M_writer(u'};\n\n')
        # SOURCE LINE 26
        for k,v in statuscodes.items():
            # SOURCE LINE 27
            __M_writer(u'#define REG_ST_')
            __M_writer(unicode(v))
            __M_writer(u'  ')
            __M_writer(unicode(k))
            __M_writer(u'\n')
        # SOURCE LINE 29
        __M_writer(u'\nbyte ping(void) { return 0; }\n\nbyte get_fw_version(void) { return 0; }\nbyte get_if_version(byte* version) { return ')
        # SOURCE LINE 33
        __M_writer(unicode(if_version))
        __M_writer(u'; }\n\n\n// ----------------------- file definitions\n\n// register in memory layout\ntypedef struct {\n')
        # SOURCE LINE 40
        for fi in files:
            # SOURCE LINE 41
            for r in fi.entries:
                # SOURCE LINE 42
                __M_writer(u'  ')
                __M_writer(unicode(fi.type))
                __M_writer(u' ')
                __M_writer(unicode(r.name))
                __M_writer(u';     // ')
                __M_writer(unicode(r.doc))
                __M_writer(u'\n')
        # SOURCE LINE 45
        __M_writer(u'} reg_file_t;\n\nvolatile reg_file_t reg_file;\n\n\n// persistance of variables: eeprom layout\n\ntypedef struct {\n')
        # SOURCE LINE 53
        for fi in files:
            # SOURCE LINE 54
            for r in filter(lambda entry: entry.persist, fi.entries):
                # SOURCE LINE 55
                __M_writer(u'  ')
                __M_writer(unicode(fi.type))
                __M_writer(u' ')
                __M_writer(unicode(r.name))
                __M_writer(u';\n')
        # SOURCE LINE 58
        __M_writer(u'} reg_file_persist_t;\n\n\nreg_file_persist_t reg_persist_eeprom EEMEM;\nuint8_t ee_valid_configuration EEMEM;\n\n\nstatic void __attribute__((constructor))\nregfile_autoinit(void) \n{\n')
        # SOURCE LINE 68
        for fi in files:
            # SOURCE LINE 69
            for r in filter(lambda entry: entry.default, fi.entries):
                # SOURCE LINE 70
                __M_writer(u'  reg_file.')
                __M_writer(unicode(r.name))
                __M_writer(u' = ')
                __M_writer(unicode(r.default))
                __M_writer(u';\n')
        # SOURCE LINE 73
        __M_writer(u'\t\n  if ( eeprom_read_byte(&ee_valid_configuration) == EEPROM_VALID_MASK) {\n\t  \n')
        # SOURCE LINE 76
        for fi in files:
            # SOURCE LINE 77
            for r in filter(lambda entry: entry.persist, fi.entries):
                # SOURCE LINE 78
                __M_writer(u'    eeprom_read_block ((void *) &reg_file.')
                __M_writer(unicode(r.name))
                __M_writer(u', \n\t\t\t\t\t   (const void *) &reg_persist_eeprom.')
                # SOURCE LINE 79
                __M_writer(unicode(r.name))
                __M_writer(u', \n\t\t\t\t\t   sizeof(')
                # SOURCE LINE 80
                __M_writer(unicode(fi.type))
                __M_writer(u'));\n')
        # SOURCE LINE 83
        __M_writer(u'  }\n  else {\n')
        # SOURCE LINE 85
        for fi in files:
            # SOURCE LINE 86
            for r in filter(lambda entry: entry.persist, fi.entries):
                # SOURCE LINE 87
                __M_writer(u'    eeprom_write_block( (const void*) &reg_file.')
                __M_writer(unicode(r.name))
                __M_writer(u', \n\t\t\t\t\t\t&reg_persist_eeprom.')
                # SOURCE LINE 88
                __M_writer(unicode(r.name))
                __M_writer(u', \n\t\t\t\t\t\tsizeof(')
                # SOURCE LINE 89
                __M_writer(unicode(fi.type))
                __M_writer(u'));\n')
        # SOURCE LINE 92
        __M_writer(u'    eeprom_write_byte(&ee_valid_configuration, EEPROM_VALID_MASK);\n  }\n}\n\n\n\n// ----------------------- file accessors\n\n')
        # SOURCE LINE 100
        for fi in files:
            # SOURCE LINE 101
            for r in fi.entries:
                # SOURCE LINE 102
                __M_writer(u'\nextern ')
                # SOURCE LINE 103
                __M_writer(unicode(fi.type))
                __M_writer(u' get_')
                __M_writer(unicode(r.name))
                __M_writer(u'(void) { return reg_file.')
                __M_writer(unicode(r.name))
                __M_writer(u'; }\nextern void  set_')
                # SOURCE LINE 104
                __M_writer(unicode(r.name))
                __M_writer(u'(const ')
                __M_writer(unicode(fi.type))
                __M_writer(u' v) {   \n  reg_file.')
                # SOURCE LINE 105
                __M_writer(unicode(r.name))
                __M_writer(u' = v; \n')
                # SOURCE LINE 106
                if r.persist:
                    # SOURCE LINE 107
                    __M_writer(u'  eeprom_write_block( (const void*) &reg_file.')
                    __M_writer(unicode(r.name))
                    __M_writer(u', \n\t\t\t\t\t  &reg_persist_eeprom.')
                    # SOURCE LINE 108
                    __M_writer(unicode(r.name))
                    __M_writer(u', \n\t\t\t\t\t  sizeof(')
                    # SOURCE LINE 109
                    __M_writer(unicode(fi.type))
                    __M_writer(u'));  \n')
                # SOURCE LINE 111
                __M_writer(u'}\n')
        # SOURCE LINE 114
        __M_writer(u'\n')
        # SOURCE LINE 115
        for fi in filter(lambda f: len(f.entries) > 0, files):
            # SOURCE LINE 116
            __M_writer(u'static byte read_')
            __M_writer(unicode(fi.type))
            __M_writer(u'_register(const byte id, ')
            __M_writer(unicode(fi.type))
            __M_writer(u'* value)  {\n  switch(id) {\n')
            # SOURCE LINE 118
            for r in filter(lambda entry: entry.read, fi.entries):
                # SOURCE LINE 119
                __M_writer(u'  case ')
                __M_writer(unicode(r.id))
                __M_writer(u': *value = get_')
                __M_writer(unicode(r.name))
                __M_writer(u'(); return REG_ST_OK; break;\n')
            # SOURCE LINE 121
            for r in filter(lambda entry: not entry.read, fi.entries):
                # SOURCE LINE 122
                __M_writer(u'  case ')
                __M_writer(unicode(r.id))
                __M_writer(u': return REG_ST_NO_ACCESS; break;\n')
            # SOURCE LINE 124
            __M_writer(u'  }\n  return REG_ST_NO_SUCH_REGISTER;\n}\n\nstatic byte write_')
            # SOURCE LINE 128
            __M_writer(unicode(fi.type))
            __M_writer(u'_register(const byte id, const ')
            __M_writer(unicode(fi.type))
            __M_writer(u' value)  {\n  switch(id) {\n')
            # SOURCE LINE 130
            for r in filter(lambda entry: entry.write, fi.entries):
                # SOURCE LINE 131
                __M_writer(u'  case ')
                __M_writer(unicode(r.id))
                __M_writer(u': set_')
                __M_writer(unicode(r.name))
                __M_writer(u'(value); return REG_ST_OK; break;\n')
            # SOURCE LINE 133
            for r in filter(lambda entry: not entry.write, fi.entries):
                # SOURCE LINE 134
                __M_writer(u'  case ')
                __M_writer(unicode(r.id))
                __M_writer(u': return REG_ST_NO_ACCESS; break;\n')
            # SOURCE LINE 136
            __M_writer(u'  }\n  return REG_ST_NO_SUCH_REGISTER;\n}\n\n')
        # SOURCE LINE 141
        __M_writer(u'\n\n\n// ----------------------- serial comm accessors\n\n\nstatic byte receive_byte(void) {\n  unsigned int v;\n  while ( (v=uart_getc()) & UART_NO_DATA );\n  return (byte) v&0xff;\n}\n\nstatic float receive_float(void) {\n  union { char b[4]; float f; } v;\n  v.b[0] = receive_byte();\n  v.b[1] = receive_byte();\n  v.b[2] = receive_byte();\n  v.b[3] = receive_byte();\n  return v.f;\n}\n\nstatic short receive_short(void) {\n  union { char b[2]; short f; } v;\n  v.b[0] = receive_byte();\n  v.b[1] = receive_byte();\n  return v.f;\n}\n\nstatic short receive_ushort(void) {\n  union { char b[2]; ushort f; } v;\n  v.b[0] = receive_byte();\n  v.b[1] = receive_byte();\n  return v.f;\n}\n\nstatic void send_byte(const byte value) {\n  uart_putc(value);\n}\n\nstatic void send_float(const float value) {\n  union { char b[4]; float f; } v;\n  v.f = value;\n\n  send_byte( v.b[0] );\n  send_byte( v.b[1] );\n  send_byte( v.b[2] );\n  send_byte( v.b[3] );\n}\n\nstatic void send_short(const short value) {\n  union { char b[2]; short f; } v;\n  v.f = value;\n\n  send_byte( v.b[0] );\n  send_byte( v.b[1] );\n}\n\nstatic void send_ushort(const short value) {\n  union { char b[2]; ushort f; } v;\n  v.f = value;\n\n  send_byte( v.b[0] );\n  send_byte( v.b[1] );\n}\n\nextern void on_receive_byte(const uint8_t ch) {\n\n  byte status = 0;\n\n  switch(ch) {\n')
        # SOURCE LINE 211
        for fu in fus:
            # SOURCE LINE 212
            __M_writer(u'  case REG_OP_')
            __M_writer(unicode(fu.name))
            __M_writer(u': {\n')
            # SOURCE LINE 213
            for p in filter(lambda p: p.direction=="in", fu.params):
                # SOURCE LINE 214
                __M_writer(u'\t  ')
                __M_writer(unicode(p.type))
                __M_writer(u' ')
                __M_writer(unicode(p.name))
                __M_writer(u' = receive_')
                __M_writer(unicode(p.type))
                __M_writer(u'();\n')
            # SOURCE LINE 216
            for p in filter(lambda p: p.direction=="out", fu.params):
                # SOURCE LINE 217
                __M_writer(u'\t  ')
                __M_writer(unicode(p.type))
                __M_writer(u' ')
                __M_writer(unicode(p.name))
                __M_writer(u' = ')
                __M_writer(unicode(init_values[p.type]))
                __M_writer(u';\n')
            # SOURCE LINE 219
            __M_writer(u'\n      status = ')
            # SOURCE LINE 220
            __M_writer(unicode(fu.name))
            __M_writer(u'(')
            __M_writer(unicode(gen_actual_params(fu.params)))
            __M_writer(u');\n\n\t  send_byte(status);\n')
            # SOURCE LINE 223
            if len(filter(lambda p: p.direction=="out", fu.params)) > 0:
                # SOURCE LINE 224
                __M_writer(u'\t  if ( REG_ST_OK == status ) {\n')
                # SOURCE LINE 225
                for p in filter(lambda p: p.direction=="out", fu.params):
                    # SOURCE LINE 226
                    __M_writer(u'\t    send_')
                    __M_writer(unicode(p.type))
                    __M_writer(u'(')
                    __M_writer(unicode(p.name))
                    __M_writer(u');\n')
                # SOURCE LINE 228
                __M_writer(u'\t  }\n')
            # SOURCE LINE 230
            __M_writer(u'\t}\n    break;\n')
        # SOURCE LINE 233
        __M_writer(u'\n  default:\n\tsend_byte(REG_ST_INVALID_OPCODE);\n  }\n}\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


