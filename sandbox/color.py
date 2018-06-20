import sys
from termcolor import colored, cprint

print('print')
sys.stderr.write('Test\n')
print('Error!', file=sys.stderr)
print('Error1!', '111111111111', file=sys.stderr)
print('Success', file=sys.stdout)

text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
print(text)
cprint('Hello, World!', 'green', 'on_red')
