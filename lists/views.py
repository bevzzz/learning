# Third-party libraries
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ValidationError

# Local libraries
from lists.models import Item, List


def home_page(request) -> HttpResponse:
    return render(request, "home.html")


def new_list(request) -> HttpResponse:
    list_ = List.objects.create()
    item = Item(text=request.POST["item_text"], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, "home.html", {"error": error})
    return redirect(f"/lists/{list_.id}/")


def add_item(request, list_id) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/lists/{list_.id}/")


def view_list(request, list_id) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": list_})
