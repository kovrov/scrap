from django.shortcuts import get_object_or_404, render_to_response
from models import Item, Collection


def collection(request, collection_id):
	collection = Collection.objects.get(pk=collection_id)
	items = collection.items.all()
	return render_to_response('store/collection.html',
				{'collection': collection, 'items_list': items,})


def item(request, item_id):
	item = Item.objects.get(pk=item_id)
	return render_to_response('store/item.html', {'item': item,})


def index(request):
	collections = Collection.objects.all()
	return render_to_response('store/index.html', {'collections_list': collections,})
