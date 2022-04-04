import read_module
from stack import Stack

def Run(input_file):
    Sigma, Starting_States, Final_States, DFA, States = read_module.Read(input_file)
    dfa = {}
    for x in DFA.items():
        dfa[x[0]] = {}
        for y in DFA[x[0]].items():
            for z in DFA[x[0]][y[0]]:
                dfa[x[0]][z] = y[0]
    n = len(States)
    Matrix = [[0 for j in range(n)] for i in range(n)]
    for i in range(1, n):
        for j in range(0, i):
            check1 = (i in Final_States)
            check2 = (j in Final_States)
            if check2 * check1 == 0 and check1 + check2 == 1 and i != j:
                Matrix[i][j] = 1
                Matrix[j][i] = 1
    ok = 1
    stack = Stack()
    while ok == 1:
        ok = 0
        for i in range(1, n):
            for j in range(0, i):
                if Matrix[i][j] == 0:
                    stack.push((i, j))
        while stack.size() > 0:
            x, y = stack.top()
            stack.pop()
            for letter in Sigma:
                if dfa[x][letter] != dfa[y][letter] and Matrix[dfa[x][letter]][dfa[y][letter]] == 1:
                    ok = 1
                    Matrix[x][y] = 1
                    Matrix[y][x] = 1
    states = []
    for i in range(1, n):
        for j in range(0, i):
            if Matrix[i][j] == 0:
                ok = 0
                for s in states:
                    if i in s or j in s:
                        s.add(i)
                        s.add(j)
                        ok = 1
                        break
                if ok == 0:
                    states.append({i, j})
    for i in States:
        ok = 0
        for s in states:
            if i in s:
                ok = 1
                break
        if ok == 0:
            states.append({i})
    print("Sigma:")
    for x in Sigma:
        print(x)
    print("End")
    print("States:")
    for s in states:
        string = ''
        start = 0
        final = 0
        for x in s:
            if x == Starting_States[0]:
                start = 1
            if x in Final_States:
                final = 1
            string = string + ',' + str(x)
        if len(string) == 2:
            print(string[1:], end='')
        else:
            print('{' + string[1:] + '}', end='')
        if start == 1:
            print(', S', end='')
        if final == 1:
            print(', F', end='')
        print()
    print("End")
    print("Transitions:")
    n = len(states)
    transitions = set()
    ConvertDict = {}
    for i in range(n):
        for x in states[i]:
            ConvertDict[x] = i
    for i in range(n):
        for x in states[i]:
            for y in DFA[x].items():
                for z in y[1]:
                    transitions.add((i, z, ConvertDict[y[0]]))
    for s in transitions:
        a = len(states[s[0]])
        b = len(states[s[2]])
        if a == 1:
            print(*states[s[0]], end=', ')
        else:
            print(states[s[0]], end=', ')
        print(s[1], end=', ')
        if b == 1:
            print(*states[s[2]])
        else:
            print(states[s[2]])
    print("End")

if __name__ == '__main__':
    input_file = "dfa_config_file"
    Run(input_file)