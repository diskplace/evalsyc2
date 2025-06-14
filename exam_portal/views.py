from django.shortcuts import render
from webinar.models import Test_Question, TestResponse, ResponseQuestionaire,Webinar
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

def generate_qr(request, id):
    url='http://127.0.0.1:8000'
    try: 
        TestQR.objects.get(test_id=id)
        #print qr already exist

    except TestQR.DoesNotExist:
        webinar=Webinar.objects.get(id=id)
        url_path=f'{url}/webinar/questionaire/{webinar.id}'
        qr=qrcode.make(url_path)

    except Webinar.DoesNotExist:
        test=Test_Question.objects.get(id=id)
        url_path=f'{url}/webinar/display_test/{id}/{test.test_type}'
        qr=qrcode.make(url_path)

    except Test_Question.DoesNotExist:
        pass
      
    buffer=BytesIO()
    qr.save(buffer, format='PNG')
    qr_img=buffer.getvalue()
    qr_db=TestQR.objects.create(
            test_id=id,
            name=f'QR_test_{id}')
    qr_db.img.save(
        f'QR_TES_ID{id}', ContentFile(qr_img))
    return redirect('display_qr', id)

def display_qr(request, id):
    qr=TestQR.objects.get(id=id)
    return render(request, 'exam_portal/display_qr.html',{
        'qr':qr
    })
        

def create_certificate(request,id):
    webinar=Webinar.objects.get(id=id)
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
