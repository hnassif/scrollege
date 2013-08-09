from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms.widgets import CheckboxSelectMultiple
from taggit.forms import TagWidget, TagField

class TeachForm(forms.Form):
    def addError(self, message):
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])

class SearchForm(forms.Form):
    q = forms.CharField(
        required=True,
        label = 'Search'
        )
class RegForm(TeachForm):
    firstname = forms.CharField(
        required=True,
        label='First Name'
    )

    lastname = forms.CharField(
        required=True,
        label='Last Name'
    )
    email = forms.EmailField(
        required=True,
        label= 'sjsu email'
    )
    """
    address = forms.CharField(
        required=True,
        label='Street Address'
    )
    """
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(render_value=False),
        label='Password'
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(render_value=False),
        label='Password Confirmation'
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data


class SignInForm(TeachForm):

    signin_email = forms.EmailField(
        required=True,
        label='Email'
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(render_value=False)
    )

class ItemForm(TeachForm):
    # def __init__(self, *args, **kwargs):
    #     super(TeachForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'controls'
    #         print type(self.fields[field].label)

    MY_CHOICES = (
    (False,u'Selling'),
    (True,u'Looking for'),
)

    item_sellOrLookFor = forms.ChoiceField(
                                label= ' I am ',
                                required=True,    
                                choices = MY_CHOICES,
                                )

    CATEGORY_CHOICES = (
        ('Item',u'Item'),
        ('Service/Job',u'Service/Job'),
        ('Housing',u'Housing'),
    )

    item_category = forms.ChoiceField(
                                label= 'Category',
                                required=True,    
                                choices = CATEGORY_CHOICES,
                                )

    item_name= forms.CharField(
		required= True,
        label = 'Name',
        max_length = 80
        # attrs={'class':'special'}
    )

    item_tags = TagField(
        label= 'Tags',
        required = False,
        # widget = TagWidget((attrs={'placeholder': 'Comma separated'}),)
    )
    # item_price= forms.DecimalField(
    #     required= True,
    #     label = 'Price'
    # )
    item_description= forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Please include the price in your description.'}),
        label= 'Description'
    )
    item_negotiable= forms.BooleanField(
        required=False,
        label= 'Price Negotiable'
    )

    image_first = forms.FileField(
        label='Upload an image (optional)',
        help_text='max. 42 megabytes',
        required=False
    )

    image_second = forms.FileField(
        label='Upload an image (optional)',
        help_text='max. 42 megabytes',
        required=False
    )

    image_third = forms.FileField(
        label='Upload an image (optional)',
        help_text='max. 42 megabytes',
        required=False
    )

class PasswordResetForm(TeachForm):

    old_password= forms.CharField(
        required= True,
        widget=forms.PasswordInput(render_value=False)
        
    )

    new_password= forms.CharField(
        required= True,
        widget=forms.PasswordInput(render_value=False)
    )

    confirm_new_password= forms.CharField(
        required= True,
        widget=forms.PasswordInput(render_value=False)
    )

