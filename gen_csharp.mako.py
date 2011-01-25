from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1286125763.7674739
_template_filename='gen_csharp.mako'
_template_uri='gen_csharp.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


# SOURCE LINE 78

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


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        files = context.get('files', UNDEFINED)
        map = context.get('map', UNDEFINED)
        opcodes = context.get('opcodes', UNDEFINED)
        fus = context.get('fus', UNDEFINED)
        zip = context.get('zip', UNDEFINED)
        statuscodes = context.get('statuscodes', UNDEFINED)
        len = context.get('len', UNDEFINED)
        filter = context.get('filter', UNDEFINED)
        range = context.get('range', UNDEFINED)
        entry = context.get('entry', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'using System;\nusing System.IO.Ports;\nusing System.Collections;\nusing System.Collections.Generic;\nusing System.Runtime.Serialization;\n\n\nnamespace AVRConnector {\n\n  public class ConnectionException : Exception, ISerializable {\n\tpublic ConnectionException(int code) : base(to_msg(code)) {\n\t}\n\n\tprivate static string to_msg(int code) {\n\t  switch(code) {\n')
        # SOURCE LINE 16
        for k,v in statuscodes.items():
            # SOURCE LINE 17
            __M_writer(u'\t  case STATUSCODE_')
            __M_writer(unicode(v))
            __M_writer(u' : return "')
            __M_writer(unicode(v))
            __M_writer(u' [')
            __M_writer(unicode(k))
            __M_writer(u']"; \n')
        # SOURCE LINE 19
        __M_writer(u'\t  default:\n\t\treturn "unknown code"; \n\t  }\n\t}\n\n')
        # SOURCE LINE 24
        for k,v in statuscodes.items():
            # SOURCE LINE 25
            __M_writer(u'\tprivate const int STATUSCODE_')
            __M_writer(unicode(v))
            __M_writer(u' = ')
            __M_writer(unicode(k))
            __M_writer(u';\n')
        # SOURCE LINE 27
        __M_writer(u'\n  }\n\n  public class AVRConnection {\n\tprivate SerialPort port;\n\n')
        # SOURCE LINE 33
        for k,v in zip(opcodes, range(len(opcodes))):
            # SOURCE LINE 34
            __M_writer(u'\tprivate const int OPCODE_FN_')
            __M_writer(unicode(k))
            __M_writer(u' = ')
            __M_writer(unicode(v))
            __M_writer(u';\n')
        # SOURCE LINE 36
        __M_writer(u'\n\n')
        # SOURCE LINE 38
        for k,v in statuscodes.items():
            # SOURCE LINE 39
            __M_writer(u'\tprivate const int STATUSCODE_')
            __M_writer(unicode(v))
            __M_writer(u' = ')
            __M_writer(unicode(k))
            __M_writer(u';\n')
        # SOURCE LINE 41
        __M_writer(u'\n\tpublic AVRConnection() {\n\t  port = new SerialPort();\n\t  port.BaudRate = 38400;\n\t  port.StopBits = StopBits.One;\n\t  port.ReadTimeout = 500;\n\t  port.Open();\n\t}\n\n\t  public Dictionary<string, object> read_all() {\n\t\tDictionary<string, object> fields = new Dictionary<string, object>();\n\n')
        # SOURCE LINE 53
        for fi in files:
            # SOURCE LINE 54
            for r in filter(lambda entry: entry.read, fi.entries):
                # SOURCE LINE 55
                __M_writer(u'        fields["')
                __M_writer(unicode(r.name))
                __M_writer(u'"] = get_')
                __M_writer(unicode(r.name))
                __M_writer(u'();\n')
        # SOURCE LINE 58
        __M_writer(u'\t    return fields;\n\t  }\n')
        # SOURCE LINE 60
        for fi in files:
            # SOURCE LINE 61
            for r in fi.entries:
                # SOURCE LINE 62
                if r.read:
                    # SOURCE LINE 63
                    __M_writer(u'     public ')
                    __M_writer(unicode(fi.type))
                    __M_writer(u' get_')
                    __M_writer(unicode(r.name))
                    __M_writer(u'() {\n\t\t')
                    # SOURCE LINE 64
                    __M_writer(unicode(fi.type))
                    __M_writer(u' value;\n        read_')
                    # SOURCE LINE 65
                    __M_writer(unicode(fi.type))
                    __M_writer(u'_register(')
                    __M_writer(unicode(r.id))
                    __M_writer(u', out value);\n\t\treturn value;\n\t}\n')
                # SOURCE LINE 69
                if r.write:
                    # SOURCE LINE 70
                    __M_writer(u'     public void set_')
                    __M_writer(unicode(r.name))
                    __M_writer(u'(')
                    __M_writer(unicode(fi.type))
                    __M_writer(u' value) {\n        write_')
                    # SOURCE LINE 71
                    __M_writer(unicode(fi.type))
                    __M_writer(u'_register(')
                    __M_writer(unicode(r.id))
                    __M_writer(u', value);\n\t }\n\n')
        # SOURCE LINE 77
        __M_writer(u'\n')
        # SOURCE LINE 91
        __M_writer(u'\n\n\n  public void WriteByte(byte b) {\n\tByte[] x = new Byte[1];\n\tx[0] = b;\n\tport.Write(x, 0, 1);\n  }\n\n  public void WriteShort(short b) {\n\t//\n  }\n\n  public void WriteUShort(ushort b) {\n\t//\n  }\n\n  public void WriteFloat(float b) {\n\t//\tByte[] x = new Byte[4];\n\t//\tx[0] = b;\n\t//\tport.Write(x, 0, 1);\n\t//tbd\n  }\n\n\n  public byte ReadByte() {\n\tByte[] x = new Byte[1];\n\tport.Read(x, 0, 1);\n\treturn x[0];\n  }\n\n  public short ReadShort() {\n\treturn 0;\n  }\n\n  public ushort ReadUShort() {\n\treturn 0;\n  }\n\n  public float ReadFloat() {\n\treturn 0.0f;\n  }\n\n\n\n')
        # SOURCE LINE 136
        for fu in fus:
            # SOURCE LINE 137
            __M_writer(u'  public void ')
            __M_writer(unicode(fu.name))
            __M_writer(u'(')
            __M_writer(unicode(", ".join( map(lambda p: "%s %s" %(p.type, p.name), filter( lambda p: p.direction=="in", fu.params)) + map(lambda p: "out %s %s" %(p.type, p.name), filter( lambda p: p.direction=="out", fu.params)) )))
            __M_writer(u') {\n\n\tport.DiscardInBuffer();\n\tport.DiscardOutBuffer();\n\n\tWriteByte(OPCODE_FN_')
            # SOURCE LINE 142
            __M_writer(unicode(fu.name))
            __M_writer(u');\n')
            # SOURCE LINE 143
            for p in filter(lambda p: p.direction=="in", fu.params):
                # SOURCE LINE 144
                __M_writer(u'\t')
                __M_writer(unicode(write_map[p.type]))
                __M_writer(u'(')
                __M_writer(unicode(p.name))
                __M_writer(u');\n')
            # SOURCE LINE 146
            __M_writer(u'\n\tint status = ReadByte();\n    if (status != STATUSCODE_OK) \n\t  throw new ConnectionException(status);\n')
            # SOURCE LINE 150
            for p in filter(lambda p: p.direction=="out", fu.params):
                # SOURCE LINE 151
                __M_writer(u'    ')
                __M_writer(unicode(p.name))
                __M_writer(u' = ')
                __M_writer(unicode(read_map[p.type]))
                __M_writer(u'();\n')
            # SOURCE LINE 153
            __M_writer(u'  }\n\n')
        # SOURCE LINE 156
        __M_writer(u'\n }\n}\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


