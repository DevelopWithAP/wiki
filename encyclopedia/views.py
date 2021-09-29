from django.shortcuts import render
from markdown2 import markdown
from django import forms
from django.contrib import messages
from . import util
import random

""" Forms section """
class Search(forms.Form):
    """ Search form """
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Search Here"
    }))

class Create(forms.Form):
    """ Create form """
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "New Entry Title",
    }))
    content = forms.CharField(label = "", widget=forms.Textarea(attrs={
        "class": "form-control mt-2",
        "placeholder": "Content",
        "rows": 4,
    }))

class Edit(forms.Form):
    """ Edit form """
    updated_title = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Update Title"
    }))
    updated_content = forms.CharField(label="", widget=forms.Textarea(attrs={
        "class": "form-control mt-2",
        "placeholder": "Update Content",
        "rows": 4
    }))

""" End of forms section """

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": Search()
    })

def wiki(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/file_not_found.html",{
            "search_form": Search()
        })
    else:
        context = {
            "title": title.capitalize(),
            "entry": markdown(entry),
            "search_form": Search()
        }
        return render(request, "encyclopedia/entry.html", context)

def search(request):
    entries = [entry.lower() for entry in util.list_entries()]
    matches = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            query_string = form.cleaned_data["title"]
            if query_string.lower() in entries:
                entry = util.get_entry(query_string)
                return render(request, "encyclopedia/entry.html", {
                    "search_form": Search(),
                    "title": query_string.capitalize(),
                    "entry": markdown(entry),
                })
            elif query_string.lower() not in entries:
                matches = [ entry for entry in entries if query_string in entry ]
            return render(request, "encyclopedia/results.html", {
                "search_form": Search(),
                "matches": matches,
                "title": query_string
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": entries,
                "search_form": Search()
            })    

def create(request):
    """ Allow users to create a new entry """
    entries = [entry.lower() for entry in util.list_entries()]
    context = {
            "search_form": Search(),
            "create_form": Create()
        }
    if request.method == "POST":
        form = Create(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["title"]
            new_content = form.cleaned_data["content"]
            if not new_title.lower() in entries:
                util.save_entry(new_title, new_content)
                new_entry = markdown(util.get_entry(new_title))
                return render(request, "encyclopedia/entry.html", {
                    "title": new_title.capitalize(),
                    "entry": markdown(new_entry),
                    "search_form": Search()
                })
            else:
                messages.warning(request, "Entry already exists.")
                return render(request, "encyclopedia/create.html", {
                    "search_form": Search(),
                    "create_form": Create(request.POST)
                })
        else:
            return render(request, "encyclopedia/create",context)
    return render(request, "encyclopedia/create.html", context)
        
def edit(request, title):
    """ Allow users to edit an entry """
    title = title
    entry = util.get_entry(title)
    """
    Since we're not interacting with a database, the update_context dictionary
    will aid in mimicing the action of fetching the entry data and passing its individual fields
    as keys to the dictionary
    """
    update_context = {
        "updated_title": title,
        "updated_content": entry
    }
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "search_form": Search(),
            "edit_form": Edit(update_context)
        })
    elif request.method == "POST":
        form = Edit(request.POST)
        if form.is_valid():
            updated_title = form.cleaned_data["updated_title"]
            updated_content = form.cleaned_data["updated_content"]
            util.save_entry(updated_title, updated_content)
            updated_entry = util.get_entry(updated_title)
            return render(request, "encyclopedia/entry.html",{
                "title": updated_title,
                "entry": markdown(updated_entry),
                "search_form": Search()
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "search_form": Search(),
                "edit_form": Edit(update_context)
            })

def generate_random(request):
    """ Allow users to access an random entry """
    entries = util.list_entries()
    random.shuffle(entries)
    title = entries[0]
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown(util.get_entry(title)),
        "search_form": Search()
    })

    
    


        
        
    
        
    
                



