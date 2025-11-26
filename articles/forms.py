from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Article, Publisher, Newsletter

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new users with role assignment.

    Extends Django's built-in UserCreationForm to include:
    - Username
    - Email
    - Role (reader, journalist, editor, publisher)
    """

    class Meta:
        model = User
        fields = ("username", "email", "role")
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'role': 'User Role'
        }
        help_texts = {
            'role': 'Select your role: reader, journalist, editor, or publisher.'
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and apply Bootstrap styling to all fields.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ArticleForm(forms.ModelForm):
    """
    Form for creating and updating Article objects.

    Includes fields:
    - Title
    - Content
    - Publisher (must exist before assignment)
    """

    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']
        labels = {
            'title': 'Article Title',
            'content': 'Content',
            'publisher': 'Publishing House'
        }
        help_texts = {
            'publisher': 'Select the publisher for this article. If none exist, please register one first.'
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form:
        - Restrict publisher queryset to all publishers.
        - Display warning if no publishers exist.
        - Apply Bootstrap styling to all fields.
        """
        super().__init__(*args, **kwargs)
        self.fields['publisher'].queryset = Publisher.objects.all()
        if not self.fields['publisher'].queryset.exists():
            self.fields['publisher'].help_text = '⚠ No publishers available. Please register one first.'
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class PublisherForm(forms.ModelForm):
    """
    Form for creating and updating Publisher objects.

    Includes fields:
    - Name
    - Description
    """

    class Meta:
        model = Publisher
        fields = ['name', 'description']
        labels = {
            'name': 'Publisher Name',
            'description': 'Description'
        }
        help_texts = {
            'name': 'Enter the official name of the publishing house.',
            'description': 'Provide a short description of the publisher.'
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form:
        - Apply Bootstrap styling to all fields.
        - Add placeholders for name and description.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter publisher name'
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Brief description of the publishing house'
        })


class NewsletterForm(forms.ModelForm):
    """
    Form for creating and updating Newsletter objects.

    Includes fields:
    - Title
    - Content
    - Articles (many-to-many, selectable via checkboxes)
    """

    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'articles']
        labels = {
            'title': 'Newsletter Title',
            'content': 'Content',
            'articles': 'Articles'
        }
        help_texts = {
            'title': 'Enter a clear, descriptive title for the newsletter.',
            'content': 'Write the full content of the newsletter.',
            'articles': 'Select one or more articles to include in this newsletter.'
        }
        widgets = {
            'articles': forms.CheckboxSelectMultiple(),  # Better UX for M2M
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form:
        - Apply Bootstrap styling to all fields.
        - Remove 'form-control' class from checkbox widget for proper rendering.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['articles'].widget.attrs.pop('class', None)





