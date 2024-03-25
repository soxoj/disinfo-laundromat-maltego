import asyncio
import logging
import requests
from mock import Mock
import sys

from maltego_trx.entities import Alias, URL
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import LINK_STYLE_DASHED

import asyncio


SEARCH_URL = "https://www.disinfo.id/api/parse-url"

class SimilarByContent(DiscoverableTransform):
    """
    Returns aliases for the input alias entity
    """

    @classmethod
    def create_entities(cls, request, response):
        url = request.Value

        res = requests.post(SEARCH_URL, data={
            'url': url,
            'country': 'us',
            'language': 'en',    
        }).json()

        for r in res['results']:
            url_main = r['url']
            score = r['score']
            title = r['title']
            sources = ', '.join(r['source'])
            engines = ', '.join(r['engines'])

            entity = response.addEntity("maltego.URL", url_main)
            entity.addProperty('url', value=url_main)
            entity.setLinkLabel(sources)
            entity.addDisplayInformation(content=title)
            entity.setWeight(int(50 + 450*score/100))

            entity.addProperty('title', 'Title', 'loose', title)
            entity.addProperty('Engines', 'Engines', 'loose', engines)
