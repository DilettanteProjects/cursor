import sys
import termios
import tty
import re

"""This module makes use of ANSI escape-codes to move the cursor around the 
terminal window(and clear lines) (not diligently tested)

xy(line, column=1):
move cursor to x line, y column

lft(), right(), up(), dwn():
(steps)
self-explanatory

hme():
move cursor home

clm(y):
move cursor to column y

get_pos():
returns cursor position

various erasers:
ercs()  (er)ases from           (c)ursor to end of  (s)creen,
erlc()  (er)ases from start of  (l)ine to           (c)ursor,
erl()   (er)ases the whole      (l)ine,
and so forth.

"""


def hme():
    """Move cursor to 1, 1"""
    print('\x1b[H', end='')
       
def xy(line, column=1):
    """Move cursor to x line, y column, starting at 1"""
    print('\x1b[{};{}H'.format(line, column), end='')
    
def up(steps=1):
    """Move cursor up a number of lines(default 1)""" 
    print(steps * '\x1b[1A', end='')
    
def dwn(steps=1):
    """ Move cursor down a number of lines(default 1)"""
    print(steps * '\x1b[1B', end='')
    
def rgt(steps=1):
    """Move cursor right a number of columns(default 1)"""
    print('\x1b[{}C'.format(steps), end='')
       
def lft(steps=1):
    """Move cursor left a number of columns(default 1)"""
    print('\x1b[{}D'.format(steps), end='')
       
def clm(y):
    """Move cursor to column y"""
    print('\x1b[{}G'.format(y), end='')
      
def ercs():
    """(Er)ase from (c)ursor to end of (s)creen"""
    print('\x1b[0J', end='')
       
def ersc():
    """(Er)ase from beginning of (s)creen to (c)ursor"""
    print('\x1b[1J', end='')
       
def ers():
    """(Er)ase (s)creen"""
    print('\x1b[2J', end='')
    
def ercl():
    """(Er)ase from (c)ursor to end of (l)ine"""
    print('\x1b[0K', end='')
    
def erlc():
    """(Er)ase from start of (l)ine to (c)ursor"""
    print('\x1b[1K', end='')
    
def erl():
    """(Er)ase current (l)ine"""
    print('\x1b[2K', end='')

def get_pos():
    """ Retun current cursor position """
    """ Lifted wholesale from StackOverflow.
    Explanation accompanying the post:
    The problem is that by default stdin is buffered and
    after writing the sequence to stdout,
    the terminal will sent it's response to stdin, 
    rather then to stdout. So the terminal act like pressing the actual keys
    without a return.
    The trick is to use tty.setcbreak(sys.stdin.fileno(), termios.TCSANOW) 
    and before that store the terminal attributes via
    termios.getattr in variable to restore the default behavior.
    With cbreak set, os.read(sys.stdin.fileno(), 1) you can read
    from stdin immediately. This also suppress the ansi controll
    code response from the terminal."""
    
    buf = ""
    stdin = sys.stdin.fileno()
    tattr = termios.tcgetattr(stdin)

    try:
        tty.setcbreak(stdin, termios.TCSANOW)
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()

        while True:
            buf += sys.stdin.read(1)
            if buf[-1] == "R":
                break

    finally:
        termios.tcsetattr(stdin, termios.TCSANOW, tattr)

    # reading the actual values, but what if a keystroke appears while reading
    # from stdin? As dirty work around, getpos() returns if this fails: None
    try:
        matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
        groups = matches.groups()
    except AttributeError:
        return None

    return (int(groups[0]), int(groups[1]))