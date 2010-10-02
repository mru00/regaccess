from xml.sax import saxutils
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces, ContentHandler
from mako.template import Template

import sys
import getopt

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return ' '.join(text.split())

files = []
opcodes = []
statuscodes = {}
if_version = 10
fus = []

class Param():
    def __init__(self, attrs):
        self.direction = attrs.get('direction', 'in')
        self.type = attrs.get('type')
        self.name = attrs.get('name')

class Fu():
    def __init__(self, attrs):
        self.name = attrs.get('name')
        self.ret = attrs.get('return', 'void')
        self.params = []

    def add_param(self, attrs):
        self.params.append( Param(attrs) )

class Entry():
    def __init__(self, attrs):
        self.id   = attrs.get('id')
        self.name = attrs.get('name')
        self.default = attrs.get('default', None)
        self.persist = attrs.get('persist', '0') in ('1', 'yes')
        self.read = attrs.get('read', '1') in ('1', 'yes')
        self.write = attrs.get('write', '1') in ('1', 'yes')
        self.doc = ''

class RegFile():
    def __init__(self, attrs):
        self.init= attrs.get('init', None)
        self.type = attrs.get('type')
        self.entries = []

    def add_entry(self, attrs):
        self.entries.append( Entry(attrs) )
        
class OpCode():
    def __init__(self, attrs):
        self.id = attrs.get('id')
        self.name = attrs.get('name')

class Handler(ContentHandler):
    def __init__(self):
        self.in_entry = False
        self.current_file = ""
        self.current_attrs = None

    def startElement(self, name, attrs):
        if name == "regaccess":
            global if_version
            if_version = attrs.get('if_version', 0)
            
        elif name == "file":
            global files
            self.current_file = RegFile(attrs) 
            files.append(self.current_file)

        elif name == "function":
            global fus, opcodes
            opcodes.append(attrs.get('name'))
            self.current_function = Fu(attrs) 
            fus.append(self.current_function)

        elif name == "param":
            self.current_function.add_param(attrs)
            
        elif name == "register":
            self.current_file.add_entry(attrs)
            
        elif name == "doc":
            self.entry_text = ""
            self.in_entry = True

        elif name == "statuscode":
            global statuscodes
            statuscodes[attrs.get('id')] = attrs.get('name')

    def endElement(self, name):

        pass
    def characters(self, ch):
        if self.in_entry:
            self.entry_text = self.entry_text + ch

__doc__ = """
usage: reg.py xml-file template-file

"""

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    module_directory = None
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hi:", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        # process options
        for o, a in opts:
            if o in ("-i"):
                module_directory = a
            if o in ("-h", "--help"):
                print __doc__
                sys.exit(0)

        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2


    assert len(args) == 2
    # Create a parser
    parser = make_parser()
    
    # Tell the parser we are not interested in XML namespaces
    parser.setFeature(feature_namespaces, 0)
    
    dh = Handler()
    
    parser.setContentHandler(dh)
        
    file = open (args[0], "rt" );
    parser.parse(file)
    
    mytemplate = Template(filename=args[1], module_directory=module_directory)
    print mytemplate.render(files=files, 
                            opcodes=opcodes, 
                            statuscodes=statuscodes, 
                            if_version=if_version,
                            fus=fus)
    
    
if __name__ == "__main__":
    sys.exit(main())


