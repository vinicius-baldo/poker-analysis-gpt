import re

from poker_hand_chart import (analyze_board_texture,
                              get_hand_action_recommendation,
                              get_hand_category, get_hand_rank,
                              get_hand_strength, get_post_flop_recommendation,
                              should_play_hand)


class HandStrengthAnalyzer:

    def __init__(self):
        self.rank_order = "AKQJT98765432"
        self.suits = ["h", "d", "c", "s"]  # hearts, diamonds, clubs, spades

    def parse_cards(self, cards_list):
        """Parse a list of card strings into structured format"""
        parsed_cards = []

        for card in cards_list:
            if len(card) >= 2:
                rank = card[0].upper()
                suit = card[1].lower()

                if rank in self.rank_order and suit in self.suits:
                    parsed_cards.append(
                        {"rank": rank, "suit": suit, "full": card.upper()}
                    )

        return parsed_cards

    def get_hand_notation(self, hero_cards):
        """Convert hero cards to poker hand notation (e.g., 'AKs', 'TTo')"""
        if len(hero_cards) != 2:
            return None

        card1, card2 = hero_cards[0], hero_cards[1]

        # Get ranks
        rank1, rank2 = card1["rank"], card2["rank"]

        # Determine order (higher rank first)
        rank1_idx = self.rank_order.index(rank1)
        rank2_idx = self.rank_order.index(rank2)

        if rank1_idx < rank2_idx:  # rank1 is higher
            high_rank, low_rank = rank1, rank2
        else:
            high_rank, low_rank = rank2, rank1

        # Check if suited
        if card1["suit"] == card2["suit"]:
            return f"{high_rank}{low_rank}s"  # suited
        else:
            return f"{high_rank}{low_rank}o"  # offsuit

    def analyze_hero_hand(
        self, hero_cards, position, stack_size, pot_size, num_players, action_history
    ):
        """Comprehensive analysis of hero's hand"""

        if not hero_cards or len(hero_cards) < 2:
            return {
                "error": "Invalid hero cards",
                "recommendation": "fold",
                "reason": "No valid hole cards detected",
            }

        # Parse cards
        parsed_cards = self.parse_cards(hero_cards)
        if len(parsed_cards) < 2:
            return {
                "error": "Invalid card format",
                "recommendation": "fold",
                "reason": "Cards not in valid format",
            }

        # Get hand notation
        hand_notation = self.get_hand_notation(parsed_cards)
        if not hand_notation:
            return {
                "error": "Could not determine hand notation",
                "recommendation": "fold",
                "reason": "Invalid hand format",
            }

        # Get hand strength and category
        strength = get_hand_strength(hand_notation)
        category = get_hand_category(hand_notation)
        rank = get_hand_rank(hand_notation)

        # Determine if hand should be played
        should_play = should_play_hand(
            hand_notation, position, stack_size, pot_size, num_players
        )

        # Get action recommendation
        action = get_hand_action_recommendation(
            hand_notation, position, stack_size, pot_size, num_players, action_history
        )

        # Calculate pot odds if applicable
        pot_odds = self.calculate_pot_odds(pot_size, stack_size, action_history)

        # Get position-based insights
        position_insights = self.get_position_insights(position, num_players)

        return {
            "hand_notation": hand_notation,
            "cards": [card["full"] for card in parsed_cards],
            "strength": strength,
            "category": category,
            "rank": rank,
            "should_play": should_play,
            "recommendation": action,
            "pot_odds": pot_odds,
            "position_insights": position_insights,
            "analysis": self.get_hand_analysis(
                hand_notation, category, position, num_players
            ),
        }

    def analyze_opponent_range(
        self, opponent_actions, position, stack_size, pot_size, num_players
    ):
        """Analyze likely opponent hand ranges based on actions"""

        # Define typical ranges by position and action
        position_ranges = {
            "UTG": {
                "raise": ["premium", "strong"],
                "call": ["premium", "strong", "medium"],
                "fold": ["speculative", "weak", "trash"],
            },
            "UTG+1": {
                "raise": ["premium", "strong"],
                "call": ["premium", "strong", "medium"],
                "fold": ["speculative", "weak", "trash"],
            },
            "UTG+2": {
                "raise": ["premium", "strong", "medium"],
                "call": ["premium", "strong", "medium", "speculative"],
                "fold": ["weak", "trash"],
            },
            "LJ": {
                "raise": ["premium", "strong", "medium"],
                "call": ["premium", "strong", "medium", "speculative"],
                "fold": ["weak", "trash"],
            },
            "HJ": {
                "raise": ["premium", "strong", "medium"],
                "call": ["premium", "strong", "medium", "speculative"],
                "fold": ["weak", "trash"],
            },
            "CO": {
                "raise": ["premium", "strong", "medium", "speculative"],
                "call": ["premium", "strong", "medium", "speculative", "weak"],
                "fold": ["trash"],
            },
            "BTN": {
                "raise": ["premium", "strong", "medium", "speculative", "weak"],
                "call": ["premium", "strong", "medium", "speculative", "weak"],
                "fold": ["trash"],
            },
            "SB": {
                "raise": ["premium", "strong", "medium", "speculative"],
                "call": ["premium", "strong", "medium", "speculative", "weak"],
                "fold": ["trash"],
            },
            "BB": {
                "raise": ["premium", "strong", "medium"],
                "call": ["premium", "strong", "medium", "speculative", "weak"],
                "fold": ["trash"],
            },
        }

        # Get last action
        last_action = "fold"  # default
        if opponent_actions:
            last_action = opponent_actions[-1].lower()
            if "raise" in last_action:
                last_action = "raise"
            elif "call" in last_action:
                last_action = "call"
            elif "check" in last_action:
                last_action = "call"  # treat check as call for range analysis
            else:
                last_action = "fold"

        # Get likely range
        likely_range = position_ranges.get(position, {}).get(last_action, ["unknown"])

        # Adjust range based on bet sizing
        range_adjustment = self.adjust_range_by_bet_sizing(
            opponent_actions, likely_range
        )

        return {
            "position": position,
            "last_action": last_action,
            "likely_range": likely_range,
            "adjusted_range": range_adjustment,
            "range_description": self.describe_range(likely_range),
            "exploitation_opportunities": self.get_exploitation_opportunities(
                likely_range, position
            ),
        }

    def analyze_board_impact(self, hero_cards, community_cards, position):
        """Analyze how the board affects hero's hand strength"""

        if not community_cards:
            return {
                "stage": "pre_flop",
                "texture": None,
                "hero_equity": "unknown",
                "recommendation": "continue_analysis",
            }

        # Analyze board texture
        texture = analyze_board_texture(community_cards)

        # Get post-flop recommendation
        if len(community_cards) >= 3:
            action, reason = get_post_flop_recommendation(
                hero_cards, community_cards, 0, 0, position, []
            )
        else:
            action, reason = "continue", "Pre-flop or early street"

        # Determine board stage
        if len(community_cards) == 3:
            stage = "flop"
        elif len(community_cards) == 4:
            stage = "turn"
        elif len(community_cards) == 5:
            stage = "river"
        else:
            stage = "pre_flop"

        # Analyze draws and outs
        draws_analysis = self.analyze_draws(hero_cards, community_cards)

        return {
            "stage": stage,
            "texture": texture,
            "action": action,
            "reason": reason,
            "draws": draws_analysis,
            "board_description": self.describe_board(community_cards, texture),
        }

    def calculate_pot_odds(self, pot_size, stack_size, action_history):
        """Calculate pot odds for calling decisions"""

        if not action_history:
            return {
                "pot_odds": 0,
                "implied_odds": 0,
                "call_profitable": False,
                "description": "No action to calculate odds",
            }

        # Find the last bet/raise amount
        last_bet = 0
        for action in reversed(action_history):
            if "raise" in action.lower() or "bet" in action.lower():
                # Extract amount from action string
                amount_match = re.search(r"\$(\d+(?:\.\d+)?)", action)
                if amount_match:
                    last_bet = float(amount_match.group(1))
                    break

        if last_bet == 0:
            return {
                "pot_odds": 0,
                "implied_odds": 0,
                "call_profitable": False,
                "description": "No bet amount found",
            }

        # Calculate pot odds
        pot_odds = pot_size / last_bet if last_bet > 0 else 0

        # Calculate implied odds (simplified)
        implied_odds = (pot_size + stack_size * 0.5) / last_bet if last_bet > 0 else 0

        # Determine if call is profitable (simplified rule)
        call_profitable = pot_odds > 3  # Need 3:1 odds to call

        return {
            "pot_odds": round(pot_odds, 2),
            "implied_odds": round(implied_odds, 2),
            "call_profitable": call_profitable,
            "description": f"Pot odds: {pot_odds:.1f}:1, Call profitable: {call_profitable}",
        }

    def get_position_insights(self, position, num_players):
        """Get insights about the current position"""

        position_insights = {
            "UTG": {
                "description": "Under the Gun - First to act",
                "strategy": "Play very tight, only premium hands",
                "advantages": "Can set the tone for the hand",
                "disadvantages": "No information about other players",
            },
            "UTG+1": {
                "description": "Under the Gun +1",
                "strategy": "Play tight, mostly premium and strong hands",
                "advantages": "Some information from UTG",
                "disadvantages": "Still early position",
            },
            "UTG+2": {
                "description": "Under the Gun +2",
                "strategy": "Can play some medium hands",
                "advantages": "More information from previous players",
                "disadvantages": "Still early position",
            },
            "LJ": {
                "description": "Lojack",
                "strategy": "Can play medium hands, some speculative",
                "advantages": "Good position, can steal blinds",
                "disadvantages": "Still vulnerable to late position",
            },
            "HJ": {
                "description": "Hijack",
                "strategy": "Can play wider range, including speculative",
                "advantages": "Strong position, can steal blinds",
                "disadvantages": "Vulnerable to button and blinds",
            },
            "CO": {
                "description": "Cutoff",
                "strategy": "Play wide range, steal frequently",
                "advantages": "Excellent position, can steal blinds",
                "disadvantages": "Vulnerable to button",
            },
            "BTN": {
                "description": "Button",
                "strategy": "Play very wide range, steal aggressively",
                "advantages": "Best position, last to act post-flop",
                "disadvantages": "None significant",
            },
            "SB": {
                "description": "Small Blind",
                "strategy": "Defend wide, 3-bet frequently",
                "advantages": "Good position post-flop, already invested",
                "disadvantages": "Out of position to big blind",
            },
            "BB": {
                "description": "Big Blind",
                "strategy": "Defend wide, check-raise frequently",
                "advantages": "Already invested, can check-raise",
                "disadvantages": "Out of position to everyone",
            },
        }

        return position_insights.get(
            position,
            {
                "description": "Unknown position",
                "strategy": "Play tight",
                "advantages": "None",
                "disadvantages": "Unknown",
            },
        )

    def get_hand_analysis(self, hand_notation, category, position, num_players):
        """Get detailed analysis of the hand"""

        analysis = {
            "pre_flop": {
                "premium": "Excellent starting hand. Play aggressively in any position.",
                "strong": "Very good starting hand. Play aggressively in most positions.",
                "medium": "Decent starting hand. Play in good position or against weak opponents.",
                "speculative": "Speculative hand. Play in good position with deep stacks.",
                "weak": "Weak hand. Fold in early position, play only in very good position.",
                "trash": "Very weak hand. Fold in most situations.",
            }
        }

        base_analysis = analysis["pre_flop"].get(category, "Unknown hand category")

        # Add position-specific advice
        if position in ["UTG", "UTG+1", "UTG+2"] and category not in [
            "premium",
            "strong",
        ]:
            base_analysis += " Fold in early position."
        elif position in ["BTN", "CO"] and category in ["medium", "speculative"]:
            base_analysis += " Can play in late position."
        elif position in ["SB", "BB"] and category in ["medium", "speculative", "weak"]:
            base_analysis += " Can defend in blinds."

        # Add player count advice
        if num_players <= 3:
            base_analysis += " Short-handed - can play wider."
        elif num_players >= 7:
            base_analysis += " Full ring - play tighter."

        return base_analysis

    def adjust_range_by_bet_sizing(self, actions, base_range):
        """Adjust opponent range based on bet sizing"""

        # This is a simplified version - in practice, this would be much more sophisticated
        if not actions:
            return base_range

        last_action = actions[-1].lower()

        # Large bets/raises suggest stronger hands
        if "raise" in last_action and any(
            "$" + str(amt) in last_action for amt in ["50", "100", "200"]
        ):
            return [cat for cat in base_range if cat in ["premium", "strong"]]

        # Small bets suggest weaker hands or bluffs
        if "raise" in last_action and any(
            "$" + str(amt) in last_action for amt in ["5", "10", "15"]
        ):
            return base_range + ["speculative"]

        return base_range

    def describe_range(self, range_categories):
        """Describe a range in human-readable terms"""

        descriptions = {
            "premium": "Premium hands (AA, KK, QQ, AK)",
            "strong": "Strong hands (JJ, TT, AQ, AJ)",
            "medium": "Medium hands (99, 88, AT, KJ)",
            "speculative": "Speculative hands (suited connectors, small pairs)",
            "weak": "Weak hands (small pairs, suited aces)",
            "trash": "Trash hands (most offsuit combinations)",
        }

        return [descriptions.get(cat, cat) for cat in range_categories]

    def get_exploitation_opportunities(self, range_categories, position):
        """Get exploitation opportunities against a range"""

        opportunities = []

        if "premium" in range_categories:
            opportunities.append("Tight range - can bluff more frequently")

        if "speculative" in range_categories or "weak" in range_categories:
            opportunities.append("Loose range - value bet more, bluff less")

        if position in ["BTN", "CO"] and "premium" not in range_categories:
            opportunities.append("Can steal blinds with wider range")

        if "trash" in range_categories:
            opportunities.append("Very loose range - exploit with value betting")

        return opportunities if opportunities else ["Standard play recommended"]

    def analyze_draws(self, hero_cards, community_cards):
        """Analyze potential draws for the hero"""

        if not hero_cards or len(hero_cards) < 2:
            return {"draws": [], "outs": 0, "description": "No hole cards"}

        if not community_cards or len(community_cards) < 3:
            return {"draws": [], "outs": 0, "description": "Pre-flop - no draws yet"}

        draws = []
        outs = 0

        # Analyze flush draws
        hero_suits = [card["suit"] for card in hero_cards]
        community_suits = [card["suit"] for card in community_cards]

        for suit in set(hero_suits):
            if hero_suits.count(suit) == 2:  # Hero has suited cards
                suit_count = community_suits.count(suit)
                if suit_count == 1:
                    draws.append("flush_draw")
                    outs += 9  # 9 remaining cards of that suit
                elif suit_count == 2:
                    draws.append("flush_draw")
                    outs += 8  # 8 remaining cards of that suit

        # Analyze straight draws
        all_ranks = [card["rank"] for card in hero_cards + community_cards]
        rank_values = [self.rank_order.index(rank) for rank in all_ranks]
        rank_values.sort()

        # Check for open-ended straight draws
        for i in range(len(rank_values) - 3):
            if rank_values[i + 3] - rank_values[i] == 3:
                draws.append("open_ended_straight_draw")
                outs += 8  # 8 cards to complete straight

        # Check for gutshot straight draws
        for i in range(len(rank_values) - 3):
            if rank_values[i + 3] - rank_values[i] == 4:
                draws.append("gutshot_straight_draw")
                outs += 4  # 4 cards to complete straight

        return {
            "draws": draws,
            "outs": outs,
            "description": f"Draws: {', '.join(draws) if draws else 'None'}, Outs: {outs}",
        }

    def describe_board(self, community_cards, texture):
        """Describe the board texture in human-readable terms"""

        if not community_cards:
            return "Pre-flop"

        descriptions = []

        if texture.get("paired", False):
            descriptions.append("Paired board")

        if texture.get("suited", False):
            descriptions.append("Suited board")

        if texture.get("connected", False):
            descriptions.append("Connected board")

        high_cards = texture.get("high_cards", 0)
        if high_cards >= 2:
            descriptions.append(f"High card board ({high_cards} high cards)")

        if not descriptions:
            descriptions.append("Dry board")

        return ", ".join(descriptions)
