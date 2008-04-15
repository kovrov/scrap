====
LZSS
====

The compression algorithm lz77 belongs to the family of compressors without loss, also called text compressors, which are called so because they omit information compressing the file, unlike compressors using lossy algorithms of the type that omitted some information but they decrease the size of the original file, which is the case with MP3 files, MPG, jpeg, etc..

Features
========

The compressors based algorithms without loss when used to compress information is critical and can not be losing information, such as in executable files, database tables, or any kind of information that does not support loss.

Lz77 The model is widely used because it is easy to implement and is quite efficient.

In 1977 1977 Abraham Lempel and Jacob Ziv Lempel Ziv compression presented their model based on dictionary for text compression-compression text refers to compression without losing any data type. To date, all compression algorithms developed compressors were basically static. The main difference is in the output, lz77 always gave to displacement / size, even if the match was a single byte (where more than eight bits used to represent a byte) so that the LZSS uses another trick to make it better : Use flags (flags), which occupies a single bit and tell us what comes after: a literal or a couple displacement / size and this algorithm is currently used, but the lzss is commonly called lz77, so let's call lz77 this point forward, but it is important to remember that can be called LZSS. LZSS can also use binary tree or trees suffixes to search more efficient.

The theory is very simple and intuitive. When is a coincidence (also called sentence or set of bytes that have already been seen in the input file) instead of writing these bytes are written displacement or size of the repeat: where is and its length.

This is a model based on dictionary, because it keeps a dictionary (which in this case is known as "Window Corrediza") and referred to it with peers displacement / size. This version of lz77, uses a sliding window, which has a maximum size, so that the window may not be the complete file, instead, keeps sliding window last byte "seen".

Compacting
==========

Imagine that we are compressing the text "ab ab", we read to "ab" and write uncompressed, then read "ab" and wrote the following: with the "displacement" of 0 was found a coincidence of two bytes repeated.

Unpacking
=========

It is quite simple. First we read "ab" and then copy the bytes hence::

	Get 'a'.  "a"
	Get 'b'.  "ab"
	Get ' '.  "ab "
	Get displacement / size. Copy two bytes from the position 0. ("ab")
	"ab ab"

How does it work?
=================

But how decompressor know if what he reads is a pair displacement / size or one byte uncompressed? The answer is simple, use a prefix, a bit serving as a flag, similar to a switch with two states that allows us to know what kind of data below.

http://www.google.com/translate?u=http://es.wikipedia.org/wiki/LZSS&langpair=es|en&hl=en&ie=UTF8
