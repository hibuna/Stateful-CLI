class ANSI:
    Reset       = "\u001b[0m"
    
    class Cursor:
        _base    = "\u001b[{n}"
        up      = lambda n: ANSI.Cursor._base.replace("{n}", str(n)) + "A"
        down    = lambda n: ANSI.Cursor._base.replace("{n}", str(n)) + "B"
        right   = lambda n: ANSI.Cursor._base.replace("{n}", str(n)) + "C"
        left    = lambda n: ANSI.Cursor._base.replace("{n}", str(n)) + "D"
        pos     = lambda n: ANSI.Cursor._base.replace("{n}", str(n)) + "G"
        save    = "\u001b[{s}"
        load    = "\u001b[{u}"

    class Clear:
        class Screen:
            cur_to_end      = "\u001b[0J"
            cur_to_start    = "\u001b[1J"
            all_            = "\u001b[2J"
        class Line:
            cur_to_end      = "\u001b[0K"
            cur_to_start    = "\u001b[1K"
            all_            = "\u001b[2K"

    class Text:
        bold        = "\u001b[1m"
        underline   = "\u001b[4m"
        reversed_    = "\u001b[7m"

        def colored(str_: str, color: str, bright=False):
            if color not in ANSI.Text.Color.__dict__:
                raise Exception(f"Color {color} doesn't exist")
            if bright:
                color = ANSI.Text.Color.Bright.__dict__.get(color)
            else:
                color = ANSI.Text.Color.__dict__.get(color)
            return color + str_ + ANSI.Reset

        class Color:
            black   = "\u001b[30m"
            red     = "\u001b[31m"
            green   = "\u001b[32m"
            yellow  = "\u001b[33m"
            blue    = "\u001b[34m"
            magenta = "\u001b[35m"
            cyan    = "\u001b[36m"
            white   = "\u001b[37m"
            class Bright:
                black   = "\u001b[30;1m"
                red     = "\u001b[31;1m"
                green   = "\u001b[32;1m"
                yellow  = "\u001b[33;1m"
                blue    = "\u001b[34;1m"
                magenta = "\u001b[35;1m"
                cyan    = "\u001b[36;1m"
                white   = "\u001b[37;1m"

    class BG:
        class Color:
            black   = "\u001b[40m"
            red     = "\u001b[41m"
            green   = "\u001b[42m"
            yellow  = "\u001b[43m"
            blue    = "\u001b[44m"
            magenta = "\u001b[45m"
            cyan    = "\u001b[46m"
            white   = "\u001b[47m"
            class Bright:
                black   = "\u001b[40m;1m"
                red     = "\u001b[41m;1m"
                green   = "\u001b[42m;1m"
                yellow  = "\u001b[43m;1m"
                blue    = "\u001b[44m;1m"
                magenta = "\u001b[45m;1m"
                cyan    = "\u001b[46m;1m"
                white   = "\u001b[47m;1m"


class KEYS:
    RETURN      = b'\x0D'
    BACKSPACE   = b'\x08'
    DELETE      = b'S'

    SPECIAL     = b'\xe0'
    ARROW_L     = b'K'
    ARROW_U     = b'H'
    ARROW_R     = b'M'
    ARROW_D     = b'P'