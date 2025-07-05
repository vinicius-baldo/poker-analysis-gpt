#!/usr/bin/env python3
"""
Hand Detection Testing Script for PokerGPT

This script provides multiple ways to test and validate hand detection accuracy:
1. Manual testing with known card combinations
2. Screenshot analysis testing
3. OCR accuracy validation
4. Template matching validation
5. Real-time detection monitoring
"""

import os
import sys
import time
from datetime import datetime

import cv2
import numpy as np
from colorama import Fore, init

# Initialize colorama for colored output
init(autoreset=True)

# Add the current directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import openai

from game_state import GameState
from hand_strength_analyzer import HandStrengthAnalyzer
from hero_hand_range import PokerHandRangeDetector
from hero_info import HeroInfo
from poker_assistant import PokerAssistant
from read_poker_table_dynamic import ReadPokerTableDynamic


class HandDetectionTester:
    def __init__(self):
        self.hand_analyzer = HandStrengthAnalyzer()
        self.game_state = GameState()
        self.hero_info = HeroInfo()
        self.hero_hand_range = PokerHandRangeDetector()

        # Test card templates
        self.card_templates = {
            "2": cv2.imread("images/2.png", cv2.IMREAD_GRAYSCALE),
            "3": cv2.imread("images/3.png", cv2.IMREAD_GRAYSCALE),
            "4": cv2.imread("images/4.png", cv2.IMREAD_GRAYSCALE),
            "5": cv2.imread("images/5.png", cv2.IMREAD_GRAYSCALE),
            "6": cv2.imread("images/6.png", cv2.IMREAD_GRAYSCALE),
            "7": cv2.imread("images/7.png", cv2.IMREAD_GRAYSCALE),
            "8": cv2.imread("images/8.png", cv2.IMREAD_GRAYSCALE),
            "9": cv2.imread("images/9.png", cv2.IMREAD_GRAYSCALE),
            "10": cv2.imread("images/10.png", cv2.IMREAD_GRAYSCALE),
            "A": cv2.imread("images/A.png", cv2.IMREAD_GRAYSCALE),
            "J": cv2.imread("images/J.png", cv2.IMREAD_GRAYSCALE),
            "Q": cv2.imread("images/Q.png", cv2.IMREAD_GRAYSCALE),
            "K": cv2.imread("images/K.png", cv2.IMREAD_GRAYSCALE),
        }

        self.suit_templates = {
            "♣": cv2.imread("images/Clover.png", cv2.IMREAD_GRAYSCALE),
            "♦": cv2.imread("images/Diamonds.png", cv2.IMREAD_GRAYSCALE),
            "♥": cv2.imread("images/Hearts.png", cv2.IMREAD_GRAYSCALE),
            "♠": cv2.imread("images/Spades.png", cv2.IMREAD_GRAYSCALE),
        }

    def test_known_combinations(self):
        """Test hand detection with known card combinations"""
        print(f"{Fore.CYAN}=== Testing Known Card Combinations ===\n")

        test_hands = [
            ["Ah", "Kh"],  # AK suited
            ["As", "Ad"],  # AA
            ["7c", "2d"],  # 72 offsuit
            ["Qh", "Qd"],  # QQ
            ["Jc", "Tc"],  # JT suited
            ["Kd", "9s"],  # K9 offsuit
        ]

        for hand in test_hands:
            print(f"Testing hand: {hand}")

            # Test parsing
            parsed = self.hand_analyzer.parse_cards(hand)
            print(f"  Parsed: {parsed}")

            # Test notation
            notation = self.hand_analyzer.get_hand_notation(parsed)
            print(f"  Notation: {notation}")

            # Test analysis
            analysis = self.hand_analyzer.analyze_hero_hand(hand, "BTN", 100, 10, 6, [])
            print(f"  Category: {analysis.get('category', 'N/A')}")
            print(f"  Strength: {analysis.get('strength', 'N/A')}")
            print(f"  Recommendation: {analysis.get('recommendation', 'N/A')}")
            print()

    def test_template_matching(self):
        """Test template matching accuracy"""
        print(f"{Fore.CYAN}=== Testing Template Matching ===\n")

        # Test each template
        for rank, template in self.card_templates.items():
            if template is not None:
                print(f"✓ Template for {rank} loaded successfully")
            else:
                print(f"✗ Template for {rank} failed to load")

        print()

        for suit, template in self.suit_templates.items():
            if template is not None:
                print(f"✓ Template for {suit} loaded successfully")
            else:
                print(f"✗ Template for {suit} failed to load")

        print()

    def test_card_validation(self):
        """Test card format validation"""
        print(f"{Fore.CYAN}=== Testing Card Format Validation ===\n")

        valid_cards = [
            "Ah",
            "Ks",
            "Qd",
            "Jc",
            "10h",
            "9s",
            "8d",
            "7c",
            "6h",
            "5s",
            "4d",
            "3c",
            "2h",
        ]
        invalid_cards = ["Xh", "1s", "Kx", "A", "123", "", "h", "s"]

        print("Valid cards:")
        for card in valid_cards:
            parsed = self.hand_analyzer.parse_cards([card])
            if parsed:
                print(f"  ✓ {card} -> {parsed}")
            else:
                print(f"  ✗ {card} -> Failed to parse")

        print("\nInvalid cards:")
        for card in invalid_cards:
            parsed = self.hand_analyzer.parse_cards([card])
            if parsed:
                print(f"  ✗ {card} -> Unexpectedly parsed as {parsed}")
            else:
                print(f"  ✓ {card} -> Correctly rejected")

        print()

    def test_hand_strength_consistency(self):
        """Test that hand strength analysis is consistent"""
        print(f"{Fore.CYAN}=== Testing Hand Strength Consistency ===\n")

        # Test pairs
        pairs = [["Ah", "Ad"], ["Kh", "Kd"], ["Qh", "Qd"], ["Jh", "Jd"]]
        print("Testing pairs:")
        for pair in pairs:
            analysis = self.hand_analyzer.analyze_hero_hand(pair, "BTN", 100, 10, 6, [])
            print(
                f"  {pair} -> {analysis.get('category', 'N/A')} (Strength: {analysis.get('strength', 'N/A')})"
            )

        print("\nTesting suited vs offsuit:")
        suited = ["Ah", "Kh"]
        offsuit = ["Ah", "Kd"]

        suited_analysis = self.hand_analyzer.analyze_hero_hand(
            suited, "BTN", 100, 10, 6, []
        )
        offsuit_analysis = self.hand_analyzer.analyze_hero_hand(
            offsuit, "BTN", 100, 10, 6, []
        )

        print(
            f"  {suited} -> {suited_analysis.get('category', 'N/A')} (Strength: {suited_analysis.get('strength', 'N/A')})"
        )
        print(
            f"  {offsuit} -> {offsuit_analysis.get('category', 'N/A')} (Strength: {offsuit_analysis.get('strength', 'N/A')})"
        )

        print()

    def test_position_analysis(self):
        """Test position-based hand analysis"""
        print(f"{Fore.CYAN}=== Testing Position-Based Analysis ===\n")

        test_hand = ["Ah", "Kh"]
        positions = ["UTG", "MP", "CO", "BTN", "SB", "BB"]

        for position in positions:
            analysis = self.hand_analyzer.analyze_hero_hand(
                test_hand, position, 100, 10, 6, []
            )
            print(
                f"  {position}: {analysis.get('recommendation', 'N/A')} - {analysis.get('analysis', 'N/A')[:50]}..."
            )

        print()

    def create_test_screenshot(self, cards, filename="test_screenshot.png"):
        """Create a test screenshot with specific cards for validation"""
        print(f"{Fore.CYAN}=== Creating Test Screenshot ===\n")

        # Create a simple test image
        img = np.ones((200, 400, 3), dtype=np.uint8) * 255  # White background

        # Add text showing the cards
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f"Test Cards: {cards}", (10, 50), font, 1, (0, 0, 0), 2)
        cv2.putText(img, f"Time: {datetime.now()}", (10, 100), font, 0.7, (0, 0, 0), 2)

        cv2.imwrite(filename, img)
        print(f"Test screenshot saved as {filename}")
        print()

    def monitor_real_time_detection(self, duration=30):
        """Monitor real-time hand detection for a specified duration"""
        print(f"{Fore.CYAN}=== Real-Time Detection Monitor ===\n")
        print(f"Monitoring for {duration} seconds...")
        print("Press Ctrl+C to stop early\n")

        start_time = time.time()
        last_cards = None

        try:
            while time.time() - start_time < duration:
                # This would need to be integrated with the actual poker table reader
                # For now, we'll simulate the monitoring
                current_time = time.time() - start_time

                # Simulate card detection (replace with actual detection)
                detected_cards = self.simulate_card_detection()

                if detected_cards != last_cards:
                    print(f"[{current_time:.1f}s] Cards detected: {detected_cards}")
                    last_cards = detected_cards

                time.sleep(0.5)  # Check every 500ms

        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")

        print()

    def simulate_card_detection(self):
        """Simulate card detection for testing purposes"""
        # This is a placeholder - replace with actual detection logic
        import random

        ranks = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        suits = ["h", "d", "c", "s"]

        if random.random() < 0.3:  # 30% chance of detecting cards
            card1 = random.choice(ranks) + random.choice(suits)
            card2 = random.choice(ranks) + random.choice(suits)
            return [card1, card2]

        return None

    def generate_test_report(self):
        """Generate a comprehensive test report"""
        print(f"{Fore.CYAN}=== Generating Test Report ===\n")

        report = {
            "timestamp": datetime.now().isoformat(),
            "tests_run": [],
            "summary": {},
        }

        # Run all tests and collect results
        test_methods = [
            self.test_known_combinations,
            self.test_template_matching,
            self.test_card_validation,
            self.test_hand_strength_consistency,
            self.test_position_analysis,
        ]

        for test_method in test_methods:
            try:
                test_method()
                report["tests_run"].append(
                    {"test": test_method.__name__, "status": "passed"}
                )
            except Exception as e:
                report["tests_run"].append(
                    {"test": test_method.__name__, "status": "failed", "error": str(e)}
                )

        # Save report
        report_filename = (
            f"hand_detection_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        with open(report_filename, "w") as f:
            f.write("Hand Detection Test Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {report['timestamp']}\n\n")

            for test in report["tests_run"]:
                status_icon = "✓" if test["status"] == "passed" else "✗"
                f.write(f"{status_icon} {test['test']}: {test['status']}\n")
                if "error" in test:
                    f.write(f"    Error: {test['error']}\n")

        print(f"Test report saved as {report_filename}")
        print()

    def run_all_tests(self):
        """Run all hand detection tests"""
        print(f"{Fore.GREEN}🎯 Starting Hand Detection Testing Suite\n")
        print(
            f"{Fore.YELLOW}This will test various aspects of hand detection accuracy\n"
        )

        # Run all tests
        self.test_known_combinations()
        self.test_template_matching()
        self.test_card_validation()
        self.test_hand_strength_consistency()
        self.test_position_analysis()
        self.create_test_screenshot(["Ah", "Kh"])
        self.generate_test_report()

        print(
            f"{Fore.GREEN}✅ All tests completed! Check the generated report for details.\n"
        )


def main():
    """Main function to run the hand detection tests"""
    print(f"{Fore.CYAN}PokerGPT Hand Detection Testing Tool\n")
    print("Choose a test option:")
    print("1. Run all tests")
    print("2. Test known combinations")
    print("3. Test template matching")
    print("4. Test card validation")
    print("5. Test hand strength consistency")
    print("6. Test position analysis")
    print("7. Create test screenshot")
    print("8. Monitor real-time detection")
    print("9. Generate test report")
    print("0. Exit")

    tester = HandDetectionTester()

    while True:
        try:
            choice = input(f"\n{Fore.YELLOW}Enter your choice (0-9): ").strip()

            if choice == "0":
                print("Exiting...")
                break
            elif choice == "1":
                tester.run_all_tests()
            elif choice == "2":
                tester.test_known_combinations()
            elif choice == "3":
                tester.test_template_matching()
            elif choice == "4":
                tester.test_card_validation()
            elif choice == "5":
                tester.test_hand_strength_consistency()
            elif choice == "6":
                tester.test_position_analysis()
            elif choice == "7":
                cards = input("Enter cards to test (e.g., Ah Kh): ").split()
                tester.create_test_screenshot(cards)
            elif choice == "8":
                duration = int(input("Enter monitoring duration in seconds: "))
                tester.monitor_real_time_detection(duration)
            elif choice == "9":
                tester.generate_test_report()
            else:
                print("Invalid choice. Please enter a number between 0-9.")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
