import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm
from catalog.models import BookInstance, Book

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date (between now and 4 weeks, default is 3).", widget=forms.SelectDateWidget)

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid Date - renewal is in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid Date - renewal is more than 4 weeks.'))

        return data

class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid Date - renewal is in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid Date - renewal is more than 4 weeks.'))

        return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back':_('New renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks. Default is set as 3.')} 

class BookModelForm(ModelForm):
    def clean_isbn(self):
        data = self.cleaned_data['isbn']

        if len(data) > 13:
            raise ValidationError(_('ISBN should be 13 characters only.'))

        return data

    class Meta:
        model = Book
        fields = '__all__'
        # labels = {'isbn':_('!3 Character')}
        # help_texts = {'due_back': _('Enter a date between now and 4 weeks. Default is set as 3.')} 
