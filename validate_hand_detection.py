#!/usr/bin/env python3
"""
Real-time Hand Detection Validation Script

This script provides a simple way to validate hand detection during actual gameplay.
It can be run alongside the main PokerGPT application to verify detection accuracy.
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


class HandDetectionValidator:
    def __init__(self):
        self.game_state = GameState()
        self.hand_analyzer = HandStrengthAnalyzer()
        self.validation_log = []

    def validate_hero_cards(self, expected_cards):
        """Validate that hero cards are detected correctly"""
        print(f"{Fore.CYAN}=== Hero Cards Validation ===\n")

        # Get detected cards from game state
        detected_cards = []
        for player_num, player_info in self.game_state.players.items():
            if player_info.get("hero"):
                detected_cards = player_info.get("cards", [])
                break

        print(f"Expected cards: {expected_cards}")
        print(f"Detected cards: {detected_cards}")

        # Compare
        if detected_cards == expected_cards:
            print(f"{Fore.GREEN}✓ Cards detected correctly!")
            return True
        else:
            print(f"{Fore.RED}✗ Cards detection mismatch!")
            return False

    def validate_community_cards(self, expected_cards):
        """Validate that community cards are detected correctly"""
        print(f"{Fore.CYAN}=== Community Cards Validation ===\n")

        detected_cards = self.game_state.community_cards

        print(f"Expected cards: {expected_cards}")
        print(f"Detected cards: {detected_cards}")

        if detected_cards == expected_cards:
            print(f"{Fore.GREEN}✓ Community cards detected correctly!")
            return True
        else:
            print(f"{Fore.RED}✗ Community cards detection mismatch!")
            return False

    def validate_hand_analysis(self, hero_cards, expected_category=None):
        """Validate hand strength analysis"""
        print(f"{Fore.CYAN}=== Hand Analysis Validation ===\n")

        if not hero_cards:
            print("No hero cards provided for analysis")
            return False

        # Get analysis
        analysis = self.hand_analyzer.analyze_hero_hand(
            hero_cards, "BTN", 100, 10, 6, []
        )

        print(f"Hero cards: {hero_cards}")
        print(f"Hand notation: {analysis.get('hand_notation', 'N/A')}")
        print(f"Category: {analysis.get('category', 'N/A')}")
        print(f"Strength: {analysis.get('strength', 'N/A')}")
        print(f"Recommendation: {analysis.get('recommendation', 'N/A')}")

        if expected_category and analysis.get("category") == expected_category:
            print(f"{Fore.GREEN}✓ Category matches expected: {expected_category}")
            return True
        elif expected_category:
            print(
                f"{Fore.YELLOW}⚠ Category doesn't match expected: {expected_category}"
            )
            return False
        else:
            print(f"{Fore.GREEN}✓ Analysis completed successfully")
            return True

    def log_validation(self, test_type, expected, detected, passed):
        """Log validation results"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "test_type": test_type,
            "expected": expected,
            "detected": detected,
            "passed": passed,
        }
        self.validation_log.append(log_entry)

    def save_validation_log(self, filename=None):
        """Save validation log to file"""
        if not filename:
            filename = f"hand_detection_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, "w") as f:
            json.dump(self.validation_log, f, indent=2)

        print(f"Validation log saved to {filename}")

    def print_validation_summary(self):
        """Print a summary of validation results"""
        if not self.validation_log:
            print("No validation data available")
            return

        total_tests = len(self.validation_log)
        passed_tests = sum(1 for entry in self.validation_log if entry["passed"])
        failed_tests = total_tests - passed_tests

        print(f"\n{Fore.CYAN}=== Validation Summary ===\n")
        print(f"Total tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")

        if failed_tests > 0:
            print(f"\n{Fore.RED}Failed tests:")
            for entry in self.validation_log:
                if not entry["passed"]:
                    print(
                        f"  - {entry['test_type']}: Expected {entry['expected']}, Got {entry['detected']}"
                    )

    def interactive_validation(self):
        """Interactive validation mode"""
        print(f"{Fore.CYAN}=== Interactive Hand Detection Validation ===\n")
        print("This mode allows you to validate hand detection in real-time.")
        print("Enter the expected cards and compare with detected cards.\n")

        while True:
            print("\nOptions:")
            print("1. Validate hero cards")
            print("2. Validate community cards")
            print("3. Validate hand analysis")
            print("4. Show validation summary")
            print("5. Save validation log")
            print("0. Exit")

            choice = input(f"\n{Fore.YELLOW}Enter your choice (0-5): ").strip()

            if choice == "0":
                break
            elif choice == "1":
                expected = input("Enter expected hero cards (e.g., Ah Kh): ").split()
                passed = self.validate_hero_cards(expected)
                self.log_validation(
                    "hero_cards", expected, "detected_from_game_state", passed
                )
            elif choice == "2":
                expected = input(
                    "Enter expected community cards (e.g., Ah Kh Qd): "
                ).split()
                passed = self.validate_community_cards(expected)
                self.log_validation(
                    "community_cards", expected, "detected_from_game_state", passed
                )
            elif choice == "3":
                cards = input("Enter hero cards for analysis (e.g., Ah Kh): ").split()
                expected_category = (
                    input("Enter expected category (optional): ").strip() or None
                )
                passed = self.validate_hand_analysis(cards, expected_category)
                self.log_validation("hand_analysis", cards, "analysis_result", passed)
            elif choice == "4":
                self.print_validation_summary()
            elif choice == "5":
                self.save_validation_log()
            else:
                print("Invalid choice. Please enter a number between 0-5.")


def main():
    """Main function"""
    print(f"{Fore.GREEN}🎯 PokerGPT Hand Detection Validator\n")

    validator = HandDetectionValidator()

    print("Choose validation mode:")
    print("1. Interactive validation (recommended)")
    print("2. Quick test with sample data")
    print("0. Exit")

    choice = input(f"\n{Fore.YELLOW}Enter your choice (0-2): ").strip()

    if choice == "1":
        validator.interactive_validation()
    elif choice == "2":
        # Quick test with sample data
        print(f"\n{Fore.CYAN}Running quick validation test...\n")

        # Test hero cards
        validator.validate_hero_cards(["Ah", "Kh"])

        # Test community cards
        validator.validate_community_cards(["Ah", "Kh", "Qd"])

        # Test hand analysis
        validator.validate_hand_analysis(["Ah", "Kh"], "premium")

        # Show summary
        validator.print_validation_summary()

        # Save log
        validator.save_validation_log()
    elif choice == "0":
        print("Exiting...")
    else:
        print("Invalid choice. Please enter 0, 1, or 2.")


if __name__ == "__main__":
    main()
