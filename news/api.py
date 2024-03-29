from datetime import datetime
from typing import List

import validators
from ninja import NinjaAPI, Schema
from ninja.pagination import PageNumberPagination, paginate

from news.models import Category, Article
from utils.scrape import scrape_summery

api_v1 = NinjaAPI()


class CategorySchema(Schema):
    title: str = None


class NewsSchema(Schema):
    id: int
    title: str
    author: str = None
    summery: str = None
    news_link: str = None
    archive_link: str = None
    category: List[CategorySchema] = None
    published_at: datetime
    updated_at: datetime


@api_v1.get("/posts", response=List[NewsSchema])
@paginate(PageNumberPagination, page_size=10)
def add(request):
    return Article.objects.all()


@api_v1.get("/getinfo")
def getInfo(request, link):
    if validators.url(link):
        try:
            return scrape_summery(link)
        except Exception:
            return 404, {"", "", ""}
