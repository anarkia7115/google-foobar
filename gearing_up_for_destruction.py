from fractions import Fraction


def answer(pegs):
    r0_frac = compute_r0(pegs)
    if r0_frac <= 1:
        return [-1, -1]
    else:
        ratio_list = compute_r(pegs, r0_frac)
        for i in range(len(ratio_list) - 1):
            r = ratio_list[i]
            r_next = ratio_list[i+1]
            p = pegs[i]
            p_next = pegs[i+1]
            if r <= 1 \
                    or r_next <= 1 \
                    or p + r + r_next != p_next:
                return [-1, -1]
        return [r0_frac.numerator, r0_frac.denominator]


def compute_r(pegs, r0):
    d_list = []
    for i in range(1, len(pegs)):
        d_list.append(pegs[i] - pegs[i - 1])

    ratio_list = [r0]

    # suppose r0 is known,
    # start at r1
    for k in range(1, len(d_list) + 1):
        # compute sum first
        sum_part = 0
        for i in range(0, k):  # exclude k
            sum_part += (-1) ** (i + k + 1) * d_list[i]
            #print(f"increasing sum_part for k:{k}:", sum_part)

        # print(f"sum_part {sum_part} for {k}")
        r_k = sum_part + (-1) ** k * r0
        ratio_list.append(r_k)

    return ratio_list


def compute_r0(pegs):
    d_list = []
    for i in range(1, len(pegs)):
        d_list.append(pegs[i] - pegs[i - 1])

    n = len(d_list)
    sum_part = 0
    k = n
    for i in range(0, k):  # exclude k
        sum_part += (-1) ** (i + k + 1) * d_list[i]
        #print(f"increasing sum_part for k:{k}:", sum_part)

    numerator = sum_part
    denominator = -1 * (-1) ** k + Fraction(1, 2)

    fract = Fraction(numerator, denominator)
    return fract


def main():
    pegs = [4, 30, 50]
    print(answer(pegs))

    pegs = [4, 25, 41, 54]
    print(answer(pegs))

    pegs = [7, 10, 12, 15]
    print(answer(pegs))

    pegs = [4, 17, 50]
    print(answer(pegs))

    pegs = [1, 1]
    print(answer(pegs))
    print(compute_r(pegs, compute_r0(pegs)))

    pegs = [1, 2, 3]
    print(answer(pegs))
    print(compute_r(pegs, compute_r0(pegs)))

    pegs = [1, 2, 4]
    print(answer(pegs))
    print(compute_r(pegs, compute_r0(pegs)))

    pegs = [1, 4, 5]
    print(answer(pegs))
    print(compute_r(pegs, compute_r0(pegs)))

if __name__ == "__main__":
    main()
