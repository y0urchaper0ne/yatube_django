from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

    def clean_subject(self):
        data = self.changed_data['text']
        if data == '':
            return forms.ValidationError('Пожалуйста, напишите пост')
        return data


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    def clean_subject(self):
        data = self.changed_data['text']
        if data == '':
            return forms.ValidationError(
                'Пожалуйста, напишите комментарий')
        return data
