import os

import openai
import pygetwindow as gw
from colorama import init

from game_state import GameState
from gui_analyzer import GUIAnalyzer
from hero_hand_range import PokerHandRangeDetector
from hero_info import HeroInfo
from player_analyzer import PlayerAnalyzer
from poker_analyzer_assistant import PokerAnalyzerAssistant
from read_poker_table_dynamic import ReadPokerTableDynamic


def main():
    # Ask the user for the hero player number (1-9, starting from bottom(1))
    while True:
        try:
            hero_player_number = int(input("Enter hero player number (1-9): "))
            if 1 <= hero_player_number <= 9:
                break
            else:
                print("Invalid number. Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Ask for maximum number of players at the table
    while True:
        try:
            max_players = int(input("Enter maximum number of players at table (2-9): "))
            if 2 <= max_players <= 9:
                break
            else:
                print("Invalid number. Please enter a number between 2 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    api_key = os.getenv("OPENAI_API_KEY")
    openai_client = openai.OpenAI(api_key=api_key)
    poker_window = locate_poker_window()
    init(autoreset=True)

    # Initialize all the instances
    if poker_window is not None:
        hero_info = HeroInfo()
        hero_hand_range = PokerHandRangeDetector()

        # Create game state without audio
        game_state = GameState(None)
        poker_assistant = PokerAnalyzerAssistant(openai_client, hero_info, game_state)

        # Initialize player analyzer for tracking opponent tendencies
        player_analyzer = PlayerAnalyzer()

        gui = GUIAnalyzer(game_state, poker_assistant, player_analyzer)
        read_poker_table = ReadPokerTableDynamic(
            poker_window,
            hero_info,
            hero_hand_range,
            poker_assistant,
            game_state,
            player_analyzer,
            max_players,
        )

        setup_read_poker_table(read_poker_table=read_poker_table)

        # Update hero player number in game state
        game_state.update_player(hero_player_number, hero=True)
        game_state.hero_player_number = hero_player_number
        game_state.extract_blinds_from_title()

        # Start the GUI
        gui.run()


def locate_poker_window():
    """Locate the poker client window."""
    windows = gw.getWindowsWithTitle("No Limit")

    for window in windows:
        if "USD" in window.title or "Money" in window.title:
            print(f"Poker client window found. Size: {window.width}x{window.height}")
            default_width = 963
            default_height = 692
            resize_poker_window(window, default_width, default_height)
            return window

    print(f"Poker client window NOT Found.")
    return None


def resize_poker_window(window, width, height):
    """Resize the poker client window to the specified width and height."""
    window.resizeTo(width, height)
    print(f"Resized window to: Width={width}, Height={height}")


def setup_read_poker_table(read_poker_table):
    # Start continuous detection of the poker table
    read_poker_table.start_continuous_detection()


if __name__ == "__main__":
    main()

# Run script:
# python poker_analyzer.py
