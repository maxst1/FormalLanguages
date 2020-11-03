import math


operators = ['.', '*', '+']

class Token:
    def __init__(self):
        self.value = 0
        self.open = False
        self.canBeEmpty = False

def solveReg(regular_value_, letter_, stack_, start):
    regular_value = regular_value_
    letter = letter_
    stack = stack_

    for i in range(start, len(regular_value)):
        symb = regular_value[i]
        if symb not in operators:
            t = Token()

            if symb == letter:
                t.value = 1
                t.open = True

            if symb == '1':
                t.canBeEmpty = True
                t.open = True

            stack.append(t)

        else:
            if symb == '+':
                if len(stack) <= 1:
                    err()

                R = stack.pop()
                L = stack.pop()

                # print("+ R = ", R.value, R.open, R.canBeEmpty)
                # print("+ L = ", L.value, L.open, L.canBeEmpty)

                t = Token()
                if L.open and R.open:
                    t.open = True
                    t.value = max(L.value, R.value)

                elif (not L.open) and (not R.open):
                    t.open = False
                    t.value = max(L.value, R.value)

                else:
                    stack.append(L)
                    tmp = list(stack)
                    res1 = solveReg(regular_value, letter, tmp, i+1)

                    stack.pop()
                    stack.append(R)
                    tmp = list(stack)
                    res2 = solveReg(regular_value, letter, tmp, i+1)
                    return max(res1, res2)

                t.canBeEmpty = L.canBeEmpty | R.canBeEmpty

                # print("+ t = ", t.value, t.open, t.canBeEmpty)
                # print()
                stack.append(t)

            if symb == '.':
                if len(stack) <= 1:
                    err()

                R = stack.pop()
                L = stack.pop()

                # print(". R = ", R.value, R.open, R.canBeEmpty)
                # print(". L = ", L.value, L.open, L.canBeEmpty)

                t = Token()
                if (not L.open) & (not R.open):
                    t.open = False
                    if (not L.canBeEmpty):
                        t.value = L.value
                    else:
                        t.value = max(L.value, R.value)

                if (L.open) & (R.open):
                    t.open = True
                    t.value = L.value + R.value

                if (L.open) & (not R.open):
                    if not R.canBeEmpty:
                        t.open = False
                        t.value = L.value + R.value

                    else:
                        stack.append(L)
                        tmp = list(stack)
                        res1 = solveReg(regular_value, letter, tmp, i + 1)

                        stack.pop()
                        t.open = False
                        t.value = L.value + R.value
                        t.canBeEmpty = L.canBeEmpty & R.canBeEmpty
                        stack.append(t)
                        tmp = list(stack)
                        res2 = solveReg(regular_value, letter, tmp, i + 1)
                        return max(res1, res2)

                if (not L.open) & (R.open):
                    if not L.canBeEmpty:
                        t.open = False
                        t.value = L.value
                    else:
                        stack.append(L)
                        tmp = list(stack)
                        res1 = solveReg(regular_value, letter, tmp, i + 1)

                        stack.pop()
                        stack.append(R)
                        tmp = list(stack)
                        res2 = solveReg(regular_value, letter, tmp, i + 1)
                        return max(res1, res2)


                t.canBeEmpty = L.canBeEmpty & R.canBeEmpty
                # print(". t = ", t.value, t.open, t.canBeEmpty)
                # print()
                stack.append(t)

            if symb == '*':
                if len(stack) <= 0:
                    err()

                T = stack.pop()

                # print("* T = ", T.value, T.open, T.canBeEmpty)

                t = Token()

                if T.open:
                    t.value = math.inf
                else:
                    t.value = T.value

                t.open = T.open
                t.canBeEmpty = True

                # print("* t = ", t.value, t.open, t.canBeEmpty)
                # print()
                stack.append(t)

    if len(stack) != 1:
        err()

    return stack[0].value

def err():
    print("ERROR")
    exit(0)

def check(rv, l):
    if not l in ['a', 'b', 'c']:
        err()

    for symb in rv:
        if not symb in ['a', 'b', 'c', '1', '.', '*', '+']:
            err()

def main():
    input_text = input().split()
    if len(input_text) != 2:
        err()

    regular_value = input_text[0]
    letter = input_text[1]

    check(regular_value, letter)

    stack = []

    result = solveReg(regular_value, letter, stack, 0)
    if result == math.inf:
        print("INF")
    else:
        print(result)

if __name__ == "__main__":
    main()
