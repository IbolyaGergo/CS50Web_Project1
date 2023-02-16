from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages

from . import util

import random

class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label="",widget=forms.Textarea(attrs={'rows': '5', 'cols': '10'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchform": SearchForm()
    })

def show_entry(request, entry):
      
    if not util.get_entry(entry):
        return render(request, "encyclopedia/error.html", {
            "searchform": SearchForm()
        })

    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(entry),
        "name": entry,
        "searchform": SearchForm()
    })

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data["q"]
        includesq = []
        for entry in util.list_entries():
            if q == entry:
                break
            elif q in entry:
                includesq.append(entry)

        if len(includesq) != 0:
            return render(request, "encyclopedia/index.html", {
            "entries": includesq,
            "searchform": SearchForm()
            })
        else:
            # return redirect('encyclopedia:show_entry', entry=q)
            return redirect('encyclopedia:show_entry', q)

def create(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                messages.warning(request, 'Sorry, the title is not available.')
                return render(request, "encyclopedia/create.html", {
                "searchform": SearchForm(),
                "newpageform": form
            })
            else:
                util.save_entry(title, content)
                return redirect('encyclopedia:show_entry', title)

    return render(request, "encyclopedia/create.html", {
        "searchform": SearchForm(),
        "newpageform": NewPageForm()
    })

def edit(request, name):

    if request.method == "POST":
        data = {"title": name, "content": request.POST['content']}
        form = NewPageForm(data)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('encyclopedia:show_entry', title)
            
    data = {"title": name, "content": util.get_entry(name)}
    form = NewPageForm(data)

    return render(request, "encyclopedia/edit.html", {
        "searchform": SearchForm(),
        "form": form,
        "name": name
    })

def random_page(request):

    entry = random.choice(util.list_entries())

    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(entry),
        "name": entry,
        "searchform": SearchForm()
    })
