from django import forms

from .models import User, Listing, Bid, Comment

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "category", "price", "image"]
        widgets = {
                "title": forms.TextInput(attrs={"class": "form-control col-12", "placeholder": "Listing title"}),
                "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Write a short description"}),
                "category": forms.Select(attrs={"class": "form-control"}),
                "price": forms.NumberInput(attrs={"class": "form-control", "min": 0.01, "placeholder": "Price (USD)"}),
                "image": forms.URLInput(attrs={"class": "form-control", "placeholder": "Image URL"})
                }

class BidSubmitForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]
        widgets = {"price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Bid"})}
        labels = {"price": ""}

class CommentSubmitForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={"class": "form-control", "placeholder": "Add a comment", "rows": 2})}
        labels = {"text": ""}