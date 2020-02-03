#!/usr/bin/python3

from bs4 import BeautifulSoup
import re
import requests


class Parser:

    def __init__(self, soup):
        self.soup = soup


class ArticleParser(Parser):
    news_num = 9

    def parse_top(self):
        tag = "a"
        keywords = "main__big__link"
        res = self.soup.find(tag, keywords)
        if res:
            attr = "href"
            link = res.get(attr)
        else:
            print("Can't load top link")
            self.news_num += 1
            link = ""
        return link

    def parse_other(self):
        tag = "a"
        keywords = "main__feed__link"
        res = self.soup.find_all(tag, keywords)
        attr = "href"
        elements = [elem.get(attr) for elem in res if res]

        if len(elements) < self.news_num:
            print("Length of news less then required")
        return elements[:self.news_num]

    def parse_all(self):
        top = [self.parse_top()]
        other = self.parse_other()
        all_links = top + other
        all_links = [''.join(elem.split('?')[0]) for elem in all_links]  # removing get attributes
        return all_links


class NewsParser(Parser):

    def parse_image(self):
        tag = "img"
        keywords = ("article__main-image__image", "js-rbcslider-image", "article__picture_big__image")
        for key in keywords:
            res = self.soup.find(tag, key)
            if res:
                attr = "src"
                link = res.get(attr)
                break
            else:
                print("Can't find image")
                link = ""
        return link

    def parse_headline(self):
        res = self.soup.find(itemprop="headline")
        headline = res.text.strip()
        return headline

    def parse_text(self):
        res = self.soup.find(itemprop="articleBody")
        raw_text = res.text.strip()
        text = clean_rbc_text(raw_text)
        return text


def clean_rbc_text(raw_text):
    buf = raw_text
    buf = buf.split(' ')
    buf = ' '.join([word.strip() for word in buf if word])  # removing duplicate whitespaces
    buf = ' '.join([word for word in buf.split('\n') if word])  # removing line feeds
    buf = re.sub(r"(function().*);", r"", buf)  # removing javascript code
    buf = ''.join(buf.split('www.adv.rbc.ru'))  # removing adv link
    buf = buf.split(' Подпишитесь на рассылку РБК. Р')[0]  # removing author and tags
    clear_text = buf
    return clear_text


def main():
    article = parse_article("http://rbc.ru")
    for link in article:
        parse_news(link)


def parse_article(link):
    resp = requests.get(link)
    article_soup = BeautifulSoup(resp.text, "lxml")
    article_parser = ArticleParser(article_soup)
    target_news = article_parser.parse_all()
    return target_news


def parse_news(link):
    resp = requests.get(link)
    news_soup = BeautifulSoup(resp.text, "lxml")
    news_parser = NewsParser(news_soup)
    headline = news_parser.parse_headline()
    img = news_parser.parse_image()
    text = news_parser.parse_text()
    news_parts = {"headline": headline, "img": img, "text": text, "source": link}
    return news_parts


if __name__ == "__main__":
    main()
