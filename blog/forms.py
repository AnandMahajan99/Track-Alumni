from django import forms
from blog.models import BlogPost, PostComment

class PostForm(forms.ModelForm):

    class Meta():
        model = BlogPost
        exclude = ('Blogpost_id', 'Author', 'Created_datetime', 'Published_datetime')

        widgets = {
            'Heading_text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
            'Sub_heading1_text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
            'Sub_heading2_text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = PostComment
        fields = ('Text',)

        widgets = {
            'Text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
