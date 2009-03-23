from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^line/(?P<line_id>[-\w]+)/$',
		view	= 'store.views.line_preview',
		name	= 'store_line_preview',
	),
#	url(r'^(?P<slug>[-\w]+)/$',
#		view	= 'store.views.store_detail',
#		name	= 'store_detail',
#	),
#	url(r'^$',
#		view	= 'store.views.store_dashboard',
#		name	= 'store_dashboard',
#	)
)
