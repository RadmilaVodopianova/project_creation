from datetime import timedelta

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import CommentForm, SubscriberForm
from .models import Category, Comment, Post, Subscriber


class CommentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='author')
        cls.reader = User.objects.create_user(username='reader')
        category = Category.objects.create(name='Новини')
        cls.post = Post.objects.create(title='Перша', content='Текст',
                                       category=category, user=cls.author)
        cls.other = Post.objects.create(title='Інша', content='Текст',
                                        category=category, user=cls.author)

    def setUp(self):
        self.url = reverse('blog:post', args=[self.post.slug])

    def test_form_exposes_only_text(self):
        self.assertEqual(list(CommentForm().fields), ['text'])

    def test_invalid_comment_lengths_and_whitespace(self):
        for text in ['', '   \n\t', 'abcd', 'x' * 501, '  abcd  ']:
            with self.subTest(text=text):
                form = CommentForm({'text': text})
                self.assertFalse(form.is_valid())
                self.assertIn('text', form.errors)

    def test_valid_boundaries_and_trim(self):
        for text in ['12345', 'x' * 500, '  Привіт  ']:
            with self.subTest(text=text):
                form = CommentForm({'text': text})
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data['text'], text.strip())

    def test_author_and_post_are_taken_from_request(self):
        self.client.force_login(self.reader)
        response = self.client.post(self.url, {
            'text': '  Чудова стаття!  ', 'author': self.author.pk,
            'post': self.other.pk,
        })
        self.assertRedirects(response, self.url)
        comment = Comment.objects.get()
        self.assertEqual(comment.author, self.reader)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.text, 'Чудова стаття!')
        self.assertIsNotNone(comment.created_at)

    def test_anonymous_post_cannot_save(self):
        response = self.client.post(self.url, {'text': 'Новий коментар'})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('admin:login'), response.url)
        self.assertIn('next=', response.url)
        self.assertFalse(Comment.objects.exists())

    def test_invalid_post_renders_errors_and_preserves_text(self):
        self.client.force_login(self.reader)
        response = self.client.post(self.url, {'text': 'abcd'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Коментар має містити щонайменше 5 символів.')
        self.assertContains(response, 'abcd')
        self.assertFalse(Comment.objects.exists())

    def test_only_this_posts_comments_newest_first(self):
        old = Comment.objects.create(post=self.post, author=self.reader, text='Старий коментар')
        Comment.objects.filter(pk=old.pk).update(created_at=timezone.now() - timedelta(days=1))
        new = Comment.objects.create(post=self.post, author=self.author, text='Новий коментар')
        Comment.objects.create(post=self.other, author=self.author, text='Інша публікація')
        response = self.client.get(self.url)
        self.assertEqual(list(response.context['comments']), [new, old])
        self.assertContains(response, new.text)
        self.assertContains(response, self.reader.username)
        self.assertContains(response, timezone.localtime(new.created_at).strftime('%d.%m.%Y %H:%M'))
        self.assertNotContains(response, 'Інша публікація')

    def test_comment_html_is_escaped(self):
        Comment.objects.create(post=self.post, author=self.reader, text='<script>alert(1)</script>')
        response = self.client.get(self.url)
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>alert(1)</script>')

    def test_missing_post_is_404(self):
        self.assertEqual(self.client.get(reverse('blog:post', args=['missing'])).status_code, 404)


class SubscriberTests(TestCase):
    def setUp(self):
        self.url = reverse('blog:subscribe')

    def test_only_email_field(self):
        self.assertEqual(list(SubscriberForm().fields), ['email'])

    def test_subscribe_and_success_message(self):
        response = self.client.post(self.url, {'email': ' Reader@Example.com '}, follow=True)
        self.assertRedirects(response, self.url)
        self.assertContains(response, 'Ви успішно підписалися!')
        subscriber = Subscriber.objects.get()
        self.assertEqual(subscriber.email, 'reader@example.com')
        self.assertIsNotNone(subscriber.created_at)
        self.client.get(self.url)
        self.assertEqual(Subscriber.objects.count(), 1)

    def test_invalid_emails(self):
        for email in ['', '   ', 'invalid', 'name@']:
            with self.subTest(email=email):
                response = self.client.post(self.url, {'email': email})
                self.assertEqual(response.status_code, 200)
                self.assertIn('email', response.context['form'].errors)
        self.assertFalse(Subscriber.objects.exists())

    def test_duplicate_emails_ignore_case(self):
        Subscriber.objects.create(email='reader@example.com')
        for email in ['reader@example.com', 'READER@EXAMPLE.COM']:
            response = self.client.post(self.url, {'email': email})
            self.assertContains(response, 'Ця електронна адреса вже підписана.')
        self.assertEqual(Subscriber.objects.count(), 1)

    def test_database_blocks_case_insensitive_duplicates(self):
        Subscriber.objects.create(email='reader@example.com')
        with self.assertRaises(IntegrityError), transaction.atomic():
            Subscriber.objects.create(email='READER@EXAMPLE.COM')

    def test_subscribers_registered_in_admin(self):
        self.assertIn(Subscriber, admin.site._registry)

    def test_subscription_link_in_blog(self):
        self.assertContains(self.client.get(reverse('blog:index')), self.url)
