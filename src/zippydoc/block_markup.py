import re
from value import Value

class TreeLevel(object):
	def __init__(self, indentation, data):
		self.elements = []
		self.indentation = indentation
		self.data = data
	
	def add(self, element):
		self.elements.append(element)
	
	def transform(self, ruleset):
		return self.transform_children(ruleset)
	
	def transform_children(self, ruleset):
		child_output = ""
		
		for child in self.elements:
			child_output += child.transform(ruleset)
			
		return ruleset.transform_children(child_output)

class Header(TreeLevel):
	def __init__(self, indentation, data, depth):
		self.elements = []
		self.indentation = indentation
		self.data = data
		self.depth = depth
		
	def transform(self, ruleset):
		return ruleset.transform_header(self.depth, Value(self.data))

class Text(TreeLevel):
	def transform(self, ruleset):
		return ruleset.transform_text(Value(self.data))

class List(TreeLevel):
	def transform(self, ruleset):
		return ruleset.transform_list([Value(line) for line in self.data])

class Exclamation(TreeLevel):
	def transform(self, ruleset):
		return ruleset.transform_exclamation(Value(self.data), self.transform_children(ruleset))

class Definition(TreeLevel):
	def __init__(self, indentation, forms):
		self.elements = []
		self.indentation = indentation
		self.forms = [form.lstrip() for form in forms]
	
	def transform(self, ruleset):
		return ruleset.transform_definition([Value(form) for form in self.forms], self.transform_children(ruleset))
	
	def get_forms(self):
		return [Value(form) for form in self.forms]
	
	def get_description(self):
		for element in self.elements:
			if element.__class__.__name__ == "Text":
				return element.data
				
		return ""
	
class Argument(TreeLevel):
	def __init__(self, indentation, data, argname):
		self.elements = []
		self.indentation = indentation
		self.data = data
		self.argname = argname
		
	def transform(self, ruleset):
		return ruleset.transform_argument(Value(self.argname), Value(self.data), self.transform_children(ruleset))

class Example(TreeLevel):
	def transform(self, ruleset):
		return ruleset.transform_example(Value(self.data), self.transform_children(ruleset))
	
class Code(TreeLevel):
	def transform(self, ruleset):
		return ruleset.transform_code(self.data)
	
class Output(TreeLevel):
	def transform(self, ruleset):
		return ruleset.transform_output(Value(self.data))

class Index(TreeLevel):
	def transform(self, ruleset):
		return ruleset.transform_toc([(definition, Value(definition.get_description())) for definition in self.data.get_definitions()])
