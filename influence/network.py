import networkx as nx
try:
    import json
except:
    import simplejson as json


class InfluenceNetwork(object):
    def __init__(self):
        self.network = nx.DiGraph()
        self.current_entity = None

    def add(self, entity_id, weight=None):
        # add a node for this entty, and an edge between this entity
        # and the previous (current) entity. then mark this entity as
        # the current entity. 
        
        # don't allow paths from the entity to itself
        if self.current_entity == entity_id:
            return
        self.network.add_node(str(entity_id))
        if self.current_entity:
            self.network.add_edge(str(self.current_entity), str(entity_id), weight)            
        self.current_entity = str(entity_id)        
        # eventually use an actual entity object that stores more info
        # about each entity.

    def as_json(self):
        ''' dumps node and edge names to json'''
        js = {}
        js['nodes'] = self.network.nodes()
        js['edges'] = self.network.edges()
        return json.dumps(js)

