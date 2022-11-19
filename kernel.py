import sys, msvcrt
from typing import Callable, Optional, List, Tuple

from static import ANSI, KEYS

class CLI:

    class Line:
        def __init__(self, state: List[str]=None):
            self.state: List[str] = [CLI.DEFAULT_PREFIX] or state
            self.chars: List[str] = [' ']
            self.cursor: int = 1
            self.string: Callable[[None], str] = lambda: ''.join(self.chars[:-1])
        
        def length(self) -> int:
            return len(self.string())
        
        def start_of_line(self) -> bool:
            return self.cursor == 1

        def end_of_line(self) -> bool:
            return self.cursor == self.length - 1

        def insert(self, char: str) -> None:
            self.chars.insert(self.cursor - 1, char)
            self.cursor += 1

        def backspace(self) -> None:
            if not self.start_of_line():
                self.chars.pop(self.cursor - 1)
                self.cursor -= 1

        def delete(self) -> None:
            if not self.end_of_line():
                self.chars.pop(self.cursor)

        def string_empty(self) -> bool:
            if self.length == 0:
                return True
            for char in self.string():
                if char != ' ':
                    return False
            return True

    class Printer:
        DEFAULT_SEP: str = ">"

        def __init__(self, cli: 'CLI', sep: str=None) -> None:
            self.sep: str = sep or CLI.Printer.DEFAULT_SEP
            self.cli: CLI = cli

        def title(self, flush: bool=True) -> None:
            sys.stdout.write(f' {self.sep} '.join(self.cli.state))
            if flush:
                self.flush()

        def prefix(self, flush: bool=True) -> None:
            sys.stdout.write(f'{self.sep} ')
            if flush:
                self.flush()

        def line(self, flush: bool=True) -> None:
            sys.stdout.write(self.cli.current.string())
            if flush:
                self.flush()

        def clear_line(self, flush: bool=True) -> None:
            # ANSI clear line command not working, workaround: print whitespace
            self.cursor(0)
            for _ in range(self.cli.current.length()):
                sys.stdout.write(' ')
            self.cursor(0)
            if flush:
                self.flush()

        def new_line(self, flush: bool=True) -> None:
            sys.stdout.write('\n')
            if flush:
                self.flush()

        def cursor(self, int_: int, fix_index: bool=True, flush: bool=True) -> None:
            if fix_index:
                int_ += 1
            sys.stdout.write(ANSI.Cursor.pos(int_))
            if flush:
                self.flush()

        def flush(self) -> None:
            sys.stdout.flush()

    DEFAULT_SIGIL: str = "-"
    DEFAULT_PREFIX: str = "CCLI"
    DEFAULT_SEPARATOR: str = ">"
    DEFAULT_MAX_HISTORY: int = 50

    def __init__(self, name: str=None, sep: str=None, max_history: int=None):
        self.sep: str = CLI.DEFAULT_SEPARATOR or sep
        self.max_history: int = max_history or self.DEFAULT_MAX_HISTORY 
        self.name: str = name or CLI.DEFAULT_PREFIX
        self.state: List[str] = [self.name]
        self.history: List[CLI.Line] = []
        self.out: CLI.Printer = CLI.Printer(self)
        self.current: CLI.Line
        
    def loop(self):
        while 1:
            self.prompt = self.new_prompt()
            # TODO: parse args, kwargs
                
    def new_prompt(self) -> str:

        self.out.title()
        self.out.new_line()

        self.history.insert(0, CLI.Line(self.state))
        self.current = self.history[0]

        while 1:

            self.out.clear_line()
            self.out.cursor(0)
            self.out.prefix()
            self.out.line()

            key_press = self.get_key()

            match(key_press):
                
                case KEYS.ARROW_L:
                    if not self.current.start_of_line():
                        self.current.cursor -= 1
                    continue

                case KEYS.ARROW_R:
                    if not self.current.end_of_line():
                        self.current.cursor += 1
                    continue

                case KEYS.ARROW_D:
                    if self.history.index(self.current):
                        self.current = self.history[self.history.index(self.current) - 1]
                    continue

                case KEYS.ARROW_U:
                    if self.history.index(self.current) < len(self.history) - 1:
                        self.current = self.history[self.history.index(self.current) + 1]
                    continue

                case KEYS.BACKSPACE:
                    if not self.current.start_of_line:
                        self.current.chars.pop(self.current.cursor - 1)
                    continue

                case KEYS.DELETE:
                    if not self.current.end_of_line():
                        self.current.chars.pop(self.current.cursor)
                    continue

                case KEYS.RETURN:
                    self.out.clear_line()
                    # TODO: implement cfg option to save command stubs instead of removing
                    # if current not newest line or newest line empty, remove newest line
                    if self.history.index(self.current) > 0 or self.current.string_empty():
                        self.history.pop(0)
                    break

            # else type key if ascii
            if str(key_press, 'utf-8').isascii():
                self.current.insert(str(key_press, 'utf-8'))
                continue

    def get_key(self):
        key = msvcrt.getch()
        if key == KEYS.SPECIAL:
            return msvcrt.getch()
        return key
    
cli = CLI()
cli.loop()