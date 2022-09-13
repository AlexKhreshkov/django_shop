from django import forms
from django.contrib.auth.models import User

from app.models import Order, Comment, Profile

MIN_ITEMS_COUNT_CART = 1
MAX_ITEMS_COUNT_CART = 10
MIN_RATING_MARK = 1
MAX_RATING_MARK = 5

items_count_choices = [(i, str(i)) for i in range(MIN_ITEMS_COUNT_CART, MAX_ITEMS_COUNT_CART + 1)]
rating_marks_choices = [(i, str(i)) for i in range(MIN_RATING_MARK, MAX_RATING_MARK + 1)]


class UpdateCountForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=items_count_choices, coerce=int)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'phone', 'delivery_address', 'issue_point')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_point': forms.Select(attrs={'class': 'form-control'}),
        }


class AddCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mark'].empty_label = 'No mark'

    class Meta:
        model = Comment
        fields = ('text', 'mark')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your text'}),
            'mark': forms.Select(attrs={'class': 'form-control'}),
        }


class ChangeCommentForm(forms.ModelForm):
    mark = forms.TypedChoiceField(choices=rating_marks_choices, coerce=int)

    class Meta:
        model = Comment
        fields = ('text', 'mark')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AddProfileInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'birth_date', 'profile_pic', 'location']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddUserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class SearchForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 1}))
