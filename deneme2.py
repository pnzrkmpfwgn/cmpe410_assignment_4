class Node:
    def __init__(self, symbol, left_child=None, right_child=None):
        self.symbol = symbol
        self.left_child = left_child
        self.right_child = right_child


error = False
next_token = ''
count = 0
data = []

def main():
    global count, next_token, error, data
    theTree = None
    file = open("input.txt", "r")
    data = file.read().split()
    count = 0
    theTree = G()
    if not error:
        printTree(theTree)
        value = evaluate(theTree)
        print("The value is", value)
    else:
        print("Input not parsed correctly")

def G():
    global count, next_token, error
    tree = None
    lex()
    print("G -> E")
    tree = E()
    if next_token == '$' and not error:
        print("success")
        return tree
    else:
        print("failure: unconsumed input=%s" % unconsumed_input())
        return None

def E():
    global error
    temp = None
    if error:
        return None
    print("E -> T R")
    temp = T()
    return R(temp)

def R(tree):
    global next_token, error
    temp1, temp2 = None, None
    if error:
        return None
    if next_token == '+':
        print("R -> + T R")
        lex()
        temp1 = T()
        temp2 = R(temp1)
        return Node('+', tree, temp2)
    elif next_token == '-':
        print("R -> - T R")
        lex()
        temp1 = T()
        temp2 = R(temp1)
        return Node('-', tree, temp2)
    else:
        print("R -> e")
        return tree

def T():
    global error
    temp = None
    if error:
        return None
    print("T -> F S")
    temp = F()
    return S(temp)

def S(tree):
    global next_token, error
    temp1, temp2 = None, None
    if error:
        return None
    if next_token == '*':
        print("S -> * F S")
        lex()
        temp1 = F()
        temp2 = S(temp1)
        return Node('*', tree, temp2)
    elif next_token == '/':
        print("S -> / F S")
        lex()
        temp1 = F()
        temp2 = S(temp1)
        return Node('/', tree, temp2)
    else:
        print("S -> e")
        return tree

def F():
    global error
    temp = None
    if error:
        return None
    if next_token == '(':
        print("F -> ( E )")
        lex()
        temp = E()
        if next_token == ')':
            lex()
            return temp
        else:
            error = True
            print("error: unexpected token", next_token)
            print("unconsumed_input", unconsumed_input())
            return None
    elif next_token in ['a', 'b', 'c', 'd']:
        print("F -> M")
        return M()
    elif next_token in ['0', '1', '2', '3']:
        print("F -> N")
        return N()
    else:
        error = True
        print("error: unexpected token", next_token)
        print("unconsumed_input", unconsumed_input())
        return None

def M():
    global next_token, error
    prev_token = next_token
    if error:
        return None
    if next_token in ['a', 'b', 'c', 'd']:
        print("M ->", next_token)
        lex()
        return Node(prev_token, None, None)
    else:
        error = True
        print("error: unexpected token", next_token)
        print("unconsumed_input", unconsumed_input())
        return None

def N():
    global next_token, error
    prev_token = next_token
    if error:
        return None
    if next_token in ['0', '1', '2', '3']:
        print("N ->", next_token)
        lex()
        return Node(prev_token, None, None)
    else:
        error = True
        print("error: unexpected token", next_token)
        print("unconsumed_input", unconsumed_input())
        return None

def lex():
    global count, next_token
    if count < len(data):
        next_token = data[count]
        count += 1
    else:
        next_token = '$'

def unconsumed_input():
    global count, data
    elements = data[count:]
    elementString = " ".join(elements)
    if elementString == "":
        return "$"
    else:
        return elementString

def printTree(tree):
    if tree is None:
        return
    printTree(tree.left_child)
    printTree(tree.right_child)
    print(tree.symbol)


def evaluate(tree):
    if tree is None:
        return -1
    if tree.symbol == 'a':
        return 10
    elif tree.symbol == 'b':
        return 20
    elif tree.symbol == 'c':
        return 30
    elif tree.symbol == 'd':
        return 40
    elif tree.symbol in ['0', '1', '2', '3']:
        return int(tree.symbol)
    elif tree.symbol == '+':
        return evaluate(tree.left_child) + evaluate(tree.right_child)
    elif tree.symbol == '-':
        return evaluate(tree.left_child) - evaluate(tree.right_child)
    elif tree.symbol == '*':
        return evaluate(tree.left_child) * evaluate(tree.right_child)
    elif tree.symbol == '/':
        return evaluate(tree.left_child) / evaluate(tree.right_child)

main()
