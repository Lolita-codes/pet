from django import forms
from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page, TranslatableMixin, Locale
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
