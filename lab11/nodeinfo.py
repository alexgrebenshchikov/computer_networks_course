from distancelist import DistanceList


class NodeInfo:

    def __init__(self, name, host, port, dist_list=None, changed_dists=None):
        self.name = name
        self.host = host
        self.port = port

        if dist_list is None:
            dist_list = {}
        if changed_dists is None:
            changed_dists = {}

        self.dist_list = DistanceList(dist_list)
        self.changed_dists = changed_dists
