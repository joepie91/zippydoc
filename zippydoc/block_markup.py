import re

class TreeLevel:
	def __init__(self, indentation, data):
		self.elements = []
		self.indentation = indentation
		self.data = data
	
	def add(self, element):
		self.elements.append(element)
		
	def output(self):
		return self.render()
		
	def render_children(self):
		child_output = ""
		
		for child in self.elements:
			child_output += child.output()
			
		return '<div class="children">%s</div>' % child_output
		
	def process_inline_markup(self, text):
		text = re.sub("`([^`]+)`", '<span class="fixed">\\1</span>', text)             # Fixed-width
		text = re.sub("\*\*([^*]+)\*\*", "<em>\\1</em>", text)                         # Emphasized
		text = re.sub("__([^_]+)__", "<strong>\\1</strong>", text)                     # Strong
		text = re.sub("{>([^}]+)}\(([^)]+)\)", '<a href="\\1.html">\\2</a>', text)     # Hyperlink with text
		text = re.sub("{>([^}]+)}", '<a href="\\1.html">\\1</a>', text)                # Hyperlink
		text = re.sub("{([^}]+:[^}]+)}\(([^)]+)\)", '<a href="\\1">\\2</a>', text)     # External hyperlink with text
		text = re.sub("{([^}]+:[^}]+)}", '<a href="\\1">\\1</a>', text)                # External hyperlink
		text = re.sub("{<([^}]+)}\(([^)]+)\)", '<a href="\\1">\\2</a>', text)          # Forced external hyperlink with text
		text = re.sub("{<([^}]+)}", '<a href="\\1">\\1</a>', text)                     # Forced external hyperlink
		
		return text
		
	def clear_markup(self, text):
		text = re.sub("`([^`]+)`", '\\1', text)             # Fixed-width
		text = re.sub("\*\*([^*]+)\*\*", "\\1", text)                         # Emphasized
		text = re.sub("__([^_]+)__", "\\1", text)                     # Strong
		text = re.sub("{>([^}]+)}\(([^)]+)\)", '\\2', text)     # Hyperlink with text
		text = re.sub("{>([^}]+)}", '\\1', text)                # Hyperlink
		text = re.sub("{([^}]+:[^}]+)}\(([^)]+)\)", '\\2', text)     # External hyperlink with text
		text = re.sub("{([^}]+:[^}]+)}", '\\1', text)                # External hyperlink
		text = re.sub("{<([^}]+)}\(([^)]+)\)", '\\2', text)          # Forced external hyperlink with text
		text = re.sub("{<([^}]+)}", '\\1', text)                     # Forced external hyperlink
		
		return text
		
	def fix_preformatted(self, text):
		return text.replace("<", "&lt;").replace(">", "&gt;")
		
	def render(self):
		return self.render_children()

class Header(TreeLevel):
	def __init__(self, indentation, data, depth):
		self.elements = []
		self.indentation = indentation
		self.data = data
		self.depth = depth
		
	def render(self):
		if self.depth <= 7:
			title_type = "h%d" % self.depth
		else:
			title_type = "h7"
			
		return "<%s>%s</%s>" % (title_type, self.data, title_type)

class Text(TreeLevel):
	def render(self):
		return '<div class="text">%s</div>' % self.process_inline_markup(self.data)

class Exclamation(TreeLevel):
	def render(self):
		return '<div class="exclamation"><strong>Important:</strong> %s</div>' % self.process_inline_markup(self.data)

class Definition(TreeLevel):
	def get_anchor(self):
		first = self.clear_markup(self.data.splitlines()[0])
		anchor = first.replace("...", "")
		anchor = anchor.replace(".", "_")
		anchor = re.sub("[^a-zA-Z0-9_]", "", anchor)
		return anchor
	
	def get_description(self):
		for element in self.elements:
			if element.__class__.__name__ == "Text":
				data = self.process_inline_markup(element.data)
				
				if len(data) > 80:
					matches = re.match("^(.{0,80})\W", data)					
					return matches.group(1) + "..."
				else:
					return data
				
		return ""
	
	def render(self):
		return '<div class="definition"><a name="def_%s">%s %s</a></div>' % (self.get_anchor(), self.process_inline_markup(self.data.replace("\n", "<br>")), self.render_children())

class Argument(TreeLevel):
	def __init__(self, indentation, data, argname):
		self.elements = []
		self.indentation = indentation
		self.data = data
		self.argname = argname
	
	def render(self):
		return '<dl><dt>%s</dt><dd>%s%s</dd></dl>' % (self.argname, self.process_inline_markup(self.data), self.render_children())

class Example(TreeLevel):
	def render(self):
		return '<div class="example">Example: %s %s</div>' % (self.data, self.render_children())
	
class Code(TreeLevel):
	def render(self):
		return '<h7>Code:</h7><pre class="code">%s</pre>' % self.fix_preformatted(self.data)
	
class Output(TreeLevel):
	def render(self):
		return '<h7>Output:</h7><pre class="output">%s</pre>' % self.fix_preformatted(self.data)

class Index(TreeLevel):
	def render(self):
		rendered = ""
		
		for item in self.data.toc_items:
			forms = item.data.splitlines()
			first = self.clear_markup(forms[0])
			
			if len(forms) > 1:
				rest = '<span class="alternatives">(also: ' + ', '.join(self.clear_markup(form) for form in forms[1:]) + ")</span>"
			else:
				rest = ""
			
			anchor = item.get_anchor()
			description = item.get_description()
			rendered += '<li><a href="#def_%s">%s</a> %s %s</li>' % (anchor, first, description, rest)
		
		return '<div class="toc"><h2>Table of contents</h2><ul>%s</ul></div>' % rendered
