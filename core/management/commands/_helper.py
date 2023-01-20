import requests
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model

from advertisement.models import SubCategory, Category, Advertisement

User = get_user_model()


def parse_job_urls(urls):
    next_urls = []

    for url in urls:
        page = requests.get(url).content
        soup = BeautifulSoup(page, "html.parser")
        next_urls += soup.find_all('a', class_='title_url')

    return next_urls


def parse_job(url):
    full_url = "http://resume.doska.kg" + "".join(url["href"].split("?")[:1])

    page = requests.get(full_url).content
    soup = BeautifulSoup(page, "html.parser")

    category, created = Category.objects.get_or_create(title="Вакансии")

    subcategory_title = soup.find("div", class_="kroshki").select("a[href*=cat]")[0].text
    subcategory, created = SubCategory.objects.get_or_create(title=subcategory_title, defaults={"category": category})

    owner = User.objects.get(email="admin@mail.ru")

    title = soup.find("div", class_="title")
    desc = soup.find_all("div", class_="desc")

    city = title.find_next("div").text
    if len(city) > 150:
        print(f"Parsing error: {full_url} has wrong city specification, i.e. {city}")
        return

    data = {
        "sub_category": subcategory,
        "title": title.text,
        "owner": owner,
        "description": desc[1].text,
        "city": title.find_next("div").text,
        "is_active": True
    }

    advertisement, created = Advertisement.objects.get_or_create(title=data['title'], city=data['city'],
                                                                 defaults=data)

    print(f"Parsing data: {advertisement.title}")
