# Interpreter for Super Language, CS 254, winter 2026.
# Dashiell Coyier

# I wrote the scanner and parser, which roughly correspond to regular expressions and pushdown automata. Source code from Josh Davis.


import copy
import re
import sys

### N-ARY TREE ###


class TreeNode(object):
    # Initializes the receiver with the given data.
    def __init__(self, data=None):
        self.setData(data)
        self.children = []

    # Returns the receiver's stored data.
    def getData(self):
        return self.data

    # Sets the receiver's stored data.
    def setData(self, data):
        self.data = data

    # Returns the list of children.
    def getChildren(self):
        return self.children

    # Adds the given node as a child of the receiver.
    def attachChild(self, node):
        self.children.append(node)

    # Returns the string representation of the tree, that is used
    # by print, etc.
    def __str__(self):
        # print(self.data)
        # if len(self.children) != 0:
        #     for i in range(1, len(self.children)):
        #         print(str(self.children[i]))

        if len(self.children) == 0:
            return str(self.data)
        else:
            s = str(self.children[0])
            for i in range(1, len(self.children)):
                s += " " + str(self.children[i])
            return "(" + s + ")"


### SCANNER AND PARSER ###


# Scans a program into the corresponding list of tokens.
# Each token is a left parenthesis (, right parenthesis ),
# '-delimited string literal, or string of non-
# parenthesis, non-', non-white-space characters.
# Input: String.
# Output: List of strings (possibly empty), or None if a
# syntax error has occurred.
def tokenList(program):
    if len(re.findall(r"\'", program)) % 2 == 1:
        return None
    else:
        return re.findall(
            r"\(|\)|\'[\w\s\d\*\(\)\+\-.=<>]+\'|[\w\d\*\+\-.=<>]+", program
        )


# Parses a token list into the corresponding parse tree.
# Input: Non-empty list of strings.
# Output: TreeNode, or None if a syntax error has occurred.
def parseTree(tokens):
    tree = TreeNode()
    parenCount = 0
    parseChild = []
    for token in tokens:
        if token == "(" or parenCount > 0:
            # if open paren, add to count and append only if not outside paren
            if token == "(":
                # if not first paren add to parseChild
                if parenCount != 0:
                    parseChild.append(token)
                # add open parenthesis to the parenCount
                parenCount += 1
            # if closed paren, subtract from count and append only if not outside paren
            elif token == ")":
                parenCount -= 1
                # if not last paren
                if parenCount != 0:
                    parseChild.append(token)
            else:
                # if not a paren then just append it
                parseChild.append(token)
            if parenCount == 0:
                # ERROR
                if len(parseChild) == 0:
                    print("error: syntax: empty parentheses")
                    return None
                # recursive call, parsing each branch
                tree.attachChild(parseTree(parseChild))
                parseChild = []
        else:
            # ERROR
            if token == ")":
                print("error: syntax: cannot start expression with )")
                return None
            # base case, just one elem
            tree.attachChild(TreeNode(token))
    # ERROR
    if parenCount != 0:
        print("error: syntax: uneven number of parentheses")
        return None

    # Check that no errors occurred
    queue = []
    queue.append(tree)
    while True:
        root = queue.pop(0)
        for child in root.getChildren():
            queue.append(child)
            if child == None:
                return None
        if len(queue) == 0:
            break

    # return complete parse tree
    return tree


### EVALUATOR: KEYWORDS ###


# Executes a set, updating environment and returning value.
# Input: List of TreeNodes. Environment dictionary.
# Output: Value (float, string, or function TreeNode) or
# None on error.
def valueOfKeywordSet(args, env):
    try:
        float(args[0].getData())
        print("error: set: cannot assign a value to a numeral")
    except ValueError:
        if len(args) != 2:
            print("error: set: usage is (set <var> <val>)")
            return None
        elif args[0].getData()[0] == "'" and args[0].getData()[-1] == "'":
            print("error: set: cannot assign a value to a string literal")
            return None
        else:
            v = value(args[1], env)
            if v != None:
                env[args[0].getData()] = v
            return v


# Builds a function as indicated by the fun keyword.
# Input: List of TreeNodes. Environment dictionary.
# Output: Value (float, string, or function TreeNode) or None.
def valueOfKeywordFun(args, env):
    if len(args) != 2:
        print("error: fun: usage (fun <vars> <body>)")
        return None
    else:
        node = TreeNode(env)
        node.attachChild(TreeNode("fun"))
        node.attachChild(args[0])
        node.attachChild(args[1])
        return node


# Executes an if-then-else, returning the value of
# whichever branch was taken.
# Input: List of TreeNodes. Environment dictionary.
# Output: Value (float, string, or function TreeNode) or
# None on error.
def valueOfKeywordIf(args, env):
    if len(args) != 3:
        print("error: if: usage (if <test> <then> <else>)")
        return None
    else:
        test = value(args[0], env)
        if test == "'TRUE'":
            return value(args[1], env)
        elif test == "'FALSE'":
            return value(args[2], env)
        elif test == None:
            return None
        else:
            print("error: if: test value", test)
            return None


### EVALUATOR: PRIMITIVES ###


# Tests equality.
# Input: Two numbers or two strings.
# Output: Strings 'TRUE' or 'FALSE', or None on error.
def valueOfPrimitiveEqual(args, env):
    vals = [value(a, env) for a in args]
    if len(args) != 2:
        print("error: =: usage (= <numOrStr> <numOrStr>)")
        return None
    else:
        if type(vals[0]) == float and type(vals[1]) == float:
            if vals[0] == vals[1]:
                return "'TRUE'"
            else:
                return "'FALSE'"
        elif type(vals[0]) == str and type(vals[1]) == str:
            if vals[0] == vals[1]:
                return "'TRUE'"
            else:
                return "'FALSE'"
        else:
            print("error: =: incomparable arguments")
            return None


# Tests whether the first argument is less than the second.
# Strings are compared by shortlex order, so shorter
# strings are always less than longer strings.
# Input: Two numbers or two strings.
# Output: Strings 'TRUE' or 'FALSE', or None on error.
def valueOfPrimitiveLessThan(args, env):
    vals = [value(a, env) for a in args]
    if len(args) != 2:
        print("error: <: usage (= <numOrStr> <numOrStr>)")
        return None
    else:
        if type(vals[0]) == float and type(vals[1]) == float:
            if vals[0] < vals[1]:
                return "'TRUE'"
            else:
                return "'FALSE'"
        elif type(vals[0]) == str and type(vals[1]) == str:
            if len(vals[0]) < len(vals[1]):
                return "'TRUE'"
            elif len(vals[0]) > len(vals[1]):
                return "'FALSE'"
            elif vals[0] < vals[1]:
                return "'TRUE'"
            else:
                return "'FALSE'"
        else:
            print("error: <: incomparable arguments")
            return None


# Returns the sum, as indicated by the + keyword.
# Input: List of TreeNodes. Environment dictionary.
# Output: Value (float or string) or None.
def valueOfPrimitivePlus(args, env):
    vals = [value(a, env) for a in args]
    # sum is either None, a float, or a string without its ''.
    sum = None
    for v in vals:
        if type(v) == float:
            if type(sum) == float:
                sum += v
            elif type(sum) == str:
                sum += str(v)
            else:
                sum = v
        elif type(v) == str:
            if type(sum) == float:
                sum = str(sum) + v[1:-1]
            elif type(sum) == str:
                sum += v[1:-1]
            else:
                sum = v[1:-1]
        else:
            print("error: +: usage (+ <numOrStr> <numOrStr> ...)")
            return None
    if type(sum) == float:
        return sum
    elif type(sum) == str:
        return "'" + sum + "'"
    else:
        # Assume the user meant an empty sum of numbers rather than strings.
        return 0.0


# Returns the product, as indicated by the * keyword.
# Input: List of TreeNodes. Environment dictionary.
# Output: Value (float or string) or None.
def valueOfPrimitiveTimes(args, env):
    vals = [value(a, env) for a in args]
    # product is either None, a float, or a string without its ''.
    product = None
    for v in vals:
        if type(v) == float:
            if type(product) == float:
                product *= v
            elif type(product) == str:
                print("error: *: usage (* <num> ... <num> <numOrStr>)")
                return None
            else:
                product = v
        elif type(v) == str:
            if type(product) == float:
                times = product
                product = ""
                i = 1.0
                while i <= times:
                    product += v[1:-1]
                    i += 1.0
            elif type(product) == str:
                print("error: *: usage (* <num> ... <num> <numOrStr>)")
                return None
            else:
                product = v[1:-1]
        else:
            print("error: *: usage (* <num> ... <num> <numOrStr>)")
            return None
    if type(product) == float:
        return product
    elif type(product) == str:
        return "'" + product + "'"
    else:
        # Assume user meant empty product of numbers rather than of strings.
        return 1.0


### EVALUATOR: CORE ###


# Returns the value of the function applied to its arguments.
# Known bug: Does not always evaluate all arguments (which
# is contrary to the specification).
# Input: TreeNode. List of TreeNodes. Environment dictionary.
# Output: Value (float, string, or function TreeNode) or
# None on error.
def valueOfApplication(f, args, env):
    # A function contains its environment in its root,
    # and it has three children: lambda, args, body.
    children = f.getChildren()
    if len(children) != 3:
        print("error: fun: ill-formed", f)
    else:
        params = children[1].getChildren()
        if len(params) != len(args):
            print("error: application: incorrect number of arguments to", f)
        else:
            # Build the local environment.
            e = {"()": f.getData()}
            for i in range(len(args)):
                # Evaluate each argument in the ambient environment, and
                # add that binding to the local environment.
                v = value(args[i], env)
                if v == None:
                    return None
                else:
                    e[params[i].getData()] = v
            # Evaluate the function body in that environment.
            return value(children[2], e)


# Returns the value corresponding to the token.
# Input: String. Environment.
# Output: Value (float, string, or function TreeNode) or
# None on error.
def valueOfVariable(token, env):
    if token in env:
        return env[token]
    elif "()" in env:
        # Implementation detail: look up value in parent environment.
        return valueOfVariable(token, env["()"])
    else:
        print("error: unknown variable", token)
        return None


# Evaluates the parse tree within the given environment.
# Input: Parse tree for a single expression. Environment.
# Output: Value (float, string, or function TreeNode) or
# None on error.
def value(tree, env):
    children = tree.getChildren()
    if len(children) == 0:
        # The tree is a simple expression: numeral, string, or variable.
        try:
            return float(tree.getData())
        except ValueError:
            if tree.getData()[0] == "'" and tree.getData()[-1] == "'":
                return tree.getData()
            else:
                return valueOfVariable(tree.getData(), env)
    else:
        # The tree is a compound expression. First handle keywords.
        head = value(children[0], env)
        if head == "set":
            return valueOfKeywordSet(children[1:], env)
        elif head == "fun":
            return valueOfKeywordFun(children[1:], env)
        elif head == "if":
            return valueOfKeywordIf(children[1:], env)
        else:
            # The tree is a function application. We could evaluate
            # the arguments right now, but we delay that slightly.
            if head == "+":
                return valueOfPrimitivePlus(children[1:], env)
            elif head == "*":
                return valueOfPrimitiveTimes(children[1:], env)
            elif head == "=":
                return valueOfPrimitiveEqual(children[1:], env)
            elif head == "<":
                return valueOfPrimitiveLessThan(children[1:], env)
            elif isinstance(head, TreeNode):
                return valueOfApplication(head, children[1:], env)
            else:
                # A compound expression can't begin with a float or string.
                if type(head) == float:
                    print("error: application: number", head)
                elif type(head) == str and head[0] == "'" and head[-1] == "'":
                    print("error: application: string", head)
                return None


### USER INTERFACE ###


# Runs the interpreter until the user presses Control-D.
# Input: None.
# Output: None.
def main():
    environment = {
        "set": "set",
        "fun": "fun",
        "if": "if",
        "+": "+",
        "*": "*",
        "=": "=",
        "<": "<",
    }
    print("Welcome to Super Language. Press Control-D to exit.")
    while True:
        try:
            program = input(":> ")
            tokens = tokenList(program)
            if tokens != None and len(tokens) >= 1:
                tree = parseTree(tokens)
                if tree != None:
                    for expression in tree.getChildren():
                        v = value(expression, environment)
                        if v != None:
                            print(v)
            else:
                print("error: syntax: does not conform to regex")
        except EOFError:
            print()
            sys.exit()


# If the user ran (rather than imported) this file, then run main.
if __name__ == "__main__":
    main()
