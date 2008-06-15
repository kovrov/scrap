rem pkg-config --cflags --libs gtk+-2.0

set CFLAGS=-mms-bitfields -IC:/soft/gtk/include/gtk-2.0 -IC:/soft/gtk/lib/gtk-2.0/include -IC:/soft/gtk/include/atk-1.0 -IC:/soft/gtk/include/cairo -IC:/soft/gtk/include/pango-1.0 -IC:/soft/gtk/include/glib-2.0 -IC:/soft/gtk/lib/glib-2.0/include
set LDFLAGS=-LC:/soft/gtk/lib -lgtk-win32-2.0 -lgdk-win32-2.0 -latk-1.0 -lgdk_pixbuf-2.0 -lpangowin32-1.0 -lgdi32 -lpangocairo-1.0 -lpango-1.0 -lcairo -lgobject-2.0 -lgmodule-2.0 -lglib-2.0 -lintl

gcc -g -o clock clock.c main.c %CFLAGS% -mwindows %LDFLAGS%
