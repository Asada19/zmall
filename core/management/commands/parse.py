from django.core.management.base import BaseCommand

from ._helper import parse_job_urls, parse_job


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        urls = ["http://resume.doska.kg/vacancy/&sortby=new",
                "http://resume.doska.kg/vacancy/&page=2&sortby=new"]

        next_urls = parse_job_urls(urls)

        for url in next_urls:
            parse_job(url)
