import re
import block_markup

class Document(object):
	def __init__(self, data):
		self.data = data
		self._parse()
		
	def _parse(self):
		paragraphs = re.split("\s*\n\s*\n", self.data)
		
		self.paragraphs = paragraphs
		self.definitions = []
		
		current_level = 0
		current_paragraph = 0
		self.current_elements = {0: block_markup.TreeLevel(0, "root")}
		
		for paragraph in paragraphs:
			if paragraph.strip() == "":
				continue
				
			current_paragraph += 1
			indentation = len(paragraph) - len(paragraph.lstrip("\t")) + 1
			
			if indentation > current_level + 1:
				raise Exception("Invalid indentation found in paragraph %d" % current_paragraph)
			
			start = indentation - 1
			lines = [line[start:] for line in paragraph.splitlines()]
			
			if lines[0].startswith("#"):
				# Header
				depth = len(lines[0]) - len(lines[0].lstrip("#"))
				lines[0] = lines[0].lstrip("# ")
				element = block_markup.Header(indentation, " ".join(lines), depth)
			elif lines[0].startswith("^"):
				# Definition
				lines[0] = lines[0].lstrip("^ ")
				element = block_markup.Definition(indentation, lines)
				self.definitions.append(element)
			elif lines[0].startswith("@"):
				# Example
				lines[0] = lines[0].lstrip("@ ")
				element = block_markup.Example(indentation, " ".join(lines))
			elif lines[0].startswith("$$") and self.current_elements[current_level].__class__.__name__ == "Code":
				# Code continuation
				self.current_elements[current_level].data += "\n\n" + "\n".join(lines).lstrip("$ ")
				continue
			elif lines[0].startswith("$"):
				# Code block start
				lines[0] = lines[0].lstrip("$ ")
				element = block_markup.Code(indentation, "\n".join(lines))
			elif lines[0].startswith(">>") and self.current_elements[current_level].__class__.__name__ == "Output":
				# Output continuation
				self.current_elements[current_level].data += "\n\n" + "\n".join(lines).lstrip("> ")
				continue
			elif lines[0].startswith(">"):
				# Output block start
				lines[0] = lines[0].lstrip("> ")
				element = block_markup.Output(indentation, "\n".join(lines))
			elif lines[0].startswith("!"):
				# Exclamation
				lines[0] = lines[0].lstrip("! ")
				element = block_markup.Exclamation(indentation, " ".join(lines))
			elif lines[0].startswith("* "):
				items = [item.replace("\n", " ") for item in "\n".join(lines)[2:].split("\n*")]
				element = block_markup.List(indentation, items)
			elif re.match(".*::\s*$", lines[0]):
				# Argument definition
				argname = re.match("(.*)::\s*$", lines[0]).group(1)
				element = block_markup.Argument(indentation, " ".join(line.lstrip() for line in lines[1:]), argname)
			elif lines[0].strip() == "{TOC}":
				# Table of contents
				element = block_markup.Index(indentation, self)
			else:
				# Text
				element = block_markup.Text(indentation, " ".join(lines))
			
			self.current_elements[indentation - 1].add(element)
			current_level = indentation
			self.current_elements[current_level] = element
	
	def transform(self, ruleset):
		return self.current_elements[0].transform(ruleset)
	
	def get_definitions(self):
		return self.definitions
