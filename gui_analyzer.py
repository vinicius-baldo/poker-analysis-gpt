import random
import time
import tkinter as tk
import tkinter.font as tkFont
from tkinter import scrolledtext, ttk


class GUIAnalyzer:

    def __init__(self, game_state, poker_assistant, player_analyzer):
        self.game_state = game_state
        self.poker_assistant = poker_assistant
        self.player_analyzer = player_analyzer
        self.root = tk.Tk()

        # Set the background color of the root window
        self.root.configure(background="#171821")

        # List of possible titles
        possible_titles = [
            "Poker Analyzer",
            "Poker Coach",
            "Poker Assistant",
            "Poker Helper",
            "Poker Advisor",
        ]

        # Select a random title from the list
        random_title = random.choice(possible_titles)
        self.root.title(random_title)

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set window size to match screen size
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Add widgets
        self.add_widgets()

        # Start the polling loop
        self.polling_update()

    def add_widgets(self):
        padding = {"padx": 10, "pady": 10}
        self.fontStyle = tkFont.Font(family="Lucida Grande", size=14, weight="bold")
        tableFont = tkFont.Font(family="Lucida Grande", size=14)
        analysisFont = tkFont.Font(family="Lucida Grande", size=12)

        input_width = 10

        # Configure the Treeview font
        style = ttk.Style(self.root)
        style.configure("Custom.Treeview", font=tableFont, padding=15)
        style.configure("Custom.Treeview.Heading", font=self.fontStyle)

        # Create a Treeview widget for player information
        self.player_tree = ttk.Treeview(self.root, height=7, style="Custom.Treeview")
        self.player_tree["columns"] = (
            "Player",
            "Status",
            "Role",
            "Cards",
            "Turn",
            "Action",
            "Amount",
            "Stack Size",
            "Play Style",
            "Strategy",
        )

        # Hide the default tree column
        self.player_tree.column("#0", width=0, stretch=tk.NO)
        self.player_tree.heading("#0", text="")

        # Define the column headings
        for col in self.player_tree["columns"]:
            self.player_tree.heading(col, text=col)
            self.player_tree.column(col, width=120, anchor="center")

        # Position the Treeview widget
        self.player_tree.grid(
            row=1, column=0, columnspan=12, pady=10, padx=10, sticky="nsew"
        )

        # Configure the first two columns to not expand unnecessarily
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=0)

        # Game State Information Section
        self.create_game_state_section(padding, input_width)

        # Analysis Section
        self.create_analysis_section(padding, analysisFont)

        # Opponent Analysis Section
        self.create_opponent_analysis_section(padding, analysisFont)

        # Player Analysis Section
        self.create_player_analysis_section(padding, analysisFont)

        # Quick Advice Section
        self.create_quick_advice_section(padding, analysisFont)

        # Log Section
        self.create_log_section(padding, analysisFont)

        # Notifications Section
        self.create_notifications_section(padding, analysisFont)

    def create_game_state_section(self, padding, input_width):
        """Create the game state information section."""
        # Total Players
        self.total_players_label = tk.Label(
            self.root,
            text="Total Players",
            font=self.fontStyle,
            bg="#171821",
            fg="white",
        )
        self.total_players_label.grid(row=0, column=0, sticky="w", **padding)
        self.total_players_info = tk.Text(
            self.root,
            height=1,
            width=input_width,
            bg="#171821",
            fg="white",
            font=self.fontStyle,
        )
        self.total_players_info.grid(row=0, column=1, sticky="w", **padding)

        # Hero Cards
        self.hero_cards_label = tk.Label(
            self.root, text="Hero Cards", font=self.fontStyle, bg="#171821", fg="white"
        )
        self.hero_cards_label.grid(row=2, column=0, sticky="w", **padding)
        self.hero_cards_info = tk.Text(
            self.root,
            height=1,
            width=input_width * 2,
            bg="#171821",
            fg="white",
            font=self.fontStyle,
        )
        self.hero_cards_info.grid(row=2, column=1, sticky="w", **padding)

        # Community Cards
        self.community_cards_label = tk.Label(
            self.root,
            text="Community Cards",
            font=self.fontStyle,
            bg="#171821",
            fg="white",
        )
        self.community_cards_label.grid(row=3, column=0, sticky="w", **padding)
        self.community_cards_info = tk.Text(
            self.root,
            height=1,
            width=input_width * 2,
            bg="#171821",
            fg="white",
            font=self.fontStyle,
        )
        self.community_cards_info.grid(row=3, column=1, sticky="w", **padding)

        # Board Stage
        self.board_stage_label = tk.Label(
            self.root, text="Board Stage", font=self.fontStyle, bg="#171821", fg="white"
        )
        self.board_stage_label.grid(row=4, column=0, sticky="w", **padding)
        self.board_stage_info = tk.Text(
            self.root,
            height=1,
            width=input_width,
            bg="#171821",
            fg="white",
            font=self.fontStyle,
        )
        self.board_stage_info.grid(row=4, column=1, sticky="w", **padding)

        # Total Pot Size
        self.pot_size_label = tk.Label(
            self.root,
            text="Total Pot Size",
            font=self.fontStyle,
            bg="#171821",
            fg="white",
        )
        self.pot_size_label.grid(row=5, column=0, sticky="w", **padding)
        self.pot_size_info = tk.Text(
            self.root,
            height=1,
            width=input_width,
            bg="#171821",
            fg="white",
            font=self.fontStyle,
        )
        self.pot_size_info.grid(row=5, column=1, sticky="w", **padding)

        # Dealer Position
        self.dealer_position_label = tk.Label(
            self.root,
            text="Dealer Position",
            font=self.fontStyle,
            bg="#171821",
            fg="white",
        )
        self.dealer_position_label.grid(row=6, column=0, sticky="w", **padding)
        self.dealer_position_info = tk.Text(
            self.root,
            height=1,
            width=input_width,
            bg="#171821",
            fg="white",
            font=self.fontStyle,
        )
        self.dealer_position_info.grid(row=6, column=1, sticky="w", **padding)

        # Hero Position
        self.hero_position_label = tk.Label(
            self.root,
            text="Hero Position",
            font=self.fontStyle,
            bg="#171821",
            fg="white",
        )
        self.hero_position_label.grid(row=7, column=0, sticky="w", **padding)
        self.hero_position_info = tk.Text(
            self.root,
            height=1,
            width=input_width,
            bg="#171821",
            fg="white",
            font=self.fontStyle,
        )
        self.hero_position_info.grid(row=7, column=1, sticky="w", **padding)

        # Round Count
        self.round_count_label = tk.Label(
            self.root, text="Rounds", font=self.fontStyle, bg="#171821", fg="white"
        )
        self.round_count_label.grid(row=8, column=0, sticky="w", **padding)
        self.round_count_info = tk.Text(
            self.root,
            height=1,
            width=input_width,
            bg="#171821",
            fg="white",
            font=self.fontStyle,
        )
        self.round_count_info.grid(row=8, column=1, sticky="w", **padding)

        # Tournament Information
        self.tournament_label = tk.Label(
            self.root,
            text="Tournament Info",
            font=self.fontStyle,
            bg="#171821",
            fg="white",
        )
        self.tournament_label.grid(row=9, column=0, sticky="w", **padding)
        self.tournament_info = tk.Text(
            self.root,
            height=3,
            width=input_width * 3,
            bg="#171821",
            fg="white",
            font=self.fontStyle,
        )
        self.tournament_info.grid(row=9, column=1, sticky="w", **padding)

        # Stack Analysis
        self.stack_analysis_label = tk.Label(
            self.root,
            text="Stack Analysis",
            font=self.fontStyle,
            bg="#171821",
            fg="white",
        )
        self.stack_analysis_label.grid(row=10, column=0, sticky="w", **padding)
        self.stack_analysis_info = tk.Text(
            self.root,
            height=2,
            width=input_width * 3,
            bg="#171821",
            fg="white",
            font=self.fontStyle,
        )
        self.stack_analysis_info.grid(row=10, column=1, sticky="w", **padding)

    def create_analysis_section(self, padding, analysisFont):
        """Create the analysis section."""
        # Analysis Label
        self.analysis_label = tk.Label(
            self.root,
            text="AI Analysis & Recommendations",
            font=self.fontStyle,
            bg="#171821",
            fg="#00ff00",
        )
        self.analysis_label.grid(row=11, column=0, columnspan=2, sticky="w", **padding)

        # Analysis Text Area
        self.analysis_info = scrolledtext.ScrolledText(
            self.root,
            height=10,
            width=80,
            bg="#171821",
            fg="#00ff00",
            font=analysisFont,
        )
        self.analysis_info.grid(
            row=12, column=0, columnspan=5, pady=10, padx=10, sticky="nw"
        )

    def create_opponent_analysis_section(self, padding, analysisFont):
        """Create the opponent analysis section."""
        # Opponent Analysis Label
        self.opponent_analysis_label = tk.Label(
            self.root,
            text="Opponent Range Analysis",
            font=self.fontStyle,
            bg="#171821",
            fg="#ff6600",
        )
        self.opponent_analysis_label.grid(
            row=13, column=0, columnspan=2, sticky="w", **padding
        )

        # Opponent Analysis Text Area
        self.opponent_analysis_info = scrolledtext.ScrolledText(
            self.root, height=8, width=80, bg="#171821", fg="#ff6600", font=analysisFont
        )
        self.opponent_analysis_info.grid(
            row=14, column=0, columnspan=5, pady=10, padx=10, sticky="nw"
        )

    def create_player_analysis_section(self, padding, analysisFont):
        """Create the player analysis section."""
        # Player Analysis Label
        self.player_analysis_label = tk.Label(
            self.root,
            text="Player Tendency Analysis",
            font=self.fontStyle,
            bg="#171821",
            fg="#00ffff",
        )
        self.player_analysis_label.grid(
            row=15, column=0, columnspan=2, sticky="w", **padding
        )

        # Player Analysis Text Area
        self.player_analysis_info = scrolledtext.ScrolledText(
            self.root, height=6, width=80, bg="#171821", fg="#00ffff", font=analysisFont
        )
        self.player_analysis_info.grid(
            row=16, column=0, columnspan=5, pady=10, padx=10, sticky="nw"
        )

    def create_quick_advice_section(self, padding, analysisFont):
        """Create the quick advice section."""
        # Quick Advice Label
        self.quick_advice_label = tk.Label(
            self.root,
            text="Quick Strategic Tips",
            font=self.fontStyle,
            bg="#171821",
            fg="#ffff00",
        )
        self.quick_advice_label.grid(
            row=17, column=0, columnspan=2, sticky="w", **padding
        )

        # Quick Advice Text Area
        self.quick_advice_info = scrolledtext.ScrolledText(
            self.root, height=6, width=80, bg="#171821", fg="#ffff00", font=analysisFont
        )
        self.quick_advice_info.grid(
            row=18, column=0, columnspan=5, pady=10, padx=10, sticky="nw"
        )

    def create_log_section(self, padding, analysisFont):
        """Create the log section."""
        # Log Label
        self.log_label = tk.Label(
            self.root, text="Game Log", font=self.fontStyle, bg="#171821", fg="white"
        )
        self.log_label.grid(row=19, column=0, columnspan=2, sticky="w", **padding)

        # Log Text Area
        self.log_info = scrolledtext.ScrolledText(
            self.root, height=8, width=80, bg="#171821", fg="white", font=analysisFont
        )
        self.log_info.grid(
            row=20, column=0, columnspan=5, pady=10, padx=10, sticky="nw"
        )

    def create_notifications_section(self, padding, analysisFont):
        """Create the notifications section."""
        # Notifications Label
        self.notifications_label = tk.Label(
            self.root,
            text="🔔 Live Notifications",
            font=self.fontStyle,
            bg="#171821",
            fg="#ff6b6b",
        )
        self.notifications_label.grid(
            row=21, column=0, columnspan=2, sticky="w", **padding
        )

        # Notifications Text Area
        self.notifications_info = scrolledtext.ScrolledText(
            self.root, height=4, width=80, bg="#171821", fg="#ff6b6b", font=analysisFont
        )
        self.notifications_info.grid(
            row=20, column=0, columnspan=5, pady=10, padx=10, sticky="nw"
        )

    def update_info(self):
        """Update all the information displays."""
        # Update player tree
        self.update_player_tree()

        # Update game state information
        self.update_game_state_info()

        # Update analysis
        self.update_analysis()

        # Update opponent analysis
        self.update_opponent_analysis()

        # Update player analysis
        self.update_player_analysis()

        # Update quick advice
        self.update_quick_advice()

        # Update logs
        self.update_logs()

        # Update notifications
        self.update_notifications()

    def update_player_tree(self):
        """Update the player tree view."""
        # Clear the existing content in the Treeview
        for i in self.player_tree.get_children():
            self.player_tree.delete(i)

        # Sort the player numbers
        sorted_player_numbers = sorted(self.game_state.players.keys(), key=int)

        # Populate the Treeview with new player information
        for player_number in sorted_player_numbers:
            player_info = self.game_state.players[player_number]

            # Handle 'cards' field when it is None or not a list
            cards = player_info.get("cards", [])
            cards_display = ", ".join(cards) if isinstance(cards, list) else "No Cards"

            self.player_tree.insert(
                "",
                "end",
                values=(
                    player_info.get("name", "N/A"),
                    player_info.get("status", "N/A"),
                    player_info.get("role", "N/A"),
                    cards_display,
                    "Yes" if player_info.get("turn", False) else "No",
                    player_info.get("action", ""),
                    player_info.get("amount", ""),
                    player_info.get("stack_size", ""),
                    player_info.get("play_style", ""),
                    player_info.get("exploitation_strategy", ""),
                ),
            )

    def update_game_state_info(self):
        """Update game state information."""
        # Update the number of active players
        self.total_players_info.delete("1.0", tk.END)
        self.total_players_info.insert(tk.END, str(len(self.game_state.active_players)))

        # Update the Hero player cards
        hero_cards = (
            ", ".join(self.game_state.hero_cards)
            if self.game_state.hero_cards
            else "None"
        )
        self.hero_cards_info.delete("1.0", tk.END)
        self.hero_cards_info.insert(tk.END, hero_cards)

        # Update the community cards
        community_cards = (
            ", ".join(self.game_state.community_cards)
            if self.game_state.community_cards
            else "None"
        )
        self.community_cards_info.delete("1.0", tk.END)
        self.community_cards_info.insert(tk.END, community_cards)

        # Update the board stage
        board_stage = self.game_state.current_board_stage
        self.board_stage_info.delete("1.0", tk.END)
        self.board_stage_info.insert("1.0", board_stage)

        # Configure tag styles for different board stages
        self.board_stage_info.tag_configure("pre_flop", foreground="#2968c7")
        self.board_stage_info.tag_configure("flop", foreground="#29c795")
        self.board_stage_info.tag_configure("turn", foreground="#c76f29")
        self.board_stage_info.tag_configure("river", foreground="#64c729")

        # Apply color based on board stage
        if "Pre-Flop" in board_stage:
            self.board_stage_info.tag_add("pre_flop", "1.0", "end")
        elif "Flop" in board_stage:
            self.board_stage_info.tag_add("flop", "1.0", "end")
        elif "Turn" in board_stage:
            self.board_stage_info.tag_add("turn", "1.0", "end")
        elif "River" in board_stage:
            self.board_stage_info.tag_add("river", "1.0", "end")

        # Update the total pot size
        self.pot_size_info.delete("1.0", tk.END)
        self.pot_size_info.insert(tk.END, f"${self.game_state.total_pot}")

        # Update the dealer position
        dealer_pos = (
            self.game_state.dealer_position
            if self.game_state.dealer_position != -1
            else "Unknown"
        )
        self.dealer_position_info.delete("1.0", tk.END)
        self.dealer_position_info.insert(tk.END, str(dealer_pos))

        # Update the hero position
        hero_position = self.poker_assistant.get_hero_position()
        self.hero_position_info.delete("1.0", tk.END)
        self.hero_position_info.insert(tk.END, hero_position)

        # Update the round count
        self.round_count_info.delete("1.0", tk.END)
        self.round_count_info.insert(tk.END, str(self.game_state.round_count))

        # Update tournament information
        tournament_analysis = self.game_state.get_tournament_analysis()

        if tournament_analysis["is_tournament"]:
            tournament_text = f"""Game Type: Tournament
Stage: {tournament_analysis['tournament_stage']}
Blind Level: {tournament_analysis['blind_level']}
Duration: {tournament_analysis['tournament_duration']} minutes"""

            if tournament_analysis["players_remaining"] > 0:
                tournament_text += (
                    f"\nPlayers Left: {tournament_analysis['players_remaining']}"
                )

            if tournament_analysis["prize_pool"] > 0:
                tournament_text += f"\nPrize Pool: ${tournament_analysis['prize_pool']}"
        else:
            tournament_text = "Game Type: Cash Game"

        self.tournament_info.delete("1.0", tk.END)
        self.tournament_info.insert(tk.END, tournament_text)

        # Update stack analysis
        stack_text = f"""Hero Stack/BB: {tournament_analysis['hero_stack_to_blind_ratio']}
Avg Stack/BB: {tournament_analysis['average_stack_to_blind_ratio']}
Stack Depth: {tournament_analysis.get('stack_depth', 'Unknown')}
Strategy Focus: {tournament_analysis.get('strategy_focus', 'Standard play')}"""

        self.stack_analysis_info.delete("1.0", tk.END)
        self.stack_analysis_info.insert(tk.END, stack_text)

    def update_analysis(self):
        """Update the analysis section."""
        # Get comprehensive analysis
        analysis = self.poker_assistant.get_comprehensive_analysis()

        # Create analysis text
        analysis_text = f"""
## GAME STATE ANALYSIS
Board Stage: {analysis['game_summary']['board_stage']}
Pot Size: ${analysis['game_summary']['pot_size']}
Hero Position: {analysis['game_summary']['hero_position']}
Active Players: {analysis['game_summary']['active_players']}
Current Turn: Player {analysis['game_summary']['current_turn'] if analysis['game_summary']['current_turn'] else 'None'}

## HERO HAND ANALYSIS
Cards: {', '.join(analysis['game_summary']['hero_cards']) if analysis['game_summary']['hero_cards'] else 'Not dealt yet'}
"""

        # Add hero hand analysis if available
        if "hero_hand" in analysis and "error" not in analysis["hero_hand"]:
            hero_hand = analysis["hero_hand"]
            analysis_text += f"""
Hand Notation: {hero_hand.get('hand_notation', 'Unknown')}
Hand Category: {hero_hand.get('category', 'Unknown')}
Hand Strength: {hero_hand.get('strength', 'Unknown')}
Should Play: {'Yes' if hero_hand.get('should_play', False) else 'No'}
Recommendation: {hero_hand.get('recommendation', 'Unknown').upper()}
Analysis: {hero_hand.get('analysis', 'No analysis available')}
"""
        else:
            analysis_text += "Hero Hand: No analysis available\n"

        # Add community cards
        analysis_text += f"""
## COMMUNITY CARDS
Board: {', '.join(analysis['game_summary']['community_cards']) if analysis['game_summary']['community_cards'] else 'None'}
"""

        # Add board impact analysis
        if "board_impact" in analysis and "error" not in analysis["board_impact"]:
            board_impact = analysis["board_impact"]
            analysis_text += f"""
Board Stage: {board_impact.get('stage', 'Unknown')}
Board Texture: {board_impact.get('board_description', 'Unknown')}
Action: {board_impact.get('action', 'Unknown').upper()}
Reason: {board_impact.get('reason', 'No reason provided')}
"""
            if "draws" in board_impact:
                draws = board_impact["draws"]
                analysis_text += f"Draws: {draws.get('description', 'None')}\n"

        # Add dealer position
        analysis_text += f"""
## DEALER POSITION
Player {analysis['game_summary']['dealer_position'] if analysis['game_summary']['dealer_position'] != -1 else 'Unknown'}

## STRATEGIC RECOMMENDATIONS
"""

        # Add strategic recommendations
        if "strategic_recommendations" in analysis:
            for i, rec in enumerate(analysis["strategic_recommendations"], 1):
                analysis_text += f"{i}. {rec}\n"

        self.analysis_info.delete("1.0", tk.END)
        self.analysis_info.insert(tk.END, analysis_text)

    def update_opponent_analysis(self):
        """Update the opponent analysis section."""
        # Get comprehensive analysis
        analysis = self.poker_assistant.get_comprehensive_analysis()

        opponent_text = "## OPPONENT RANGE ANALYSIS\n\n"

        if "opponent_ranges" in analysis and analysis["opponent_ranges"]:
            for player_num, range_analysis in analysis["opponent_ranges"].items():
                opponent_text += f"Player {player_num}:\n"
                opponent_text += (
                    f"  Position: {range_analysis.get('position', 'Unknown')}\n"
                )
                opponent_text += (
                    f"  Last Action: {range_analysis.get('last_action', 'Unknown')}\n"
                )
                opponent_text += f"  Likely Range: {', '.join(range_analysis.get('likely_range', []))}\n"
                opponent_text += f"  Range Description: {', '.join(range_analysis.get('range_description', []))}\n"
                opponent_text += f"  Exploitation: {', '.join(range_analysis.get('exploitation_opportunities', []))}\n\n"
        else:
            opponent_text += "No opponent analysis available yet.\n"
            opponent_text += "Waiting for opponent actions...\n"

        self.opponent_analysis_info.delete("1.0", tk.END)
        self.opponent_analysis_info.insert(tk.END, opponent_text)

    def update_player_analysis(self):
        """Update the player analysis display."""
        self.player_analysis_info.delete(1.0, tk.END)

        try:
            # Get all active players and their analysis
            active_players = []
            for i in range(1, 10):  # Check players 1-9
                player_key = f"player_{i}"
                if hasattr(self.game_state, player_key):
                    player_data = getattr(self.game_state, player_key)
                    if player_data and player_data.get("active", False):
                        player_name = f"Player {i}"
                        active_players.append(player_name)

            if not active_players:
                self.player_analysis_info.insert(
                    tk.END, "No active players detected..."
                )
                return

            analysis_text = "=== PLAYER TENDENCY ANALYSIS ===\n\n"

            for player_name in active_players:
                try:
                    summary = self.player_analyzer.get_player_summary(player_name)

                    analysis_text += f"🎯 {player_name.upper()}\n"
                    analysis_text += f"Style: {summary['playing_style']}\n"
                    analysis_text += f"VPIP: {summary['stats']['vpip']}% | PFR: {summary['stats']['pfr']}% | AF: {summary['stats']['af']}\n"
                    analysis_text += f"Hands: {summary['stats']['total_hands']} | Sessions: {summary['stats']['sessions']}\n"

                    if summary["tendencies"]:
                        analysis_text += "🔍 Tendencies:\n"
                        for tendency in summary["tendencies"]:
                            analysis_text += f"  • {tendency}\n"

                    if summary["exploitation"]:
                        analysis_text += "💡 Exploitation:\n"
                        for strategy in summary["exploitation"][:3]:  # Show top 3
                            analysis_text += f"  • {strategy}\n"

                    analysis_text += "\n" + "=" * 50 + "\n\n"

                except Exception as e:
                    analysis_text += f"⚠️ {player_name}: No data yet ({len(self.player_analyzer.player_profiles.get(player_name, {}).get('hands_played', []))} hands)\n\n"

            self.player_analysis_info.insert(tk.END, analysis_text)

        except Exception as e:
            self.player_analysis_info.insert(tk.END, f"Player analysis error: {str(e)}")

    def update_quick_advice(self):
        """Update the quick advice section."""
        advice = self.poker_assistant.provide_quick_advice()

        advice_text = f"""
Position: {advice['position']}
Board Stage: {advice['board_stage']}
Pot Size: ${advice['pot_size']}

Quick Tips:
"""

        for tip in advice["quick_tips"]:
            advice_text += f"• {tip}\n"

        self.quick_advice_info.delete("1.0", tk.END)
        self.quick_advice_info.insert(tk.END, advice_text)

    def update_logs(self):
        """Update the log section."""
        # Get the latest log entries
        log_entries = self.game_state.get_log()

        # Display the last 20 entries
        recent_logs = log_entries[-20:] if len(log_entries) > 20 else log_entries

        log_text = "\n".join(recent_logs)

        self.log_info.delete("1.0", tk.END)
        self.log_info.insert(tk.END, log_text)

    def update_notifications(self):
        """Update the notifications display."""
        self.notifications_info.delete("1.0", tk.END)

        notifications = []
        current_time = time.time()

        # Check for recent player actions (last 10 seconds)
        for player_num, player_info in self.game_state.players.items():
            if player_info.get("action") and player_info.get("action") != "None":
                action_time = player_info.get("action_time", 0)
                if action_time > 0 and action_time < 10:  # Recent action
                    action = player_info["action"]
                    amount = player_info.get("amount", 0)
                    if amount > 0:
                        notifications.append(
                            f"🎮 Player {player_num}: {action} ${amount}"
                        )
                    else:
                        notifications.append(f"🎮 Player {player_num}: {action}")

        # Check for board stage changes
        if hasattr(self.game_state, "current_board_stage"):
            board_stage = self.game_state.current_board_stage
            if board_stage and board_stage != "Unknown":
                notifications.append(f"🃏 Board Stage: {board_stage}")

        # Check for hero role changes
        if self.game_state.hero_player_number:
            hero_role = self.game_state.players.get(
                self.game_state.hero_player_number, {}
            ).get("role")
            if hero_role:
                notifications.append(f"👤 Hero Role: {hero_role}")

        # Check for pot size changes
        if self.game_state.total_pot > 0:
            notifications.append(f"💰 Pot Size: ${self.game_state.total_pot}")

        # Display notifications
        if notifications:
            notification_text = "\n".join(
                notifications[-5:]
            )  # Show last 5 notifications
        else:
            notification_text = "No recent notifications..."

        self.notifications_info.insert(tk.END, notification_text)

    def polling_update(self):
        """Update the GUI with the latest information."""
        self.update_info()
        self.root.after(
            500, self.polling_update
        )  # Update every 500ms for faster response

    def run(self):
        """Start the GUI."""
        self.root.mainloop()
