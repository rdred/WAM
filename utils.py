"""Utility functions used in sibling scripts"""
from colorama import Fore, Style


def print_color(string, color):
    """Determine the Fore.color and print the string in that color."""
    color_code = getattr(Fore, color, Fore.RESET)
    reset_code = Style.RESET_ALL
    print(color_code + string + reset_code)


def input_color(prompt, color):
    """Determine the Fore.color and get the user's input in that color."""
    color_code = getattr(Fore, color, Fore.RESET)
    reset_code = Style.RESET_ALL
    user_input = input(color_code + prompt + reset_code)
    return user_input
