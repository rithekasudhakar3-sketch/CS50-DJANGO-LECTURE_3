from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import Markdown
from requests import request
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect


class NewPageForm(forms.Form):
    page = forms.CharField(label = "newpage")
    content = forms.CharField(widget=forms.Textarea)


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

def entry(request,name):
    entry_data = []
    entries = util.list_entries()
    for entry in entries:
        html = util.get_entry(entry)
        content = md_to_html(entry)
        entry_data.append({"title":entry,"Content":content})
    if html == None:
        return render(request,"encyclopedia/error.html")
    else:
        return render(request,"encyclopedia/entry.html",{
        "entries": entry_data})
    
def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["page"]
            content = form.cleaned_data["content"]
            entries = [i.lower() for i in  util.list_entries()]
            if(entry.lower() in entries):
               return  render(request,"encyclopedia/error.html")
            # Save the new entry using util.save_entry or similar logic
            util.save_entry(entry,content )  # You may want to add content from the form
            return HttpResponseRedirect(reverse("index"))
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/create_page.html", {"form": form})


def random(request):
    return render(request, "encyclopedia/random.html")

