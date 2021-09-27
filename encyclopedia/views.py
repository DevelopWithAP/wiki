from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import markdown
from django import forms
from django.contrib import messages
from . import util

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

def create(request):
    """ Allow users to create a new entry """
    entries = [entry.lower()for entry in util.list_entries()]
    print(entries)
    context = {
            "search_form": Search(),
            "create_form": Create()
        }
    print(entries)
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
                return redirect("create")
        else:
            return render(request, "encyclopedia/create",context)

    return render(request, "encyclopedia/create.html", context)
        
def edit(request, title):
    """ Allow users to edit an entry """
    entry = util.get_entry(title)
    if request.method == "POST":
        pass
    else:
        print(request.GET)
        return render(request, "encyclopedia/edit.html",{
            "search_form": Search(),
            "edit_form": Edit(request.GET)
        })
        
        
    
        
    
                



