from . import grep

def selector(prompt, choices):
    from pyutil.termctl import Terminal


    terminal = Terminal()
    terminal.set_raw()
    terminal.hide_cursor()

    buffer = ""
    lines_written = 0
    selected = 0
    try:
        while True:
            lines_written = 0

            terminal.write(prompt + " " + buffer, True, True)

            terminal.write("\n")
            lines_written += 1
            valid_choices = choices | grep(buffer, i=True)

            selected = int(len(valid_choices)/2) if len(valid_choices)<5 else 2

            """
            Something with index of selected, that as pivot point
            when hit arrow key
            shift index aka pivot (selected -= 1 and then index of previous - 1 or something)
            """

            for choice in valid_choices:
                if lines_written >= 6:
                    break

                m=f"  {choice}"
                if lines_written-1 == selected:
                    m=f"> {choice}"
                terminal.write(m, True, True, True)
                lines_written += 1


            char = terminal.read(1)
            if char == terminal.K_UP:
                selected -= 1
            if char == terminal.K_DOWN:
                selected += 1
            
            if char in terminal.TERMINATOR:
                terminal.move_cursor(lines_written, terminal.C_UP)
                for _ in range(lines_written): terminal.write("", True, True, True)
                terminal.move_cursor(lines_written, terminal.C_UP)
                terminal.write(valid_choices[selected], True, True, True)
                break
            elif char in terminal.BACKSPACE:
                if len(buffer) > 1:
                    buffer = buffer[:-1]
                else:
                    buffer = ""
            elif char.isprintable():
                buffer += char
            
            
            terminal.move_cursor(lines_written, terminal.C_UP)
            for _ in range(lines_written): terminal.write("", True, True, True)
            terminal.move_cursor(lines_written, terminal.C_UP)

    except KeyboardInterrupt:
        terminal.move_cursor(lines_written, terminal.C_UP)
        for _ in range(lines_written): terminal.write("", True, True, True)
        terminal.move_cursor(lines_written, terminal.C_UP)

        return None

    finally:
        terminal.reset()

    return valid_choices[selected]