from selenium import webdriver
from django.test import TestCase
import unittest


class HomePageTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_check_run(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Home', self.browser.title)
