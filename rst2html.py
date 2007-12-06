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

overrides = {
	'embed_stylesheet': False,
	'stylesheet_path': None,
	'stylesheet': '_support/style.css',
	}


import docutils.parsers.rst.directives
def code_block(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
	language = arguments[0]
	node = docutils.nodes.literal_block(text='\n'.join(content))
	node.attributes['code'] = language
	return [node]
# http://docutils.sourceforge.net/spec/howto/rst-directives.html
code_block.options = {'language': docutils.parsers.rst.directives.unchanged}
code_block.arguments = (
	1,  # Number of required arguments
	0,  # Number of optional arguments
	False)  # final argument may contain whitespace
code_block.content = True  # content is allowed


from docutils.parsers.rst import directives
directives.register_directive('code-block', code_block)


from docutils.writers import html4css1

class MyHTMLTranslator(html4css1.HTMLTranslator):
	def visit_document(self, node):
		html4css1.HTMLTranslator.visit_document(self, node)
		self.head.append('<script type="text/javascript" src="_support/highlight.js"></script>\n')
		self.head.append('<script type="text/javascript">initHighlightingOnLoad("cpp");</script>\n')
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

from docutils.core import publish_file, publish_parts

publish_file(
		source_path=in_file,
		destination_path=out_file,
		settings_overrides=overrides,
		#writer_name='html'
		writer=html_writer)
