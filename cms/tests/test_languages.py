from django.test import TestCase, RequestFactory, Client
from wagtail.models import Locale

from .factories import HomePageFactory, ArticlePageFactory, ArticleIndexPageFactory
from wagtail.core.models import Page, Site
from django.conf import settings
from django.urls import reverse
from ..views import set_language_from_url
from django.utils import translation


class TestChangeLanguageViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.factory = RequestFactory()
        cls.site = Site.objects.create(is_default_site=True, root_page=Page.get_first_root_node())
        cls.homepage = HomePageFactory()
        cls.articleindexpage = ArticleIndexPageFactory(parent=cls.homepage)
        cls.articlepage1 = ArticlePageFactory(parent=cls.articleindexpage)
        cls.foreign_language_code = [code for code, lang in settings.LANGUAGES if code != settings.LANGUAGE_CODE][0]
        cls.foreign_language = Locale.objects.get_or_create(language_code=cls.foreign_language_code)[0]

    def test_change_language_without_previous_page(self):
        response = self.client.get(
            reverse('set_language_from_url', kwargs={'language_code': self.foreign_language_code}))
        expected_url = '/' + self.foreign_language_code + '/'
        self.assertEquals(response.url, expected_url)

    def test_change_language_of_login_url(self):
        # get the url from the get_language_from_url view and make a request object
        url = reverse('set_language_from_url', kwargs={'language_code': self.foreign_language_code})
        request = self.factory.get(url)

        # manually set the HTTP_REFERER value to login url
        request.META['HTTP_REFERER'] = '/' + settings.LANGUAGE_CODE + '/accounts/login/'
        translation.activate(settings.LANGUAGE_CODE)
        response = set_language_from_url(request, self.foreign_language_code)
        expected_url = '/' + self.foreign_language_code + '/accounts/login/'
        self.assertEquals(response.url, expected_url)


