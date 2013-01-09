import os, argparse, sys, re
import zippydoc

parser = argparse.ArgumentParser(description='Converts ZippyDoc source files to HTML.')

parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                   help='files to convert to HTML')

args = parser.parse_args()
options = vars(args)

files = options["files"]

docparser = zippydoc.Parser(open("template.html").read())

for zpy in files:
	destination = os.path.splitext(zpy)[0] + ".html"
	
	f = open(zpy, "r")
	data = f.read()
	f.close()
	
	rendered = docparser.render(data)
	
	f = open(destination, "w")
	f.write(rendered)
	f.close()
	
	print "Rendered %s" % destination
