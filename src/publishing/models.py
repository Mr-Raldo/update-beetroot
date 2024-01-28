from django.db import models
from django import forms
# Add these:


from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.snippets.models import register_snippet
from django.contrib.auth import get_user_model
from wagtail.models import Page , Orderable 

from wagtail.fields import RichTextField

from wagtail.admin.panels import  FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index

from wagtail.fields import StreamField

from wagtail import blocks
from wagtail.api import APIField

from modelcluster.contrib.taggit import  ClusterTaggableManager
from taggit.models import TaggedItemBase

User = get_user_model()

# * To capture responses from questionnaire page
class ResponseQuestionnaire(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    responder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,default='1')
    title = models.CharField(max_length=100)
    questionnaire_id = models.CharField(max_length=100, default='1')
    is_completed = models.BooleanField(null=True, blank=True)

class ResponseSection(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    responder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,default='1')
    response_questionnaire = models.ForeignKey(ResponseQuestionnaire, on_delete=models.CASCADE, related_name='sections')
    questionnaire_id = models.CharField(max_length=100, default='1')
    questionnaire_section_id = models.CharField(max_length=100, default='1')
    section_title = models.CharField(max_length=100)
    is_completed = models.BooleanField(null=True, blank=True)

class Response(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    section = models.ForeignKey(ResponseSection, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,default='1')
    questionnaire_id = models.CharField(max_length=100, default='1')
    question = models.CharField(max_length=100)
    response = models.CharField(max_length=255)


class QuestionnaireSection(blocks.StructBlock):
    section_title = blocks.CharBlock(required=True, help_text='Title of the section')
    # response_status
    questions = blocks.ListBlock(
        blocks.StructBlock([
            ('question', blocks.CharBlock(required=True, help_text='Question text')),
            ('answer', blocks.CharBlock(required=False, null=True, blank=True, help_text='Question Response text')),
            ('question_type', blocks.ChoiceBlock(choices=[
                ('text', 'Text'),
                ('multiple_choice', 'Multiple Choice'),
                # Add more question types as needed
            ], icon='radio-full')),
        ])
    )
    api_fields = [
        APIField('id'),
        APIField('questions'),
        # APIField('feed_image'),
        # APIField('authors'),  # This will nest the relevant PublishingPageAuthor objects in the API response
    ]


class QuestionnairePage(Page):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sections = StreamField([
        ('section', QuestionnaireSection()),
    ], use_json_field=True)  # Add use_json_field=True here

    content_panels = Page.content_panels + [
        FieldPanel('user'),
        FieldPanel('sections'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('user'),
        FieldPanel('sections'),
    ]
        # Export fields over the API
    api_fields = [
        APIField('user'),
        APIField('sections'),
        # APIField('feed_image'),
        # APIField('authors'),  # This will nest the relevant PublishingPageAuthor objects in the API response
    ]

    def get_context(self, request):
        context = super().get_context(request)
        # Retrieve and add the objects to the context
        questionnaire_objects = QuestionnairePage.objects.all()  # Replace with your actual query
        context['questionnaire_objects'] = questionnaire_objects
        return context
# * Class to show who created the question--

#* Creating the question model

class QuestionPage(Page):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length=300)
    question = models.CharField(max_length=255)
    
    content_panels = Page.content_panels + [
        FieldPanel('user'),
        
        FieldPanel('topic'),
        
        FieldPanel('question'),
        InlinePanel('answers', label='Answers'),
        
        ]
            # Export fields over the API
    api_fields = [
        APIField('user'),
        APIField('topic'),
        APIField('question'),
    ]

    def get_answers(self):
        
        return Answer.objects.filter(question=self)
    
    def get_questions(self):
        return QuestionPage.objects.all()
    # * For getting all the answers related to that question
   
#*  Creating the answer model
    
class Answer(models.Model):
    question = ParentalKey(QuestionPage, on_delete=models.CASCADE, null=True, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    answer_text = models.TextField()

    panels = [
        FieldPanel('user'),
        FieldPanel('answer_text'),
    ]
            # Export fields over the API
    api_fields = [
        APIField('user'),
        APIField('question'),
        APIField('answer_text'),
    ]
  
# * Adding a comment model

# class Comment(models.Model):
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True,  related_name='comments')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     add_time = models.DateTimeField(auto_now_add=True)
#     comment_text = models.TextField()

# #* Adding model for upvote 
# class UpVote(models.Model):
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="upvote_user")
    

# #* Adding model for down vote
# class DownVote(models.Model):
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="downvote_user")
    




# * class for tag posts 
class PublishingPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'PublishingPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

#* Tag index page to let users click buttons of tags.

class PublishingTagIndexPage(Page):
    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        publishingpages = PublishingPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['publishingpages'] = publishingpages
        return context



class PublishingPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    authors = ParentalManyToManyField('publishing.Author', blank=True)
    tags = ClusterTaggableManager(through=PublishingPageTag, blank=True)
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),

            # Add this:
            FieldPanel('tags'),
        ], heading="Publishing information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]
    api_fields = [
        APIField('tags'),
        APIField('intro'),
        APIField('body'),
        APIField('gallery_images'),
    ]

class PublishingIndexPage(Page):
    intro = RichTextField(blank=True)
    # add the get_context method:
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        publishingpages = self.get_children().live().order_by('-first_published_at')
        context['publishingpages'] = publishingpages
        return context


class PublishingPageGalleryImage(Orderable):
    page = ParentalKey(PublishingPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
    api_fields = [
        APIField('image'),
        APIField('caption'),
        APIField('page'),
    ]

class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='author'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]
    api_fields = [
        APIField('name'),
        APIField('author_image'),
    ]
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'


class ArticleSharingTags(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tagged_profile_id = models.CharField(max_length=100)
    article_id = models.CharField(max_length=100)
    tagged_profile_endorsed = models.BooleanField(default=False)
    endorsed_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
