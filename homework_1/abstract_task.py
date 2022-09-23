import networkx as nx


class AbstractTask:
    def __init__(self, graph: nx.Graph):
        self.G = graph

    def run(self):
        raise NotImplementedError

    def get_features(self):
        features = []
        for k, v in self.__dict__.items():
            if k != 'G':
                features.append(k)
        return features

    def get_values(self):
        return [getattr(self, name) for name in self.get_features()]
