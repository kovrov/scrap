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
#include <time.h>

#include "clock.h"

#define EGG_CLOCK_FACE_GET_PRIVATE(obj) (G_TYPE_INSTANCE_GET_PRIVATE ((obj), EGG_TYPE_CLOCK_FACE, EggClockFacePrivate))

G_DEFINE_TYPE (EggClockFace, egg_clock_face, GTK_TYPE_DRAWING_AREA);

static gboolean egg_clock_face_expose (GtkWidget *clock, GdkEventExpose *event);
static gboolean egg_clock_face_update (gpointer data);

typedef struct _EggClockFacePrivate EggClockFacePrivate;

struct _EggClockFacePrivate
{
	struct tm time;	/* the time on the clock face */
};

static void
egg_clock_face_class_init (EggClockFaceClass *class)
{
	GObjectClass *obj_class;
	GtkWidgetClass *widget_class;

	obj_class = G_OBJECT_CLASS (class);
	widget_class = GTK_WIDGET_CLASS (class);

	widget_class->expose_event = egg_clock_face_expose;

	g_type_class_add_private (obj_class, sizeof (EggClockFacePrivate));
}

static void
egg_clock_face_init (EggClockFace *clock)
{
	egg_clock_face_update (clock);

	/* update the clock once a second */
	g_timeout_add (1000, egg_clock_face_update, clock);
}

static void
draw (GtkWidget *clock, cairo_t *cr)
{
	EggClockFacePrivate *priv;
	double x, y;
	double radius;
	int i;
	int hours, minutes, seconds;

	priv = EGG_CLOCK_FACE_GET_PRIVATE (clock);
	
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

	/* clock hands */
	hours = priv->time.tm_hour;
	minutes = priv->time.tm_min;
	seconds = priv->time.tm_sec;
	/* hour hand:
	 * the hour hand is rotated 30 degrees (pi/6 r) per hour +
	 * 1/2 a degree (pi/360 r) per minute
	 */
	cairo_save (cr);
	cairo_set_line_width (cr, 2.5 * cairo_get_line_width (cr));
	cairo_move_to (cr, x, y);
	cairo_line_to (cr, x + radius / 2 * sin (M_PI / 6 * hours +
						 M_PI / 360 * minutes),
			   y + radius / 2 * -cos (M_PI / 6 * hours +
				   		 M_PI / 360 * minutes));
	cairo_stroke (cr);
	cairo_restore (cr);
	/* minute hand:
	 * the minute hand is rotated 6 degrees (pi/30 r) per minute
	 */
	cairo_move_to (cr, x, y);
	cairo_line_to (cr, x + radius * 0.75 * sin (M_PI / 30 * minutes),
			   y + radius * 0.75 * -cos (M_PI / 30 * minutes));
	cairo_stroke (cr);
	/* seconds hand:
	 * operates identically to the minute hand
	 */
	cairo_save (cr);
	cairo_set_source_rgb (cr, 1, 0, 0); /* red */
	cairo_move_to (cr, x, y);
	cairo_line_to (cr, x + radius * 0.7 * sin (M_PI / 30 * seconds),
			   y + radius * 0.7 * -cos (M_PI / 30 * seconds));
	cairo_stroke (cr);
	cairo_restore (cr);
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

static void
egg_clock_face_redraw_canvas (EggClockFace *clock)
{
	GtkWidget *widget;
	GdkRegion *region;
	
	widget = GTK_WIDGET (clock);

	if (!widget->window) return;

	region = gdk_drawable_get_clip_region (widget->window);
	/* redraw the cairo canvas completely by exposing it */
	gdk_window_invalidate_region (widget->window, region, TRUE);
	gdk_window_process_updates (widget->window, TRUE);

	gdk_region_destroy (region);
}

static gboolean
egg_clock_face_update (gpointer data)
{
	EggClockFace *clock;
	EggClockFacePrivate *priv;
	time_t timet;

	clock = EGG_CLOCK_FACE (data);
	priv = EGG_CLOCK_FACE_GET_PRIVATE (clock);
	
	/* update the time */
	time (&timet);
	priv->time = *localtime (&timet);
	
	egg_clock_face_redraw_canvas (clock);

	return TRUE; /* keep running this event */
}

GtkWidget *
egg_clock_face_new (void)
{
	return g_object_new (EGG_TYPE_CLOCK_FACE, NULL);
}
