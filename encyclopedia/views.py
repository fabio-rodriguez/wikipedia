from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from django import forms

from . import util

from random import choice
import markdown2

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Markdown Content", widget=forms.Textarea())
    
class EditEntryForm(forms.Form):
    content = forms.CharField(label="Markdown Content", widget=forms.Textarea())
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):

    markdown = util.get_entry(title)
    if not markdown:
        return HttpResponseRedirect(reverse('encyclopedia:wrong_entry',args=[title]))
        
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "markdown": markdown2.markdown(markdown)
    })

def wrong_entry(request, title):
    return render(request, "encyclopedia/error.html", {
        "message": f"ERROR: The entry '{title}' doesn't exist"
    })
 
def search(request):

    if request.method == "GET":
        raise Http404

    content = request.POST
    markdown = util.get_entry(content["q"])
    if markdown:
        return HttpResponseRedirect(reverse('encyclopedia:title',args=[content["q"]]))
    else:
        results = [s for s in util.list_entries() if content["q"].lower() in s.lower()]
        if results:
            return render(request, "encyclopedia/search.html", {
                "entries": results,
                "text": content["q"]
            })
    
    return HttpResponseRedirect(reverse('encyclopedia:wrong_entry',args=[content["q"]]))
    
def addentry(request):

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title):
                form.add_error("title", "This entry already exists")
                return render(request, "encyclopedia/add.html", {
                    "form": form
                })

            util.save_entry(title,content)
            return HttpResponseRedirect(reverse('encyclopedia:title',args=[title]))

        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })

    return render(request, "encyclopedia/add.html", {
                "form": NewEntryForm(),
            })

def editentry(request, title):

    markdown = util.get_entry(title) 
    if markdown == None:
        return HttpResponseRedirect(reverse('encyclopedia:wrong_entry',args=[title]))

    if request.method == "POST":
        form = EditEntryForm(request.POST)
        
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse('encyclopedia:title',args=[title]))
        
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title, 
                "form": form
            })
    
    form = EditEntryForm(initial={"content": markdown})
    return render(request, "encyclopedia/edit.html", {
                "title": title, 
                "form": form
            })


def random(request):

    entries = util.list_entries()
    title = choice(entries)

    return HttpResponseRedirect(reverse('encyclopedia:title',args=[title]))

     