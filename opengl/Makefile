SOURCES=xlib-gl3-test.c game.c application.c scene.c queue.c matrix.c

CC=gcc
CFLAGS=-g -W
#CFLAGS=-g -W -pedantic
LDLIBS=-lGL -lm

all: xlib-gl3-test

xlib-gl3-test: $(SOURCES)
	$(CC) $(SOURCES) $(CFLAGS) $(LDLIBS) -o xlib-gl3-test
