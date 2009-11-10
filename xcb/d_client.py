#!/usr/bin/env python
from xml.etree.cElementTree import *
from os.path import basename
import getopt
import sys
import re

# Jump to the bottom of this file for the main routine

# Some hacks to make the API more readable, and to keep backwards compability
_cname_re = re.compile('([A-Z0-9][a-z]+|[A-Z0-9]+(?![a-z])|[a-z]+)')
_cname_special_cases = {'DECnet':'decnet'}

_extension_special_cases = ['XPrint', 'XCMisc', 'BigRequests']

_cplusplus_annoyances = {'class' : '_class',
						 'new'   : '_new',
						 'delete': '_delete'}

_clines = []
_clevel = 0
_ns = None

def _d(fmt, *args):
	'''
	Writes the given line to the source file.
	'''
	_clines[_clevel].append(fmt % args)

def _c_setlevel(idx):
	'''
	Changes the array that source lines are written to.
	Supports writing to different sections of the source file.
	'''
	global _clevel
	while len(_clines) <= idx:
		_clines.append([])
	_clevel = idx

def _n_item(str):
	'''
	Does C-name conversion on a single string fragment.
	Uses a regexp with some hard-coded special cases.
	'''
	if str in _cname_special_cases:
		return _cname_special_cases[str]
	else:
		split = _cname_re.finditer(str)
		name_parts = [match.group(0) for match in split]
		return '_'.join(name_parts)

def _cpp(str):
	'''
	Checks for certain C++ reserved words and fixes them.
	'''
	if str in _cplusplus_annoyances:
		return _cplusplus_annoyances[str]
	else:
		return str

def _ext(str):
	'''
	Does C-name conversion on an extension name.
	Has some additional special cases on top of _n_item.
	'''
	if str in _extension_special_cases:
		return _n_item(str).lower()
	else:
		return str.lower()

def _n(list):
	'''
	Does C-name conversion on a tuple of strings.
	Different behavior depending on length of tuple, extension/not extension, etc.
	Basically C-name converts the individual pieces, then joins with underscores.
	'''
	if len(list) == 1:
		parts = list
	elif len(list) == 2:
		parts = [list[0], _n_item(list[1])]
	elif _ns.is_ext:
		parts = [list[0], _ext(list[1])] + [_n_item(i) for i in list[2:]]
	else:
		parts = [list[0]] + [_n_item(i) for i in list[1:]]
	return '_'.join(parts).lower()

def _t(list):
	'''
	Does C-name conversion on a tuple of strings representing a type.
	Same as _n but adds a "_t" on the end.
	'''
	if len(list) == 1:
		parts = list
	elif len(list) == 2:
		parts = [list[0], _n_item(list[1]), 't']
	elif _ns.is_ext:
		parts = [list[0], _ext(list[1])] + [_n_item(i) for i in list[2:]] + ['t']
	else:
		parts = [list[0]] + [_n_item(i) for i in list[1:]] + ['t']
	return '_'.join(parts).lower()


def c_open(self):
	'''
	Exported function that handles module open.
	Opens the files and writes out the auto-generated comment, header file includes, etc.
	'''
	global _ns
	_ns = self.namespace
	_ns.c_ext_global_name = _n(_ns.prefix + ('id',))

	# Build the type-name collision avoidance table used by c_enum
	build_collision_table()

	_c_setlevel(0)

	_d('/*')
	_d(' * This file generated automatically from %s by d_client.py.', _ns.file)
	_d(' * Edit at your peril.')
	_d(' */')
	_d('')

	_d('/**')
	_d(' * @defgroup XCB_%s_API XCB %s API', _ns.ext_name, _ns.ext_name)
	_d(' * @brief %s XCB Protocol Implementation.', _ns.ext_name)
	_d(' * @{')
	_d(' **/')
	_d('')
	_d('module %s;', _ns.header)
	_d('')
	_d('import xcb;')

	_d('import xcbext;')

	if _ns.is_ext:
		for (n, h) in self.imports:
			_d('#include "%s.h"', h)

	if _ns.is_ext:
		_d('')
		_d('enum')
		_d('{')
		_d('	XCB_%s_MAJOR_VERSION = %s,', _ns.ext_name.upper(), _ns.major_version)
		_d('	XCB_%s_MINOR_VERSION = %s,', _ns.ext_name.upper(), _ns.minor_version)
		_d('}')
		_d('')
		_d('xcb_extension_t %s = { "%s", 0 };', _ns.c_ext_global_name, _ns.ext_xname)

def c_close(self):
	'''
	Exported function that handles module close.
	Writes out all the stored content lines, then closes the files.
	'''
	_c_setlevel(2)
	_d('')

	# Write source file
	cfile = open('%s.d' % _ns.header, 'w')
	for list in _clines:
		for line in list:
			cfile.write(line)
			cfile.write('\n')
	cfile.close()

def build_collision_table():
	global namecount
	namecount = {}

	for v in module.types.values():
		name = _t(v[0])
		namecount[name] = (namecount.get(name) or 0) + 1

def c_enum(self, name):
	'''
	Exported function that handles enum declarations.
	'''

	tname = _t(name)
	if namecount[tname] > 1:
		tname = _t(name + ('enum',))

	_c_setlevel(0)
	_d('')
	_d('enum %s', tname)
	_d('{')

	for (enam, eval) in self.values:
		equals = ' = ' if eval != '' else ''
		_d('    %s%s%s,', _n(name + (enam,)).upper(), equals, eval)

	_d('}')

def _c_type_setup(self, name, postfix, v=False):
	'''
	Sets up all the C-related state by adding additional data fields to
	all Field and Type objects.  Here is where we figure out most of our
	variable and function names.

	Recurses into child fields and list member types.
	'''
	# Do all the various names in advance
	self.c_type = _t(name + postfix)
	self.c_wiretype = 'char' if self.c_type == 'void' else self.c_type
	self.c_iterator_type = _t(name + ('iterator',))
	self.c_next_name = _n(name + ('next',))
	self.c_end_name = _n(name + ('end',))
	self.c_request_name = _n(name)
	self.c_checked_name = _n(name + ('checked',))
	self.c_unchecked_name = _n(name + ('unchecked',))
	self.c_reply_name = _n(name + ('reply',))
	self.c_reply_type = _t(name + ('reply',))
	self.c_cookie_type = _t(name + ('cookie',))

	if not self.is_container:
		return

	self.c_container = 'union' if self.is_union else 'struct'
	prev_varsized_field = None
	prev_varsized_offset = 0
	first_field_after_varsized = None

	for field in self.fields:
		_c_type_setup(field.type, field.field_type, ())
		if field.type.is_list:
			_c_type_setup(field.type.member, field.field_type, ())

		field.c_field_type = _t(field.field_type)
		field.c_field_const_type = ('' if field.type.nmemb == 1 else 'const ') + field.c_field_type
		field.c_field_name = _cpp(field.field_name)
		field.c_subscript = '[%d]' % field.type.nmemb if (field.type.nmemb > 1) else ''
		field.c_pointer = ' ' if field.type.nmemb == 1 else '*'

		field.c_iterator_type = _t(field.field_type + ('iterator',))      # xcb_fieldtype_iterator_t
		field.c_iterator_name = _n(name + (field.field_name, 'iterator')) # xcb_container_field_iterator
		field.c_accessor_name = _n(name + (field.field_name,))            # xcb_container_field
		field.c_length_name = _n(name + (field.field_name, 'length'))     # xcb_container_field_length
		field.c_end_name = _n(name + (field.field_name, 'end'))           # xcb_container_field_end

		field.prev_varsized_field = prev_varsized_field
		field.prev_varsized_offset = prev_varsized_offset

		if prev_varsized_offset == 0:
			first_field_after_varsized = field
		field.first_field_after_varsized = first_field_after_varsized

		if field.type.fixed_size():
			prev_varsized_offset += field.type.size
		else:
			self.last_varsized_field = field
			prev_varsized_field = field
			prev_varsized_offset = 0

def _c_iterator_get_end(field, accum):
	'''
	Figures out what C code is needed to find the end of a variable-length structure field.
	For nested structures, recurses into its last variable-sized field.
	For lists, calls the end function
	'''
	if field.type.is_container:
		accum = field.c_accessor_name + '(' + accum + ')'
		# XXX there could be fixed-length fields at the end
		return _c_iterator_get_end(field.type.last_varsized_field, accum)
	if field.type.is_list:
		# XXX we can always use the first way
		if field.type.member.is_simple:
			return field.c_end_name + '(' + accum + ')'
		else:
			return field.type.member.c_end_name + '(' + field.c_iterator_name + '(' + accum + '))'

def _c_iterator(self, name):
	'''
	Declares the iterator structure and next/end functions for a given type.
	'''
	_c_setlevel(0)
	_d('')
	_d('/**')
	_d(' * @brief %s', self.c_iterator_type)
	_d(' **/')
	_d('struct %s', self.c_iterator_type)
	_d('{')
	_d('    %s* data;', self.c_type)
	_d('    int%s rem;', ' ' * (len(self.c_type) - 2))
	_d('    int%s index;', ' ' * (len(self.c_type) - 2))
	_d('}')

	_c_setlevel(1)
	_d('')
	_d('')
	_d('/**')
	_d(' * Get the next element of the iterator')
	_d(' * @param i Pointer to a %s', self.c_iterator_type)
	_d(' *')
	_d(' * Get the next element in the iterator. The member rem is')
	_d(' * decreased by one. The member data points to the next')
	_d(' * element. The member index is increased by %s.sizeof', self.c_type)
	_d(' */')
	_d(' ')
	_d('void %s(%s* i)', self.c_next_name, self.c_iterator_type)
	_d('{')

	if not self.fixed_size():
		_d('    %s* R = i.data;', self.c_type)
		_d('    xcb_generic_iterator_t child = %s;', _c_iterator_get_end(self.last_varsized_field, 'R'))
		_d('    --i.rem;')
		_d('    i.data = cast(%s*)child.data;', self.c_type)
		_d('    i.index = child.index;')
	else:
		_d('    --i.rem;')
		_d('    ++i.data;')
		_d('    i.index += %s.sizeof;', self.c_type)

	_d('}')

	_d('')
	_d('')
	_d('/**')
	_d(' * Return the iterator pointing to the last element')
	_d(' * @param i An %s', self.c_iterator_type)
	_d(' * @return  The iterator pointing to the last element')
	_d(' *')
	_d(' * Set the current element in the iterator to the last element.')
	_d(' * The member rem is set to 0. The member data points to the')
	_d(' * last element.')
	_d(' */')
	_d('')
	_d('xcb_generic_iterator_t %s(%s i)', self.c_end_name, self.c_iterator_type)
	_d('{')
	_d('    xcb_generic_iterator_t ret;')

	if self.fixed_size():
		_d('    ret.data = i.data + i.rem;')
		_d('    ret.index = i.index + (cast(char*)ret.data - cast(char*)i.data);')
		_d('    ret.rem = 0;')
	else:
		_d('    while (i.rem > 0)')
		_d('        %s(&i);', self.c_next_name)
		_d('    ret.data = i.data;')
		_d('    ret.rem = i.rem;')
		_d('    ret.index = i.index;')

	_d('    return ret;')
	_d('}')

def _c_accessor_get_length(expr, prefix=''):
	'''
	Figures out what C code is needed to get a length field.
	For fields that follow a variable-length field, use the accessor.
	Otherwise, just reference the structure field directly.
	'''
	prefarrow = '' if prefix == '' else prefix + '.'

	if expr.lenfield != None and expr.lenfield.prev_varsized_field != None:
		return expr.lenfield.c_accessor_name + '(' + prefix + ')'
	elif expr.lenfield_name != None:
		return prefarrow + expr.lenfield_name
	else:
		return str(expr.nmemb)

def _c_accessor_get_expr(expr, prefix=''):
	'''
	Figures out what C code is needed to get the length of a list field.
	Recurses for math operations.
	Returns bitcount for value-mask fields.
	Otherwise, uses the value of the length field.
	'''
	lenexp = _c_accessor_get_length(expr, prefix)

	if expr.op != None:
		return '(' + _c_accessor_get_expr(expr.lhs, prefix) + ' ' + expr.op + ' ' + _c_accessor_get_expr(expr.rhs, prefix) + ')'
	elif expr.bitfield:
		return 'xcb_popcount(' + lenexp + ')'
	else:
		return lenexp

def _c_accessors_field(self, field):
	'''
	Declares the accessor functions for a non-list field that follows a variable-length field.
	'''
	if field.type.is_simple:
		_d('')
		_d('')
		_d('/*****************************************************************************')
		_d(' **')
		_d(' ** %s %s', field.c_field_type, field.c_accessor_name)
		_d(' ** ')
		_d(' ** @param const %s* R', self.c_type)
		_d(' ** @returns %s', field.c_field_type)
		_d(' **/')
		_d(' ')
		_d('%s', field.c_field_type)
		_d('%s(const %s* R)', field.c_accessor_name, self.c_type)
		_d('{')
		_d('    xcb_generic_iterator_t prev = %s;', _c_iterator_get_end(field.prev_varsized_field, 'R'))
		_d('    return * cast(%s*)(cast(char*)prev.data + XCB_TYPE_PAD(%s, prev.index) + %d);', field.c_field_type, field.first_field_after_varsized.type.c_type, field.prev_varsized_offset)
		_d('}')
	else:
		_d('')
		_d('')
		_d('/*****************************************************************************')
		_d(' **')
		_d(' ** %s*  %s', field.c_field_type, field.c_accessor_name)
		_d(' ** ')
		_d(' ** @param const %s* R', self.c_type)
		_d(' ** @returns %s* ', field.c_field_type)
		_d(' **/')
		_d(' ')
		_d('%s* ', field.c_field_type)
		_d('%s(const %s* R)', field.c_accessor_name, self.c_type)
		_d('{')
		_d('    xcb_generic_iterator_t prev = %s;', _c_iterator_get_end(field.prev_varsized_field, 'R'))
		_d('    return cast(%s*)(cast(char*)prev.data + XCB_TYPE_PAD(%s, prev.index) + %d);', field.c_field_type, field.first_field_after_varsized.type.c_type, field.prev_varsized_offset)
		_d('}')

def _c_accessors_list(self, field):
	'''
	Declares the accessor functions for a list field.
	Declares a direct-accessor function only if the list members are fixed size.
	Declares length and get-iterator functions always.
	'''
	list = field.type

	_c_setlevel(1)
	if list.member.fixed_size():
		_d('')
		_d('')
		_d('/*****************************************************************************')
		_d(' **')
		_d(' ** %s* %s', field.c_field_type, field.c_accessor_name)
		_d(' ** ')
		_d(' ** @param const %s* R', self.c_type)
		_d(' ** @returns %s* ', field.c_field_type)
		_d(' **/')
		_d(' ')
		_d('%s* ', field.c_field_type)
		_d('%s(const %s* R)', field.c_accessor_name, self.c_type)
		_d('{')

		if field.prev_varsized_field == None:
			_d('    return cast(%s*)(R + 1);', field.c_field_type)
		else:
			_d('    xcb_generic_iterator_t prev = %s;', _c_iterator_get_end(field.prev_varsized_field, 'R'))
			_d('    return cast(%s*)(cast(char*)prev.data + XCB_TYPE_PAD(%s, prev.index) + %d);', field.c_field_type, field.first_field_after_varsized.type.c_type, field.prev_varsized_offset)

		_d('}')

	_d('')
	_d('')
	_d('/*****************************************************************************')
	_d(' **')
	_d(' ** int %s', field.c_length_name)
	_d(' ** ')
	_d(' ** @param const %s* R', self.c_type)
	_d(' ** @returns int')
	_d(' **/')
	_d(' ')
	_d('int %s(const %s* R)', field.c_length_name, self.c_type)
	_d('{')
	_d('    return %s;', _c_accessor_get_expr(field.type.expr, 'R'))
	_d('}')

	if field.type.member.is_simple:
		_d('')
		_d('')
		_d('/*****************************************************************************')
		_d(' **')
		_d(' ** xcb_generic_iterator_t %s', field.c_end_name)
		_d(' ** ')
		_d(' ** @param const %s* R', self.c_type)
		_d(' ** @returns xcb_generic_iterator_t')
		_d(' **/')
		_d(' ')
		_d('xcb_generic_iterator_t %s(const %s* R)', field.c_end_name, self.c_type)
		_d('{')
		_d('    xcb_generic_iterator_t i;')

		if field.prev_varsized_field == None:
			_d('    i.data = (cast(%s*)(R + 1)) + (%s);', field.type.c_wiretype, _c_accessor_get_expr(field.type.expr, 'R'))
		else:
			_d('    xcb_generic_iterator_t child = %s;', _c_iterator_get_end(field.prev_varsized_field, 'R'))
			_d('    i.data = (cast(%s*)child.data) + (%s);', field.type.c_wiretype, _c_accessor_get_expr(field.type.expr, 'R'))

		_d('    i.rem = 0;')
		_d('    i.index = cast(char*)i.data - cast(char*)R;')
		_d('    return i;')
		_d('}')

	else:
		_d('')
		_d('')
		_d('/*****************************************************************************')
		_d(' **')
		_d(' ** %s %s', field.c_iterator_type, field.c_iterator_name)
		_d(' ** ')
		_d(' ** @param const %s* R', self.c_type)
		_d(' ** @returns %s', field.c_iterator_type)
		_d(' **/')
		_d(' ')
		_d('%s', field.c_iterator_type)
		_d('%s(const %s* R)', field.c_iterator_name, self.c_type)
		_d('{')
		_d('    %s i;', field.c_iterator_type)

		if field.prev_varsized_field == None:
			_d('    i.data = cast(%s*)(R + 1);', field.c_field_type)
		else:
			_d('    xcb_generic_iterator_t prev = %s;', _c_iterator_get_end(field.prev_varsized_field, 'R'))
			_d('    i.data = cast(%s*)(cast(char*)prev.data + XCB_TYPE_PAD(%s, prev.index));', field.c_field_type, field.c_field_type)

		_d('    i.rem = %s;', _c_accessor_get_expr(field.type.expr, 'R'))
		_d('    i.index = cast(char*)i.data - cast(char*)R;')
		_d('    return i;')
		_d('}')

def _c_accessors(self, name, base):
	'''
	Declares the accessor functions for the fields of a structure.
	'''
	for field in self.fields:
		if field.type.is_list and not field.type.fixed_size():
			_c_accessors_list(self, field)
		elif field.prev_varsized_field != None:
			_c_accessors_field(self, field)

def c_simple(self, name):
	'''
	Exported function that handles cardinal type declarations.
	These are types which are typedef'd to one of the CARDx's, char, float, etc.
	'''
	_c_type_setup(self, name, ())

	if (self.name != name):
		# Typedef
		_c_setlevel(0)
		my_name = _t(name)
		_d('')
		_d('alias %s %s;', _t(self.name), my_name)

		# Iterator
		_c_iterator(self, name)

def _c_complex(self):
	'''
	Helper function for handling all structure types.
	Called for all structs, requests, replies, events, errors.
	'''
	_c_setlevel(0)
	_d('')
	_d('/**')
	_d(' * @brief %s', self.c_type)
	_d(' **/')
	_d('%s %s', self.c_container, self.c_type)
	_d('{')

	struct_fields = []
	maxtypelen = 0

	varfield = None
	for field in self.fields:
		if not field.type.fixed_size():
			varfield = field.c_field_name
			continue
		if varfield != None and not field.type.is_pad and field.wire:
			errmsg = '%s: warning: variable field %s followed by fixed field %s\n' % (self.c_type, varfield, field.c_field_name)
			sys.stderr.write(errmsg)
			# sys.exit(1)
		if field.wire:
			struct_fields.append(field)

	for field in struct_fields:
		if len(field.c_field_type) + len(field.c_subscript) > maxtypelen:
			maxtypelen = len(field.c_field_type) + len(field.c_subscript)

	for field in struct_fields:
		spacing = ' ' * (maxtypelen - len(field.c_field_type) - len(field.c_subscript))
		_d('    %s%s%s %s;', field.c_field_type, field.c_subscript, spacing, field.c_field_name)

	_d('}')

def c_struct(self, name):
	'''
	Exported function that handles structure declarations.
	'''
	_c_type_setup(self, name, ())
	_c_complex(self)
	_c_accessors(self, name, name)
	_c_iterator(self, name)

def c_union(self, name):
	'''
	Exported function that handles union declarations.
	'''
	_c_type_setup(self, name, ())
	_c_complex(self)
	_c_iterator(self, name)

def _c_request_helper(self, name, cookie_type, void, regular):
	'''
	Declares a request function.
	'''

	# Four stunningly confusing possibilities here:
	#
	#   Void            Non-void
	# ------------------------------
	# "req"            "req"
	# 0 flag           CHECKED flag   Normal Mode
	# void_cookie      req_cookie
	# ------------------------------
	# "req_checked"    "req_unchecked"
	# CHECKED flag     0 flag         Abnormal Mode
	# void_cookie      req_cookie
	# ------------------------------


	# Whether we are _checked or _unchecked
	checked = void and not regular
	unchecked = not void and not regular

	# What kind of cookie we return
	func_cookie = 'xcb_void_cookie_t' if void else self.c_cookie_type

	# What flag is passed to xcb_request
	func_flags = '0' if (void and regular) or (not void and not regular) else 'XCB_REQUEST_CHECKED'

	# Global extension id variable or NULL for xproto
	func_ext_global = '&' + _ns.c_ext_global_name if _ns.is_ext else '0'

	# What our function name is
	func_name = self.c_request_name
	if checked:
		func_name = self.c_checked_name
	if unchecked:
		func_name = self.c_unchecked_name

	param_fields = []
	wire_fields = []
	maxtypelen = len('xcb_connection_t')

	for field in self.fields:
		if field.visible:
			# The field should appear as a call parameter
			param_fields.append(field)
		if field.wire and not field.auto:
			# We need to set the field up in the structure
			wire_fields.append(field)

	for field in param_fields:
		if len(field.c_field_const_type) > maxtypelen:
			maxtypelen = len(field.c_field_const_type)

	_c_setlevel(1)
	_d('')
	_d('')
	_d('/**')
	_d(' * Delivers a request to the X server')
	_d(' * @param c The connection')
	_d(' * @return A cookie')
	_d(' *')
	_d(' * Delivers a request to the X server.')
	if checked:
		_d(' * ')
		_d(' * This form can be used only if the request will not cause')
		_d(' * a reply to be generated. Any returned error will be')
		_d(' * saved for handling by xcb_request_check().')
	if unchecked:
		_d(' * ')
		_d(' * This form can be used only if the request will cause')
		_d(' * a reply to be generated. Any returned error will be')
		_d(' * placed in the event queue.')
	_d(' */')
	_d('')

	comma = ',' if len(param_fields) else ')'
	_d('%s %s(xcb_connection_t* c%s', cookie_type, func_name, comma)

	func_spacing = ' ' * (len(func_name) + 2)
	count = len(param_fields)
	for field in param_fields:
		count = count - 1
		spacing = ' ' * (maxtypelen - len(field.c_field_const_type))
		comma = ',' if count else ')'
		_d('%s%s%s %s%s%s', func_spacing, field.c_field_const_type, spacing, field.c_pointer, field.c_field_name, comma)

	count = 2
	for field in param_fields:
		if not field.type.fixed_size():
			count = count + 2

	_d('{')
	_d('    static const xcb_protocol_request_t xcb_req = {')
	_d('        /* count */ %d,', count)
	_d('        /* ext */ %s,', func_ext_global)
	_d('        /* opcode */ %s,', self.c_request_name.upper())
	_d('        /* isvoid */ %d', 1 if void else 0)
	_d('    };')
	_d('    ')
	_d('    struct iovec[%d] xcb_parts;', count + 2)
	_d('    %s xcb_ret;', func_cookie)
	_d('    %s xcb_out;', self.c_type)
	_d('    ')

	for field in wire_fields:
		if field.type.fixed_size():
			if field.type.is_expr:
				_d('    xcb_out.%s = %s;', field.c_field_name, _c_accessor_get_expr(field.type.expr))

			elif field.type.is_pad:
				if field.type.nmemb == 1:
					_d('    xcb_out.%s = 0;', field.c_field_name)
				else:
					_d('    memset(xcb_out.%s, 0, %d);', field.c_field_name, field.type.nmemb)
			else:
				if field.type.nmemb == 1:
					_d('    xcb_out.%s = %s;', field.c_field_name, field.c_field_name)
				else:
					_d('    memcpy(xcb_out.%s, %s, %d);', field.c_field_name, field.c_field_name, field.type.nmemb)

	_d('    ')
	_d('    xcb_parts[2].iov_base = cast(char*)&xcb_out;')
	_d('    xcb_parts[2].iov_len = xcb_out.sizeof;')
	_d('    xcb_parts[3].iov_base = 0;')
	_d('    xcb_parts[3].iov_len = -xcb_parts[2].iov_len & 3;')

	count = 4
	for field in param_fields:
		if not field.type.fixed_size():
			_d('    xcb_parts[%d].iov_base = cast(char*)%s;', count, field.c_field_name)
			if field.type.is_list:
				_d('    xcb_parts[%d].iov_len = %s * %s.sizeof;', count, _c_accessor_get_expr(field.type.expr), field.type.member.c_wiretype)
			else:
				_d('    xcb_parts[%d].iov_len = %s * %s.sizeof;', count, 'Uh oh', field.type.c_wiretype)
			_d('    xcb_parts[%d].iov_base = 0;', count + 1)
			_d('    xcb_parts[%d].iov_len = -xcb_parts[%d].iov_len & 3;', count + 1, count)
			count = count + 2

	_d('    xcb_ret.sequence = xcb_send_request(c, %s, xcb_parts + 2, &xcb_req);', func_flags)
	_d('    return xcb_ret;')
	_d('}')

def _c_reply(self, name):
	'''
	Declares the function that returns the reply structure.
	'''
	_d('')
	_d('')
	_d('/**')
	_d(' * Return the reply')
	_d(' * @param c      The connection')
	_d(' * @param cookie The cookie')
	_d(' * @param e      The xcb_generic_error_t supplied')
	_d(' *')
	_d(' * Returns the reply of the request asked by')
	_d(' * ')
	_d(' * The parameter @p e supplied to this function must be NULL if')
	_d(' * %s(). is used.', self.c_unchecked_name)
	_d(' * Otherwise, it stores the error if any.')
	_d(' *')
	_d(' * The returned value must be freed by the caller using free().')
	_d(' */')
	_d('')
	_d('%s* %s(xcb_connection_t* c, %s cookie, xcb_generic_error_t** e)',
			self.c_reply_type, self.c_reply_name, self.c_cookie_type)
	_d('{')
	_d('    return cast(%s*)xcb_wait_for_reply(c, cookie.sequence, e);', self.c_reply_type)
	_d('}')

def _c_opcode(name, opcode):
	'''
	Declares the opcode define for requests, events, and errors.
	'''
	_c_setlevel(0)
	_d('')
	_d('/** Opcode for %s. */', _n(name))
	_d('immutable %s = %s;', _n(name).upper(), opcode)

def _c_cookie(self, name):
	'''
	Declares the cookie type for a non-void request.
	'''
	_c_setlevel(0)
	_d('')
	_d('/**')
	_d(' * @brief %s', self.c_cookie_type)
	_d(' **/')
	_d('struct %s', self.c_cookie_type)
	_d('{')
	_d('    unsigned int sequence;')
	_d('}')

def c_request(self, name):
	'''
	Exported function that handles request declarations.
	'''
	_c_type_setup(self, name, ('request',))

	if self.reply:
		# Cookie type declaration
		_c_cookie(self, name)

	# Opcode define
	_c_opcode(name, self.opcode)

	# Request structure declaration
	_c_complex(self)

	if self.reply:
		_c_type_setup(self.reply, name, ('reply',))
		# Reply structure definition
		_c_complex(self.reply)
		# Request prototypes
		_c_request_helper(self, name, self.c_cookie_type, False, True)
		_c_request_helper(self, name, self.c_cookie_type, False, False)
		# Reply accessors
		_c_accessors(self.reply, name + ('reply',), name)
		_c_reply(self, name)
	else:
		# Request prototypes
		_c_request_helper(self, name, 'xcb_void_cookie_t', True, False)
		_c_request_helper(self, name, 'xcb_void_cookie_t', True, True)

def c_event(self, name):
	'''
	Exported function that handles event declarations.
	'''
	_c_type_setup(self, name, ('event',))

	# Opcode define
	_c_opcode(name, self.opcodes[name])

	if self.name == name:
		# Structure definition
		_c_complex(self)
	else:
		# Typedef
		_d('')
		_d('alias %s %s;', _t(self.name + ('event',)), _t(name + ('event',)))

def c_error(self, name):
	'''
	Exported function that handles error declarations.
	'''
	_c_type_setup(self, name, ('error',))

	# Opcode define
	_c_opcode(name, self.opcodes[name])

	if self.name == name:
		# Structure definition
		_c_complex(self)
	else:
		# Typedef
		_d('')
		_d('alias %s %s;', _t(self.name + ('error',)), _t(name + ('error',)))



# Main routine starts here

# Must create an "output" dictionary before any xcbgen imports.
output = {'open'    : c_open,
		  'close'   : c_close,
		  'simple'  : c_simple,
		  'enum'    : c_enum,
		  'struct'  : c_struct,
		  'union'   : c_union,
		  'request' : c_request,
		  'event'   : c_event,
		  'error'   : c_error}

# Boilerplate below this point

# Check for the argument that specifies path to the xcbgen python package.
try:
	opts, args = getopt.getopt(sys.argv[1:], 'p:')
except getopt.GetoptError, err:
	print str(err)
	print 'Usage: d_client.py [-p path] file.xml'
	sys.exit(1)

for (opt, arg) in opts:
	if opt == '-p':
		sys.path.append(arg)

# Import the module class
try:
	#import xcbgen.xtypes
	import xtypes
	xtypes.tcard8 = xtypes.SimpleType(('ubyte',), 1)
	xtypes.tcard16 = xtypes.SimpleType(('ushort',), 2)
	xtypes.tcard32 = xtypes.SimpleType(('uint',), 4)
	xtypes.tint8 =  xtypes.SimpleType(('byte',), 1)
	xtypes.tint16 = xtypes.SimpleType(('short',), 2)
	xtypes.tint32 = xtypes.SimpleType(('int',), 4)
	xtypes.tchar =  xtypes.SimpleType(('char',), 1)
	xtypes.tfloat = xtypes.SimpleType(('float',), 4)
	xtypes.tdouble = xtypes.SimpleType(('double',), 8)
	#from xcbgen.state import Module
	from state import Module
except ImportError:
	print '''
	Failed to load the xcbgen Python package!
	Make sure that xcb/proto installed it on your Python path.
	If not, you will need to create a .pth file or define $PYTHONPATH
	to extend the path.
	Refer to the README file in xcb/proto for more info.
	'''
	raise

# Parse the xml header
module = Module(args[0], output)

# Build type-registry and resolve type dependencies
module.register()
module.resolve()

# Output the code
module.generate()
