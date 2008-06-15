CFLAGS := $(shell pkg-config --cflags gtk+-2.0)
LDFLAGS := $(shell pkg-config --libs gtk+-2.0)

all: clock

clock: clock.c clock.h main.c clock-marshallers.c clock-marshallers.h
	gcc -g -o clock clock.c main.c clock-marshallers.c $(CFLAGS) $(LDFLAGS)

clock-marshallers.c: clock-marshallers.list
	glib-genmarshal --prefix _clock_marshal --body $< > $@

clock-marshallers.h: clock-marshallers.list
	glib-genmarshal --prefix _clock_marshal --header $< > $@
