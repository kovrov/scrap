
DC = dmd.exe
SRC = $(wildcard *.d)
LIBS = win32.lib opengl.lib
OBJS = -objs
#GUI = -L/EXET:NT/SU:windows
#IPATH = -Ic:/soft/digitalmars/bindings
DEBUG = -g -debug=1
CFLAGS = $(GUI) $(IPATH) -odobjs $(DEBUG) -version=WindowsXP
TARGET = -oftest.exe
#RES = wintest.res

all:
	$(DC) $(SRC) $(LIBS) $(RES) $(TARGET) $(CFLAGS)

docs:
	$(DC) $(SRC)  $(CFLAGS) -o- -D -Dddoc
