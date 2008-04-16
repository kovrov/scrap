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

If the prefix is 0, then what lies ahead is a byte uncompressed. If, instead, the prefix is 1, then what follows is a par displacement / size. These prefixes are also called "flags". 

The couple displacement / size is called a keyword. A keyword is a group of bits (or bytes) containing some kind of information used by the compressor and decompressor. The other possible exit is a literal lz77, which is just one byte uncompressed, so that the output can be lz77 in three ways:

1. Literals: they are simply bytes uncompressed.
2. Keywords: in our case are pairs size / displacement.
3. Flags: just tell us if there is data below are verbatim or keywords. 

Now, as an example, see again our chain and a real departure lz77 an algorithm::

	Get 'a'.  Without coincidence.  Flag 0. Literal 'a'.
	Get 'b'.  Without coincidence.  Flag 0. Literal 'b'.
	Get ' '.  Without coincidence.  Flag 0. Literal ' '.
	Get 'a'.  Coincidencia.         Flag 1. Keyword: displacement = 0, size = 2.

As you can see the flag has only two possible states, so that only need a bit to represent. Now we should not represent the flags as byte complete, we should work with bits. The output of this compression is called a stream of bits, it is a stream of symbols of variable size, and the minimum unit is the bit.

Sliding Window
==============

Looking at the above example again, one might ask: Where do we look for matches for a phrase? The answer is to look backwards, in the data we have already processed. This is known as the sliding window. The sliding window is a buffer that holds the bytes that are before the current position in the file. All bytes of uncompressed output (literal) are added to the sliding window and the bytes that make up a match.

Let's look at our example again::

	Get 'a'. VC: "".    Without coincidence.  Flag 0. Literal 'a'.
	Get 'b'. VC: "a".   Without coincidence.  Flag 0. Literal 'b'.
	Get ' '. VC: "ab".  Without coincidence.  Flag 0. Literal ' '.
	Get 'a'. VC: "ab ". Coincidence.          Flag 1. Keyword: displacement = 0, size = 2.

As can be seen, when we seek common ground and compare the data we have in our sliding window (VC) with the data in the current position.

So we have to maintain a buffer with data on the current position and a buffer with the sliding window? In some implementations this may be true, but the implementation shown here is not how they do things, because both the sliding window and the bytes in the current position, they are the same file. Only maintain a buffer, which contains the file. Then we need only worry pointer to the current position, and this just before sliding window of that pointer. In fact it is recommended to have the complete file (or at least a big block of it) and compressing it, so that we do not care to read more bytes.

Let's talk now about the sliding window, what size should have? We could work with the entire file, but we must think about the movement necessary to specify the position or coincidence. This shift is not from the position 0 (the top of the file) to the coincidence, is from the current position backwards. So in the example displacement must be 3 instead of 0 (so that, when it decompresses, the decompressor gets a three and the remainder of the current displacement). As expected, the larger the window size, the greater number of bits needed to store the pointer, so we must choose a size for the sliding window. 4096K is a commonly used size, but it is known that the greater the sliding window, the better compression. So when implemented can choose any size and consider that if, for example, choose a size of 13 bits 8192K need for the movement.

Sizes
=====

Another aspect is that we should choose the size of the length. So, how many bits we use for the length? We can choose any size you want, but we must consider that refine the bits the size of the length and bits of the pointer displacement we can improve the compression in some files and worse in others, so if we are designing a compressor for a single file, values should be more appropriate, otherwise we will use a size of 0-32, only 5 bits.

Another important aspect is the minimum length of a match. In our case we have chosen to use 13-bit displacement and 5 in the length of the match, a total of 18 bits, so that a match should be at least 3 bytes. Because if encrypt a coincidence with two bytes (16 bits) and use 18 bits to store the string we are using 2 bits that if we keep as a literal.

Then they rose another question. If I ever have matches 0, 1 or 2 bytes, then why do we have space for them at length?

To make the most possible. Our size will still be represented with 5 bits, but its range rather than 0-32 will be 3-35. How do we do this? Just gloss size (before saving) 3, and decompressor read it and add 3. 

Marker End
==========

Now that we know what the decompression must note that the decompressor should know when to stop or how to end. This can be done in two ways:

* It is a symbol that marks the end of the data.
* It's kept next to the string of bits the size of the input file. 

Perhaps the second method is preferable. It is a bit slower, but at the same time it is used to know the end of the data. It can be used in a possible interface and can help avoid some problems. Either way, if you want to use a marker so we could use data to zero size. The way that is done is the following:

* The range will be from 3-34, in this case we must subtract the size (when store) 2. So the range 1-32 became 3-34, and the compressor should only deal with this by compressing the file, once compression is completed, the output displacement / size has size 0.
* The decompressor must then verify every time he reads a size if this size is 0, to see if you reach the end of the file. 

Working with Bits
=================

As can be seen, displacement and sizes are of variable length, and the flags took only a bit, so we must use bits instead of bytes. This is very important in most of the compression algorithms.

Most operations working with bytes and when you write information to a minimum unit is a byte, then, to write bits make clever use of some instructions.

To achieve this we use ASM, or if not, can be implemented in C. Continue operations with bits in ASM. The main idea is to keep a byte and a counter with bits written, then when we have 8-bit byte to write this file and start again with the next byte. The following is an example using instructions from ASM.
::

	@@put_bits_loop:
	push cx                ;the number of bits to write
	mov bh,_byte_out       ;the output byte (where to write)
	mov bl,_byte_in        ;the input byte (the bits to write)
	mov al, bl             ;we store the byte to read from in al
	shr al,1               ;we shift to the right al, first bit in the carry flag
	xor ah, ah             ;put ah=0
	adc ah,0               ;we add to ah 0 and the carry
	mov bl, al             ;save the input byte
	mov cl,_total_bits     ;the bits that we have writed
	shl ah, cl             ;put the bit in his position by shifting it to the left
	or bh, al              ;put the bit in the output byte
	mov _byte_out,bh       ;save
	inc _total_bits        ;the bits written
	cmp _total_bits,8      ;Do we have write the whole byte?
	jne @@no_write_byte    ;nop E-)
	mov di,ptr_buffer      ;the pointer to the buffer
	mov es:[di],bh         ;save the byte (es is the segment of the buffer)
	inc di                 ;next byte in the buffer
	mov ptr_buffer,di      ;save it for the next time
	inc bytes_writed       ;when the buffer its full write it to
	mov _byte_out,0        ;a file or something like that so the next time is clear
	@@no_write_byte:       ;we saved it
	pop cx                 ;more bits to write?
	dec cx                 ;yes, repeat everything
	jnz @@put_bits_loop

We present the routine putbits, the names of the variables are self-explanatory but still and all present here a description:

* **_byte_out:** The byte that will be written in the buffer output keeps the bits that we are now writing.
* **_byte_in:** The byte that contains the bits that we want to write.
* **_total_bits:** The number of bits that have been written today, zero at the beginning.
* **Ptr_buffer:** displacement of the buffer. 

When you enter this routine cx must have the number of bits to write, and to write _bite_in bits. Be careful, after entering the cycle we must test whether cx 0 because if it is zero and is not proof write a bit, then would cx - 1, which would result in 255 to write 255 bits.

Remember::

	Test cx, cx
	jz@@put_bits_end

This is the structure (how the bits are written) for a byte:

======= ======= ======= ======= ======= ======= ======= ======= 
Bit 8 	Bit 7 	Bit 6 	Bit 5 	Bit 4 	Bit 3 	Bit 2 	Bit 1
======= ======= ======= ======= ======= ======= ======= ======= 

When you have written all the bits (compression has been completed) should be tested if there are still bits waiting to be written, so if there are some (total_bits! = 0) wrote _byte_out and increase all pointers in a way that does not leave without data write.

File Output
===========

We must now define the format of output file, which will be simple, simply fill our needs, the compressed data will be like:

* First a word with the size of the original file, and if you want some numbers as identification.
* Then the flow of bits, which constitutes and contains compressed data. 

Pseudo code
===========

Remember how it works lz77, one is at a given position and seeking backwards (because it is certain that the decompressor and already decoded these bytes when one is in such a position) a coincidence, bytes that are equal to the bytes at the current position, if they are writing a keyword, otherwise you write a letter to continue compressing.

basic sequence: Compressor
--------------------------
* Save the file size to compress.
* Repeat until they have more bytes to compress.
* Scan the buffer input beginning at posición_actual - tamaño_de_ventana_corrediza until we are comparing current byte. (Note that the decompressor can not copy bytes in a position where their bytes have not been previously defined).
* Did we find a byte equal to the present?
* If Case:
   * Compare the following byte from the current position with the change in the position where we find after a byte equal to the first.
   * Continue comparing until we find a byte that is not the same.
   * It has been found that not one byte equals. Is the number of bytes higher than last year?
   * If Case:
      * Writing the displacement of the first byte found and the number of bytes repeated (size).
      * We move the pointer to the position with the number of bytes repeated (because we have not "saved") and still looking.
      * It also writes a flag 1. 
   * Case No.:
      * The quest.
* Case No.:
   * If there is no coincidence, simply writes a byte uncompressed (also write a letter if there is no data in the sliding window).
   * Must remember to put the flag to 0. 

Sequence basic Descompresor
---------------------------

* We read the uncompressed file size.
* It was repeated until everything was decompressed file.
* It reads a bit (the flag).
* If 0:
   * It read 8 bits are written to the output buffer (remember that it is a byte uncompressed) and the pointer is incremented to the exit.
* If 1:
   * We read the full displacement (13-bit), then the size, copy "size" bytes of "displacement" to the current position, and add to the output pointer to "size".

Finding Matches
===============

The way they are searching for the matches are as follows: maintaining a pointer to the current position. At the beginning of every iteration, we compute the commute to the sliding window. This can easily be done by obtaining pointer to the current position by curtailing the size of the sliding window, if it is less than zero (negative) simply conforms to zero.

Say we have a window of sliding 4 () 1234567 "
::

	Pc:0. Pvc=0-4=0. Current: "1234567" Sliding Window: "..."
	Pc:1. Pvc=1-4=0. Current: "234567" Sliding Window: "1"
	Pc:2. Pvc=2-4=0. Current: "34567" Sliding Window: "12"
	Pc:3. Pvc=3-4=0. Current: "4567" Sliding Window: "123"
	Pc:4. Pvc=4-4=0. Current: "567" Sliding Window: "1234"
	Pc:5. Pvc=5-4=1. Current: "67" Sliding Window: "2345"
	Pc:6. Pvc=6-4=2. Current: "7" Sliding Window: "3456"

Pc. Where is the pointer to the current byte, and PVC is the pointer to the beginning of the sliding window. When using pointers to the input file complete, should care for the size of the sliding window.

Bibliography
============

* `Compression Algorithm lz77 <http://www.doschivos.com/display.asp?ID=405>`_
* `Labor of the LZ77 Compression Algorithms, and LZW LZ78 <http://es.geocities.com/fh040234>`_ (Broken Link) 
