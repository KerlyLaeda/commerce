from django import forms
from .models import *


# Form to create a new auction listing
class NewListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "photo", "category"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),  # weird bug # adding separate img field doesnt help, it looks the same anyways
            "category": forms.Select(attrs={"class": "form-control"})
        }

        # Default for foreign key (DecimalField) is <select>
        # widgets = {
        #     'price': forms.NumberInput(attrs={'step': '0.01'}),
        # }
