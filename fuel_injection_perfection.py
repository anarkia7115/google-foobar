def answer(n):
    # import sys
    # sys.setrecursionlimit(2000)
    sol = Solution()
    return sol.divide_until_one_bin_method(sol.dec_to_bin(n))


def slow_answer(n):
    # import sys
    # sys.setrecursionlimit(2000)
    sol = Solution()
    return sol.divide_until_one(n)


class Solution(object):
    def __init__(self):
        self.num_map = dict()
        pass

    @staticmethod
    def add_one(n, base=10):
        result = ""
        carrier = 1
        for digit in n[::-1]:
            sum = int(digit) + carrier
            if sum > base - 1:  # if brings up carrier
                carrier = 1
                sum = 0
            else:
                carrier = 0
            try:
                result += str(sum)
            except RuntimeError:
                print("[RE]n:", n)
                print("[RE]sum:", sum)
                print("[RE]result:", result)
                raise

        result = result[::-1]
        if carrier != 0:
            result = '1' + result

        return result

    @staticmethod
    def divide(n, divisor=2):
        # assume divisor is small
        # if isinstance(n, int):
        #     n = str(n)
        remainder = 0
        result = ""
        for digit in n:
            int_d = remainder * 10 + int(digit)
            remainder = int_d % divisor
            quotient = (int_d - remainder) // divisor
            result += str(quotient)

        quotient = result
        if quotient != '0':
            quotient = quotient.lstrip('0')
        return quotient, str(remainder)

    def dec_to_bin(self, n):
        result_str = ""
        quotient = n
        while quotient != '0':
            # print("quotient:", quotient)
            quotient, remainder = self.divide(quotient)
            result_str += str(remainder)
        return result_str[::-1].lstrip("0")

    def divide_until_one_ignoring_remainder(self, n):
        if n != '1':
            quotient, _ = self.divide(n)
            print("quotient:", quotient)
            self.divide_until_one_ignoring_remainder(quotient)

    def divide_until_one_bin_method(self, n):
        """
        1. check if n == '1', if true, return opration_num
        2. check if `n` is tailing `0`
            a) if tailing `0`:
                    divide by 2
                    operation_num +=1
            b) else tailing not `0`
                    add/minus one
                    operation_num +=1
        3. recursive next
        :param n: binary n
        :param operation_num:
        :return:
        """
        # print("operation_num:{}\tn:{}".format(operation_num, n))
        # print("size of num_set:{}".format(len(self.num_map)))
        if n == '1':
            return 0

        # do not need to compute again
        if n in self.num_map:
            return self.num_map[n]

        # compute is inevitable
        orig_n = n
        if n.endswith('0'):
            # divided by 2
            n = n[:-1]
            operation_num = self.divide_until_one_bin_method(n)
            operation_num_optimized = operation_num + 1
        else:
            # add
            n = self.add_one(orig_n, base=2)
            operation_num_add = self.divide_until_one_bin_method(n) + 1
            # minus, operation += 2
            n = orig_n[:-1]
            operation_num_minus = self.divide_until_one_bin_method(n) + 2
            if operation_num_minus > operation_num_add:  # return smaller
                operation_num_optimized = operation_num_add
            else:
                operation_num_optimized = operation_num_minus

        self.num_map[orig_n] = operation_num_optimized
        return operation_num_optimized

    def divide_until_one(self, n, remainder='0', operation_num=0):
        # print("operation number", operation_num)

        # print("n", n)
        if n == '1' and remainder == '0':
            return operation_num

        if remainder == '0':
            # print('divide')
            # divide
            next_n, next_remainder = self.divide(n)
            return self.divide_until_one(
                next_n,
                remainder=next_remainder,
                operation_num=operation_num+1)
        else:
            # 2 options, add or minus
            # choose the faster one
            # print("add & minus")
            op_num_add = self.divide_until_one(
                self.add_one(n),
                remainder='0',
                operation_num=operation_num+1
            )
            op_num_minus = self.divide_until_one(
                n,
                remainder='0',
                operation_num=operation_num+1
            )
            if op_num_add < op_num_minus:
                return op_num_add
            else:
                return op_num_minus


def test_answer():
    n = '5'
    print("answer({}) = {}".format(n, answer(n)))
    n = '4'
    print("answer({}) = {}".format(n, answer(n)))
    print("slow_answer({}) = {}".format(n, slow_answer(n)))
    n = '15'
    print("answer({}) = {}".format(n, answer(n)))
    print("slow_answer({}) = {}".format(n, slow_answer(n)))
    n = '9' * 7
    print("answer({}) = {}".format(n, answer(n)))
    print("slow_answer({}) = {}".format(n, slow_answer(n)))

    for n in range(2, 999):

        ans1 = answer(str(n))
        ans2 = slow_answer(str(n))
        if ans1 != ans2:
            print("answer({}) = {}".format(n, ans1))
            print("slow_answer({}) = {}".format(n, ans2))


def test_pure_divide():
    sol = Solution()
    n = '9' * 30
    sol.divide_until_one_ignoring_remainder(n)


def test_dec2bin():
    sol = Solution()
    n = '123'
    bin_str = sol.dec_to_bin(n)
    print("bin:", bin_str)
    print("corresponding int:", int(bin_str, 2))
    return bin_str


def test_add_bin():
    sol = Solution()
    n = '123'
    bin_str = sol.dec_to_bin(n)
    # bin_str = "111"
    print("origin bin:", bin_str)
    bin_add_one_str = sol.add_one(bin_str, base=2)
    print("add one:", bin_add_one_str)
    return bin_str


def main():
    test_answer()
    #test_dec2bin()
    # test_add_bin()


if __name__ == "__main__":
    main()
