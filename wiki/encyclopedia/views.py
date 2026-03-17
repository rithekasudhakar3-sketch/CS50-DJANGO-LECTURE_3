from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import Markdown
from requests import request
from . import util

def md_to_html(title):
    content = util.get_entry(title)
    
    if content is None:
        return None

    markdowner = Markdown()
    return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    html = md_to_html(title)
    if html == None:
        return render(request,"encyclopedia/error.html")
    else:
        return render(request,"encyclopedia/entry.html")
