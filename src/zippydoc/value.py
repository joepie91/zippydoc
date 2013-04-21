import re

class Value(str):
	def transform(self, ruleset):
		text = self
		text = re.sub("`([^`]+)`", 				lambda x: ruleset.transform_fixed_width(Value(x.group(1))), text)                     # Fixed-width
		text = re.sub("\*\*([^*]+)\*\*", 			lambda x: ruleset.transform_emphasis(Value(x.group(1))), text)                        # Emphasized
		text = re.sub("__([^_]+)__", 				lambda x: ruleset.transform_strong(Value(x.group(1))), text)                          # Strong
		text = re.sub("{>([^}]+)}\(([^)]+)\)", 			lambda x: ruleset.transform_reference(Value(x.group(1)), Value(x.group(2))), text)           # Hyperlink with text
		text = re.sub("{>([^}]+)}", 				lambda x: ruleset.transform_reference(Value(x.group(1)), Value(x.group(1))), text)           # Hyperlink
		text = re.sub("{([^}]+:[^}]+)}\(([^)]+)\)", 		lambda x: ruleset.transform_external_reference(Value(x.group(1)), Value(x.group(2))), text)  # External hyperlink with text
		text = re.sub("{([^}]+:[^}]+)}", 			lambda x: ruleset.transform_external_reference(Value(x.group(1)), Value(x.group(1))), text)  # External hyperlink
		text = re.sub("{<([^}]+)}\(([^)]+)\)", 			lambda x: ruleset.transform_external_reference(Value(x.group(1)), Value(x.group(2))), text)  # Forced external hyperlink with text
		text = re.sub("{<([^}]+)}", 				lambda x: ruleset.transform_external_reference(Value(x.group(1)), Value(x.group(1))), text)  # Forced external hyperlink
		return text
		
	def clean(self):
		text = self
		text = re.sub("`([^`]+)`", '\\1', text)                  # Fixed-width
		text = re.sub("\*\*([^*]+)\*\*", "\\1", text)            # Emphasized
		text = re.sub("__([^_]+)__", "\\1", text)                # Strong
		text = re.sub("{>([^}]+)}\(([^)]+)\)", '\\2', text)      # Hyperlink with text
		text = re.sub("{>([^}]+)}", '\\1', text)                 # Hyperlink
		text = re.sub("{([^}]+:[^}]+)}\(([^)]+)\)", '\\2', text) # External hyperlink with text
		text = re.sub("{([^}]+:[^}]+)}", '\\1', text)            # External hyperlink
		text = re.sub("{<([^}]+)}\(([^)]+)\)", '\\2', text)      # Forced external hyperlink with text
		text = re.sub("{<([^}]+)}", '\\1', text)                 # Forced external hyperlink
		return text
	
