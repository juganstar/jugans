from django import forms
from .models import Post, Category
from .models import Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    date_from = forms.DateField(
        label='From date',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        label='To date',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']