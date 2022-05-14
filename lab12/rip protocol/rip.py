from time import sleep


MAX_DIST = 16


class Rip:
    def __init__(self):
        self.is_graph_changed = False
        self.dists = dict()
        self.next_hop = dict()
        self.current_step = 1

    def _add_edge(self, src, dest, w):
        if src not in self.dists:
            self.dists[src] = dict()
            self.next_hop[src] = dict()
        self.dists[src][dest] = w
        self.next_hop[src][dest] = dest

    def add_edge(self, src, dest):
        self._add_edge(src, dest, 1)
        self._add_edge(dest, src, 1)
        self._add_edge(src, src, 0)
        self._add_edge(dest, dest, 0)

    def _get_dist(self, a, b):
        if a in self.dists:
            if b in self.dists[a]:
                return self.dists[a][b]
        return MAX_DIST

    def try_to_update(self, vertex_from, vertex_to, vertex_using):
        if self._get_dist(vertex_using, vertex_to) + 1 < self._get_dist(vertex_from, vertex_to):
            self.dists[vertex_from][vertex_to] = self.dists[vertex_using][vertex_to] + 1
            self.next_hop[vertex_from][vertex_to] = vertex_using
            return True
        return False

    def update(self):
        print(f'Step {self.current_step} simulation')

        self.is_graph_changed = False

        for (v, vals) in self.dists.items():
            for (u, d) in vals.items():
                if d != 1: 
                    continue
                for k in self.dists.keys():
                    self.is_graph_changed |= self.try_to_update(u, k, v)

        self.print_current_state()
        self.current_step += 1
      

    def start(self):
        while True:
            self.update()
            sleep(0.5)
            if not self.is_graph_changed:
                print('Simulation finished!')
                break

    def print_current_state(self):
        for (v, vals) in self.dists.items():
            print(f' Simulation step {self.current_step} of router {v}')
            print('[Source IP]         [Destination IP]    [Next Hop]          [Metric]')
            for (u, d) in vals.items():
                if d != 0:
                    print(f'{v:<20}{u:<20}{self.next_hop[v][u]:<20}{d:<20}')
            print()
        print('------------------------------------------')