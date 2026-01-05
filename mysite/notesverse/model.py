from relation import Relator
from relation.map import create_graph
from pyvis.network import Network

class Subject(Relator):
    def __init__(self, name, relations=None, children=None, parents=None):
        self.name = name
        self.topics = relations if isinstance(relations, dict) else {}
        self.children = children if children is not None else []
        self.parents = parents if parents is not None else []

    def get(self, name, relations=None, children=None, parents=None):
        if name in self.topics:
            existing = self.topics[name]
            existing |= Topic(name, relations, children, parents)
            return existing
        else:
            instance = Topic(name, relations, children, parents)
            self.topics[name] = instance
            return instance
    def convert_string(self, str):
        sentences = str.splitlines()
        for sentence in sentences:
            if ":" in sentence:
                parts = sentence.split(":")
                topic_name = parts[0].strip()
                description = parts[1].strip()
                if ">" in description:
                    desc_parts = description.split(">")
                    function_name = desc_parts[0].strip()
                    topic2_name = desc_parts[1].strip()
                    topic = self.get(topic_name)
                    topic * Description(function_name, children=[self.get(topic2.strip()) for topic2 in topic2_name.split(",")])
                else:
                    topic = self.get(topic_name)
                    for desc in description.split(","):
                        desc = desc.strip()
                        topic * Description(desc)
            elif ">" in sentence:
                parts = sentence.split(">")
                topic_name = parts[0].strip()
                topic2_name = parts[1].strip()
                topic = self.get(topic_name)
                topic + [self.get(topic2.strip()) for topic2 in topic2_name.split(",")]
    def make_graph(self):
        graph = Network(directed=True)
        visited = set()
        drawn_edges = set()
        for topic in self.topics.values():
            create_graph(topic, net=graph, visited=visited, drawn_edges=drawn_edges)
        return graph.generate_html()
class Topic(Relator):
    def make_graph(self):
        graph = create_graph(self, depth=1, relations=False)
        create_graph(self, net=graph, ancestors=False, descendants=False, depth=2)
        return graph.generate_html()

class Description(Relator):
    pass

