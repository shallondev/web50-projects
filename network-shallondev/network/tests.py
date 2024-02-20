from django.test import TestCase

from .models import User, Post


# Class for testing Posts
class PostTestCase(TestCase):

    # Set up a dummy user
    def setUp(self):

        # Create a user
        self.user = User.objects.create(username='u1', email='u1@email.com', password='123')

    # Test if post has content
    def test_has_content_with_content(self):

        # Create a post with content
        post_with_content = Post.objects.create(poster=self.user, content='Some content')
        self.assertTrue(post_with_content.has_content())

    # Test if post without content return false
    def test_has_content_without_content(self):

        # Create a post without content
        post_without_content = Post.objects.create(poster=self.user)
        self.assertFalse(post_without_content.has_content())
