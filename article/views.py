from django.http import HttpResponse
from django.shortcuts import render
from .models import News
from .parser import parse_article, parse_news

TOKEN = 'sg32r4gsdgw4ts'


def is_authorized(attrs):
    status = False
    if 'token' in attrs:
        token = attrs['token']
        if token == TOKEN:
            status = True
    return status


def fill_db():
    news = News.objects
    article = parse_article("http://rbc.ru")
    for link in article:
        exist = news.filter(source_link=link)
        if not exist:
            news_data = parse_news(link)
            add_news(news_data)
        else:
            continue


def add_news(news_data):
    headline = news_data["headline"]
    img = news_data["img"]
    text = news_data["text"]
    source = news_data["source"]
    news_model = News(headline=headline, img_link=img, text=text, source_link=source)
    news_model.save()


def index(request):
    all_news = News.objects.all().order_by('-id')
    method = request.method
    if method == 'GET':
        attrs = request.GET
        if is_authorized(attrs):
            token = attrs['token']
            if 'get_news' in attrs:
                fill_db()
            response = render(request, 'index.html', context={'all_news': all_news, 'token': token})
        else:
            response = HttpResponse("401 Unauthorized")
            response.status_code = 401
    return response


def news_detail_view(request, news_id):
    attrs = request.GET
    if is_authorized(attrs):
        news = News.objects
        target_news = news.get(id=news_id)
        response = render(request, 'news_detail.html', context={'target_news': target_news})
    else:
        response = HttpResponse("401 Unauthorized")
        response.status_code = 401
    return response
