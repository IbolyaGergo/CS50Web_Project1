from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry(request, entry):

    form = SearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data["q"]
        includesq = []
        for entry in util.list_entries():
            if q == entry:
                entry = q
                break
            elif q in entry:
                includesq.append(entry)

        if len(includesq) != 0:
            return render(request, "encyclopedia/index.html", {
            "entries": includesq,
            "form": SearchForm()
            })
        else:
            entry = q
            
    if not util.get_entry(entry):
        return render(request, "encyclopedia/error.html", {
            "form": SearchForm()
        })

    return render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(entry),
        "name": entry,
        "form": SearchForm()
    })
