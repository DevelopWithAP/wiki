from logging import info
from re import A
from typing import ContextManager
from encyclopedia.forms import Search
from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import markdown
from django import forms
from . import util

""" Forms section """
class Search(forms.Form):
    """ Search form """
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Search Here"
    }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": Search()
    })

def wiki(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/file_not_found.html")
    else:
        context = {
            "title": title.capitalize(),
            "entry": markdown(entry),
            "search_form": Search()
        }
        return render(request, "encyclopedia/entry.html", context)

def search(request):
    entries = [entry.lower() for entry in util.list_entries()]
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            query_string = form.cleaned_data["title"]
            entry = util.get_entry(query_string)
            #  if the search query is in the list of entries, it is a valid entry.
            if query_string.lower() not in entries:
                for entry in entries:
                    if query_string in entry:
                        result = markdown(util.get_entry(entry))
            else:
                result = markdown(entry)
            context={
                "query": query_string,
                "result": result,
                "search_form": Search()
            }
            return render(request, "encyclopedia/search_results.html", context)
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": entries,
                "search_form": Search()
            })    


