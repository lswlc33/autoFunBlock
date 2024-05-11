import os


def pTitle(str):
    title = f" {str} "
    terminal_width = os.get_terminal_size().columns
    terminal_width -= len(title) + 2
    centered_title = title.center(terminal_width, '-')
    return(centered_title)


def cleanT():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
