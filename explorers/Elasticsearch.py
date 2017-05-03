import elasticsearch

from explorers.Explorer import Explorer
from datetime import datetime

from logger import logger


class Elasticsearch(Explorer):
    def __init__(self):
        super().__init__('Elasticsearch')
        self.client = elasticsearch.Elasticsearch()

    def get_template(self):
        return 'explorers/elasticsearch.html'

    def get_indexes(self):
        res = self.client.indices.get('_all')

        ret = []

        for index,value in res.items():
            logger.debug('INDEX: %s' % index)

            fields = set()
            for mapping in value['mappings'].values():
                fields.update(mapping['properties'].keys())

            logger.debug('FIELDS: %s' % ','.join(fields))

            ret.append({
                'index': index,
                'alias': value['aliases'],
                'created': datetime.fromtimestamp(float(value['settings']['index']['creation_date'])/1000).isoformat(),
                # 'created': int(value['settings']['index']['creation_date']),
                'fields': list(fields)
            })

        return ret
