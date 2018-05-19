import elasticsearch

from string import ascii_letters
from explorers.Explorer import Explorer
from datetime import datetime
from json import dumps

from logger import logger
from cache import get_cache


class Elasticsearch(Explorer):
    def __init__(self):
        super().__init__('Elasticsearch')
        self.client = elasticsearch.Elasticsearch(host='10.40.109.166')
        self.cache = get_cache()

    def get_template(self):
        return 'explorers/elasticsearch.html'


    @staticmethod
    def flatten_fields(mappings, field_name=[]):
        fields = set()

        for field, value in mappings.items():
            if len(field) == 0 or field[0] not in ascii_letters:
                continue

            field_name.append(field)

            if 'properties' in value:
                fields.update(Elasticsearch.flatten_fields(value['properties'], field_name))
            else:
                fields.add('.'.join(field_name))

            # remove the field name regardless
            field_name.pop()

        return fields

    def get_indexes(self):
        # ret = self.cache.get('es_indices')
        # ret = None

        # if ret is not None:
        #     return ret

        res = self.cache.get('es_indices')
        # res = None

        if res is None:
            res = self.client.indices.get('_all')
            self.cache.set('es_indices', res)

        ret = []

        for index,value in res.items():
            if str(index)[0] not in ascii_letters:  # filter any funky named indices
                continue

            # logger.debug('INDEX: %s' % index)

            # flatten out the fields
            fields = set()

            for map_name, mapping in value['mappings'].items():
                if 'properties' in mapping:
                    fields.update(Elasticsearch.flatten_fields(mapping['properties']))

            ret.append({
                'index': index,
                'created': datetime.fromtimestamp(float(value['settings']['index']['creation_date'])/1000).isoformat(),
                'fields': sorted(fields)
            })

        # self.cache.set('es_indices', ret)

        return ret
