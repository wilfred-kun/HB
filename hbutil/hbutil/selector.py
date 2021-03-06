#!/usr/bin/python3

from hbutil import grep
from hbutil.termctl import Terminal, CTLSEQ, COLORS
from sys import stderr as STDERR


def selector(prompt, choices):
    """
    Allows the user to choose from a list of options

    prompt -> str
    choices -> [str]

    Returns a string which contains the choice, and
    corresponds to an entry in `choices`.
    
    Ctrl+C (KeyboardInterrupt) kills the function
    Returns `None`
    """
    
    terminal = Terminal(of=STDERR)
    terminal.set_raw()
    terminal.hide_cursor()

    buffer = ""
    scroll = lines_written = selected = 0
    try:
        while True:
            lines_written = 0

            if len(buffer):
                terminal.write(prompt + " " + buffer, True, True)
            else:
                terminal.write(prompt + COLORS.BBLACK + " (Start typing to search)" + COLORS.END, True, True)

            terminal.write("\n")
            lines_written += 1
            valid_choices = choices | grep(buffer, i=True)
            vc_length = len(valid_choices)
            
            # Scrolling through the list
            scroll = vc_length if vc_length==0 else scroll % vc_length
            valid_choices = valid_choices[scroll:] + valid_choices[:scroll]

            """
            Something with index of selected, that as pivot point
            when hit arrow key
            shift index aka pivot (selected -= 1 and then index of previous - 1 or something)
            """

            selected = int(vc_length/2) if vc_length<5 else 2
            
            for choice in valid_choices:
                if lines_written >= 6:
                    break

                m=f"  {choice}"
                if lines_written-1 == selected:
                    m=f"{COLORS.BOLD}{COLORS.BBLUE}>{COLORS.END} {choice}"
                terminal.write(m, True, True, True)
                lines_written += 1


            char = terminal.read(1)
            if char == CTLSEQ.K_UP:
                scroll -= 1
            if char == CTLSEQ.K_DOWN:
                scroll += 1

            
            if char in CTLSEQ.TERMINATOR:
                if len(valid_choices) > 0:
                    terminal.move_cursor(lines_written, CTLSEQ.C_UP)
                    for _ in range(lines_written): terminal.write("", True, True, True)
                    terminal.move_cursor(lines_written, CTLSEQ.C_UP)
                    terminal.write(valid_choices[selected], True, True, True)
                    break
            elif char in CTLSEQ.BACKSPACE:
                if len(buffer) > 1:
                    buffer = buffer[:-1]
                else:
                    buffer = ""
            elif char.isprintable():
                buffer += char
            
            
            terminal.move_cursor(lines_written, CTLSEQ.C_UP)
            for _ in range(lines_written): terminal.write("", True, True, True)
            terminal.move_cursor(lines_written, CTLSEQ.C_UP)

    except KeyboardInterrupt:
        terminal.move_cursor(lines_written, CTLSEQ.C_UP)
        for _ in range(lines_written): terminal.write("", True, True, True)
        terminal.move_cursor(lines_written, CTLSEQ.C_UP)

        return None

    finally:
        terminal.reset()

    return valid_choices[selected]


def main():
    import sys

    if len(sys.argv) < 3:
        print("Not enough arguments")
        exit(1)
    prompt = sys.argv[1]
    options = sys.argv[2:]


    result = selector(prompt, options)
    if not result: return 1

    print(result)
    return 0

if __name__ == '__main__':
    main()
