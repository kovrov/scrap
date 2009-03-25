from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^line/(?P<line_id>[-\w]+)/$',
		view = 'store.views.line',
		name = 'store-line-view',
	),
	url(r'^item/(?P<item_id>[-\w]+)/$',
		view = 'store.views.item',
		name = 'store-item-view',
	),
	url(r'^$',
		view = 'store.views.index',
		name = 'store-index',
	)
)
