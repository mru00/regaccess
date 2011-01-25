from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1286038962.78476
_template_filename='gen_avr_header.mako'
_template_uri='gen_avr_header.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


# SOURCE LINE 1

def gen_formal_params(fu):
    if len(fu) == 0:
        return "void"
    return ",".join( map(lambda p: p.type + " " + ('*' if p.direction=='out' else '') + p.name, fu))

def p_is_external(fn):
  return fn.name not in ("write_float_register", "read_float_register", "write_short_register", "read_short_register", "write_byte_register", "read_byte_register", "get_if_version")



def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        files = context.get('files', UNDEFINED)
        filter = context.get('filter', UNDEFINED)
        fus = context.get('fus', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 10
        __M_writer(u'')
        # SOURCE LINE 11
        __M_writer(u'#ifndef _regaccess_h\n#define _regaccess_h\n\ntypedef uint8_t byte;\ntypedef uint16_t ushort;\n\n// ----------------------- accessors\n\n')
        # SOURCE LINE 19
        for fi in files:
            # SOURCE LINE 20
            for r in fi.entries:
                # SOURCE LINE 21
                __M_writer(u'\nextern ')
                # SOURCE LINE 22
                __M_writer(unicode(fi.type))
                __M_writer(u' get_')
                __M_writer(unicode(r.name))
                __M_writer(u'(void);\nextern void  set_')
                # SOURCE LINE 23
                __M_writer(unicode(r.name))
                __M_writer(u'(const ')
                __M_writer(unicode(fi.type))
                __M_writer(u' f);\n')
        # SOURCE LINE 26
        __M_writer(u'\n// ----------------------- serial comm accessors\n\nextern void on_receive_byte(const uint8_t ch);\n\n\n\n// ----------------------- declarations of external functions\n\n')
        # SOURCE LINE 35
        for fu in filter(p_is_external, fus):
            # SOURCE LINE 36
            __M_writer(u'extern byte ')
            __M_writer(unicode(fu.name))
            __M_writer(u'(')
            __M_writer(unicode(gen_formal_params(fu.params)))
            __M_writer(u');\n')
        # SOURCE LINE 38
        __M_writer(u'\n#endif\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


