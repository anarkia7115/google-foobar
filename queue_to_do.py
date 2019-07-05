def checksum_bitwise(checksum, curr_num):
    checksum = checksum ^ curr_num
    return checksum


def answer(start, length:int):

    line_start = None
    curr_length = length
    line_num = 0
    checksum = 0

    while curr_length > 0:
        line_num += 1
        if line_start is None:
            line_start = start
        #print(line_start)
        # arr[cycle*4] = arr[0]
        # arr_idx = cycle * 4 + remainder (remainder < 4)
        remainder = (curr_length-1) % 4
        #print("remainder", remainder)
        # 0 1 2 3 4 5 6 7 8 9 (length = 10), remainder = 2
        # 9 should be calculated, arr[0] == arr[8]
        # arr[length - remainder + 1:] = [9]
        # START FROM LENGTH - REMAINDER + 1
        # until length

        start:int = curr_length - remainder
        end = curr_length

        #print("line_start", line_start)
        if line_start % 2 == 0:
            # do nothing
            start = start - 1
            #print("({}, {})".format(start, end))
            #print("row: ", 0, end="")  # if odd
            pass
        else:
            checksum ^= line_start
            #print("({}, {})".format(start, end))
            #print("row: ", line_start, end="")  # if odd
        for i in range(start, end):
            curr_num = i + line_start
            checksum ^= curr_num
            #print(" ^", curr_num, end="")
            # print(curr_num, end=",")

        #print()
        # print("curr_length", curr_length)

        line_start = line_start + length
        curr_length -= 1

    return checksum


def golden_slow_answer(start, length):
    curr_num = None
    checksum = None

    curr_length = length

    while curr_length > 0:

        # for every elem in row
        for i in range(length):
            # occur once globally
            if curr_num is None:
                curr_num = start
                checksum = curr_num
            else:
                curr_num = curr_num + 1
                # need to add to checksum?
                if i >= curr_length:
                    # no need
                    pass
                else:
                    checksum = checksum ^ curr_num

        # goto next row
        curr_length -= 1

    return checksum


def bitwise_until(start, end):
    checksum = 0
    for i in range(start, end):
        checksum = checksum ^ i

    return checksum


def find_zero_cycle(start=19, end=1000):
    checksum = 0
    for i in range(start, end):
        checksum = checksum ^ i
        if checksum == 0:
            print("checksum: {} *".format(checksum))
        else:
            print("checksum:", checksum)


def test_answer():
    start = 0
    length = 3
    print("start:{}, length:{}".format(start, length))
    print(answer(start, length))
    print(golden_slow_answer(start, length))

    start = 17
    length = 4
    print("start:{}, length:{}".format(start, length))
    print(answer(start, length))
    print(golden_slow_answer(start, length))

    start = 10
    length = 5
    print("start:{}, length:{}".format(start, length))
    print(answer(start, length))
    print(golden_slow_answer(start, length))


def main():
    #find_zero_cycle()
    test_answer()


if __name__ == "__main__":
    main()
