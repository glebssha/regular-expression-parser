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
        if res1.Max > res2.Max:
            return left
        else:
            return right


def multiply(element, stack, sym_list):
    if len(element.Symbol) == element.LCounter and len(element.Symbol) == element.RCounter:
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
    list_cpy = copy(symbols_list)
    for symbol in symbols_list:
        try:
            list_cpy.pop(0)
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
                    stack.append(plus(left_sym, right_sym, stack, list_cpy))
                elif symbol.Symbol == '*':
                    last_sym = stack.pop()
                    stack.append(multiply(last_sym, stack, list_cpy))
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
    stack = deque()
    a = solve(stack, symbols_list)
    print(a.Max)
