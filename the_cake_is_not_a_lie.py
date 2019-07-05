def answer(s):
    max_split_size = 0
    for split_size in range(1, len(s) + 1):
        i = 0
        # check is splitable
        if len(s) % split_size != 0:
            continue

        chunk_size = len(s) // split_size
        first_chunk = s[:chunk_size]
        i += chunk_size

        while i + chunk_size <= len(s):
            curr_sub_seq = s[i:i+chunk_size]
            if curr_sub_seq == first_chunk:
                i += chunk_size
            else:
                break

        if i == len(s):  # verified
            max_split_size = split_size  # update

    return max_split_size


def main():
    input = "abccbaabccba"
    print(answer(input))

    input = "abcabcabcabc"
    print(answer(input))


if __name__ == "__main__":
    main()