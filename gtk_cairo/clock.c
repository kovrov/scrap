/**
 * clock.c
 *
 * A GTK+ widget that implements a clock face
 *
 * (c) 2005, Davyd Madeley
 *
 * Authors:
 *   Davyd Madeley  <davyd@madeley.id.au>
 */

#include <gtk/gtk.h>

#include "clock.h"

G_DEFINE_TYPE (EggClockFace, egg_clock_face, GTK_TYPE_DRAWING_AREA);
static gboolean egg_clock_face_expose (GtkWidget *clock, GdkEventExpose *event);

static void
egg_clock_face_class_init (EggClockFaceClass *class)
{
	GtkWidgetClass *widget_class;

	widget_class = GTK_WIDGET_CLASS (class);

	widget_class->expose_event = egg_clock_face_expose;
}

static void
egg_clock_face_init (EggClockFace *clock)
{
}

static gboolean
egg_clock_face_expose (GtkWidget *clock, GdkEventExpose *event)
{
	return FALSE;
}

GtkWidget *
egg_clock_face_new (void)
{
	return g_object_new (EGG_TYPE_CLOCK_FACE, NULL);
}
