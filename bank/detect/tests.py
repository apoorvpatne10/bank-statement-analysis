from django.test import TestCase


class HomePageTest(TestCase):

    def test_uses_index_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'detect/index.html')
