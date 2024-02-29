import argparse
from pylox.lox import Lox

parser = argparse.ArgumentParser(prog='PyLox', description='A lox interpreter written in python.')
parser.add_argument('source', nargs='?', help='Path to the file containing the lox script', type=argparse.FileType('r'))

args = parser.parse_args()
source = args.source

lox = Lox()
if source is None:
    while True:
        try:
            code = input('> ')
            lox.interpret(code)
            lox.clear_errors()
        except KeyboardInterrupt as e:
            break
else:
    lox.interpret(source.read())
    if lox.error: exit(65)
    if lox.runtime_error: exit(70)

