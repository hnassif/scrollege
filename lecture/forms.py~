from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms.widgets import CheckboxSelectMultiple

class TeachForm(forms.Form):
    def addError(self, message):
        self._errors[NON_FIELD_ERRORS] = self.error_class([message])


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
        label= 'MIT email'
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

    item_name= forms.CharField(
		required= True
    )
    item_type= forms.MultipleChoiceField(
		required= True,
		widget= CheckboxSelectMultiple, 
		choices = (('book', 'Book'), ('electronic', 'Electronic'), ('food', 'Food'))
     )


    item_description= forms.CharField(
        required=False,
        widget=forms.Textarea,
        label= 'Porduct Description (Optional)'
    )
    item_image= forms.ImageField(
        required=False,
        label= 'Image (Optional)'
    )
