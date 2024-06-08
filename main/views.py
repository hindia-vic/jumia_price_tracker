from django.shortcuts import render,redirect
import requests
from django.conf import settings
from django.core.mail import send_mail
from . models import ProductSearch
from bs4 import BeautifulSoup
from . models import ProductSearch
from apscheduler.schedulers.background import BackgroundScheduler


def home(request):
    return render(request,'home.html')

def search(request):
    if request.method=='POST':
        link=request.POST.get('search')
        limit=request.POST.get('price')
        if link!="" and limit !="":
            user=request.user
            product=ProductSearch(user=user,search=link,price=limit)
            product.save()
            return redirect('search')
    return render(request,'search.html')


def product_search():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for product in ProductSearch.objects.all():
        if product.status==False:
           user=product.user
           search=product.search
           email=user.email
           price_product=product.price
           result=requests.get(search,headers=headers)
           soup=BeautifulSoup(result.content,'html.parser')
           span=soup.find('span',class_='-b -ubpt -tal -fs24 -prxs').text[4:]
           span=span.split(',')
           price=int(''.join(span))
           if price<=price_product:
              subject='You product has now reduced to your recommended price value'
              message=f'Hi,{user.username},your product{search}, that you were tracking has now reduced to{price}'
              email_from=settings.EMAIL_HOST_USER
              recipient_mail=[email]
              try:
                    send_mail(subject, message, email_from, recipient_mail)
                    product.status = True
                    product.save()
                    print(f'Email sent to {email}')
              except Exception as e:
                    print(f'Error sending email to {email}: {e}')
              #send_mail(subject,message,email_from,recipient_mail)
              #product.status=True
              #product.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(product_search,'interval', minutes=2)
    scheduler.start()

# Create your views here.
