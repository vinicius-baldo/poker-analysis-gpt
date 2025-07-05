import json
import time

from colorama import Fore

from hand_strength_analyzer import HandStrengthAnalyzer


class PokerAnalyzerAssistant:

    def __init__(self, openai_client, hero_info, game_state):
        print("Initializing PokerAnalyzerAssistant...")

        self.client = openai_client
        self.hero_info = hero_info
        self.game_state = game_state
        self.hand_analyzer = HandStrengthAnalyzer()

    def analyze_game_state(self, poker_game_data):
        """Analyze the current game state and provide recommendations."""
        print(f"{Fore.YELLOW}AnalyzeGameState(): Starting analysis...")

        gpt4_output = self.analyze_game_state_with_gpt4(poker_game_data)

        print(f"{Fore.YELLOW}AnalyzeGameState(): Finished analysis...")

        if gpt4_output is not None:
            print(f"{Fore.GREEN}----------------------------------------------")
            print(f"{Fore.GREEN}GPT4 ANALYSIS:")
            print(f"{Fore.GREEN}----------------------------------------------")
            print(f"{Fore.GREEN} {gpt4_output}")
            print(f"{Fore.GREEN}----------------------------------------------")

            return self.extract_analysis_from_gpt4_output(gpt4_output)
        else:
            print(f"{Fore.RED}Failed to get analysis response in 30 seconds...")
            return None

    def create_user_prompt(self, realtime_game_data):
        """Create user prompt for GPT-4 analysis."""
        print(f"{Fore.YELLOW}Creating analysis prompt...")

        hero_round_actions_history = self.hero_info.get_recent_actions()
        hero_strategy_history = self.hero_info.get_recent_strategies()
        hero_tactics_history = self.hero_info.get_recent_tactics()

        active_player_analysis = ""
        # Loop through all players
        for player_number in range(1, 10):  # Support up to 9 players
            if player_number in self.game_state.players:
                player_info = self.game_state.players[player_number]
                player_last_action = player_info.get("action", "")

                if "Fold" not in player_last_action:
                    player_type = player_info.get("player_type", "Unknown")
                    player_strategy = player_info.get("exploitation_strategy", "None")

                    if player_strategy and "None" not in player_strategy:
                        player_data = f"#Player {player_number} Analysis:\nType: {player_type}\nExploitation Strategy:\n{player_strategy}\n"
                        active_player_analysis += (
                            player_data + "\n----------------------\n"
                        )

        # Get tournament analysis
        tournament_analysis = self.game_state.get_tournament_analysis()
        tournament_info = ""
        if tournament_analysis["is_tournament"]:
            tournament_info = f"""
                        #Tournament Information:
                        '''
                        Game Type: Tournament
                        Tournament Stage: {tournament_analysis['tournament_stage']}
                        Blind Level: {tournament_analysis['blind_level']}
                        Tournament Duration: {tournament_analysis['tournament_duration']} minutes
                        Players Remaining: {tournament_analysis['players_remaining']}
                        Prize Pool: ${tournament_analysis['prize_pool']}
                        
                        Stack Analysis:
                        - Hero Stack/BB Ratio: {tournament_analysis['hero_stack_to_blind_ratio']}
                        - Average Stack/BB Ratio: {tournament_analysis['average_stack_to_blind_ratio']}
                        - Stack Depth: {tournament_analysis.get('stack_depth', 'Unknown')}
                        - Strategy Focus: {tournament_analysis.get('strategy_focus', 'Standard play')}
                        
                        Blind Levels: SB ${tournament_analysis['small_blind']} / BB ${tournament_analysis['big_blind']}
                        '''
                        """
        else:
            tournament_info = """
                        #Game Information:
                        '''
                        Game Type: Cash Game
                        Blind Levels: Extracted from window title
                        '''
                        """

        user_prompt = f"""
                        {tournament_info}
                        ---------------------------

                        #Hero Actions History:
                        '''
                        {hero_round_actions_history}
                        '''
                        #Hero Strategy History:
                        '''
                        {hero_strategy_history}
                        '''
                        #Hero Tactics History:
                        '''
                        {hero_tactics_history}
                        '''
                        ---------------------------

                        #Player Analysis: 
                        '''
                        {active_player_analysis}
                        '''
                        ---------------------------

                        #Texas Holdem Poker Game Data:
                        '''
                        {realtime_game_data}
                        '''
                        """

        return user_prompt

    def analyze_game_state_with_gpt4(self, realtime_game_data):
        """Analyze game state using GPT-4."""
        try:
            print(f"{Fore.GREEN}Analyzing game state with GPT-4...")

            # Create the user prompt with the real-time game data
            user_message_prompt = self.create_user_prompt(realtime_game_data)

            start_time = time.time()

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"""
                        You are a professional poker analyst and coach. Your objective is to analyze real-time online poker data from a dynamic Texas Holdem game (2-9 players, Cash/Tournament) and provide strategic insights and recommendations.

                        --------------------------

                        #ANALYSIS GUIDELINES:

                        - GAME STATE ANALYSIS: Analyze the current board, pot size, position, and player actions
                        - TOURNAMENT CONSIDERATIONS: For tournaments, consider ICM, stack depth, and tournament stage
                        - STACK-TO-BLIND ANALYSIS: Evaluate stack depth and its impact on strategy
                        - PLAYER TENDENCIES: Identify patterns in opponent behavior and playing styles
                        - POSITIONAL AWARENESS: Consider the impact of position on decision making
                        - POT ODDS: Calculate and explain pot odds when relevant
                        - HAND STRENGTH: Evaluate the strength of the hero's hand relative to the board
                        - OPPONENT RANGES: Estimate what hands opponents might have based on their actions

                        --------------------------

                        #RECOMMENDATION STRUCTURE:

                        Provide your analysis in the following format:

                        ## GAME STATE ANALYSIS
                        - Board Stage: [Pre-flop/Flop/Turn/River]
                        - Pot Size: $[amount]
                        - Position: [Hero's position relative to dealer]
                        - Current Action: [What's happening now]
                        - Tournament Stage: [Early/Middle/Late/Final Table] (if applicable)
                        - Stack Depth: [Short/Medium/Deep stack analysis]

                        ## OPPONENT ANALYSIS
                        - Player Tendencies: [Describe each active opponent's style]
                        - Likely Ranges: [What hands they might have]
                        - Betting Patterns: [How they've been betting]

                        ## HERO HAND EVALUATION
                        - Hand Strength: [Evaluate hero's hand]
                        - Draw Potential: [Any draws available]
                        - Relative Strength: [How it compares to likely opponent hands]

                        ## STRATEGIC RECOMMENDATIONS
                        - Recommended Action: [Fold/Call/Raise/Check]
                        - Bet Sizing: [If raising, suggest amount]
                        - Reasoning: [Why this action is recommended]
                        - Tournament Considerations: [ICM, stack depth, stage-specific advice]
                        - Alternative Lines: [Other viable options]

                        ## RISK ASSESSMENT
                        - Pot Odds: [If calling, what odds you're getting]
                        - Implied Odds: [Future betting potential]
                        - Risk Level: [Low/Medium/High]

                        Note: Focus on providing educational insights that help improve poker understanding, not just immediate action recommendations.
                        """,
                    },
                    {"role": "user", "content": user_message_prompt},
                ],
                max_tokens=1500,
                temperature=0.7,
            )

            end_time = time.time()
            print(
                f"{Fore.GREEN}GPT-4o analysis completed in {end_time - start_time:.2f} seconds"
            )

            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
            else:
                print(f"{Fore.RED}No response received from GPT-4o")
                return None

        except Exception as e:
            print(f"{Fore.RED}Error in analyze_game_state_with_gpt4o: {e}")
            return None

    def extract_analysis_from_gpt4_output(self, gpt4_output):
        """Extract structured analysis from GPT-4 output."""
        try:
            # Parse the analysis and extract key components
            analysis_data = {
                "game_state": {},
                "opponent_analysis": {},
                "hero_evaluation": {},
                "recommendations": {},
                "risk_assessment": {},
            }

            # Extract different sections
            sections = gpt4_output.split("##")

            for section in sections:
                if "GAME STATE ANALYSIS" in section:
                    analysis_data["game_state"] = self.parse_section(section)
                elif "OPPONENT ANALYSIS" in section:
                    analysis_data["opponent_analysis"] = self.parse_section(section)
                elif "HERO HAND EVALUATION" in section:
                    analysis_data["hero_evaluation"] = self.parse_section(section)
                elif "STRATEGIC RECOMMENDATIONS" in section:
                    analysis_data["recommendations"] = self.parse_section(section)
                elif "RISK ASSESSMENT" in section:
                    analysis_data["risk_assessment"] = self.parse_section(section)

            return analysis_data

        except Exception as e:
            print(f"{Fore.RED}Error extracting analysis: {e}")
            return None

    def parse_section(self, section_text):
        """Parse a section of the analysis text."""
        lines = section_text.strip().split("\n")
        parsed_data = {}

        for line in lines:
            line = line.strip()
            if ":" in line and not line.startswith("#"):
                key, value = line.split(":", 1)
                parsed_data[key.strip()] = value.strip()

        return parsed_data

    def analyze_players_gpt4(self, historical_data):
        """Analyze player tendencies using GPT-4."""
        try:
            print(f"{Fore.YELLOW}Analyzing player tendencies...")

            formatted_data = self.format_historical_data(historical_data)

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are a poker player analyst. Analyze the provided player data and identify:
                        1. Player types (Tight-Aggressive, Loose-Passive, etc.)
                        2. Betting patterns and tendencies
                        3. Exploitation strategies for each player
                        4. Key behavioral indicators
                        
                        Return your analysis in JSON format with player numbers as keys.
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"Analyze these players: {formatted_data}",
                    },
                ],
                max_tokens=1000,
                temperature=0.5,
            )

            if response.choices and len(response.choices) > 0:
                analysis_text = response.choices[0].message.content
                return self.parse_and_update_player_analysis(analysis_text)
            else:
                print(f"{Fore.RED}No player analysis response received from GPT-4o")
                return None

        except Exception as e:
            print(f"{Fore.RED}Error in analyze_players_gpt4o: {e}")
            return None

    def format_historical_data(self, historical_data):
        """Format historical data for analysis."""
        formatted = {}
        for player_number, data in historical_data.items():
            if data:
                formatted[player_number] = {
                    "actions": data.get("actions", []),
                    "betting_patterns": data.get("betting_patterns", []),
                    "stack_changes": data.get("stack_changes", []),
                    "positions": data.get("positions", []),
                }
        return formatted

    def parse_and_update_player_analysis(self, player_analysis_json):
        """Parse and update player analysis from JSON."""
        try:
            # Try to extract JSON from the response
            json_start = player_analysis_json.find("{")
            json_end = player_analysis_json.rfind("}") + 1

            if json_start != -1 and json_end != 0:
                json_str = player_analysis_json[json_start:json_end]
                analysis_data = json.loads(json_str)

                # Update game state with player analysis
                for player_number, analysis in analysis_data.items():
                    try:
                        player_num = int(player_number)
                        self.game_state.update_player(
                            player_num,
                            player_type=analysis.get("type", "Unknown"),
                            exploitation_strategy=analysis.get(
                                "exploitation_strategy", "None"
                            ),
                        )
                    except ValueError:
                        continue

                return analysis_data
            else:
                print(f"{Fore.YELLOW}No valid JSON found in player analysis")
                return None

        except json.JSONDecodeError as e:
            print(f"{Fore.RED}JSON decode error: {e}")
            return None
        except Exception as e:
            print(f"{Fore.RED}Error parsing player analysis: {e}")
            return None

    def get_current_game_summary(self):
        """Get a summary of the current game state."""
        summary = {
            "board_stage": self.game_state.current_board_stage,
            "pot_size": self.game_state.total_pot,
            "dealer_position": self.game_state.dealer_position,
            "hero_position": self.get_hero_position(),
            "active_players": len(self.game_state.active_players),
            "hero_cards": self.game_state.hero_cards,
            "community_cards": self.game_state.community_cards,
            "current_turn": self.game_state.get_current_player_turn(),
        }
        return summary

    def get_hero_position(self):
        """Calculate hero's position relative to dealer."""
        if self.game_state.dealer_position == -1:
            return "Unknown"

        hero_pos = self.game_state.hero_player_number
        dealer_pos = self.game_state.dealer_position

        # Calculate position (1 = dealer, 2 = small blind, 3 = big blind, etc.)
        position = (hero_pos - dealer_pos) % len(self.game_state.active_players)

        positions = {
            1: "Dealer",
            2: "Small Blind",
            3: "Big Blind",
            4: "UTG",
            5: "UTG+1",
            6: "UTG+2",
        }

        return positions.get(position, f"Position {position}")

    def provide_quick_advice(self):
        """Provide quick strategic advice based on current state."""
        summary = self.get_current_game_summary()

        advice = {
            "position": summary["hero_position"],
            "board_stage": summary["board_stage"],
            "pot_size": summary["pot_size"],
            "quick_tips": [],
        }

        # Add position-based advice
        if "Blind" in summary["hero_position"]:
            advice["quick_tips"].append(
                "You're in the blinds - be more defensive with weak hands"
            )
        elif "UTG" in summary["hero_position"]:
            advice["quick_tips"].append(
                "Early position - play tighter, raise with strong hands"
            )
        elif "Dealer" in summary["hero_position"]:
            advice["quick_tips"].append(
                "Late position - you can play more hands and be more aggressive"
            )

        # Add board stage advice
        if summary["board_stage"] == "Pre-Flop":
            advice["quick_tips"].append(
                "Pre-flop - focus on position and hand strength"
            )
        elif summary["board_stage"] in ["Flop", "Turn", "River"]:
            advice["quick_tips"].append(
                f"{summary['board_stage']} - evaluate your hand strength vs the board"
            )

        return advice

    def analyze_hero_hand_strength(self):
        """Analyze hero's current hand strength"""
        summary = self.get_current_game_summary()

        if not summary["hero_cards"] or len(summary["hero_cards"]) < 2:
            return {
                "error": "No hero cards detected",
                "recommendation": "fold",
                "reason": "Cannot analyze without hole cards",
            }

        # Get hero's stack size
        hero_stack = 0
        if self.game_state.hero_player_number in self.game_state.players:
            hero_stack = self.game_state.players[
                self.game_state.hero_player_number
            ].get("stack_size", 0)

        # Get action history (simplified)
        action_history = []
        for player_num, player_info in self.game_state.players.items():
            if player_info.get("action"):
                action_history.append(player_info["action"])

        # Analyze hero hand
        hero_analysis = self.hand_analyzer.analyze_hero_hand(
            summary["hero_cards"],
            summary["hero_position"],
            hero_stack,
            summary["pot_size"],
            summary["active_players"],
            action_history,
        )

        return hero_analysis

    def analyze_opponent_ranges(self):
        """Analyze likely opponent hand ranges"""
        opponent_analyses = {}

        for player_num, player_info in self.game_state.players.items():
            if player_num == self.game_state.hero_player_number:
                continue  # Skip hero

            if player_info.get("status") == "Active":
                # Get player's position (simplified)
                position = self.estimate_player_position(player_num)

                # Get player's stack
                stack_size = player_info.get("stack_size", 0)

                # Get player's actions
                actions = []
                if player_info.get("action"):
                    actions.append(player_info["action"])

                # Analyze opponent range
                range_analysis = self.hand_analyzer.analyze_opponent_range(
                    actions,
                    position,
                    stack_size,
                    self.game_state.total_pot,
                    len(self.game_state.active_players),
                )

                opponent_analyses[player_num] = range_analysis

        return opponent_analyses

    def estimate_player_position(self, player_num):
        """Estimate a player's position based on their number and dealer position"""
        if self.game_state.dealer_position == -1:
            return "Unknown"

        # Calculate position relative to dealer
        dealer_pos = self.game_state.dealer_position
        player_pos = player_num

        # Calculate relative position
        relative_pos = (player_pos - dealer_pos) % len(self.game_state.active_players)

        positions = {
            1: "Dealer",
            2: "SB",
            3: "BB",
            4: "UTG",
            5: "UTG+1",
            6: "UTG+2",
            7: "LJ",
            8: "HJ",
            9: "CO",
        }

        return positions.get(relative_pos, f"Pos{relative_pos}")

    def analyze_board_impact(self):
        """Analyze how the board affects hand strength"""
        summary = self.get_current_game_summary()

        if not summary["hero_cards"]:
            return {"error": "No hero cards", "stage": "pre_flop", "impact": "unknown"}

        # Get hero's position
        hero_position = summary["hero_position"]

        # Analyze board impact
        board_analysis = self.hand_analyzer.analyze_board_impact(
            summary["hero_cards"], summary["community_cards"], hero_position
        )

        return board_analysis

    def get_comprehensive_analysis(self):
        """Get comprehensive analysis including hand strength, opponent ranges, and board impact"""

        analysis = {
            "hero_hand": self.analyze_hero_hand_strength(),
            "opponent_ranges": self.analyze_opponent_ranges(),
            "board_impact": self.analyze_board_impact(),
            "game_summary": self.get_current_game_summary(),
            "quick_advice": self.provide_quick_advice(),
        }

        # Add strategic recommendations
        analysis["strategic_recommendations"] = self.generate_strategic_recommendations(
            analysis
        )

        return analysis

    def generate_strategic_recommendations(self, analysis):
        """Generate strategic recommendations based on comprehensive analysis"""

        recommendations = []

        # Hero hand recommendations
        hero_hand = analysis["hero_hand"]
        if "recommendation" in hero_hand:
            if hero_hand["recommendation"] == "fold":
                recommendations.append("Fold - Hand too weak for current situation")
            elif hero_hand["recommendation"] == "raise":
                recommendations.append("Raise - Strong hand, build the pot")
            elif hero_hand["recommendation"] == "call":
                recommendations.append("Call - Decent hand, see more cards")
            elif hero_hand["recommendation"] == "all_in":
                recommendations.append("All-in - Premium hand, maximize value")

        # Position-based recommendations
        position = analysis["game_summary"]["hero_position"]
        if "UTG" in position or "UTG+1" in position or "UTG+2" in position:
            recommendations.append("Early position - play tight, only strong hands")
        elif "BTN" in position or "CO" in position:
            recommendations.append("Late position - can play wider range")
        elif "Blind" in position:
            recommendations.append("Blind position - defend with wider range")

        # Board-based recommendations
        board_impact = analysis["board_impact"]
        if "stage" in board_impact:
            if board_impact["stage"] == "flop":
                recommendations.append("Flop - evaluate hand strength vs board")
            elif board_impact["stage"] == "turn":
                recommendations.append("Turn - reassess hand strength")
            elif board_impact["stage"] == "river":
                recommendations.append("River - final decision, maximize value")

        # Opponent-based recommendations
        opponent_ranges = analysis["opponent_ranges"]
        tight_opponents = 0
        loose_opponents = 0

        for player_num, range_analysis in opponent_ranges.items():
            if "premium" in range_analysis.get("likely_range", []):
                tight_opponents += 1
            elif "speculative" in range_analysis.get(
                "likely_range", []
            ) or "weak" in range_analysis.get("likely_range", []):
                loose_opponents += 1

        if tight_opponents > loose_opponents:
            recommendations.append("Tight table - bluff more, value bet less")
        elif loose_opponents > tight_opponents:
            recommendations.append("Loose table - value bet more, bluff less")

        return recommendations
