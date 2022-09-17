import networkx as nx


class AbstractTask:
    def __init__(self, graph: nx.Graph):
        self.G = graph

    def run(self):
        raise NotImplementedError

    def report(self):
        if None in self.get_values():
            msg = 'Some features are None. Use an implemented .run() to get values for it.'
            raise TypeError(f'{msg}')
        for feature in self.get_features():
            v = getattr(self, feature)
            s = f'{feature}'
            if isinstance(v, float):
                print(f'{s:40}: {v:.3f}')
            else:
                print(f'{s:40}: {v}')

    def get_features(self):
        features = []
        for k, v in self.__dict__.items():
            if k != 'G':
                features.append(k)
        return features

    def get_values(self):
        return [getattr(self, name) for name in self.get_features()]
