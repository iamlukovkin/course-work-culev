from src.main.console_menu import *


def application() -> None:
    is_continue: bool = True
    start_print()
    while is_continue:
        print(get_actions())
        action: int = get_next_action()
        is_continue = determine_action(action)
    return exit_app()
