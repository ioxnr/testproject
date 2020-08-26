from datetime import datetime

from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect

from mysite1 import settings
from web.models import Publication, Comment, Contacts


def index(request):
    return render(request, 'index.html')


def contacts(request):
    if request.method == 'GET':
        return render(request, 'contacts.html')
    else:
        feedback_contacts = request.POST["feedback contacts"]
        feedback_text = request.POST["feedback text"]

        if len(feedback_contacts) == 0:
            return render(request, 'contacts.html', {
                'error': 'Empty contacts'
            })

        if len(feedback_text) == 0:
            return render(request, 'contacts.html', {
                'error': 'Empty text'
            })

        Contacts(name=feedback_contacts, date=datetime.now(), text=feedback_text).save()

        return redirect('/contacts/')


def publish(request):
    if request.method == 'GET':
        return render(request, 'publish.html')
    else:
        secret = request.POST["secret"]
        name = request.POST["name"]
        text = request.POST["text"]

        if secret != settings.SECRET_KEY:
            return render(request, 'publish.html', {
                'error': 'Wrong secret key'
            })

        if len(name) == 0:
            return render(request, 'publish.html', {
                'error': 'Empty name'
            })

        if len(text) == 0:
            return render(request, 'publish.html', {
                'error': 'Empty text'
            })

        Publication(name=name, date=datetime.now(), text=text.replace('\n', '<br />')).save()

        return redirect('/publications/')


def publications(request):
    search_query = request.GET.get('search', '')

    if search_query:
        return render(request, 'publications.html', {
            'publications': Publication.objects.filter(
                Q(name__icontains=search_query) | Q(text__icontains=search_query))
        })
    else:
        return render(request, 'publications.html', {
            'publications': Publication.objects.all()
        })


def publication(request, number):
    pubs = Publication.objects.filter(id=number)

    if len(pubs) == 1:
        pub = model_to_dict(pubs[0])

        comments = Comment.objects.filter(publication_id=number)

        if len(comments) > 0:
            context = {'content': pub,
                       'comments': comments}
        else:
            context = {'content': pub}

        if request.method == 'GET':
            return render(request, 'publication.html', context)
        else:
            user_id = request.POST["user_id"]
            comment = request.POST["comment"]

            if len(user_id) == 0:
                context['error'] = 'Please write your name'
                return render(request, 'publication.html', context)

            if len(comment) == 0:
                context['error'] = 'Empty comment'
                return render(request, 'publication.html', context)

            Comment(publication=Publication.objects.get(id=number), user_id=user_id, date=datetime.now(),
                    comment=comment).save()

            return render(request, 'publication.html', context)
    else:
        return redirect('/')
