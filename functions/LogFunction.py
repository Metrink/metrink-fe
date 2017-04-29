from datetime import datetime
from pandas import DataFrame
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from functions.QueryFunction import QueryFunction
from logger import logger


class LogFunction(QueryFunction):
    def __init__(self, indices, fields):
        super().__init__('log', (indices, fields))
        self.indices = indices
        self.fields = fields
        self.client = Elasticsearch()

    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):
        logger.debug('Log request: index=%s fields=%s' % (str(self.indices), str(self.fields)))

        search = Search(using=self.client, index=self.indices[0])
        search = search.filter("range", publish_date={'gte': start_time, 'lte': end_time})
        search = search.query("match", **self.fields)

        response = search.execute()

        for hit in response:
            print(hit.meta.score, hit.title)
