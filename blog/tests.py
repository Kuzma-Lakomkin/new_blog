from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post

class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username= 'testuser',
            email= 'test@mail.ru',
            password= 'secret'
        )

        self.post = Post.objects.create(
            title= 'Title',
            body= 'Content',
            author = self.user
        )

    def test_string_representation(self):
        post = Post(title='Sample title')
        self.assertEqual(str(post), post.title)


    def test_post_contetnt(self):
        self.assertEqual(f'{self.post.title}', 'Title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Content')

    def test_post_list_view(self):
        responce = self.client.get(reverse('home'))
        self.assertEqual(responce.status_code, 200)
        self.assertContains(responce, 'Content')
        self.assertTemplateUsed(responce, 'home.html')

    def test_post_detail_view(self):
        responce = self.client.get('/post/1/')
        no_responce = self.client.get('/post/1000/')
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(no_responce.status_code, 404)
        self.assertContains(responce, 'Title')
        self.assertTemplateUsed(responce, 'post_detail.html')

# Create your tests here.
