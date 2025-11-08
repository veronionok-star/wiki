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
    
def search(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data["search_text"]
            print("form is valid")
            if search_text in util.list_entries():
                return HttpResponseRedirect(f'/wiki/{search_text}')
                print("redirected")
        else:
            print("not valid")
            return render(request, "tasks/add.html", {
                "form": form
            })
