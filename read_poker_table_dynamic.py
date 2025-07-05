import re
import threading
import time
import tkinter as tk
from datetime import datetime
from threading import Lock

import cv2
import keyboard
import mss
import numpy as np
import pyautogui
import pytesseract
from colorama import Fore
from PIL import Image, ImageTk


class ReadPokerTableDynamic:

    def __init__(
        self,
        poker_window,
        hero_info,
        hero_hand_range,
        poker_assistant,
        game_state,
        player_analyzer,
        max_players=6,
    ):
        self.game_state_lock = Lock()
        self.hero_info = hero_info
        self.hero_hand_range = hero_hand_range
        self.game_state = game_state
        self.poker_assistant = poker_assistant
        self.player_analyzer = player_analyzer
        self.max_players = max_players
        self.save_screenshots = False
        self.tesseract_cmd = r"C:\Users\Admin\Desktop\PokerGPT\tesseract\tesseract.exe"
        self.cards_on_table = False
        self.previous_hashes = {}
        self.photo = None
        self.last_active_player = 1
        self.last_action_player = 0
        # Removed action-related variables since we only provide analysis
        self.last_detected_cards = []
        self.window = poker_window
        self.poker_window_width = self.window.width
        self.poker_window_height = self.window.height
        self.window_activation_error_reported = False

        # Load the images
        self.dealer_button_image = cv2.imread(
            "images/dealer_button.png", cv2.IMREAD_GRAYSCALE
        )
        self.card_icon_templates = {
            "♣": cv2.imread("images/Clover.png", cv2.IMREAD_GRAYSCALE),
            "♦": cv2.imread("images/Diamonds.png", cv2.IMREAD_GRAYSCALE),
            "♥": cv2.imread("images/Hearts.png", cv2.IMREAD_GRAYSCALE),
            "♠": cv2.imread("images/Spades.png", cv2.IMREAD_GRAYSCALE),
        }
        self.card_number_templates = {
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

        self.shutdown_flag = threading.Event()
        self.threads = []
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd

        # Initialize player regions based on max_players
        self.player_regions = self.generate_player_regions()

    def generate_player_regions(self):
        """Generate player regions based on the maximum number of players."""
        # Base regions for 6 players (standard configuration)
        base_regions = {
            1: {
                "stack": (0.467, 0.732),
                "action": (0.467, 0.701),
                "turn": (0.578, 0.734),
            },
            2: {
                "stack": (0.059, 0.560),
                "action": (0.059, 0.529),
                "turn": (0.049, 0.562),
            },
            3: {
                "stack": (0.093, 0.265),
                "action": (0.093, 0.235),
                "turn": (0.084, 0.266),
            },
            4: {
                "stack": (0.430, 0.173),
                "action": (0.430, 0.144),
                "turn": (0.428, 0.172),
            },
            5: {
                "stack": (0.814, 0.265),
                "action": (0.814, 0.235),
                "turn": (0.916, 0.260),
            },
            6: {
                "stack": (0.846, 0.560),
                "action": (0.842, 0.530),
                "turn": (0.947, 0.558),
            },
        }

        # Extended regions for 7-9 players (approximated positions)
        extended_regions = {
            7: {
                "stack": (0.250, 0.650),
                "action": (0.250, 0.620),
                "turn": (0.260, 0.652),
            },
            8: {
                "stack": (0.650, 0.650),
                "action": (0.650, 0.620),
                "turn": (0.660, 0.652),
            },
            9: {
                "stack": (0.450, 0.100),
                "action": (0.450, 0.070),
                "turn": (0.460, 0.102),
            },
        }

        regions = {}
        for i in range(1, min(self.max_players + 1, 7)):
            regions[i] = base_regions[i]

        # Add extended regions if needed
        for i in range(7, self.max_players + 1):
            if i in extended_regions:
                regions[i] = extended_regions[i]

        return regions

    def activate_window(self):
        """Activate the poker client window."""
        if self.window:
            try:
                self.window.activate()
                self.window_activation_error_reported = False
            except Exception as e:
                if not self.window_activation_error_reported:
                    print(f"Error activating window: {e}")
                    self.window_activation_error_reported = True
        else:
            if not self.window_activation_error_reported:
                print("Window not located or cannot be activated.")
                self.window_activation_error_reported = True

    def is_pixel_white(self, pixel, min_white=230, max_white=255):
        """Check if a pixel is within the white range."""
        r, g, b = pixel
        return all(min_white <= value <= max_white for value in (r, g, b))

    def capture_screen_area(self, relative_x, relative_y, width, height, filename=None):
        """Capture a screen area based on relative coordinates."""
        if not self.window:
            print("Window not located. Please locate the window first.")
            return None

        abs_x = int(self.window.left + self.poker_window_width * relative_x)
        abs_y = int(self.window.top + self.poker_window_height * relative_y)

        with mss.mss() as sct:
            monitor = {"top": abs_y, "left": abs_x, "width": width, "height": height}
            screenshot = sct.grab(monitor)

            if self.save_screenshots or filename:
                filepath = f'Screenshots/{filename if filename else datetime.now().strftime("%Y%m%d_%H%M%S_%f")}.png'
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=filepath)

        return screenshot

    def contains_white(self, image):
        """Check if the image contains any pixels within the specified white color range."""
        self.white_color_lower = np.array([210, 210, 210])
        self.white_color_upper = np.array([255, 255, 255])

        # Convert PIL image to numpy array if needed
        if hasattr(image, "rgb"):
            image_array = np.array(image.rgb)
        else:
            image_array = np.array(image)

        # Create a mask for white pixels
        white_mask = cv2.inRange(
            image_array, self.white_color_lower, self.white_color_upper
        )

        # Check if any white pixels exist
        return np.any(white_mask > 0)

    def contains_blue(self, image):
        """Check if the image contains any pixels within the specified blue color range."""
        self.blue_color_lower = np.array([100, 100, 200])
        self.blue_color_upper = np.array([200, 200, 255])

        # Convert PIL image to numpy array if needed
        if hasattr(image, "rgb"):
            image_array = np.array(image.rgb)
        else:
            image_array = np.array(image)

        # Create a mask for blue pixels
        blue_mask = cv2.inRange(
            image_array, self.blue_color_lower, self.blue_color_upper
        )

        # Check if any blue pixels exist
        return np.any(blue_mask > 0)

    def image_hash(self, image):
        """Generate a hash for the image."""
        # Convert PIL image to numpy array if needed
        if hasattr(image, "rgb"):
            image_array = np.array(image.rgb)
        else:
            image_array = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

        # Resize to 8x8
        resized = cv2.resize(gray, (8, 8))

        # Calculate hash
        hash_value = 0
        for i in range(8):
            for j in range(8):
                if resized[i, j] > 128:
                    hash_value |= 1 << (i * 8 + j)

        return hash_value

    def has_image_changed(self, unique_id, image):
        """Check if the image has changed significantly."""
        current_hash = self.image_hash(image)

        if unique_id not in self.previous_hashes:
            self.previous_hashes[unique_id] = current_hash
            return True

        previous_hash = self.previous_hashes[unique_id]

        def hamming_distance(hash1, hash2):
            """Calculate the Hamming distance between two hashes."""
            return bin(hash1 ^ hash2).count("1")

        distance = hamming_distance(current_hash, previous_hash)
        threshold = 5  # Adjust this threshold as needed

        if distance > threshold:
            self.previous_hashes[unique_id] = current_hash
            return True

        return False

    def detect_text(self, relative_x, relative_y, width, height):
        """Detect text in a specific area using OCR."""
        try:
            screenshot = self.capture_screen_area(relative_x, relative_y, width, height)
            if screenshot is None:
                return None

            # Convert to PIL Image for OCR
            pil_image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

            # Use Tesseract OCR
            text = pytesseract.image_to_string(
                pil_image,
                config="--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,$() ",
            )

            # Clean up the text
            text = text.strip()
            return text if text else None

        except Exception as e:
            print(f"Error in detect_text: {e}")
            return None

    def detect_text_changed(
        self, player_number, unique_id, relative_x, relative_y, width, height
    ):
        """Detect text only if the image has changed."""
        screenshot = self.capture_screen_area(relative_x, relative_y, width, height)
        if screenshot is None:
            return None

        if self.has_image_changed(unique_id, screenshot):
            return self.detect_text(relative_x, relative_y, width, height)

        return None

    def detect_player_stack_and_action(self, player_number):
        """Detect player stack size and action for any player number."""
        if player_number not in self.player_regions:
            return

        if self.last_action_player == player_number:
            return

        region_stack_x, region_stack_y = self.player_regions[player_number]["stack"]
        region_action_x, region_action_y = self.player_regions[player_number]["action"]

        width = 95
        height = 24

        # Detect and parse stack size
        detected_stack_text = self.detect_text_changed(
            player_number,
            player_number + 10,
            region_stack_x,
            region_stack_y,
            width,
            height,
        )

        if detected_stack_text is None:
            return

        # Update player active state
        self.update_player_active_state(player_number, detected_stack_text)

        current_stack_size, stack_size_change = self.get_player_stack_size(
            player_number, detected_stack_text
        )

        if current_stack_size is not None:
            self.game_state.update_player(player_number, stack_size=current_stack_size)

        # Detect and parse player action
        detected_action_text = self.detect_text_changed(
            player_number,
            player_number + 20,
            region_action_x,
            region_action_y,
            width,
            height,
        )

        if detected_action_text is None:
            return

        detected_action = detected_action_text.lower()
        bet_amount = 0

        if current_stack_size is not None:
            if stack_size_change < 20:
                bet_amount = stack_size_change

        # Process different actions
        if detected_action == "fold":
            self.game_state.update_player(player_number, action="Fold")
            self.update_player_analyzer(player_number, "Fold", 0)
            self.last_action_player = player_number
        elif detected_action == "resume":
            self.game_state.update_player(player_number, action="Resume")
            self.last_action_player = player_number
        elif detected_action == "check":
            self.game_state.update_player(player_number, action="Check")
            self.update_player_analyzer(player_number, "Check", 0)
            self.last_action_player = player_number
        elif detected_action == "call":
            self.game_state.update_player(
                player_number,
                stack_size=current_stack_size,
                amount=bet_amount,
                action="Call",
            )
            self.update_player_analyzer(player_number, "Call", bet_amount)
            self.last_action_player = player_number
        elif detected_action == "raise":
            self.game_state.update_player(
                player_number,
                stack_size=current_stack_size,
                amount=bet_amount,
                action="Raise",
            )
            self.update_player_analyzer(player_number, "Raise", bet_amount)
            self.last_action_player = player_number
        elif detected_action == "bet":
            self.game_state.update_player(
                player_number,
                stack_size=current_stack_size,
                amount=bet_amount,
                action="Bet",
            )
            self.update_player_analyzer(player_number, "Bet", bet_amount)
            self.last_action_player = player_number
        elif "won" in detected_action:
            won_amount_number = self.get_won_amount(detected_action)
            self.game_state.update_player(
                player_number,
                stack_size=current_stack_size,
                won_amount=won_amount_number,
            )
            self.last_action_player = player_number

    def update_player_active_state(self, player_number, detected_stack_text):
        """Update player active state based on detected text."""
        if re.search(r"sitting|seat|disconnect", detected_stack_text, re.IGNORECASE):
            current_status = self.game_state.players.get(player_number, {}).get(
                "status"
            )
            if current_status == "Active":
                self.game_state.update_player(player_number, status="Inactive")
        else:
            self.game_state.update_player(player_number, status="Active")

    def get_won_amount(self, detected_text):
        """Extract won amount from detected text."""
        detected_text = detected_text.replace(",", "")
        match = re.search(r"\d+(\.\d+)?", detected_text)
        if match:
            return float(match.group())
        return 0

    def update_player_analyzer(self, player_number, action, amount):
        """Update player analyzer with detected action."""
        if not self.player_analyzer:
            return

        try:
            player_name = f"Player {player_number}"
            position = self.get_player_position(player_number)
            board_stage = self.game_state.current_board_stage.lower().replace(" ", "_")
            pot_size = self.game_state.total_pot

            self.player_analyzer.update_player_action(
                player_name=player_name,
                action=action,
                amount=amount,
                pot_size=pot_size,
                position=position,
                board_stage=board_stage,
            )
        except Exception as e:
            print(f"{Fore.RED}Error updating player analyzer: {e}{Fore.RESET}")

    def get_player_position(self, player_number):
        """Get player position relative to dealer."""
        dealer_pos = self.game_state.dealer_position
        if dealer_pos == -1:
            return "unknown"

        # Calculate position relative to dealer
        hero_pos = self.hero_info.hero_player_number
        total_players = len(self.player_regions)

        # Calculate positions clockwise from dealer
        positions = [
            "blinds",
            "blinds",
            "early",
            "early",
            "middle",
            "middle",
            "late",
            "late",
            "late",
        ]

        # Adjust for actual number of players
        if total_players <= 6:
            positions = positions[:total_players]

        # Calculate player's position relative to dealer
        relative_pos = (player_number - dealer_pos) % total_players
        if relative_pos < len(positions):
            return positions[relative_pos]

        return "unknown"

    def get_player_stack_size(self, player_number, detected_text):
        """Parse the detected text for stack size."""
        detected_text = detected_text.replace(",", "")
        match = re.search(r"\d+(\.\d+)?", detected_text)

        if match:
            current_stack_size = float(match.group())
            old_stack_size = self.game_state.players.get(player_number, {}).get(
                "stack_size", 0.0
            )

            if old_stack_size == 0:
                self.game_state.update_player(
                    player_number, stack_size=current_stack_size
                )
                return None, None

            if old_stack_size != current_stack_size:
                stack_size_change = current_stack_size - old_stack_size
                if stack_size_change < 0:
                    stack_size_change = -stack_size_change
                return current_stack_size, stack_size_change

        return None, None

    def detect_player_turn(self):
        """Detect which player's turn it is."""
        for player_number, regions in self.player_regions.items():
            region_x, region_y = regions["turn"]
            abs_x, abs_y = self.convert_to_screen_coords(region_x, region_y)

            if self.is_gray_bar_present(abs_x, abs_y):
                self.game_state.update_player(player_number, turn=True)
                self.last_active_player = player_number
                return player_number
            else:
                self.game_state.update_player(player_number, turn=False)

        return None

    def is_gray_bar_present(self, x, y):
        """Check if a gray bar is present at the specified coordinates."""
        try:
            # Capture a small area around the coordinates
            width, height = 20, 5
            screenshot = self.capture_screen_area(
                x / self.poker_window_width, y / self.poker_window_height, width, height
            )

            if screenshot is None:
                return False

            # Convert to numpy array
            image_array = np.array(screenshot.rgb)

            # Define gray color range
            gray_lower = np.array([100, 100, 100])
            gray_upper = np.array([150, 150, 150])

            # Create mask for gray pixels
            gray_mask = cv2.inRange(image_array, gray_lower, gray_upper)

            # Check if gray pixels exist
            return np.any(gray_mask > 0)

        except Exception as e:
            print(f"Error in is_gray_bar_present: {e}")
            return False

    def detect_total_pot_size(self):
        """Detect the total pot size."""
        try:
            # Pot size is typically displayed in the center of the table
            pot_x, pot_y = 0.45, 0.45  # Approximate center
            width, height = 120, 30

            detected_text = self.detect_text(pot_x, pot_y, width, height)

            if detected_text:
                # Clean up the text and extract numeric value
                detected_text = detected_text.replace(",", "").replace("$", "")
                match = re.search(r"\d+(\.\d+)?", detected_text)
                if match:
                    pot_size = float(match.group())
                    self.game_state.update_total_pot(pot_size)

        except Exception as e:
            print(f"Error in detect_total_pot_size: {e}")

    def convert_to_screen_coords(self, rel_x, rel_y):
        """Convert relative coordinates to absolute screen coordinates."""
        abs_x = int(self.window.left + self.poker_window_width * rel_x)
        abs_y = int(self.window.top + self.poker_window_height * rel_y)
        return abs_x, abs_y

    def find_dealer_button(self, button_template):
        """Find the dealer button position."""
        try:
            # Capture the entire poker table area
            screenshot = self.capture_screen_area(
                0.1,
                0.1,
                int(self.poker_window_width * 0.8),
                int(self.poker_window_height * 0.8),
            )

            if screenshot is None:
                return None

            # Convert to numpy array
            image_array = np.array(screenshot.rgb)
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

            # Template matching
            result = cv2.matchTemplate(gray, button_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val > 0.7:  # Threshold for matching
                # Convert back to relative coordinates
                rel_x = (max_loc[0] + 0.1) / self.poker_window_width
                rel_y = (max_loc[1] + 0.1) / self.poker_window_height

                # Determine which player position this corresponds to
                for player_number, regions in self.player_regions.items():
                    turn_x, turn_y = regions["turn"]
                    if abs(rel_x - turn_x) < 0.1 and abs(rel_y - turn_y) < 0.1:
                        self.game_state.update_dealer_position(player_number)
                        return player_number

            return None

        except Exception as e:
            print(f"Error in find_dealer_button: {e}")
            return None

    def continuous_detection_player_action(self, player_number):
        """Continuously detect actions for a specific player."""
        while not self.shutdown_flag.is_set():
            if not self.window:
                time.sleep(0.4)
                continue

            time.sleep(0.1)
            self.detect_player_stack_and_action(player_number)
            time.sleep(0.2)

    def continuous_detection_player_turn(self):
        """Continuously detect player turns."""
        while not self.shutdown_flag.is_set():
            if not self.window:
                time.sleep(0.2)
                continue

            self.detect_player_turn()
            time.sleep(0.3)

    def continuous_detection_dealer_button(self):
        """Continuously detect dealer button position."""
        while not self.shutdown_flag.is_set():
            if not self.window:
                time.sleep(0.2)
                continue

            self.find_dealer_button(self.dealer_button_image)
            time.sleep(1.0)

    def continuous_detection_total_pot_size(self):
        """Continuously detect total pot size."""
        while not self.shutdown_flag.is_set():
            if not self.window:
                time.sleep(0.2)
                continue

            self.detect_total_pot_size()
            time.sleep(0.6)

    def continuous_detection_tournament_info(self):
        """Continuously detect tournament information."""
        while not self.shutdown_flag.is_set():
            if not self.window:
                time.sleep(0.2)
                continue

            self.detect_tournament_info()
            time.sleep(5.0)  # Check tournament info every 5 seconds

    def detect_tournament_info(self):
        """Detect and update tournament information."""
        try:
            # Extract tournament info from window title
            if self.game_state.extract_blinds_from_title():
                # Recalculate stack-to-blind ratios
                self.game_state.calculate_stack_to_blind_ratios()

                # Update tournament analysis
                tournament_analysis = self.game_state.get_tournament_analysis()

                # Log tournament changes
                if tournament_analysis["is_tournament"]:
                    print(f"{Fore.CYAN}Tournament Info Updated:")
                    print(f"  Stage: {tournament_analysis['tournament_stage']}")
                    print(f"  Blind Level: {tournament_analysis['blind_level']}")
                    print(
                        f"  Hero Stack/BB: {tournament_analysis['hero_stack_to_blind_ratio']}"
                    )
                    print(
                        f"  Avg Stack/BB: {tournament_analysis['average_stack_to_blind_ratio']}"
                    )
                    print(
                        f"  Duration: {tournament_analysis['tournament_duration']} minutes"
                    )
                    if tournament_analysis["players_remaining"] > 0:
                        print(
                            f"  Players Left: {tournament_analysis['players_remaining']}"
                        )
                    print(f"{Fore.RESET}")

        except Exception as e:
            print(f"Error in detect_tournament_info: {e}")

    def initiate_shutdown(self):
        """Initiate the shutdown process."""
        print("Shutdown initiated...")
        self.shutdown_flag.set()
        self.shutdown()

    def shutdown(self):
        """Shut down all threads gracefully."""
        print("Shutting down threads...")
        print(
            f"Active threads at the beginning of shutdown: {threading.active_count()}"
        )

        for thread in self.threads:
            if thread.is_alive():
                self.shutdown_flag.set()
                thread.join()
                print(
                    f"Active threads after joining a thread: {threading.active_count()}"
                )

        print("All threads have been joined.")
        keyboard.unhook_all()

    def start_continuous_detection(self):
        """Start the continuous detection for all players."""
        # Create threads for each player
        for player_number in range(1, self.max_players + 1):
            thread = threading.Thread(
                target=self.continuous_detection_player_action, args=(player_number,)
            )
            self.threads.append(thread)
            thread.start()

        # Create other detection threads
        turn_detection_thread = threading.Thread(
            target=self.continuous_detection_player_turn
        )
        dealer_detection_thread = threading.Thread(
            target=self.continuous_detection_dealer_button
        )
        pot_detection_thread = threading.Thread(
            target=self.continuous_detection_total_pot_size
        )
        tournament_detection_thread = threading.Thread(
            target=self.continuous_detection_tournament_info
        )

        self.threads.extend(
            [
                turn_detection_thread,
                dealer_detection_thread,
                pot_detection_thread,
                tournament_detection_thread,
            ]
        )

        turn_detection_thread.start()
        dealer_detection_thread.start()
        pot_detection_thread.start()
        tournament_detection_thread.start()

        print(f"Started detection for {self.max_players} players")
