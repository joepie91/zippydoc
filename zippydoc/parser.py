from block_markup import *

class Parser():
	def __init__(self, template):
		self.template = template
	
	def render(self, text):
		paragraphs = re.split("\s*\n\s*\n", text)
		self.toc_items = []
		current_level = 0
		current_paragraph = 0
		current_elements = {0: TreeLevel(0, "root")}
		
		for paragraph in paragraphs:
			if paragraph.strip() == "":
				continue
				
			current_paragraph += 1
			indentation = len(paragraph) - len(paragraph.lstrip("\t")) + 1
			
			if indentation > current_level + 1:
				raise Exception("Invalid indentation found in paragraph %d" % current_paragraph)
			
			element_type = TreeLevel
			start = indentation - 1
			
			lines = [line[start:] for line in paragraph.splitlines()]
			
			if lines[0].startswith("#"):
				element_type = Header
				depth = len(lines[0]) - len(lines[0].lstrip("#"))
				lines[0] = lines[0].lstrip("# ")
				data = " ".join(lines)
			elif lines[0].startswith("^"):
				element_type = Definition
				lines[0] = lines[0].lstrip("^ ")
				data = "\n".join(lines)
			elif lines[0].startswith("@"):
				element_type = Example
				lines[0] = lines[0].lstrip("@ ")
				data = " ".join(lines)
			elif lines[0].startswith("$$") and current_elements[current_level].__class__.__name__ == "Code":
				current_elements[current_level].data += "\n\n" + "\n".join(lines).lstrip("$ ")
				continue
			elif lines[0].startswith("$"):
				element_type = Code
				lines[0] = lines[0].lstrip("$ ")
				data = "\n".join(lines)
			elif lines[0].startswith(">>") and current_elements[current_level].__class__.__name__ == "Output":
				current_elements[current_level].data += "\n\n" + "\n".join(lines).lstrip("> ")
				continue
			elif lines[0].startswith(">"):
				element_type = Output
				lines[0] = lines[0].lstrip("> ")
				data = "\n".join(lines)
			elif lines[0].startswith("!"):
				element_type = Exclamation
				lines[0] = lines[0].lstrip("! ")
				data = " ".join(lines)
			elif re.match(".*::\s*$", lines[0]):
				element_type = Argument
				argname = lines[0][:-2]
				data = " ".join(line.lstrip() for line in lines[1:])
			elif lines[0].strip() == "{TOC}":
				element_type = Index
				data = self
			else:
				element_type = Text
				data = " ".join(lines)
				
			if element_type.__name__ == "Header":
				element = Header(indentation, data, depth)
			elif element_type.__name__ == "Argument":
				element = Argument(indentation, data, argname)
			else:
				element = element_type(indentation, data)
			
			if element_type.__name__ == "Definition":
				self.toc_items.append(element)
			
			current_elements[indentation - 1].add(element)
			
			current_level = indentation
			current_elements[current_level] = element
		
		return self.template.replace("{CONTENT}", current_elements[0].output())
