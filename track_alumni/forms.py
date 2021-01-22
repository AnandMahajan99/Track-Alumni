from django import forms
from track_alumni.models import Contact
# 
# class ContactForm(forms.ModelForm):
#
#     class Meta:
#         model = Contact
#         fields = ('Text', 'Subject', 'Email', 'Name')
#
#         widgets = {
#             'Text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
#             }
