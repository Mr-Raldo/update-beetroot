from rest_framework import serializers
from .models import ArticleSharingTags, ResponseSection, ResponseQuestionnaire, QuestionnaireSection, Answer, Response


class QuestionnaireSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireSection
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'

class ResponseQuestionnaireSerializer(serializers.ModelSerializer):
    sections = ResponseSerializer(many=True)

    class Meta:
        model = ResponseQuestionnaire
        fields = ("id","responder","response_questionnaire","section_title","is_completed","sections")

class ResponseSectionSerializer(serializers.ModelSerializer):
    responses = ResponseSerializer(many=True)
    class Meta:
        model = ResponseSection
        fields = ("id","questionnaire_section_id","questionnaire_id","responder","response_questionnaire","section_title","is_completed","responses")
class ArticleSharingTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleSharingTags
        fields = ("id","created_at","tagged_profile_id","article_id","tagged_profile_endorsed","endorsed_at")