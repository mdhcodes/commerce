# Create forms from models.
# https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/
# https://www.geeksforgeeks.org/django-modelform-create-form-from-models/


from django import forms
from .models import Listing, Bid, Comment


# Create a ModelForm.
class CreateListingForm(forms.ModelForm):
    # Specify the name of the model to use.
    class Meta:
        model = Listing
        fields = "__all__"
        # http://www.semicolom.com/blog/add-a-hidden-field-to-a-django-form/
        # https://stackoverflow.com/questions/22606786/how-to-hide-a-field-in-django-modelform
        # https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
        # https://medium.com/swlh/how-to-style-your-django-forms-7e8463aae4fa
        # https://docs.djangoproject.com/en/5.0/ref/forms/widgets/
        # Style Django forms with built-in widgets.
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "category": forms.TextInput(attrs={'class': 'form-control'}),
            # "image": forms.ImageField(),
            # "Bid": forms.DecimalField(),     
            "createdBy": forms.HiddenInput(),
            "watchlist": forms.HiddenInput(),
            "is_open": forms.HiddenInput()
        } 
        # exclude = ["watchlist"]


class CreateBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = "__all__"
        widgets = {
            # "bid": forms.DecimalField(attrs={'class': 'form-control'}),
            "listing": forms.HiddenInput(),
            "placedBy": forms.HiddenInput()  
        }


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        widgets = {
            # "comment": forms.Textarea(attrs={'class': 'form-control'}),
            "listing": forms.HiddenInput(),
            "author": forms.HiddenInput()  
        }