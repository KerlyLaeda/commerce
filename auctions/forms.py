from django import forms
from .models import *


# Form to create a new auction listing
class NewListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "price", "photo", "category"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Add a title"}),
            "description": forms.Textarea(attrs={"class": "form-control",
                                                 "placeholder": "Add a description", "rows": "6"}),
            "price": forms.NumberInput(attrs={"class": "form-control",
                                              "placeholder": "Set a starting bid",
                                              "step": "0.5",
                                              "min": "0"}),
            "photo": forms.URLInput(attrs={"class": "form-control", "placeholder": "Image URL"}),
            "category": forms.Select(attrs={"class": "form-control"})
        }


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control",
                                          "placeholder": "Add a comment", "rows": "6"})
        }
