from rply import LexerGenerator, ParserGenerator
from ast import literal_eval
import sys

LG = LexerGenerator()
LG.ignore(r"\s+")
LG.add("LPARAN", r"\(")
LG.add("RPARAN", r"\)")
LG.add("*", r"\*")
LG.add("/", r"\/")
LG.add("+", r"\+")
LG.add("-", r"\-")
LG.add("^", r"\^")
LG.add("num", r"(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
LG.ignore(r"\s+")

SYMBOLS = ['*', '/', '+', '-', '^', 'num', 'LPARAN', 'RPARAN']
PRECEDENCE = [('left', ['+', '-']),
              ('left', ['*', '/']),
              ('right', ['^'])]

LEXER = LG.build()
PG = ParserGenerator(SYMBOLS, PRECEDENCE)

@PG.production('exp : num')
def num(e):
  if(type(literal_eval(e[0].value)) is int):
    return int(e[0].value)
  elif(type(literal_eval(e[0].value)) is float):
    return float(e[0].value)

@PG.production('exp : LPARAN exp RPARAN')
def exp_paran(e):
  return e[1]

@PG.production('exp : exp + exp')
@PG.production('exp : exp - exp')
@PG.production('exp : exp / exp')
@PG.production('exp : exp * exp')
@PG.production('exp : exp ^ exp')
def arith(e):
  left_token = e[0]
  op_token = e[1]
  right_token = e[2]
  if op_token.gettokentype() == '+':
    return left_token + right_token
  if op_token.gettokentype() == '-':
    return left_token - right_token
  if op_token.gettokentype() == '/':
    return left_token / right_token
  if op_token.gettokentype() == '*':
    return left_token * right_token
  if op_token.gettokentype() == '^':
    return left_token ** right_token

PARSER = PG.build()

# Comment these lines to test out sample expressions
input = sys.stdin.readline()
print(PARSER.parse(LEXER.lex(input)))

# Remove comment for this line to test out sample expressions
# print(PARSER.parse(LEXER.lex("2 + 2")))
# print(PARSER.parse(LEXER.lex("2 + 2 / 2")))
# print(PARSER.parse(LEXER.lex("2.")))
# print(PARSER.parse(LEXER.lex("2. - .33")))
# print(PARSER.parse(LEXER.lex("2 + (2 / 2^2) - 2")))
# print(PARSER.parse(LEXER.lex("2 + (2 / 2.0^2) - 2.2")))
# print(PARSER.parse(LEXER.lex("2 + (2 / 2.0^2) - 2.2")))
