INF = 9999  # time_limit < 999


def solution(times, time_limit):
    """
    0. check no loop
    1. compute D, using Floyd-Warshall
    2. find one `simple path` from start to one bunny, 
      check if the time_left can be consumed for going to bulkhead.
      We should stop current rescue if time_to_bulkhead is not enough. 
    3. return all rescue plan

    Details:
      a) We should have 2 lists for every plan to record:
        1) bunny_to_rescue
        2) rescued_bunny
    """
    pass


def solution_for_only_one_bunny_in_arm(times, time_limit):
    """
    1. shortest paths: only 3 types off sp-tree should be computed (bellman-ford)
      a) start -> bunnies
      b) bunnies -> bulkhead
      c) bulkhead -> bunnies
    2. route has 2 types:
      a) start -> bunny -> bulkhead (only execute once)
      b) bulkhead -> bunny -> bulkhead
    3. optimize(max) bunny number:
      * route numbers are small and limited, we can permutate all and choose the best plan
      a) choose one bunny to rescue first (bunny x, route_type_a) 
      b) start from bulkhead, choose next bunny with least cost to rescue (Bunnies - {bunny_x}, route_type_b)
      c) repeat `b` until exceed time_limit, save optimized bunny number as opt_bunny_number[bunny_x]
      d) repeat `a,b,c`, then choose best bunny number from opt_bunny_number
    """
    # empty graph
    G = Graph()

    w = times
    # get inverted weight for shortest path to bulkhead
    inv_w = invert_mat(w)

    # init empty vertices, and edges using size of w
    init_graph(G, w)

    # first shortest path tree, detect loop
    contains_loop = not bellman_ford(G, w, 'start')  # a) start -> all points
    if contains_loop:
        #print("contains loop")
        # contains loop, all bunnies can be rescued
        return list(range(len(w) - 2))

    # another two shortest path tree
    bellman_ford(G, w, 'bulkhead')  # b) all points -> bulkhead
    bellman_ford(G, inv_w, 'to_bulkhead')  # c) bulkhead -> all points

    # a) choose one bunny to rescue first (bunny x, route_type_a) 
    bunny_num = len(w) - 2
    rescued_bunny_ids_options = []
    for bunnyx in range(bunny_num):
        time_cost = 0
        rescued_bunnies = []
        bunnies_to_rescue = list(range(bunny_num))
        # bunny x vertice index
        bunnyx_idx = bunnyx + 1

        # update time cost
        # route_a of bunny x
        time_cost += route_cost(G, bunnyx_idx, 'a')
        rescued_bunny = bunnyx

        # b) start from bulkhead, choose next bunny with least cost to rescue (Bunnies - {bunny_x}, route_type_b)
        while time_limit - time_cost >= 0:
            rescued_bunnies.append(rescued_bunny)
            bunnies_to_rescue.remove(rescued_bunny)

            another_bunnyi, min_time_cost = next_rescue_bunny(G, bunnies_to_rescue)
            # update time cost
            time_cost += min_time_cost
            rescued_bunny = another_bunnyi

        rescued_bunny_ids_options.append(rescued_bunnies)

    rescued_numbers = [len(bunnies) for bunnies in rescued_bunny_ids_options]
    max_idx = rescued_numbers.index(max(rescued_numbers))
    print("all options: " + ", ".join(["-".join([str(xxx) for xxx in xx]) for xx in rescued_bunny_ids_options]))
    return rescued_bunny_ids_options[max_idx]

    # c) repeat `b` until exceed time_limit, save optimized bunny number as opt_bunny_number[bunny_x]
    # d) repeat `a,b,c`, then choose best bunny number from opt_bunny_number


def next_rescue_bunny(G, bunnies_to_rescue):
    # TODO: O(n), can be optimized (sorted)
    # choose next bunny with least cost to rescue (route_type_b)

    next_bunny = INF
    min_cost = INF
    # loop all bunnies
    for bunny_i in bunnies_to_rescue:
        bunny_idx = bunny_i + 1
        time_cost = route_cost(G, bunny_idx, 'b')
        # update min_cost
        if time_cost < min_cost:
            min_cost = time_cost
            next_bunny = bunny_i

    return next_bunny, min_cost


def route_cost(G, v_idx, route_type):
    v = G.V[v_idx]
    if route_type == 'a':
        # a) start -> bunny -> bulkhead (only execute once)
        time_cost = v.d_from_start + v.d_to_bulkhead
    elif route_type == 'b':
        # b) bulkhead -> bunny -> bulkhead
        time_cost = v.d_from_bulkhead + v.d_to_bulkhead
    else:
        raise Exception("Unknown route type {}".format(route_type))

    return time_cost


class Graph(object):
    def __init__(self):
        self.V = []
        self.E = []
        self.s = None


class Vertice(object):
    def __init__(self, G, v_id):
        # initialize distance and pi
        self.d_from_start = INF
        self.d_from_bulkhead = INF
        self.d_to_bulkhead = INF
        self.pi_from_start = None
        self.pi_from_bulkhead = None
        self.pi_to_bulkhead = None
        self.G = G
        self.id = v_id

    @property
    def d(self):
        if self.G.s == 'start':
            return self.d_from_start
        elif self.G.s == 'bulkhead':
            return self.d_from_bulkhead
        elif self.G.s == 'to_bulkhead':
            return self.d_to_bulkhead
        else:
            raise Exception("Unknown source_name {}".format(self.G.s))

    @d.setter
    def d(self, val):
        #print("setting d to {}".format(val))
        if self.G.s == 'start':
            self.d_from_start = val
        elif self.G.s == 'bulkhead':
            self.d_from_bulkhead = val
        elif self.G.s == 'to_bulkhead':
            self.d_to_bulkhead = val
        else:
            raise Exception("Unknown source_name {}".format(self.G.s))

    @property
    def pi(self):
        return self.get_pi(self.G.s)

    def get_pi(self, source_name):
        if source_name == 'start':
            return self.pi_from_start
        elif source_name == 'bulkhead':
            return self.pi_from_bulkhead
        elif source_name == 'to_bulkhead':
            return self.pi_to_bulkhead
        else:
            raise Exception("Unknown source_name {}".format(source_name))

    @pi.setter
    def pi(self, val):
        if self.G.s == 'start':
            self.pi_from_start = val
        elif self.G.s == 'bulkhead':
            self.pi_from_bulkhead = val
        elif self.G.s == 'to_bulkhead':
            self.pi_to_bulkhead = val
        else:
            raise Exception("Unknown source_name {}".format(self.G.s))

    def __repr__(self):
        return """
        V.id: {}
        V.d: s:{}, b:{}, to_b:{}
        V.pi: s:{}, b:{}, to_b:{}
        """.format(
                self.id, self.d_from_start, 
                self.d_from_bulkhead, self.d_to_bulkhead, 
                self.pi_from_start, 
                self.pi_from_bulkhead, self.pi_to_bulkhead)

    def __str__(self):
        return str(self.id)

    def shortest_path(self, source_name):
        # get parent until None is met
        path = "{} -> ".format(self.id)
        pi = self.get_pi(source_name)
        while pi is not None:
            path += "{} -> ".format(pi.id)
            pi = pi.get_pi(source_name)

        path += "empty"
        return path


def floyd_warshall(W):
    n = len(W)
    D = [None] * n
    D[0] = W
    for k in range(1, n):
        D[k] = new_mat(n)
        for i in range(n):
            for j in range(n):
                D[k][i][j] = min(
                        D[k-1][i][j], 
                        D[k-1][i][k] + 
                        D[k-1][k][j])
    return D[n-1]


def new_mat(n):
    return [[0 for j in range(n)] for i in range(n)]


def bellman_ford(G, w, s):
    # init has done naturally
    init_single_source(G, s)
    # relax every edge |G.V| - 1 time
    for _ in range(len(G.V) - 1):
        for (u, v) in G.E:
            relax(u, v, w)

    # check negative loop, (using triangular rule)
    for (u, v) in G.E:
        if v.d > u.d + w[u.id][v.id]:
            return False

    return True


def relax(u, v, w):
    """
    direct is in (`start`, `bulkhead`)
    relax to satisfy triangular rule
    v.d <= u.d + w(u, v)
    """
    #print("checking {} and {}".format(u, v))
    #print("checking {} and {}".format(repr(u), repr(v)))
    if v.d > u.d + w[u.id][v.id]:
        #print("relaxing {} and {}".format(repr(u), repr(v)))
        #print("v.d before relax:", v.d)
        v.d = u.d + w[u.id][v.id]
        #print("v.d relaxed:", v.d)
        # assign parent
        v.pi = u
        #print("relaxed {} and {}".format(repr(u), repr(v)))


def init_graph(G, w):
    # init empty vertices 
    for u in range(len(w)):
        G.V.append(Vertice(G, u))

    # init edge
    for u in range(len(w)):
        for v in range(len(w)):
            G.E.append((G.V[u], G.V[v]))

    # mark start and bulkhead
    G.V[0].d_from_start = 0
    G.V[-1].d_from_bulkhead = 0
    G.V[-1].d_to_bulkhead = 0


def init_single_source(G, s):
    G.s = s


def invert_mat(l):
    return list(map(list, zip(*l)))


def get_sample_mat():
    return [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]]
    #return [[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]]


def init_env():
    G = Graph()

    w = get_sample_mat()
    inv_w = invert_mat(w)

    init_graph(G, w)
    contains_loop = not bellman_ford(G, w, 'start')
    if contains_loop:
        print("contains loop")
        return (None, None, None)
    bellman_ford(G, w, 'bulkhead')
    bellman_ford(G, inv_w, 'to_bulkhead')

    return G, w, inv_w

def main():
    #result = solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
    result = solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
    print("result: {}".format(result))

if __name__ == "__main__":
    main()
