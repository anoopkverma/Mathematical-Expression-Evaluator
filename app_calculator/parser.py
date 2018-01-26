"""
Parser class to check syntax of the expression

Here, recursive descent parser is used to parse the mathematical expression.

Recursive descent is a simple parsing algorithm that is very easy to implement.
It is a top-down parsing algorithm because it builds the parse tree from the
top (the start symbol) down.

Expression grammar used:

S => E
E => T | E + T | E - T
T => F | T * F | T / F
F => 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | (a-z) | (A-Z)
[ S, E, T, and F are nonterminal symbols, and (a-z)|(A-Z), and the digits 0-9
 are terminal symbols.
 S = Statement
 E = Expression
 T = Term
 F = Factor
 ]

Unfortunately, this grammar is not suitable for parsing by recursive descent,
because it uses left recursion.

After eliminating the left recursion, we get following grammer,

E => T E'
E' => + T E'
E' => - T E'
E' => null
T => F T'
T' => * F T'
T' => / F T'
T' => null
F => digits | (non-digits)

The names used in following parser corresponding to above symbols,

E = exp
E' = _exp
T = term
T' = _term
F = factor

The above grammer is implemented in following parser.

"""

class Parser:
    def __init__(self, token, look):
        self.tokens = token
        self.look = look
        self.length = len(self.tokens)

    def check(self):
        if self.look == len(self.tokens):
            return "success"
        else:
            return "fail"

    def match(self):
        self.look = self.look+1

    def beginparse(self):
        self.exp()

    def exp(self):
        self.term()
        self._exp()

    def _exp(self):
        if (self.look < self.length and (self.tokens[self.look] == '+'
                or self.tokens[self.look] == '-')):
            self.match()
            self.term()
            self._exp()
        else:
            return

    def term(self):
        self.factor()
        self._term()

    def _term(self):
        if (self.look < self.length and (self.tokens[self.look] == '*'
                or self.tokens[self.look] == '/')):
            self.match()
            self.factor()
            self._term()
        else:
            return

    def factor(self):
        if self.look < self.length and self.tokens[self.look] == '(':
            self.match()
            self.exp()
            if self.look < self.length and self.tokens[self.look] == ')':
                self.match()
            else:
                self.look = 100000000
        else:
            self.match()

"""End of Parser class"""
