from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanelExtend
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from cms.blocks import InlineImageBlock, InlineVideoBlock


class HomePage(Page):
    template = "home_page.html"
    intro = RichTextField(blank=True)
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
            FieldPanel('article_section_title'),
            FieldPanel('article_section_intro', classname='full'),
            PageChooserPanel('article_section'),
        ], heading="Article section", classname='collapsible'),
    ]


class ArticlePage(Page):
    intro = RichTextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+', verbose_name="Image"
    )
    featured = models.BooleanField(default=False)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock(
            features=['h1', 'h2', 'h3', 'h4', 'h5', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'image', 'code',
                      'blockquote'])),
        ('image', InlineImageBlock()),
        ('video', InlineVideoBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('featured'),
        FieldPanel('image'),
        FieldPanel('body'),
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

