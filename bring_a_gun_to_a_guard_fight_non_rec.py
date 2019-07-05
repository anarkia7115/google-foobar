import math
#import matplotlib.pyplot as plt
from fractions import Fraction, gcd
def solution(dimensions, your_position, guard_position, distance):
    """
    Start from highest mirror, where is it?
    d: Distance
    y_dim: Dimention of y 
    x_dim: Dimention of x
    ceil(d / y)

    Try to find a iteration method and end point. 

    record a path matrix
        path_mat = dict(dict())
        if path_mat[i][j] == 1:
            // this road has been walked

    every point has 9 moves(including not moving)
        1 2 3  (-1,  1) ( 0,  1) ( 1,  1)
        4 0 5  (-1,  0) ( 0,  0) ( 1,  0)
        6 7 8  (-1, -1) ( 0, -1) ( 1, -1)

    how to compute mirror of self/enermy? with mirror offset (x_offset, y_offset)
        self   - (sx, sy)
        enermy - (ex, ey)
        o----------------------------------o----------------------------------o----------------------------------o
        |                                  |                                  |                                  |
        |                                  |                                  |                                  |
        |                    (ex, ey)      |      (ex, ey)                    |                    (ex, ey)      |
        |                                  |                                  |                                  |
 {y_dim}|                                  |                                  |                                  |
        |                                  |                                  |                                  |
        |   (sx, sy)                       |                       (sx, sy)   |   (sx, sy)                       |
        |                                  |                                  |                                  |
        |                                  |                                  |                                  |
  (0, 0)o--------------{x_dim}-------------o----------------------------------o----------------------------------o
        |                                  |                                  |                                  |
        |                                  |                                  |                                  |
        |   (sx, sy)                       |                       (sx, sy)   |   (sx, sy)                       |
        |                                  |                                  |                                  |
        |                                  |                                  |                                  |
        |                                  |                                  |                                  |
        |                    (ex, ey)      |      (ex, ey)                    |                    (ex, ey)      |
        |                                  |                                  |                                  |
        |                                  |                                  |                                  |
        o----------------------------------o----------------------------------o----------------------------------o

        x_offset - x offset from origin space to mirror space
        y_offset - y offset from origin space to mirror space

        mirr_self   - (msx, msy)
        mirr_enermy - (mex, mey)

        if x_offset is odd
            msx = x_offset * x_dim + (x_dim - sx + 1)
            msy = y_offset * y_dim + (y_dim - sy + 1)

        if x_offset is even
            msx = x_offset * x_dim + sx
            msy = y_offset * y_dim + sy

        1. Check current space is visited. If path_mat[x_offset][y_offset] == 1, return. Since current space is visited, skip
        2. Compute current mirror x, y. (msx, msy), (mex, mey)
        3. Compute distance. dist(orig_self, mirror)^2 = (osx - mx) ^2 + (osy - my) ^2 If distance is too far, return.
        4. If distance is in range, compute slope. Abbreviation. And add slope to sets. 
        5. Result: len(enermy_slope_set - self_slope_set)

    how to compute distance? with mirror offset (x_offset, y_offset)
        x_offset - x offset from origin to mirror
        y_offset - y offset from origin to mirror

    """
    # init mat and set
    path_mat = dict()
    self_slope_set = dict()
    enermy_slope_set = dict()
    x_dim, y_dim = dimensions
    k_x = int(math.ceil(distance / x_dim))
    k_y = int(math.ceil(distance / y_dim))
    for x_offset in range(-k_x-1, k_x + 2):
        for y_offset in range(-k_y-1, k_y + 2):
            #print(x_offset, y_offset)
            compute_shoot_angle(dimensions, your_position, guard_position, x_offset, y_offset, 
                    path_mat, distance, self_slope_set, enermy_slope_set)
    #print("enermy_slope_set:", enermy_slope_set)
    #print("self_slope_set:", self_slope_set)
    diff_set = min_dist_diff(enermy_slope_set, self_slope_set)
    #print(diff_set)
    return len(diff_set)

"""
def plot(point_type, x, y, x_off, y_off):
    if point_type == 'self':
        plt.scatter(x, y, color='g', marker='o')
    else:
        plt.scatter(x, y, color='r', marker='x')

    #plt.annotate("({}, {})".format(x, y), (x, y))
"""

def compute_slope(point_a, point_b):
    (mex, mey) = point_a
    (sx, sy) = point_b

    dx = mex - sx
    dy = mey - sy 

    g = abs(gcd(dx, dy))

    # dx / dy
    if g == 0:
        slope = (0, 0)
    else:
        slope = (int(dx / g), int(dy / g))

    #print("slop with points {} and {} are {}".format(point_a, point_b, slope))
    return slope

def min_dist_diff(enermy_slope_set, self_slope_set):
    #print("min_dist_diff")
    # for same direction, if self.distance is less than enermy.distance, remove from slope_set
    for e_slope, e_dist in enermy_slope_set.copy().items():
        if e_slope in self_slope_set and self_slope_set[e_slope] < e_dist:
                enermy_slope_set.pop(e_slope)

    return enermy_slope_set


def min_dist_add(enermy_slope_set, enermy_slope, dist_sq_enermy):
    #print("min_dist_add")
    if dist_sq_enermy == 0:
        return # skip 0 distance

    # check has this direction
    if enermy_slope not in enermy_slope_set:
        enermy_slope_set[enermy_slope] = dist_sq_enermy
    else:
        # choose a minimun dist for current direction
        enermy_slope_set[enermy_slope] = min(dist_sq_enermy, enermy_slope_set[enermy_slope])

def compute_shoot_angle(
        dimensions, 
        orig_self, 
        orig_enermy, 
        x_offset, y_offset, 
        path_mat, 
        distance, 
        self_slope_set, enermy_slope_set
        ):
    """
        1. Check current space is visited. If path_mat[x_offset][y_offset] == 1, return. Since current space is visited, skip
        2. Compute current mirror x, y. (msx, msy), (mex, mey)
        3. Compute distance. dist(orig_self, mirror)^2 = (osx - mx) ^2 + (osy - my) ^2 If distance is too far, return.
        4. If distance is in range, compute slope. Abbreviation. And add slope to sets. 
        5. Iterate to surrounding spaces
        6. Result: len(enermy_slope_set - self_slope_set)
    """
    # 1. Check current space is visited. If path_mat[x_offset][y_offset] == 1, return. Since current space is visited, skip
    #if path_mat[x_offset][y_offset]  == 1:
    if path_mat.setdefault(x_offset, dict()).setdefault(y_offset, 0) == 1:
        #print("already visited")
        return
    else:
        path_mat[x_offset][y_offset] = 1

    # 2. Compute current mirror x, y. (msx, msy), (mex, mey)
    x_dim, y_dim = dimensions
    #x_dim += 1
    #y_dim += 1

    sx, sy = orig_self
    ex, ey = orig_enermy

    if x_offset % 2 == 1:
        msx = x_offset * x_dim + (x_dim - sx)
        mex = x_offset * x_dim + (x_dim - ex)
    else:
        msx = x_offset * x_dim + sx
        mex = x_offset * x_dim + ex

    if y_offset % 2 == 1:
        msy = y_offset * y_dim + (y_dim - sy)
        mey = y_offset * y_dim + (y_dim - ey)
    else:
        msy = y_offset * y_dim + sy
        mey = y_offset * y_dim + ey

    #print("self: {} enermy: {}".format(orig_self, (mex, mey)))
    #plot('self', msx, msy, x_offset, y_offset)
    #plot('enermy', mex, mey, x_offset, y_offset)
    #plt.waitforbuttonpress()
    #plt.draw()
    #plt.show(block=False)

    # 3. Compute distance. dist(orig_self, mirror)^2 = (osx - mx) ^2 + (osy - my) ^2 If distance is too far, return.
    dist_sq_enermy = (sx - mex) ** 2 + (sy - mey) ** 2
    if dist_sq_enermy > distance ** 2:
        #print("out of range, dist**2: {}".format(dist_sq_enermy))
        # 4. If distance is in range, compute slope. Abbreviate. And add slope to sets. 
        #return # too distant to shoot the enermy
        pass
    else:
        #print("enermy can be shoot, dist**2: {}".format(dist_sq_enermy))
        enermy_slope = compute_slope((mex, mey), (sx, sy))
        min_dist_add(enermy_slope_set, enermy_slope, dist_sq_enermy)
        pass

    # can or cannot shoot self
    dist_sq_self = (sx - msx) ** 2 + (sy - msy) ** 2
    if dist_sq_self <= distance ** 2:
        can_hurt = True
    else:
        can_hurt = False


    if can_hurt:
        self_slope = compute_slope((msx, msy), (sx, sy))
        #print("this direction can hurt")
        min_dist_add(self_slope_set, self_slope, dist_sq_self)

    return

"""
def init_image(dimensions, your_position, distance):
    fig = plt.figure()
    ax = plt.gca()
    c = plt.Circle(your_position, distance, fill=False)
    ax.add_artist(c)
    plt.plot([0, dimensions[0], dimensions[0], 0, 0], [0, 0, dimensions[1], dimensions[1], 0])
"""

def main():
    dimensions = [3,2]
    your_position = [1,1]
    guard_position = [2,1]
    distance = 4

    #init_image(dimensions, your_position, distance)
    choices = solution(dimensions, your_position, guard_position, distance)
    #plt.grid(linestyle='dotted')
    #plt.show()
    print(choices)

    dimensions, your_position, guard_position, distance = [300,275], [150,150], [185,100], 500
    #init_image(dimensions, your_position, distance)
    choices = solution(dimensions, your_position, guard_position, distance)
    #plt.grid(linestyle='dotted')
    #plt.show()
    print(choices)

    dimensions, your_position, guard_position, distance = [4, 4], [1, 1], [2, 2], 10
    #dimensions, your_position, guard_position, distance = [40, 40], [1, 1], [20, 20], 1
    #init_image(dimensions, your_position, distance)
    choices = solution(dimensions, your_position, guard_position, distance)
    #plt.grid(linestyle='dotted')
    #plt.show()
    print(choices)

    #dimensions, your_position, guard_position, distance = [100, 100], [50, 50], [51, 51], 100
    #init_image(dimensions, your_position, distance)
    #choices = solution(dimensions, your_position, guard_position, distance)
    #plt.grid(linestyle='dotted')
    #plt.show()
    #print(choices)

if __name__ == "__main__":
    main()
