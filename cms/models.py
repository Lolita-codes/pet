from django import forms
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel, InlinePanel
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page, TranslatableMixin, Locale, Orderable
from wagtail.snippets.models import register_snippet

from cms.blocks import InlineImageBlock, InlineVideoBlock


class HomePage(Page):
    template = "home_page.html"
    intro = RichTextField(blank=True)
    theme_section_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Title to display above the theme section",
    )
    theme_section_intro = RichTextField(blank=True)
    theme_section = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Featured section for the homepage. Will display all themes.",
        verbose_name="Theme section",
    )
    article_section_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Title to display above the article section",
    )
    article_section_intro = RichTextField(blank=True)
    article_section = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Featured articles for the homepage",
        verbose_name="Article section",
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        MultiFieldPanel([
            FieldPanel('theme_section_title'),
            FieldPanel('theme_section_intro', classname='full'),
            PageChooserPanel('theme_section'),
        ], heading='Theme section', classname='collapsible'),
        MultiFieldPanel([
            FieldPanel('article_section_title'),
            FieldPanel('article_section_intro', classname='full'),
            PageChooserPanel('article_section'),
        ], heading="Article section", classname='collapsible'),
    ]


@register_snippet
class Theme(TranslatableMixin, models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name


class ThemePage(Page):
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, related_name='themepages')
    intro = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+'
    )
    caption = models.CharField(blank=True, null=True, max_length=255)

    def articlepages(self):
        print('hi')
        return self.theme.articlepages.filter(locale=self.locale_id).live().order_by('-first_published_at')

    content_panels = Page.content_panels + [
        FieldPanel('theme'),
        FieldPanel('intro', classname='full'),
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


class ArticlePage(Page):
    intro = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+', verbose_name="Image"
    )
    themes = ParentalManyToManyField(Theme, blank=True, related_name='articlepages', verbose_name="Themes")
    featured = models.BooleanField(default=False)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock(
            features=['h1', 'h2', 'h3', 'h4', 'h5', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'image', 'code',
                      'blockquote'])),
        ('image', InlineImageBlock()),
        ('video', InlineVideoBlock()),
    ], use_json_field=True)

    def themepages(self):
        ans = ThemePage.objects.filter(theme__in=self.themes.all(), locale=self.locale_id)
        print(ans)
        return ans

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('themes', widget=forms.CheckboxSelectMultiple),
        FieldPanel('featured'),
        FieldPanel('image'),
        FieldPanel('body'),
    ]


class ThemeIndexPage(Page):
    intro = RichTextField(blank=True)

    # Specifies that only ThemePage objects can live under this index page
    subpage_types = ['ThemePage']

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]


class ArticleIndexPage(Page):
    intro = RichTextField(blank=True)

    # Specifies that only ArticlePage objects can live under this index page
    subpage_types = ['ArticlePage']

    # A method to access and reorder the children of the page (i.e. ArticlePage objects)
    def articlepages(self):
        return ArticlePage.objects.child_of(self).live().order_by('-first_published_at')

    def featured_articlepages(self):
        return self.articlepages().filter(featured=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]


class TextPage(Page):
    text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('text', classname='full'),
    ]


@register_snippet
class Menu(ClusterableModel):

    title = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='title', editable=True, help_text="Unique identifier of menu. Will be populated "
                                                                         "automatically from title of menu. "
                                                                         "Change only if needed.")

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('slug'),
        ], heading=_("Menu")),
        InlinePanel('menu_items', label=_("Menu Item"))
    ]

    def __str__(self):
        return self.title


class MenuItem(Orderable):
    menu = ParentalKey('Menu', related_name='menu_items', help_text=_("Menu to which this item belongs"))
    title = models.CharField(max_length=50, help_text=_("Title of menu item that will be displayed"))
    link_url = models.CharField(max_length=500, blank=True, null=True,
                                help_text=_("URL to link to, e.g. /accounts/signup (no language prefix, LEAVE BLANK if "
                                            "you want to link to a page instead of a URL)"))
    link_page = models.ForeignKey(
        Page, blank=True, null=True, related_name='+', on_delete=models.CASCADE,
        help_text=_("Page to link to (LEAVE BLANK if you want to link to a URL instead)"),
    )
    title_of_submenu = models.CharField(
        blank=True, null=True, max_length=50,
        help_text=_("Title of submenu (LEAVE BLANK if there is no custom submenu)")
    )
    icon = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
    )
    show_when = models.CharField(
        max_length=15,
        choices=[('always', _("Always")), ('logged_in', _("When logged in")), ('not_logged_in', _("When not logged in"))],
        default='always',
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('link_url'),
        PageChooserPanel('link_page'),
        FieldPanel('title_of_submenu'),
        FieldPanel('icon'),
        FieldPanel('show_when'),
    ]

    def trans_page(self, language_code):
        print(language_code)
        if self.link_page:
            can_page = self.link_page
            if language_code == settings.LANGUAGE_CODE: # requested language is the canonical language
                return can_page
            try:
                language = Locale.objects.get(language_code=language_code)
                print('hey')
            except Locale.DoesNotExist:# no language found, return original page
                return self.link_page
            translated_page = can_page.get_translation(language)
            return translated_page
            # return Page.objects.get(locale_id=language, path=can_page)
        return None

    def trans_url(self, language_code):
        if self.link_url:
            return '/' + language_code + str(self.link_url)
        elif self.link_page:
            return self.trans_page(language_code).url
        return None

    @property
    def slug_of_submenu(self):
        # becomes slug of submenu if there is one, otherwise None
        if self.title_of_submenu:
            return slugify(self.title_of_submenu)
        return None

    def show(self, authenticated):
        return ((self.show_when == 'always')
                or (self.show_when == 'logged_in' and authenticated)
                or (self.show_when == 'not_logged_in' and not authenticated))

    def __str__(self):
        return self.title


@register_snippet
class CompanyLogo(models.Model):
    name = models.CharField(max_length=250)
    logo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        FieldPanel('name', classname='full'),
        FieldPanel('logo'),
    ]

    def __str__(self):
        return self.name
