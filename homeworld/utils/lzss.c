#include <stdlib.h>
#include <stdio.h>
#include <errno.h>

#define FALSE   0
#define TRUE    1

#define OFFSET_BITS     12
#define LENGTH_BITS     4
/* maximum match length not encoded and maximum length encoded (4 bits) */
#define MAX_UNCODED     2
#define MAX_CODED       ((1 << LENGTH_BITS) + MAX_UNCODED)
/* wraps array index within array bounds (assumes value < 2 * limit) */
#define Wrap(value, limit)      (((value) < (limit)) ? (value) : ((value) - (limit)))
/* We want a sliding window*/
#define WINDOW_SIZE     (1 << OFFSET_BITS)

#define ENCODED     0       /* encoded string */
#define UNCODED     1       /* unencoded character */


typedef enum
{
    BF_READ = 0,
    BF_WRITE = 1,
    BF_APPEND= 2,
    BF_NO_MODE
} BF_MODES;

typedef enum
{
    BF_UNKNOWN_ENDIAN,
    BF_LITTLE_ENDIAN,
    BF_BIG_ENDIAN
} endian_t;

/***************************************************************************
* This data structure stores an encoded string in (offset, length) format.
* The actual encoded string is stored using OFFSET_BITS for the offset and
* LENGTH_BITS for the length.
***************************************************************************/
typedef struct encoded_string_t
{
    unsigned int offset;    /* offset to start of longest match */
    unsigned int length;    /* length of longest match */
} encoded_string_t;


typedef struct
{
    FILE *fp;                   /* file pointer used by stdio functions */
    endian_t endian;            /* endianess of architecture */
    unsigned char bitBuffer;    /* bits waiting to be read/written */
    unsigned char bitCount;     /* number of bits in bitBuffer */
    BF_MODES mode;              /* open for read, write, or append */
} bit_file_t;



/* cyclic buffer sliding window of already read characters */
extern unsigned char slidingWindow[];
extern unsigned char uncodedLookahead[];




/***************************************************************************
*   Function   : BitFileToFILE
*   Description: This function flushes and frees the bitfile structure,
*                returning a pointer to a stdio file.
*   Parameters : stream - pointer to bit file stream being closed
*   Effects    : The specified bitfile will be made usable as a stdio
*                FILE.
*   Returned   : Pointer to FILE.  NULL for failure.
***************************************************************************/
FILE *BitFileToFILE(bit_file_t *stream)
{
    FILE *fp = NULL;

    if (stream == NULL)
    {
        return(NULL);
    }

    if ((stream->mode == BF_WRITE) || (stream->mode == BF_APPEND))
    {
        /* write out any unwritten bits */
        if (stream->bitCount != 0)
        {
            (stream->bitBuffer) <<= 8 - (stream->bitCount);
            fputc(stream->bitBuffer, stream->fp);   /* handle error? */
        }
    }

    /***********************************************************************
    *  TO DO: Consider writing an additional byte indicating the number of
    *  valid bits (bitCount) in the previous byte.
    ***********************************************************************/

    /* close file */
    fp = stream->fp;

    /* free memory allocated for bit file */
    free(stream);

    return(fp);
}


/***************************************************************************
*   Function   : BitFileGetBitsInt
*   Description: This function provides a machine independent layer that
*                allows a single function call to stuff an arbitrary number
*                of bits into an integer type variable.
*   Parameters : stream - pointer to bit file stream to read from
*                bits - address to store bits read
*                count - number of bits to read
*                size - sizeof type containing "bits"
*   Effects    : Calls a function that reads bits from the bit buffer and
*                file stream.  The bit buffer will be modified as necessary.
*                the bits will be written to "bits" from least significant
*                byte to most significant byte.
*   Returned   : EOF for failure, otherwise the number of bits read by the
*                called function.
***************************************************************************/
int BitFileGetBitsInt(bit_file_t *stream, void *bits, const unsigned int count,
    const size_t size)
{
    int returnValue;

    if ((stream == NULL) || (bits == NULL))
    {
        return(EOF);
    }

    if (stream->endian == BF_LITTLE_ENDIAN)
    {
        returnValue = BitFileGetBitsLE(stream, bits, count);
    }
    else if (stream->endian == BF_BIG_ENDIAN)
    {
        returnValue = BitFileGetBitsBE(stream, bits, count, size);
    }
    else
    {
        returnValue = EOF;
    }

    return returnValue;
}


/***************************************************************************
*   Function   : BitFileGetChar
*   Description: This function returns the next byte from the file passed as
*                a parameter.
*   Parameters : stream - pointer to bit file stream to read from
*   Effects    : Reads next byte from file and updates buffer accordingly.
*   Returned   : EOF if a whole byte cannot be obtained.  Otherwise,
*                the character read.
***************************************************************************/
int BitFileGetChar(bit_file_t *stream)
{
    int returnValue;
    unsigned char tmp;

    if (stream == NULL)
    {
        return(EOF);
    }

    returnValue = fgetc(stream->fp);

    if (stream->bitCount == 0)
    {
        /* we can just get byte from file */
        return returnValue;
    }

    /* we have some buffered bits to return too */
    if (returnValue != EOF)
    {
        /* figure out what to return */
        tmp = ((unsigned char)returnValue) >> (stream->bitCount);
        tmp |= ((stream->bitBuffer) << (8 - (stream->bitCount)));

        /* put remaining in buffer. count shouldn't change. */
        stream->bitBuffer = returnValue;

        returnValue = tmp;
    }

    return returnValue;
}




/***************************************************************************
*   Function   : BitFileGetBit
*   Description: This function returns the next bit from the file passed as
*                a parameter.  The bit value returned is the msb in the
*                bit buffer.
*   Parameters : stream - pointer to bit file stream to read from
*   Effects    : Reads next bit from bit buffer.  If the buffer is empty,
*                a new byte will be read from the file.
*   Returned   : 0 if bit == 0, 1 if bit == 1, and EOF if operation fails.
***************************************************************************/
int BitFileGetBit(bit_file_t *stream)
{
    int returnValue;

    if (stream == NULL)
    {
        return(EOF);
    }

    if (stream->bitCount == 0)
    {
        /* buffer is empty, read another character */
        if ((returnValue = fgetc(stream->fp)) == EOF)
        {
            return EOF;
        }
        else
        {
            stream->bitCount = 8;
            stream->bitBuffer = returnValue;
        }
    }

    /* bit to return is msb in buffer */
    stream->bitCount--;
    returnValue = (stream->bitBuffer) >> (stream->bitCount);

    return (returnValue & 0x01);
}



/***************************************************************************
*   Function   : MakeBitFile
*   Description: This function naively wraps a standard file in a
*                bit_file_t structure.  ANSI-C doesn't support file status
*                functions commonly found in other C variants, so the
*                caller must be passed as a parameter.
*   Parameters : stream - pointer to the standard file being wrapped.
*                mode - The mode of the file being wrapped.
*   Effects    : A bit_file_t structure will be created for the stream
*                passed as a parameter.
*   Returned   : Pointer to the bit_file_t structure for the bit file
*                or NULL on failure.  errno will be set for all failure
*                cases.
***************************************************************************/
bit_file_t *MakeBitFile(FILE *stream, const BF_MODES mode)
{
    bit_file_t *bf;

    if (stream == NULL)
    {
        /* can't wrapper empty steam */
        errno = EBADF;
        bf = NULL;
    }
    else
    {
        bf = (bit_file_t *)malloc(sizeof(bit_file_t));

        if (bf == NULL)
        {
            /* malloc failed */
            errno = ENOMEM;
        }
        else
        {
            /* set structure data */
            bf->fp = stream;
            bf->bitBuffer = 0;
            bf->bitCount = 0;
            bf->mode = mode;
        }
    }

    bf->endian = DetermineEndianess();

    return (bf);
}


/****************************************************************************
*   Function   : DecodeLZSSByFile
*   Description: This function will read an LZSS encoded input file and
*                write an output file.  This algorithm encodes strings as 16
*                bits (a 12 bit offset + a 4 bit length).
*   Parameters : fpIn - pointer to the open binary file to decode
*                fpOut - pointer to the open binary file to write decoded
*                       output
*   Effects    : fpIn is decoded and written to fpOut.  Neither file is
*                closed after exit.
*   Returned   : EXIT_SUCCESS or EXIT_FAILURE
****************************************************************************/
int DecodeLZSSByFile(FILE *fpIn, FILE *fpOut)
{
    bit_file_t *bfpIn;

    int c;
    unsigned int i, nextChar;
    encoded_string_t code;              /* offset/length code for string */

    if (fpIn == NULL)
    {
        /* use stdin if no input file */
        bfpIn = MakeBitFile(stdin, BF_READ);
    }
    else
    {
        /* convert output file to bitfile */
        bfpIn = MakeBitFile(fpIn, BF_READ);
    }

    /* use stdout if no output file */
    if (fpOut == NULL)
    {
        fpOut = stdout;
    }

    /************************************************************************
    * Fill the sliding window buffer with some known vales.  EncodeLZSS must
    * use the same values.  If common characters are used, there's an
    * increased chance of matching to the earlier strings.
    ************************************************************************/
    memset(slidingWindow, ' ', WINDOW_SIZE * sizeof(unsigned char));

    nextChar = 0;

    while (TRUE)
    {
        if ((c = BitFileGetBit(bfpIn)) == EOF)
        {
            /* we hit the EOF */
            break;
        }

        if (c == UNCODED)
        {
            /* uncoded character */
            if ((c = BitFileGetChar(bfpIn)) == EOF)
            {
                break;
            }

            /* write out byte and put it in sliding window */
            putc(c, fpOut);
            slidingWindow[nextChar] = c;
            nextChar = Wrap((nextChar + 1), WINDOW_SIZE);
        }
        else
        {
            /* offset and length */
            code.offset = 0;
            code.length = 0;

            if ((BitFileGetBitsInt(bfpIn, &code.offset, OFFSET_BITS,
                sizeof(unsigned int))) == EOF)
            {
                break;
            }

            if ((BitFileGetBitsInt(bfpIn, &code.length, LENGTH_BITS,
                sizeof(unsigned int))) == EOF)
            {
                break;
            }

            code.length += MAX_UNCODED + 1;

            /****************************************************************
            * Write out decoded string to file and lookahead.  It would be
            * nice to write to the sliding window instead of the lookahead,
            * but we could end up overwriting the matching string with the
            * new string if abs(offset - next char) < match length.
            ****************************************************************/
            for (i = 0; i < code.length; i++)
            {
                c = slidingWindow[Wrap((code.offset + i), WINDOW_SIZE)];
                putc(c, fpOut);
                uncodedLookahead[i] = c;
            }

            /* write out decoded string to sliding window */
            for (i = 0; i < code.length; i++)
            {
                slidingWindow[(nextChar + i) % WINDOW_SIZE] =
                    uncodedLookahead[i];
            }

            nextChar = Wrap((nextChar + code.length), WINDOW_SIZE);
        }
    }

    /* we've decoded everything, free bitfile structure */
    BitFileToFILE(bfpIn);

    return (EXIT_SUCCESS);
}


int main(int argc, char *argv[])
{
	printf("Hello, world\n");
	return 0;
}
