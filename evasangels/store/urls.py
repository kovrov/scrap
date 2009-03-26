from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^collection/(?P<collection_id>[-\w]+)/$',
		view = 'store.views.collection',
		name = 'store-collection-view',
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
