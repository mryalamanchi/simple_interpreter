from rply import LexerGenerator, ParserGenerator
from ast import literal_eval
import sys

LG = LexerGenerator()
LG.ignore(r"\s+")

'''
For some weird reason adding double increment and decrement ops
before add and sub ops, makes it work
'''
LG.add("di", r"\+\+")
LG.add("dd", r"\-\-")

LG.add("LPARAN", r"\(")
LG.add("RPARAN", r"\)")
LG.add("*", r"\*")
LG.add("/", r"\/")
LG.add("+", r"\+")
LG.add("-", r"\-")
LG.add("^", r"\^")
LG.add("%", r"\%")
LG.add("geq", r"\>\=")
LG.add("leq", r"\<\=")
LG.add("gt", r"\>")
LG.add("lt", r"\<")
LG.add("eq", r"\=\=")
LG.add("neq", r"\!\=")
LG.add("and", r"\&\&")
LG.add("neq", r"\|\|")
LG.add("bitneg", r"\~")
LG.add("bitand", r"\&")
LG.add("bitor", r"\|")
LG.add("num", r"(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
LG.ignore(r"\s+")

SYMBOLS = ['di', 'dd', '*', '/', '+', '-', 'geq', 'leq', 'neq', 'gt', 'lt', 'eq', 'and', 'or', 'bitand', 'bitor', 'bitneg', '^', '%', 'num', 'LPARAN', 'RPARAN']
PRECEDENCE = [('left', ['+', '-']),
              ('left', ['*', '/']),
              ('left', ['di', 'dd']),
              ('right', ['%']),
              ('right', ['^']),
              ('left', ['geq']),
              ('left', ['leq']),
              ('left', ['neq']),
              ('left', ['gt']),
              ('left', ['lt']),
              ('left', ['eq']),
              ('left', ['and']),
              ('left', ['or']),
              ('left', ['bitand']),
              ('left', ['bitor']),
              ('left', ['bitneg'])]

LEXER = LG.build()
PG = ParserGenerator(SYMBOLS, PRECEDENCE)

# When the input is empty
@PG.production('exp :')
def empty(e):
  pass

@PG.production('exp : num')
def num(e):
  if(type(literal_eval(e[0].value)) is int):
    return int(e[0].value)
  elif(type(literal_eval(e[0].value)) is float):
    return float(e[0].value)

@PG.production('exp : + exp')
@PG.production('exp : - exp')
def num_neg(e):
  if e[0].gettokentype() == "+":
    return e[1]
  elif e[0].gettokentype() == "-":
    return -e[1]

@PG.production('exp : bitneg num')
def num_bit_neg(e):
  if(type(literal_eval(e[1].value)) is int):
    return (~int(e[1].value))

@PG.production('exp : di exp')
@PG.production('exp : dd exp')
def num_pre(e):
  if e[0].gettokentype() == "di":
    return e[1] + 1
  elif e[0].gettokentype() == "dd":
    return e[1] - 1

@PG.production('exp : LPARAN exp RPARAN')
def exp_paran(e):
  return e[1]

@PG.production('exp : exp + exp')
@PG.production('exp : exp - exp')
@PG.production('exp : exp / exp')
@PG.production('exp : exp * exp')
@PG.production('exp : exp ^ exp')
@PG.production('exp : exp % exp')
@PG.production('exp : exp geq exp')
@PG.production('exp : exp leq exp')
@PG.production('exp : exp neq exp')
@PG.production('exp : exp gt exp')
@PG.production('exp : exp lt exp')
@PG.production('exp : exp eq exp')
@PG.production('exp : exp and exp')
@PG.production('exp : exp or exp')
@PG.production('exp : exp bitand exp')
@PG.production('exp : exp bitor exp')
def arith(e):
  left_token = e[0]
  op_token = e[1]
  right_token = e[2]

  #print(left_token, op_token, right_token)
  if op_token.gettokentype() == '+':
    return left_token + right_token
  elif op_token.gettokentype() == '-':
    return left_token - right_token
  elif op_token.gettokentype() == '/':
    return left_token / right_token
  elif op_token.gettokentype() == '*':
    return left_token * right_token
  elif op_token.gettokentype() == '^':
    return left_token ** right_token
  elif op_token.gettokentype() == '%':
    return left_token % right_token
  elif op_token.gettokentype() == "geq":
    return left_token >= right_token
  elif op_token.gettokentype() == "leq":
    return left_token <= right_token
  elif op_token.gettokentype() == "gt":
    return left_token > right_token
  elif op_token.gettokentype() == "lt":
    return left_token < right_token
  elif op_token.gettokentype() == "eq":
    return left_token == right_token
  elif op_token.gettokentype() == "neq":
    return left_token != right_token
  elif op_token.gettokentype() == "and":
    return left_token and right_token
  elif op_token.gettokentype() == "or":
    return left_token or right_token
  elif op_token.gettokentype() == "bitand":
    return left_token & right_token
  elif op_token.gettokentype() == "bitor":
    return left_token | right_token

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
# print(PARSER.parse(LEXER.lex("2 <= (2 - 2.2)")))
