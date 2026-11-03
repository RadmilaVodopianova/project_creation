
from django.contrib.auth.models import User
from django.db import models
from slugify import slugify


def generate_unique_slug(instance, value):
    """Generate an ASCII slug that is unique within the model."""
    model = type(instance)
    max_length = model._meta.get_field("slug").max_length
    base = slugify(value)[:max_length] or "item"
    candidate = base
    number = 2
    while model.objects.filter(slug=candidate).exclude(pk=instance.pk).exists():
        suffix = f"-{number}"
        candidate = base[:max_length - len(suffix)] + suffix
        number += 1
    return candidate


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Назва",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        null=True,
        allow_unicode=True,
        verbose_name="Слаг",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
            if kwargs.get("update_fields") is not None:
                kwargs["update_fields"] = set(kwargs["update_fields"]) | {"slug"}
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Назва",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        allow_unicode=True,
        verbose_name="Слаг",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)
            if kwargs.get("update_fields") is not None:
                kwargs["update_fields"] = set(kwargs["update_fields"]) | {"slug"}
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Post(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        null=True,
        allow_unicode=True,
        verbose_name="Слаг",
    )
    content = models.TextField(
        verbose_name="Вміст",
    )
    image = models.ImageField(
        upload_to='posts/%Y/%m/',
        blank=True,
        verbose_name='Зображення',
    )
    published_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публікації",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категорія",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Теги",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
            if kwargs.get("update_fields") is not None:
                kwargs["update_fields"] = set(kwargs["update_fields"]) | {"slug"}
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_date"]
        verbose_name = "Публікація"
        verbose_name_plural = "Публікації"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Користувач",
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Про себе",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Місто",
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата народження",
    )

    def __str__(self):
        return f"Профіль: {self.user.username}"

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публікація',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення',
    )

    def __str__(self):
        return f'{self.author.username}: {self.text[:50]}'

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
