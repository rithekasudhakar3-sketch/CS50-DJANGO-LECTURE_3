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
    
def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["page"]
            # Save the new entry using util.save_entry or similar logic
            util.save_entry(entry, "")  # You may want to add content from the form
            return HttpResponseRedirect(reverse("index"))
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/create_page.html", {"form": form})


def random(request):
    return render(request, "encyclopedia/random.html")

