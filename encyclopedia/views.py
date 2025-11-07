from django.shortcuts import render

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, name):
    entry_md = util.get_entry(name)
    html = markdown2.markdown(entry_md)
    return render(request, "encyclopedia/entry.html", {
        "entry": html,
        "entry_name": name
    })
