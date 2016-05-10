from functions.QueryFunction import QueryFunction


class MetricFunction(QueryFunction):
    def __init__(self, host:str, group:str, name:str):
        super().__init__('metric', (host, group, name))
        self.host = host
        self.group = group
        self.name = name

