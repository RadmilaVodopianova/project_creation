from django import forms

from .models import Comment, Post, Subscriber, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if widget.is_hidden:
                continue
            if isinstance(widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            elif isinstance(widget, forms.Select):
                css_class = 'form-select'
            else:
                css_class = 'form-control'
            classes = widget.attrs.get('class', '').split()
            if css_class not in classes:
                classes.append(css_class)
            widget.attrs['class'] = ' '.join(classes)


class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['username'].widget.attrs['placeholder'] = 'Ваш логін'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].widget.attrs['placeholder'] = 'Ваш пароль'


class CommentForm(StyledFormMixin, forms.ModelForm):
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


class SubscriberForm(StyledFormMixin, forms.ModelForm):
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


class PostForm(StyledFormMixin, forms.ModelForm):
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
class RegisterForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField(
        required=True, label='Електронна адреса',
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email', 'placeholder': 'name@example.com',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['username'].widget.attrs['autocomplete'] = 'username'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повторіть пароль'
        for name in ('password1', 'password2'):
            self.fields[name].widget.attrs['autocomplete'] = 'new-password' 

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        labels = {'first_name': "Ім’я", 'last_name': 'Прізвище'}
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control', 'autocomplete': 'given-name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control', 'autocomplete': 'family-name',
            }),
        }


class ProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'city', 'birth_date')
        labels = {
            'bio': 'Про себе',
            'city': 'Місто',
            'birth_date': 'Дата народження',
        }
        help_texts = {
            'birth_date': 'Цю дату у профілі бачите лише ви.',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'city': forms.TextInput(attrs={
                'class': 'form-control', 'autocomplete': 'address-level2',
            }),
            'birth_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date'},
            ),
        }

    def clean_birth_date(self):
        from django.utils import timezone

        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > timezone.localdate():
            raise forms.ValidationError(
                'Дата народження не може бути в майбутньому.'
            )
        return birth_date
