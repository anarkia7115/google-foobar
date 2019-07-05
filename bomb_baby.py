MAX_ITER = 5000
def find_root(x, y):
    rep_cycle = 0
    for i in range(MAX_ITER):  # x, y is less than 10 ** 50, max iteration should be small
        #print("(x, y): ({}, {})".format(x, y))
        #print("iteration: ", i)
        if x == 0:  # (x, y) is one step more than root
            return (x, y, rep_cycle - 1)
        x, y, diff_time = find_parent(x, y)
        #print("diff_time: ", diff_time)
        rep_cycle += diff_time
        #print("rep_cycle: ", rep_cycle)

    raise Exception("ITERATION exceed")


def find_parent(x, y):
    """
    return (diff(x, y), min(x, y))
    """
    # diff
    if x > y:
        diff_time = x // y
        return (x % y, y, diff_time)
    elif y > x:
        diff_time = y // x
        return (y % x, x, diff_time)
    else:
        raise Exception("x, y has no parent((x, y) is root)")

def solution(x, y):
    """
    keep compute difference of (x, y), keep finding the parent of (x, y) untill root
    why it works? recursion tree will show. 
    (diff(x, y), min(x, y)) is the parent of (x, y)
    """
    x = int(x)
    y = int(y)
    root_x, root_y, rep_cycle = find_root(x, y)

    if root_x != 0 or root_y != 1:
        return "impossible"
    else:
        return str(rep_cycle)

def main():
    x, y = '4', '7'
    print(solution(x, y))

    x, y = '2', '4'
    print(solution(x, y))

    x, y = '2', '1'
    print(solution(x, y))

    x, y = str(10 ** 50), str(10 ** 50 // 2 + 1)
    print(solution(x, y))


if __name__ == "__main__":
    main()
