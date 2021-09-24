from django.shortcuts import render
from markdown2 import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/file_not_found.html")
    else:
        context = {
            "title": title.capitalize(),
            "entry": markdown(entry),
        }
        return render(request, "encyclopedia/entry.html", context)
        



