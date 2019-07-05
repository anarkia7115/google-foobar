INF=500

def add(x, y):
    """
    support add infinity
    """
    if x >= INF or y >= INF:
        return INF
    else:
        return x + y

def min_with_inf(*elems):
    min_e = INF
    for elem in elems:
        if min_e > elem:
            min_e = elem

    return min_e


def compute_sp(map, sp, i, j):
    """
    Goal: compute shortest path to escape pod, where type is not wall
    1. initial check:
           if i == h-1, j == w-1, sp[i][j] = 1
    2. check surrounding (i_nb, j_nb), make recursion when (and connect):
           a) (i_nb, j_nb) is valid <=> i_nb <= h-1, j_nb <= w-1
           x b) this position has not been computed before, sp[i_nb][j_nb] == INF
           c) this position is not wall, map[i_nb][j_nb] != INF
    2.5 update sp
        policy:
            1. compute sp for i_nb, j_nb
            2. **compare** with existing sp[][]

    2.6 recursion:
           if updated, go next
           sp[i_nb][j_nb] = 1+sp[i][j]
           sp = compute_sp(map, sp, i_nb, j_nb)
    3. after surroundings are all visited, return sp
    """
    # 1. initialization
    w = len(map[0])
    h = len(map)
    if i == h-1 and j == w-1:
        sp[i][j] = 1

    assert map[i][j] != 1

    # Assume sp[i][j] is computed in current path

    #2. check surrounding
    for i_nb, j_nb in (
            (i-1, j), (i+1, j), (i, j-1), (i, j+1)
            ):
        # is valid?
        # a) in bound
        cond1 = (0<= i_nb <= h-1 and 0<= j_nb <= w-1)
        # b) novel x
        #cond2 = (sp[i_nb][j_nb] == INF)
        # c) not wall
        if cond1:
            cond3 = (map[i_nb][j_nb] != 1)
        else:
            cond3 = False

        #print("i_nb", i_nb)
        #print("j_nb", j_nb)
        #print("cond1", cond1)
        #print("cond3", cond3)
        # do recursion?
        if cond1 and cond3:
            # update sp
            sp, is_updated = update_sp(sp, i_nb, j_nb, add(1, sp[i][j]))
            if is_updated:
                # go to next position
                sp = compute_sp(map, sp, i_nb, j_nb)

    return sp


def update_sp(sp, i_nb, j_nb, new_value):
    # tell outside if sp has been updated
    is_updated = False
    if sp[i_nb][j_nb] >= INF or new_value < sp[i_nb][j_nb]:
        # update better result
        sp[i_nb][j_nb] = new_value
        is_updated = True
        return sp, is_updated
    else:
        return sp, is_updated


def compute_ssp(map, sp, ssp):
    """
    after sp are all computed, 
    first parse
        for walls:
            ssp[i][j] = min(sp[l, r, u, d]) + 1
        for non-walls:
            ssp[i][j] = sp[i][j]

    when elements are all computed
    second parse
        for non-walls:
            ssp[i][j] = min(ssp[l, r, u, d]) + 1
    """
    w = len(map[0])
    h = len(map)

    # first parse
    for i in range(h):
        for j in range(w):
            # 1. check is wall
            if map[i][j] == 1: # is wall

                # min around neighbour
                # for (i_nb, j_nb) in index_of(up, down, left, right)
                for i_nb, j_nb in (
                        (i-1, j), (i+1, j), (i, j-1), (i, j+1)
                        ):
                    # 2. check in bound, minimize
                    # ssp[i][j] = min(sp[l, r, u, d]) + 1
                    if 0 <= i_nb < h and 0 <= j_nb < w:
                        ssp[i][j] = min_with_inf(ssp[i][j], add(sp[i_nb][j_nb], 1))
            else: # is non-wall
                ssp[i][j] = sp[i][j]

    #print_map(ssp)

    # second parse
    for i in range(h):
        for j in range(w):
            ssp = update_ssp(map, ssp, i, j)

    return ssp


def update_ssp(map, ssp, i, j):
    w = len(map[0])
    h = len(map)

    # only process non-wall
    if not (0 <= i < h and 0 <= j < w) or map[i][j] == 1: # not in bound or is wall
        return ssp

    min_nb_ssp = INF
    # min around neighbour
    for i_nb, j_nb in (
            (i-1, j), (i+1, j), (i, j-1), (i, j+1)
            ):
        # check in bound, minimize
        if 0 <= i_nb < h and 0 <= j_nb < w:
            min_nb_ssp = min_with_inf(min_nb_ssp, ssp[i_nb][j_nb])

    # if current ssp need to be updated
    if min_nb_ssp+1 < ssp[i][j]:
        # reassign current ssp
        ssp[i][j] = min_nb_ssp+1
        # update neighbour ssp
        ssp = update_ssp(map, ssp, i-1, j)
        ssp = update_ssp(map, ssp, i+1, j)
        ssp = update_ssp(map, ssp, i, j-1)
        ssp = update_ssp(map, ssp, i, j+1)

    return ssp


def solution(map):
    """
    sp[i]: shortest path from point `i` to escape pod.
    s_sp[i]: super shortest path from point `i` to escape pod where wall removal privilege is used in the shortest path. 

    1. compute all sp(shortest path), (buttom-up?)
    2. compute all s_sp where type is wall (1s)
    3. fill in the remaining unsigned s_sp[i] with sp[i]
    4. recompute all s_sp where type is not wall (0s)
    """
    w = len(map[0])
    h = len(map)

    # init sp, ssp
    sp = [[INF for i in range(w)] for i in range(h)]
    ssp = [[INF for i in range(w)] for i in range(h)]

    sp = compute_sp(map, sp, h-1, w-1)
    #print_map(sp)
    ssp = compute_ssp(map, sp, ssp)
    #print_map(ssp)
    return ssp[0][0]


def print_map(map):
    for row in map:
        print("\t".join([str(x) for x in row]))
    print("\n")


def main():
    #map = [[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]
    #map = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    map = [[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]
    """
    map = [
            [0, 0, 0, 0, 0, 0], 
            [1, 1, 0, 1, 1, 0], 
            [0, 1, 1, 0, 1, 1], 
            [0, 1, 1, 0, 1, 1], 
            [0, 1, 1, 0, 1, 1], 
            [0, 1, 1, 0, 1, 1], 
            [0, 0, 0, 0, 0, 0]]
    """

    #print_map(map)
    sol = solution(map)
    print(sol)
    #print_map(sol)


if __name__ == "__main__":
    main()
