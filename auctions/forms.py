# Create forms from models.
# https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/
# https://www.geeksforgeeks.org/django-modelform-create-form-from-models/


from django import forms
from .models import Listing, Bid


# Create a ModelForm.
class CreateListingForm(forms.ModelForm):
    # Specify the name of the model to use.
    class Meta:
        model = Listing
        fields = "__all__"
        # http://www.semicolom.com/blog/add-a-hidden-field-to-a-django-form/
        # https://stackoverflow.com/questions/22606786/how-to-hide-a-field-in-django-modelform
        widgets = {
            "createdBy": forms.HiddenInput(),
            "watchlist": forms.HiddenInput()
        } 
        # exclude = ["watchlist"]


class CreateBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = "__all__"
        widgets = {
            "listing": forms.HiddenInput(),
            "placedBy": forms.HiddenInput()  
        }