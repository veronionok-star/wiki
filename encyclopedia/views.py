from django.shortcuts import render
from django import forms

from . import util
import markdown2

class NewSearchForm(forms.Form):
    search_text = forms.CharField(label="my")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm
    })

def entries(request, name):
    try:
        entry_md = util.get_entry(name)
        html = markdown2.markdown(entry_md)
        return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "entry_name": name
        })
    except TypeError:
        return render(request, "encyclopedia/error.html", {
            "entry_name": name
        })