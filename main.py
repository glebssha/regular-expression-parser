from enum import IntEnum
import math

alphabet = {'a', 'b', 'c'}
literal = {'1'}
operators = {'*', '.', '+'}


class Type(IntEnum):
    infix = 0
    prefix = 1
    suffix = 2
    inf = 3


class Solve:
    def __init__(self):
        self.dp = []

    def concatenate(self):
        infix_2, infix_1 = self.dp[Type.infix].pop(), self.dp[Type.infix].pop()
        prefix_2, prefix_1 = self.dp[Type.prefix].pop(), self.dp[Type.prefix].pop()
        suffix_2, suffix_1 = self.dp[Type.suffix].pop(), self.dp[Type.suffix].pop()
        inf2, inf1 = self.dp[Type.inf].pop(), self.dp[Type.inf].pop()

        self.dp[Type.infix].append(max(max(infix_1, infix_2), suffix_1 + prefix_2))
        if inf1 != -1:
            self.dp[Type.prefix].append(max(prefix_1, inf1 + prefix_2))
        else:
            self.dp[Type.prefix].append(prefix_1)
        if inf2 != -1:
            self.dp[Type.suffix].append(max(suffix_2, inf2 + suffix_1))
        else:
            self.dp[Type.suffix].append(suffix_2)
        if inf1 != -1 and inf2 != -1:
            self.dp[Type.inf].append(inf1 + inf2)
        else:
            self.dp[Type.inf].append(-1)

    def plus(self):
        self.dp[Type.infix].append(max(self.dp[Type.infix].pop(), self.dp[Type.infix].pop()))
        self.dp[Type.prefix].append(max(self.dp[Type.prefix].pop(), self.dp[Type.prefix].pop()))
        self.dp[Type.suffix].append(max(self.dp[Type.suffix].pop(), self.dp[Type.suffix].pop()))
        self.dp[Type.inf].append(max(self.dp[Type.inf].pop(), self.dp[Type.inf].pop()))

    def multiply(self):
        tmp = self.dp[Type.suffix][len(self.dp[Type.suffix]) - 1]
        tmp += self.dp[Type.prefix][len(self.dp[Type.prefix]) - 1]
        self.dp[Type.infix].append(max(self.dp[Type.infix].pop(), tmp))
        self.dp[Type.inf].pop()
        self.dp[Type.inf].append(0)

    def solve(self, expression, x):
        self.dp = [[] for i in range(4)]
        for value in expression:
            if value in alphabet:
                if value == x:
                    for i in range(4):
                        self.dp[i].append(1)
                    continue
                else:
                    self.dp[Type.infix].append(0)
                    self.dp[Type.prefix].append(0)
                    self.dp[Type.suffix].append(0)
                    self.dp[Type.inf].append(-1)
                    continue

            elif value in literal:
                for i in range(4):
                    self.dp[i].append(0)
                continue

            elif value in operators:
                if value == '+':
                    if len(self.dp[Type.infix]) < 2:
                        print('ERROR: inconsistent regular expression')
                        exit(0)
                    self.plus()
                elif value == '.':
                    if len(self.dp[Type.infix]) < 2:
                        print('ERROR: inconsistent regular expression')
                        exit(0)
                    self.concatenate()
                elif value == '*':
                    if len(self.dp[Type.infix]) < 1:
                        print('ERROR: inconsistent regular expression')
                        exit(0)
                    if self.dp[Type.inf][len(self.dp[Type.inf]) - 1] > 0:
                        return "INF"
                    self.multiply()
            else:
                print(f'ERROR: UNKNOWN SYMBOL {value}')
                exit(0)
        if len(self.dp[Type.infix]) > 1:
            print('ERROR: inconsistent regular expression')
            exit(0)
        return self.dp[Type.infix][0]


if __name__ == "__main__":
    expression, x = input().split()
    print(Solve().solve(expression, x))
