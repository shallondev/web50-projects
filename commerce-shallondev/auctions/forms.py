from django.forms import ModelForm
from django import forms

from .models import Listing, Bid, Comments, Categories


class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'price', 'image_url'
            ]
        exclude = ['created_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Image URL'}),
        }
        required = {
            'title': True,
            'description': True,
            'price': True,
            'image_url': False,
        }

class CategoryFilterForm(forms.Form):
    category = forms.ModelChoiceField(
            queryset=Categories.objects.all(),
            empty_label='Select a category',
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    
class WatchListForm(forms.Form):
    action = forms.ChoiceField(
        choices=[('add', 'Add to Watchlist'), ('remove', 'Remove from Watchlist')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label=''
    )

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        exclude = ['user', 'listing']

    amount = forms.DecimalField(
        required=True, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bid Amount'}),
        label=''  
    )

class CloseAuctionForm(forms.Form):
    close_auction = forms.BooleanField(
        label='', 
        required=True)

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'cols': 80, 'rows': 4, 'placeholder': 'Enter Comment'}),
        }

    text = forms.CharField(
        required=True, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 80, 'rows': 4, 'placeholder': 'Enter Comment'}),
        label=""
    )