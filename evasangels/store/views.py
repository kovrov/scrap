from django.shortcuts import get_object_or_404, render_to_response
from models import Item, Collection


def line(request, line_id):
	collection = Collection.objects.get(pk=line_id)
	items = collection.items.all()
	return render_to_response('store/line.html',
				{'line': collection, 'model_list': items,})


def item(request, item_id):
	item = Item.objects.get(pk=item_id)
	return render_to_response('store/model.html', {'model': item,})


def index(request):
	collections = Collection.objects.all()
	return render_to_response('store/index.html', {'lines_list': collections,})
