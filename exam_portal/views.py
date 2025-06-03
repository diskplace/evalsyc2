from django.shortcuts import render
from webinar.models import Test_Question, TestResponse, ResponseQuestionaire
from .models import TestResult

# Create your views here.

def test_result(request, id, type):
    try:
        
        test_reponse=TestResponse.objects.get(id=id)
        webinar=test_reponse.question.webinar
        tests=webinar.question.filter(test_type=type)

        for test in tests:
            responses=test.test_reponse
            if responses.is_correct:
                score+=1
            TestResult.objects.create(
                user=responses.user,
                test=test_reponse.id,
                type=test_reponse.question.test_type,
                score=score
            )

    except TestResponse.DoesNotExist:
        ResponseQuestionaire.objects.get(id=id)
        
        pass


    except ResponseQuestionaire.DoesNotExist:
        pass
