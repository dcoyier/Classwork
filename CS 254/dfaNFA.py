# Dashiell Coyier HW D04
# Starter code from Carleton College CS 254 w26, taught by Josh Davis


### Sets ###

# This Python program makes heavy use of the frozenset class. A frozenset
# object is an immutable set object. A set object is the Python representation
# of a mathematical set. The only gotcha is that the elements of a set must be
# hashable (meaning, essentially, fairly simple). The following two functions
# could be methods of a frozenset subclass, but let's just leave them as
# functions.


def setProduct(a, b):
    """a and b are frozensets. Returns the Cartesian product a x b as a frozenset."""
    return frozenset([(x, y) for x in a for y in b])


def setPower(a):
    """a is a frozenset. Returns the power set as a frozenset."""
    if len(a) == 0:
        return frozenset([frozenset()])
    else:
        # Separate a specific (but arbitrary) element from the set.
        aSet = set(a)
        singleton = frozenset([aSet.pop()])
        # Half of the subsets do not contain the specific element.
        half = setPower(frozenset(aSet))
        # The other half of the subsets do contain the specific element.
        other = frozenset([singleton.union(subset) for subset in half])
        return half.union(other)


### DFAs ###


class dfa(object):
    """An object of this class is a DFA M = (Q, Sigma, q0, F, delta). To make the code clearer, we write the DFA as M = (states, alphabet, start, finals, transition)."""

    def __init__(self, states, alphabet, start, finals, transition):
        """states, alphabet, and finals are frozensets. start is an element of states, and finals is a subset of states. transition is a Python function that takes two inputs --- one from states and one from alphabet --- and produces as output an element of states."""
        self.states = states
        self.alphabet = alphabet
        self.start = start
        self.finals = finals
        self.transition = transition

    def accepts(self, string):
        """string is a string of characters, which are assumed to be a valid input to the DFA. Returns True or False indicating whether the DFA accepts the string."""
        current = self.start
        while len(string) > 0:
            current = self.transition(current, string[0])
            string = string[1:]
        if current in self.finals:
            return True

        return False

    def intersection(self, other):
        """other is a DFA, assumed to have the same alphabet as self. Returns a DFA whose language is the intersection of self's language and other's language."""
        new_states = setProduct(self.states, other.states)
        new_alphabet = self.alphabet.union(other.alphabet)
        new_start = (self.start, other.start)
        new_finals = setProduct(self.finals, other.finals)

        def new_transition(state, a):
            positionA = self.transition(state[0], a)
            positionB = other.transition(state[1], a)
            return (positionA, positionB)

        return dfa(new_states, new_alphabet, new_start, new_finals, new_transition)


def dfaThree():
    """Returns a DFA for bit strings with number of 0s divisible by three."""

    def transition(q, a):
        if a == "1":
            return q
        elif q == "0":
            return "1"
        elif q == "1":
            return "2"
        else:
            return "0"

    return dfa(frozenset("012"), frozenset("01"), "0", frozenset("0"), transition)


def dfaTwo():
    """Returns a DFA for bit strings with number of 0s divisible by two."""

    def transition(q, a):
        if a == "1":
            return q
        elif q == "0":
            return "1"
        elif q == "1":
            return "0"

    return dfa(frozenset("01"), frozenset("01"), "0", frozenset("0"), transition)


### NFAs ###


class nfa(object):
    """An object of this class is a NFA-without-epsilon-transitions N = (Q, Sigma, q0, F, delta). To make the code clearer, we write the NFA as N = (states, alphabet, start, finals, transition)."""

    def __init__(self, states, alphabet, start, finals, transition):
        """states, alphabet, and finals are frozensets. start is an element of states, and finals is a subset of states. transition is a Python function that takes two inputs --- one from states and one from alphabet --- and produces as output a subset of states (as a frozenset)."""
        self.states = states
        self.alphabet = alphabet
        self.start = start
        self.finals = finals
        self.transition = transition

    def dfa(self):
        """Returns a DFA whose language equals that of self."""
        new_states = setPower(self.states)
        new_alphabet = self.alphabet
        new_start = frozenset(self.start)

        new_finals = set()
        for new_state in new_states:
            for final in self.finals:
                if final in new_state and new_state not in new_finals:
                    new_finals.add(new_state)
        new_finals = frozenset(new_finals)

        def new_transition(states, a):
            next_states = set()
            for state in states:
                next_states_from_state = self.transition(state, a)
                for next_state_from_state in next_states_from_state:
                    if next_state_from_state not in next_states:
                        next_states.add(next_state_from_state)
            return frozenset(next_states)

        new_dfa = dfa(new_states, new_alphabet, new_start, new_finals, new_transition)
        return new_dfa


def nfaPenultimate():
    """Returns an NFA for bit strings of length >= 2 whose second-to-last symbol is 1."""

    def transition(q, a):
        if q == "a":
            if a == "0":
                return frozenset("a")
            else:
                return frozenset("ab")
        elif q == "b":
            return frozenset("c")
        else:
            return frozenset()

    return nfa(frozenset("abc"), frozenset("01"), "a", frozenset("c"), transition)


### Main ###


# Runs five tests.
def main():
    strings = ["", "0", "000", "000000", "010", "11", "0111001111"]
    print("First test: strings with 0s divisible by three...")
    m = dfaThree()
    for string in strings:
        print(string, m.accepts(string))
    print("Second test: strings with 0s divisible by two...")
    n = dfaTwo()
    for string in strings:
        print(string, n.accepts(string))
    print("Third test: strings with 0s divisible by two and three...")
    p = m.intersection(n)
    for string in strings:
        print(string, p.accepts(string))
    print("Fourth test: strings with penultimate 1...")
    o = nfaPenultimate().dfa()
    for string in strings:
        print(string, o.accepts(string))
    print("Fifth test: strings with 0s divisible by three and penultimate 1...")
    p = m.intersection(o)
    for string in strings:
        print(string, p.accepts(string))


# If the user imports this file as a module into another program, then don't
# run main(). If the user runs this file directly, then do run main().
if __name__ == "__main__":
    main()
