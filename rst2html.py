#!C:\soft\python\python.exe

try:
	import locale
	locale.setlocale(locale.LC_ALL, '')
except:
	pass

import sys
import os

in_file = sys.argv[1]
out_file = os.path.splitext(in_file)[0] + ".html"


from docutils.parsers.rst import directives
from docutils.nodes import literal_block

def code_block(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
	language = arguments[0]
	node = literal_block(text='\n'.join(content))
	node.attributes['code'] = language
	return [node]
# http://docutils.sourceforge.net/spec/howto/rst-directives.html
code_block.options = {'language': directives.unchanged}
code_block.arguments = (1, 0, False)
code_block.content = True

directives.register_directive('code', code_block)


from docutils.writers import html4css1

class MyHTMLTranslator(html4css1.HTMLTranslator):
	def visit_document(self, node):
		html4css1.HTMLTranslator.visit_document(self, node)
		self.head.append('<script type="text/javascript" src="_support/highlight.js"></script>\n')
		self.head.append('<script type="text/javascript">initHighlightingOnLoad();</script>\n')
	def visit_literal_block(self, node):
		html4css1.HTMLTranslator.visit_literal_block(self, node)
		if (node.hasattr('code')):
			self.body.append(self.starttag(node, 'code', CLASS=node.get('code')))
	def depart_literal_block(self, node):
		if (node.hasattr('code')):
			self.body.append('\n</code>\n')
		html4css1.HTMLTranslator.depart_literal_block(self, node)

html_writer = html4css1.Writer()
html_writer.translator_class = MyHTMLTranslator


from docutils.core import publish_file

publish_file(
		source_path=in_file,
		destination_path=out_file,
		writer=html_writer,
		settings_overrides={
			'embed_stylesheet': False,
			'stylesheet_path':  None,
			'stylesheet':      '_support/style.css'})
