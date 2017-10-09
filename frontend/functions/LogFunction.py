from datetime import datetime
from pandas import DataFrame
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Range

from frontend.functions.QueryFunction import QueryFunction
from frontend.logger import logger


class LogFunction(QueryFunction):
    def __init__(self, indices, fields):
        super().__init__('log', (indices, fields))
        self.indices = indices
        self.fields = fields
        self.client = Elasticsearch(host='10.40.109.166')

    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):
        logger.debug('Start: %s  End: %s  Log: index=%s fields=%s' % (start_time.isoformat(), end_time.isoformat(), str(self.indices), str(self.fields)))

        search = Search(using=self.client, index=self.indices[0])
        search = search.filter(Range(** {'@timestamp': {'gte': start_time.isoformat(), 'lte': end_time.isoformat()}}))

        for k,v in self.fields.items():
            if isinstance(v, list):
                for sv in v:
                    search = search.query("match", **{k:sv})

            else:
                search = search.query("match", **{k:v})

        logger.debug('ES Query: %s' % str(search.to_dict()))
        response = search.execute()

        logger.debug('Results: success:%d failed:%d hits:%d' % (response._shards.successful, response._shards.failed, len(response.hits)))

        for hit in response:
            # filter out the meta key and flatten the values
            row = {k: str(hit[k]) for k in hit if k != 'meta'}

            logger.debug(row)
            input = input.append(row, ignore_index=True)

        return input
