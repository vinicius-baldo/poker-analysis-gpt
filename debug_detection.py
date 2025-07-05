#!/usr/bin/env python3
"""
Real-time Hand Detection Debugging Script

This script provides real-time monitoring of hand detection for debugging purposes.
It can be run alongside the main PokerGPT application to see what's being detected.
"""

import json
import os
import sys
import time
from datetime import datetime

from colorama import Fore, init

# Initialize colorama for colored output
init(autoreset=True)

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_state import GameState
from hand_strength_analyzer import HandStrengthAnalyzer


class DetectionDebugger:
    def __init__(self):
        self.game_state = GameState()
        self.hand_analyzer = HandStrengthAnalyzer()
        self.last_hero_cards = None
        self.last_community_cards = None
        self.last_board_stage = None
        self.debug_log = []

    def monitor_detection(self, duration=60, interval=1):
        """Monitor hand detection in real-time"""
        print(f"{Fore.CYAN}=== Real-Time Detection Monitor ===\n")
        print(f"Monitoring for {duration} seconds (checking every {interval}s)")
        print("Press Ctrl+C to stop early\n")

        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                current_time = time.time() - start_time

                # Get current detection state
                hero_cards = self.get_hero_cards()
                community_cards = self.game_state.community_cards
                board_stage = self.game_state.current_board_stage

                # Check for changes
                hero_changed = hero_cards != self.last_hero_cards
                community_changed = community_cards != self.last_community_cards
                stage_changed = board_stage != self.last_board_stage

                if hero_changed or community_changed or stage_changed:
                    print(f"\n[{current_time:.1f}s] Detection Update:")

                    if hero_changed:
                        print(
                            f"  {Fore.GREEN}Hero cards: {self.last_hero_cards} → {hero_cards}"
                        )
                        self.analyze_hero_hand(hero_cards)

                    if community_changed:
                        print(
                            f"  {Fore.BLUE}Community cards: {self.last_community_cards} → {community_cards}"
                        )

                    if stage_changed:
                        print(
                            f"  {Fore.YELLOW}Board stage: {self.last_board_stage} → {board_stage}"
                        )

                    # Log the change
                    self.log_detection_change(hero_cards, community_cards, board_stage)

                    # Update last known values
                    self.last_hero_cards = hero_cards
                    self.last_community_cards = community_cards
                    self.last_board_stage = board_stage

                time.sleep(interval)

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Monitoring stopped by user")

        print(f"\n{Fore.CYAN}=== Monitoring Complete ===\n")
        self.print_debug_summary()

    def get_hero_cards(self):
        """Get hero cards from game state"""
        for player_num, player_info in self.game_state.players.items():
            if player_info.get("hero"):
                return player_info.get("cards", [])
        return []

    def analyze_hero_hand(self, hero_cards):
        """Analyze hero hand if cards are detected"""
        if not hero_cards or len(hero_cards) < 2:
            return

        try:
            analysis = self.hand_analyzer.analyze_hero_hand(
                hero_cards, "BTN", 100, 10, 6, []
            )

            print(f"    {Fore.MAGENTA}Analysis:")
            print(f"      Notation: {analysis.get('hand_notation', 'N/A')}")
            print(f"      Category: {analysis.get('category', 'N/A')}")
            print(f"      Strength: {analysis.get('strength', 'N/A')}")
            print(f"      Recommendation: {analysis.get('recommendation', 'N/A')}")

        except Exception as e:
            print(f"    {Fore.RED}Analysis error: {e}")

    def log_detection_change(self, hero_cards, community_cards, board_stage):
        """Log detection changes"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "hero_cards": hero_cards,
            "community_cards": community_cards,
            "board_stage": board_stage,
        }
        self.debug_log.append(log_entry)

    def print_debug_summary(self):
        """Print a summary of detection activity"""
        if not self.debug_log:
            print("No detection changes recorded")
            return

        print(f"Detection changes recorded: {len(self.debug_log)}")

        # Count different types of changes
        hero_changes = sum(1 for entry in self.debug_log if entry["hero_cards"])
        community_changes = sum(
            1 for entry in self.debug_log if entry["community_cards"]
        )
        stage_changes = sum(
            1 for entry in self.debug_log if entry["board_stage"] != "Pre-Flop"
        )

        print(f"Hero card changes: {hero_changes}")
        print(f"Community card changes: {community_changes}")
        print(f"Board stage changes: {stage_changes}")

        # Show last few entries
        print(f"\n{Fore.CYAN}Last 5 detection changes:")
        for entry in self.debug_log[-5:]:
            print(
                f"  {entry['timestamp']}: Hero={entry['hero_cards']}, Community={entry['community_cards']}, Stage={entry['board_stage']}"
            )

    def save_debug_log(self, filename=None):
        """Save debug log to file"""
        if not filename:
            filename = (
                f"detection_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

        with open(filename, "w") as f:
            json.dump(self.debug_log, f, indent=2)

        print(f"Debug log saved to {filename}")

    def show_current_state(self):
        """Show current detection state"""
        print(f"{Fore.CYAN}=== Current Detection State ===\n")

        hero_cards = self.get_hero_cards()
        community_cards = self.game_state.community_cards
        board_stage = self.game_state.current_board_stage

        print(f"Hero cards: {hero_cards}")
        print(f"Community cards: {community_cards}")
        print(f"Board stage: {board_stage}")
        print(f"Total pot: {self.game_state.total_pot}")
        print(f"Active players: {len(self.game_state.active_players)}")

        if hero_cards:
            self.analyze_hero_hand(hero_cards)

    def test_specific_cards(self, cards):
        """Test analysis with specific cards"""
        print(f"{Fore.CYAN}=== Testing Specific Cards ===\n")
        print(f"Testing cards: {cards}")

        if not cards or len(cards) < 2:
            print("Invalid cards provided")
            return

        try:
            analysis = self.hand_analyzer.analyze_hero_hand(
                cards, "BTN", 100, 10, 6, []
            )

            print(f"Hand notation: {analysis.get('hand_notation', 'N/A')}")
            print(f"Category: {analysis.get('category', 'N/A')}")
            print(f"Strength: {analysis.get('strength', 'N/A')}")
            print(f"Recommendation: {analysis.get('recommendation', 'N/A')}")
            print(f"Analysis: {analysis.get('analysis', 'N/A')}")

        except Exception as e:
            print(f"Analysis error: {e}")


def main():
    """Main function"""
    print(f"{Fore.GREEN}🔍 PokerGPT Detection Debugger\n")

    debugger = DetectionDebugger()

    print("Choose debugging option:")
    print("1. Monitor detection in real-time")
    print("2. Show current detection state")
    print("3. Test specific cards")
    print("4. Save debug log")
    print("0. Exit")

    choice = input(f"\n{Fore.YELLOW}Enter your choice (0-4): ").strip()

    if choice == "1":
        duration = input("Enter monitoring duration in seconds (default 60): ").strip()
        duration = int(duration) if duration.isdigit() else 60

        interval = input("Enter check interval in seconds (default 1): ").strip()
        interval = float(interval) if interval.replace(".", "").isdigit() else 1

        debugger.monitor_detection(duration, interval)

        # Ask if user wants to save log
        save = input("Save debug log? (y/n): ").strip().lower()
        if save == "y":
            debugger.save_debug_log()

    elif choice == "2":
        debugger.show_current_state()

    elif choice == "3":
        cards = input("Enter cards to test (e.g., Ah Kh): ").split()
        debugger.test_specific_cards(cards)

    elif choice == "4":
        debugger.save_debug_log()

    elif choice == "0":
        print("Exiting...")

    else:
        print("Invalid choice. Please enter a number between 0-4.")


if __name__ == "__main__":
    main()
