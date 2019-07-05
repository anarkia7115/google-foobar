def answer(x, y):
    height_start = x + y - 1
    width_step = x - 1
    start_num = 0
    for i in range(1, height_start):  # final but last level
        start_num += i

    start_num += 1  # goto final level

    return str(start_num + width_step)


def main():
    print(answer(3, 2))

    print(answer(5, 10))


if __name__ == "__main__":
    main()
