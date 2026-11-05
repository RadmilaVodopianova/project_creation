from django import forms

from .models import Comment, Post, Subscriber
from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label='Ваш коментар', min_length=5, max_length=500, strip=True,
        help_text='Від 5 до 500 символів. Пробіли на початку та в кінці не враховуються.',
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 3, 'minlength': 5, 'maxlength': 500,
            'placeholder': 'Напишіть свій коментар...',
        }),
        error_messages={
            'required': 'Коментар не може бути порожнім або складатися лише з пробілів.',
            'min_length': 'Коментар має містити щонайменше 5 символів.',
            'max_length': 'Коментар має містити не більше 500 символів.',
        },
    )

    class Meta:
        model = Comment
        fields = ['text']

        labels = {
            'text': 'Ваш коментар',
        }

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишіть свій коментар...',
                'rows': 3,
            }),
        }


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        labels = {'email': 'Ваша електронна адреса'}
        widgets = {'email': forms.EmailInput(attrs={
            'class': 'form-control', 'placeholder': 'name@example.com',
            'autocomplete': 'email',
        })}
        error_messages = {'email': {
            'required': 'Введіть електронну адресу.',
            'invalid': 'Введіть коректну електронну адресу.',
            'unique': 'Ця електронна адреса вже підписана.',
        }}

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if Subscriber.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ця електронна адреса вже підписана.')
        return email


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'category', 'tags')

        labels = {
            'title': 'Заголовок',
            'content': 'Текст публікації',
            'image': 'Зображення',
            'category': 'Категорія',
            'tags': 'Теги',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")