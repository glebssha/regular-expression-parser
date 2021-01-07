# Даны α и буква x. Найти максимальное k, такое что в L есть слова, содержащие
# подслово x^k .
from enum import IntEnum
from collections import namedtuple, deque
from copy import copy

alphabet = {'a', 'b', 'c'}
literal = {'1'}
operators = {'*', '.', '+'}


class Type(IntEnum):
    LETTER = 1
    OPERATOR = 2
    LITERAL = 3


Symbol = namedtuple('Symbol', ['Symbol', 'Type', 'LCloser', 'RCloser', 'LCounter', 'RCounter', 'Max'])


def convert(expression, s):
    result = []
    for value in expression:
        if value in alphabet:
            if value == s:
                result.append(Symbol(Symbol='1', Type=Type.LETTER, LCloser=0, RCloser=0, LCounter=1, RCounter=1, Max=1))
            else:
                result.append(Symbol(Symbol='0', Type=Type.LETTER, LCloser=1, RCloser=1, LCounter=0, RCounter=0, Max=0))
            continue
        elif value in operators:
            result.append(Symbol(Symbol=value, Type=Type.OPERATOR, LCloser=0, RCloser=0, LCounter=0, RCounter=0, Max=0))
            continue
        elif value in literal:
            result.append(Symbol(Symbol='0', Type=Type.LITERAL, LCloser=1, RCloser=1, LCounter=0, RCounter=0, Max=0))
            continue
        else:
            print(f'ERROR: UNKNOWN SYMBOL {value}')
            exit(0)
    return result


def concatenate(left, right):
    maximum = max(left.Max, right.Max)
    if left.Type == Type.LITERAL:
        return right
    if right.Type == Type.LITERAL:
        return left
    if left.RCloser == right.LCloser:
        max_center = left.RCounter + right.LCounter
        result = left.Symbol[0:-1] + f'{max_center}' + right.Symbol[1:]
        if result.count('0') > 1:
            result = result[0:result.find('0')] + result[result.rfind('0'):]
            maximum = max(maximum, max_center)
            return Symbol(Symbol=result,
                          Type=Type.LETTER,
                          LCloser=left.LCloser,
                          RCloser=right.RCloser,
                          LCounter=left.LCounter,
                          RCounter=right.RCounter,
                          Max=maximum
                          )
        maximum = max(max_center, maximum)
        res_l_counter = (left.Symbol.count('0') == 0) * right.LCounter + left.LCounter
        res_r_counter = (right.Symbol.count('0') == 0) * left.RCounter + right.RCounter
        return Symbol(Symbol=result,
                      Type=Type.LETTER,
                      LCloser=left.LCloser,
                      RCloser=right.RCloser,
                      LCounter=res_l_counter,
                      RCounter=res_r_counter,
                      Max=maximum
                      )
    else:
        result = (left.Symbol + right.Symbol)
        if result.count('0') > 1:
            result = result[0:result.find('0')] + result[result.rfind('0'):]
        return Symbol(Symbol=result,
                      Type=Type.LETTER,
                      LCloser=left.LCloser,
                      RCloser=right.RCloser,
                      LCounter=left.LCounter,
                      RCounter=right.RCounter,
                      Max=maximum
                      )


def plus(left, right, stack, sym_list):
    if left.Symbol == '0' and left.Type != Type.LITERAL:
        return right
    elif right.Symbol == '0' and right.Type != Type.LITERAL:
        return left
    else:
        stack.append(left)
        tmp = copy(sym_list)
        tmp_stack = copy(stack)
        res1 = solve(tmp_stack, tmp)
        stack.pop()
        stack.append(right)
        tmp = copy(sym_list)
        tmp_stack = copy(stack)
        res2 = solve(tmp_stack, tmp)
        stack.pop()
        mult_max = -1
        if sym_list[0].Symbol == '*':
            mult_max = max(concatenate(left, right).Max, concatenate(right, left).Max)
        if res1.Max > res2.Max:
            maximum = max(left.Max, mult_max)
            return Symbol(Symbol=left.Symbol,
                          Type=left.Type,
                          LCloser=left.LCloser,
                          RCloser=left.RCloser,
                          LCounter=left.LCounter,
                          RCounter=left.RCounter,
                          Max=maximum
                          )
        else:
            maximum = max(right.Max, mult_max)
            return Symbol(Symbol=right.Symbol,
                          Type=right.Type,
                          LCloser=right.LCloser,
                          RCloser=right.RCloser,
                          LCounter=right.LCounter,
                          RCounter=right.RCounter,
                          Max=maximum
                          )


def multiply(element, stack, sym_list):
    if int(element.Symbol) == element.LCounter and int(element.Symbol) == element.RCounter and element.Symbol != '0':
        print("INF")
        exit(0)
    elif element.LCounter + element.RCounter > element.Max:
        element = concatenate(element, element)

    stack.append(element)
    tmp = copy(sym_list)
    tmp_stack = copy(stack)
    res1 = solve(tmp_stack, tmp)
    stack.pop()
    blank_element = Symbol(Symbol='0', Type=Type.LITERAL, LCloser=1, RCloser=1, LCounter=0, RCounter=0,
                           Max=0)
    stack.append(blank_element)
    tmp = copy(sym_list)
    tmp_stack = copy(stack)
    res2 = solve(tmp_stack, tmp)
    stack.pop()
    if res1.Max > res2.Max:
        return element
    else:
        return blank_element


def solve(stack, symbols_list):
    n = len(symbols_list)
    for i in range(n):
        try:
            symbol = symbols_list.pop(0)
            if symbol.Type == Type.LETTER or symbol.Type == Type.LITERAL:
                stack.append(symbol)
            elif symbol.Type == Type.OPERATOR:
                if symbol.Symbol == '.':
                    right_sym = stack.pop()
                    left_sym = stack.pop()
                    stack.append(concatenate(left_sym, right_sym))
                elif symbol.Symbol == '+':
                    right_sym = stack.pop()
                    left_sym = stack.pop()
                    stack.append(plus(left_sym, right_sym, stack, symbols_list))
                elif symbol.Symbol == '*':
                    last_sym = stack.pop()
                    stack.append(multiply(last_sym, stack, symbols_list))
        except IndexError:
            print('ERROR: inconsistent regular expression')
            exit(0)
    if len(stack) > 1:
        print('ERROR: inconsistent regular expression')
        exit(0)

    return stack.pop()


if __name__ == "__main__":
    expression, x = input().split()
    symbols_list = convert(expression, x)
    stack = []
    a = solve(stack, symbols_list)
    print(a.Max)
