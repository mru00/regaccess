from xml.sax import saxutils
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces, ContentHandler
from mako.template import Template

import sys
import getopt

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return ' '.join(text.split())

files = {}
opcodes = {}
statuscodes = {}

class Entry():
    def __init__(self, attrs):
        self.id   = attrs.get('id')
        self.name = attrs.get('name')
        self.default = attrs.get('default', None)
        self.persist = attrs.get('persist', '0') in ('1', 'yes')
        self.read = attrs.get('read', '1') in ('1', 'yes')
        self.write = attrs.get('write', '1') in ('1', 'yes')
        self.doc = ''

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
        if name == "file":
            self.current_file = attrs.get('type', "") 
            files[self.current_file] = []
            
        elif name == "register":
            self.entry = Entry(attrs)
            
        elif name == "doc":
            self.entry_text = ""
            self.in_entry = True

        elif name == "opcode":
            opcodes[attrs.get('id')] = attrs.get('name')

        elif name == "statuscode":
            statuscodes[attrs.get('id')] = attrs.get('name')

    def endElement(self, name):

        if name == "doc":
            self.in_entry = False
            self.entry.doc = normalize_whitespace(self.entry_text)
        elif name == "register":

            files[self.current_file].append( self.entry )

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
    print mytemplate.render(files=files, opcodes=opcodes, statuscodes=statuscodes)
    
    
if __name__ == "__main__":
    sys.exit(main())


