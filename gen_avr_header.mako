#ifndef _regaccess_h
#define _regaccess_h

typedef uint8_t byte;

// ----------------------- accessors

% for type in files:
% for r in files[type]:

extern ${type} get_${r.name}(void);
extern void  set_${r.name}(const ${type} f);
% endfor
% endfor

// ----------------------- serial comm accessors

extern void receive_reg(const uint8_t ch);
extern void regfile_init(void);

#endif
