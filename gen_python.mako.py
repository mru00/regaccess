from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1286049235.5475559
_template_filename='gen_python.mako'
_template_uri='gen_python.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


# SOURCE LINE 69

type_map = { 'float':  'f', 
             'short':  'h',
             'ushort': 'H',
             'byte':   'B' }
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
        statuscodes = context.get('statuscodes', UNDEFINED)
        len = context.get('len', UNDEFINED)
        filter = context.get('filter', UNDEFINED)
        o = context.get('o', UNDEFINED)
        entry = context.get('entry', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'import serial\nimport struct\n\n__doc__ = """\ngenerated interface file for serial communication with avr controller\nbased on the xml register definitions\n"""\n\n')
        # SOURCE LINE 9
        __M_writer(unicode(",".join(map(lambda o: "OPCODE_FN_" +o, opcodes))))
        __M_writer(u' = range(')
        __M_writer(unicode(len(opcodes)))
        __M_writer(u')\n\n')
        # SOURCE LINE 11
        for k,v in statuscodes.items():
            # SOURCE LINE 12
            __M_writer(u'STATUSCODE_')
            __M_writer(unicode(v))
            __M_writer(u' = ')
            __M_writer(unicode(k))
            __M_writer(u'\n')
        # SOURCE LINE 14
        __M_writer(u'\nstatus_names = {\n')
        # SOURCE LINE 16
        for k,v in statuscodes.items():
            # SOURCE LINE 17
            __M_writer(u'STATUSCODE_')
            __M_writer(unicode(v))
            __M_writer(u" : '")
            __M_writer(unicode(v))
            __M_writer(u' [')
            __M_writer(unicode(k))
            __M_writer(u"]',\n")
        # SOURCE LINE 19
        __M_writer(u'}\n\nclass ConnectionException(Exception):\n    def __init__(self, code):\n        self.code = code\n\n    def __str__(self):\n        global status_names\n        if self.code in status_names.keys():\n            return status_names[self.code]\n        return "unknown status code [%d]" % self.code\n\nclass RegConnection():\n    def __init__(self):\n        # configure the serial connections (the parameters differs on the device you are connecting to)\n        self.ser = serial.Serial(\n            port=\'/dev/ttyS0\',\n            baudrate=38400,\n            parity=serial.PARITY_NONE,\n            stopbits=serial.STOPBITS_ONE,\n            bytesize=serial.EIGHTBITS,\n            timeout=1\n            )\n\n        self.ser.open()\n        self.ser.isOpen()        \n\n    def read_all(self):\n        fields = {}\n')
        # SOURCE LINE 48
        for fi in files:
            # SOURCE LINE 49
            for r in filter(lambda entry: entry.read, fi.entries):
                # SOURCE LINE 50
                __M_writer(u'        fields["')
                __M_writer(unicode(r.name))
                __M_writer(u'"] = self.get_')
                __M_writer(unicode(r.name))
                __M_writer(u'()\n')
        # SOURCE LINE 53
        __M_writer(u'        return fields\n\n')
        # SOURCE LINE 55
        for fi in files:
            # SOURCE LINE 56
            for r in fi.entries:
                # SOURCE LINE 57
                if r.read:
                    # SOURCE LINE 58
                    __M_writer(u'    def get_')
                    __M_writer(unicode(r.name))
                    __M_writer(u'(self):\n        return self.read_')
                    # SOURCE LINE 59
                    __M_writer(unicode(fi.type))
                    __M_writer(u'_register(')
                    __M_writer(unicode(r.id))
                    __M_writer(u')\n')
                # SOURCE LINE 61
                if r.write:
                    # SOURCE LINE 62
                    __M_writer(u'    def set_')
                    __M_writer(unicode(r.name))
                    __M_writer(u'(self, value):\n        self.write_')
                    # SOURCE LINE 63
                    __M_writer(unicode(fi.type))
                    __M_writer(u'_register(')
                    __M_writer(unicode(r.id))
                    __M_writer(u', value)\n\n')
        # SOURCE LINE 68
        __M_writer(u'\n')
        # SOURCE LINE 78
        __M_writer(u'\n')
        # SOURCE LINE 79
        for fu in fus:
            # SOURCE LINE 80
            __M_writer(u'    def ')
            __M_writer(unicode(fu.name))
            __M_writer(u'(self, ')
            __M_writer(unicode(", ".join( map(lambda p: p.name, filter( lambda p: p.direction=="in", fu.params)))))
            __M_writer(u'):\n\n        self.ser.flushInput()\n\tself.ser.write(struct.pack("=B", OPCODE_FN_')
            # SOURCE LINE 83
            __M_writer(unicode(fu.name))
            __M_writer(u'))\n')
            # SOURCE LINE 84
            for p in filter(lambda p: p.direction=="in", fu.params):
                # SOURCE LINE 85
                __M_writer(u'\tself.ser.write(struct.pack("=')
                __M_writer(unicode(type_map[p.type]))
                __M_writer(u'", ')
                __M_writer(unicode(p.name))
                __M_writer(u'))\n')
            # SOURCE LINE 87
            __M_writer(u'\n        ( status, ) = struct.unpack("=B", self.ser.read(1))\n        if status != STATUSCODE_OK: \n            raise ConnectionException(status)\n')
            # SOURCE LINE 91
            for p in filter(lambda p: p.direction=="out", fu.params):
                # SOURCE LINE 92
                __M_writer(u'        ( ')
                __M_writer(unicode(p.name))
                __M_writer(u', ) = struct.unpack("=')
                __M_writer(unicode(type_map[p.type]))
                __M_writer(u'", self.ser.read(')
                __M_writer(unicode(size_map[p.type]))
                __M_writer(u'));\n')
            # SOURCE LINE 94
            __M_writer(u'        return ')
            __M_writer(unicode(",".join(map(lambda p: p.name,filter( lambda p: p.direction=="out", fu.params)))))
            __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


