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
#include <math.h>

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

static void
draw (GtkWidget *clock, cairo_t *cr)
{
	double x, y;
	double radius;
	int i;
	
	x = clock->allocation.x + clock->allocation.width / 2;
	y = clock->allocation.y + clock->allocation.height / 2;
	radius = MIN (clock->allocation.width / 2,
		      clock->allocation.height / 2) - 5;

	/* clock back */
	cairo_arc (cr, x, y, radius, 0, 2 * M_PI);
	cairo_set_source_rgb (cr, 1, 1, 1);
	cairo_fill_preserve (cr);
	cairo_set_source_rgb (cr, 0, 0, 0);
	cairo_stroke (cr);

	/* clock ticks */
	for (i = 0; i < 12; i++)
	{
		int inset;
	
		cairo_save (cr); /* stack-pen-size */
		
		if (i % 3 == 0)
		{
			inset = 0.2 * radius;
		}
		else
		{
			inset = 0.1 * radius;
			cairo_set_line_width (cr, 0.5 *
					cairo_get_line_width (cr));
		}
		
		cairo_move_to (cr,
				x + (radius - inset) * cos (i * M_PI / 6),
				y + (radius - inset) * sin (i * M_PI / 6));
		cairo_line_to (cr,
				x + radius * cos (i * M_PI / 6),
				y + radius * sin (i * M_PI / 6));
		cairo_stroke (cr);
		cairo_restore (cr); /* stack-pen-size */
	}
}

static gboolean
egg_clock_face_expose (GtkWidget *clock, GdkEventExpose *event)
{
	cairo_t *cr;

	/* get a cairo_t */
	cr = gdk_cairo_create (clock->window);

	cairo_rectangle (cr,
			event->area.x, event->area.y,
			event->area.width, event->area.height);
	cairo_clip (cr);
	
	draw (clock, cr);

	cairo_destroy (cr);

	return FALSE;
}

GtkWidget *
egg_clock_face_new (void)
{
	return g_object_new (EGG_TYPE_CLOCK_FACE, NULL);
}
