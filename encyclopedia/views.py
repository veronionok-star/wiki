from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
import markdown2
import random

class NewSearchForm(forms.Form):
    search_text = forms.CharField(max_length=100)
    search_text.label = ""

class NewPageForm(forms.Form):
    page_name = forms.CharField(max_length=50, label="Put the title of your page here:",
        widget=forms.TextInput)
    page_text = forms.CharField(
        widget=forms.Textarea,
        label="Put the text of your page here:"
    )

class EditPageForm(forms.Form):
    page_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    page_text = forms.CharField(
        widget=forms.Textarea,
        label="Edit the text here:"
    )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm,
        "text": "All pages"
    })
    
def search(request):
    if request.method == "POST":
        entries = []
        all_entries = util.list_entries()
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data["search_text"]
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
            return render(request, "encyclopedia/index.html", {
                "form": form
            })

def new(request):
    return render(request, "encyclopedia/new.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm,
        "text_form": NewPageForm,
        "title": 'Add new page'
    })

def add(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            page_name = form.cleaned_data["page_name"]
            page_text = form.cleaned_data["page_text"]
            if page_name not in util.list_entries():
                util.save_entry(page_name, page_text)
                return HttpResponseRedirect(f'/wiki/{page_name}')
            else:
                return render(request, "encyclopedia/error.html", {
            "form": NewSearchForm,
            "error_title": "Page already exists",
            "error_text": f'ERROR: A page with the title "{page_name}" already exists'
            })

def save(request):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            page_text = form.cleaned_data["page_text"]
            page_name = form.cleaned_data["page_name"]
            util.save_entry(page_name, page_text)
            return HttpResponseRedirect(f'/wiki/{page_name}')

def random_entry(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(f'/wiki/{random_entry}')

def edit(request, name):
    editing = True
    initial_data = {
        "page_name": name,
        "page_text": util.get_entry(name),
    }
    text_form = EditPageForm(initial=initial_data)
    return render(request, "encyclopedia/new.html", {
        "entry_name": name,
        "form": NewSearchForm,
        "text_form": text_form,
        "title": f'Edit "{name}"',
        "editing": editing
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
            "error_title": "Page not found",
            "error_text": f'ERROR: A page with the title "{name}" does not exist'
        })