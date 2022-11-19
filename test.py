from rply import LexerGenerator, ParserGenerator
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
LG.add("num", r"\d+")
LG.add("CR", r"\r")
LG.ignore(r"\s+")

SYMBOLS = ['*', '/', '+', '-', '^', 'num', 'LPARAN', 'RPARAN', 'CR']
PRECEDENCE = [('left', ['+', '-']),
              ('left', ['*', '/']),
              ('right', ['^'])]

LEXER = LG.build()
PG = ParserGenerator(SYMBOLS, PRECEDENCE)

@PG.production('exp : num')
def num(e):
  return int(e[0].value)

@PG.production('exp : LPARAN exp RPARAN')
def exp_paran(e):
  return e[1]

@PG.production('exp : num CR')
def cr(e):
  return e[0]

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

input = "".join(sys.stdin.readline())
PARSER = PG.build()
#print(PARSER.parse(LEXER.lex('1 + 2- 2^2/4')))
#print(PARSER.parse(LEXER.lex('1 + 2- 2^2/2^2')))
print(PARSER.parse(LEXER.lex(input)))
