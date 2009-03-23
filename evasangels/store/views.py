from django.shortcuts import get_object_or_404, render_to_response
from models import Item, Collection


def line_preview(request, line_id):
	collection = Collection.objects.get(pk=line_id)
	items = collection.items.all()
	return render_to_response('store/line.html',
				{'line': collection, 'model_list': items,})
