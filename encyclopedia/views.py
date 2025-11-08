from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
import markdown2

class NewSearchForm(forms.Form):
    search_text = forms.CharField(max_length=100)
    search_text.label = ""

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm,
        "text": "All pages"
    })

def entries(request, name):
    try:
        entry_md = util.get_entry(name)
        html = markdown2.markdown(entry_md)
        return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "entry_name": name,
            "form": NewSearchForm,
        })
    except TypeError:
        return render(request, "encyclopedia/error.html", {
            "entry_name": name,
            "form": NewSearchForm,
        })
    
def search(request):
    if request.method == "POST":
        entries = []
        all_entries = util.list_entries()
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data["search_text"]
            print("form is valid")
            if search_text in all_entries:
                return HttpResponseRedirect(f'/wiki/{search_text}')
            else:
                for i in all_entries:
                    if search_text in i:
                        entries.append(i)
                return render(request, "encyclopedia/index.html", {
                "form": form,
                "entries": entries,
                "text": "Results"
            })
        else:
            print("not valid")
            return render(request, "encyclopedia/index.html", {
                "form": form
            })
def new(request):
    return render(request, "encyclopedia/new.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm
    })

def add(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm,
        "text": "All pages"
    })