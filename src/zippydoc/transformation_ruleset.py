class TransformationRuleset(object):
	def transform_children(self, text):
		pass
		
	def transform_header(self, depth, text):
		pass
	
	def transform_definition(self, forms, children):
		pass
		
	def transform_argument(self, name, description, children):
		pass
	
	def transform_example(self, title, children):
		pass
	
	def transform_code(self, text):
		pass
		
	def transform_output(self, text):
		pass
		
	def transform_exclamation(self, text, children):
		pass
	
	def transform_text(self, text):
		pass
	
	def transform_list(self, items):
		pass
		
	def transform_reference(self, target, description):
		pass
	
	def transform_external_reference(self, target, description):
		pass
		
	def transform_fixed_width(self, text):
		pass
		
	def transform_emphasis(self, text):
		pass
		
	def transform_strong(self, text):
		pass
		
	def transform_toc(self, items):
		pass
