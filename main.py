from src.view import View
from src.terminal import Terminal

def main():
    view = View()
    terminal = Terminal(view)
    view.window.mainloop()

main()