from django.shortcuts import render
from webinar.models import Test_Question, TestResponse, ResponseQuestionaire,Webinar,WebinarAttendees
from .models import TestResult,TestQR, CertificateTemplate
from django.shortcuts import redirect

from django.core.files.base import ContentFile

import qrcode
from io import BytesIO


# Create your views here.

def test_result(request, id, type):
    test_reponse=TestResponse.objects.get(id=id)
    webinar=test_reponse.question.webinar
    tests=webinar.question.filter(test_type=type)

    for test in tests:
        responses=test.test_reponse
        if responses.is_correct:
            score+=1
        TestResult.objects.create(
            webinar=webinar,
            user=responses.user,
            test=test_reponse.id,
            type=test_reponse.question.test_type,
            score=score
            )
        return redirect("index")

def display_result(request, id):
    webinar=Webinar.objects.get(id=id)
    test_results=TestResult.objects.filter(webinar=webinar)
    evaluations=ResponseQuestionaire.objects.filter(webinar=webinar)

    evaluation_responses=[]
    pre_test_result=[]
    post_test_result=[]

    result={
        'evaluation_resonses':evaluation_responses,
        'pre_test_result':pre_test_result,
        'post_test_result':post_test_result
    }

    for evaluation in evaluations:
        total=evaluation.q1+evaluation.q2+evaluation.q3+ evaluation.q4+evaluation.q5
        evaluation_responses.append(total)


    for test_result in test_results:
        if test_result.type=='pre_test':
            pre_test_result.append(test_result.score)
        else:
            post_test_result.append(test_result.score)


    return render(request, 'exam_portal/statistics.html',{
        'result':result
    })

def generate_qr(request, id, type):
    url = 'http://127.0.0.1:8000'
    
    qr=TestQR.objects.filter(test__id=id, type=type)


    if not qr:
        
        webinar=Webinar.objects.get(id=id)
        url_path=f'{url}/webinar/display_test/{id}/{type}'
        qr = qrcode.make(url_path)
        
        # Save to database
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        qr_img = buffer.getvalue()
        

        qr_db = TestQR.objects.create(
            test=webinar,
            type=type,
            name=f'QR_test_{id}'
        )
        qr_db.img.save(
            f'QR_TEST_ID_{id}.png', ContentFile(qr_img))
        
    return redirect('display_qr', id, type)

def display_qr(request, id, type):
 
    qr=TestQR.objects.get(test__id=id, type=type)
    return render(request, 'exam_portal/display_qr.html',{
        'qr':qr
    })
        
def display_test(request, id, type):
    webinar=Webinar.objects.get(id=id)

    question=webinar.question.filter(test_type=type)
    
    return render(request, "exam_portal/display_test.html", {
        "questions":question,
        "id":id,
        "type":type
    })


def create_certificate(request,id):
    webinar=Webinar.objects.get(id=id)
    try:

        certificate=CertificateTemplate.objects.get(webinar=webinar)
        return redirect("redirect_certificate", certificate.id)

        
    except CertificateTemplate.DoesNotExist:

        return render(request, 'exam_portal/createCertificate.html', {
            "webinar":webinar
            })

def redirect_certificate(request, id):
    img=CertificateTemplate.objects.get(id=id)
    messages=""

    if request.session.pop('apply_edit', False):
        messages="The Changes has Been Apllied"
    else:
        messages=""

    return render(request, 'exam_portal/createCertificate.html', {
            'img':img,
            'webinar':img.webinar,
            "messages":messages
        })

def upload_img(request, id):
    if request.method=='POST':
        webinar=Webinar.objects.get(id=id)
        img=request.FILES["img"]
        try:
            img_save=CertificateTemplate.objects.get(webinar=webinar)
            img_save.img=img
            img_save.save()
        



        except CertificateTemplate.DoesNotExist:
            img_save=CertificateTemplate.objects.create(
                webinar=webinar,
                img=img,
                
            )
        
        return redirect("redirect_certificate", img_save.id)
        

def save_certificate(request, id):
    if request.method=='POST':
        title=request.POST.get("certificate-title").strip(" ")
        subtitle=request.POST.get("certificate-subtitle").strip(" ")
        participant=request.POST.get("certificate-name").strip(" ")
        host=request.POST.get("certificate-host").strip(" ")
        subject=request.POST.get("certificate-subject").strip(" ")
        address=request.POST.get("certificate-address").strip(" ")
        date=request.POST.get("certificate-date").strip(" ")


        certificate=CertificateTemplate.objects.get(id=id)
        certificate.title=title
        certificate.subtitle=subtitle
        certificate.participant=participant
        certificate.host=host
        certificate.subject=subject
        certificate.address=address
        certificate.date=date
        certificate.save()

        request.session['apply_edit']=True

        return redirect('redirect_certificate', certificate.id)
