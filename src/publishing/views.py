#views.py

from django.shortcuts import render, redirect
from .forms import ResponseForm
from .serializers import QuestionnaireSectionSerializer, ResponseSerializer, ResponseSectionSerializer, ResponseQuestionnaireSerializer
from .models import Response as QuestionnaireResponse,ArticleSharingTags, Answer, QuestionnaireSection, ResponseSection, ResponseQuestionnaire
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from .serializers import ArticleSharingTagsSerializer
import json
User = get_user_model()

def submit_response(request):
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or return a success message
            return redirect('questionnaire_page.html')  # Replace 'success_page' with the actual name of your success page URL
    else:
        form = ResponseForm()
    return render(request, 'questionnaire_page.html', {'form': form})


@api_view(['GET', 'POST'])
def submit_questionnaire_section(request):
    if request.method == "POST":
        print('Post method request.data',request.data )
        print('Post method request.data',request.data['questionaire_id'] )
        # questionnaire_section_id
        questionaire_id = request.data['questionaire_id']
        questionaire_title = request.data['questionaire_title']
        section_title = request.data['answeredQuestionnaireSection']['section_title']
        questionnaire_section_id = request.data['answeredQuestionnaireSection']['id']
        responder_id = int(request.data['owner'])
        print('responder_id', responder_id)
        responder = User.objects.get(pk=responder_id)
        response_questionnaire, created = ResponseQuestionnaire.objects.get_or_create(questionnaire_id=questionaire_id,
                                                                                      title=questionaire_title,
                                                                                      responder=responder,
                                                                                      is_completed=False)
        section, created = ResponseSection.objects.get_or_create(
                                                        response_questionnaire=response_questionnaire, 
                                                        responder=responder,
                                                        questionnaire_id=questionaire_id,
                                                        questionnaire_section_id=questionnaire_section_id,
                                                        section_title=section_title)
        print('responder', responder)
        checkExistingResponseSection = ResponseSection.objects.filter(pk = section.id, is_completed=True).exists()
        if checkExistingResponseSection:
            print('QuestionnaireResponse Does Exist')
            # response = ResponseSection.objects.get(pk = section.id)
            # serializer = ResponseSectionSerializer(response)
            # print('serializer.data',json.dumps(serializer.data) )

            # return Response(json.dumps(serializer.data), status=status.HTTP_200_OK)
            response = ResponseSection.objects.get(pk = section.id)
            serializer = ResponseSectionSerializer(response)
            print('serializer.data',json.dumps(serializer.data) )
            return Response(json.dumps(serializer.data), status=status.HTTP_200_OK)

        print('QuestionnaireResponse.DoesNotExist')
        for qsn in request.data['answeredQuestionnaireSection']['questions']:
            response, created = QuestionnaireResponse.objects.get_or_create(
                    responder=responder,
                    questionnaire_id = questionaire_id,
                    section = section,
                    question = qsn['question'],
                    response = qsn['answer'],
            )
            print(response, created)
        if created:
                section.is_completed = True
                section.save()
                response = ResponseSection.objects.get(pk = section.id)
                serializer = ResponseSectionSerializer(response)
                print('serializer.data',json.dumps(serializer.data) )
                return Response(json.dumps(serializer.data), status=status.HTTP_200_OK)

        return Response({'message': 'Invalid HTTP method'})
    if request.method == "GET":
         res = QuestionnaireResponse.objects.all()
         serializer = QuestionnaireSectionSerializer(res, many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET', 'POST'])
def submit_tagged_profiles(request):
    if request.method == "POST":
        print('request.data article_id',request.data['article_id'] )
        print('request.data tags',request.data['tags'] )
        article_id = request.data['article_id']
        tags = request.data['tags'] 
        for tag in request.data['tags']:
            print('tag',tag)
            article_tags, created = ArticleSharingTags.objects.get_or_create(
                    article_id = article_id,
                    tagged_profile_id=tag
            )
            print(article_tags, created)
        if created:
                response = ArticleSharingTags.objects.filter(article_id = article_id)
                serializer = ArticleSharingTagsSerializer(response, many=True)
                print('serializer.data',json.dumps(serializer.data) )
                return Response(json.dumps(serializer.data), status=status.HTTP_200_OK)


        return Response({'message': 'Invalid HTTP method'})
    if request.method == "GET":
         res = QuestionnaireResponse.objects.all()
         serializer = QuestionnaireSectionSerializer(res, many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
