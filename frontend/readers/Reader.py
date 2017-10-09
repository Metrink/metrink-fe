from datetime import datetime

class Reader(object):
    def __init__(self):
        pass

    def get_results(self, start_time:datetime, end_time:datetime, tags:dict, tags_include=None:dict):
        """
        Returns a Pandas DataFrame given a search specification
        :param start_time: start of the time range
        :param end_time: end of the time range
        :param tags: tags to search by
        :param tags_include: tags to include in the result
        :return: Pandas DataFrame
        """
        pass