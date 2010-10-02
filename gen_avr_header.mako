<%!
def gen_formal_params(fu):
    if len(fu) == 0:
        return "void"
    return ",".join( map(lambda p: p.type + " " + ('*' if p.direction=='out' else '') + p.name, fu))

def p_is_external(fn):
  return fn.name not in ("write_float_register", "read_float_register", "write_short_register", "read_short_register", "write_byte_register", "read_byte_register", "get_if_version")

%>\
#ifndef _regaccess_h
#define _regaccess_h

typedef uint8_t byte;
typedef uint16_t ushort;

// ----------------------- accessors

% for fi in files:
% for r in fi.entries:

extern ${fi.type} get_${r.name}(void);
extern void  set_${r.name}(const ${fi.type} f);
% endfor
% endfor

// ----------------------- serial comm accessors

extern void on_receive_byte(const uint8_t ch);



// ----------------------- declarations of external functions

% for fu in filter(p_is_external, fus):
extern byte ${fu.name}(${gen_formal_params(fu.params)});
% endfor

#endif
