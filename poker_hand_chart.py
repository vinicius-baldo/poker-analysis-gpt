# poker_hand_chart.py

# The matrix values from the chart (manually extracted)
hand_chart_matrix = [
    # A   K    Q    J    T    9    8    7    6    5    4    3    2
    ["∞", 277, 137, 92, 70, 52, 45, 40, 36, 35, 35, 33, 31],  # A
    [166, 477, 43, 36, 31, 24, 20, 19, 16, 15, 14, 13, 13],  # K
    [96, 29, 239, 25, 22, 16, 13, 11, 9, 9, 8, 7, 7],  # Q
    [68, 25, 16, 160, 18, 13, 10, 9, 7, 7, 6, 6, 5],  # J
    [23, 15, 12, 10, 120, 11, 9, 7, 6, 5, 4, 3, 2],  # T
    [14, 12, 9, 7, 8, 96, 8, 6, 5, 4, 3, 2, 2],  # 9
    [36, 15, 10, 7, 6, 5, 80, 6, 5, 4, 3, 2, 2],  # 8
    [31, 15, 9, 6, 6, 5, 5, 67, 5, 4, 3, 2, 2],  # 7
    [28, 13, 8, 5, 4, 4, 4, 3, 48, 3, 3, 2, 1],  # 6
    [28, 13, 8, 5, 4, 3, 3, 2, 2, 49, 2, 2, 1],  # 5
    [26, 11, 7, 4, 3, 3, 3, 2, 2, 2, 41, 2, 1],  # 4
    [24, 10, 6, 3, 2, 2, 2, 2, 1, 2, 2, 33, 1],  # 3
    [23, 10, 6, 3, 2, 2, 2, 1, 1, 1, 1, 1, 24],  # 2
]

ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

# Create a lookup dict
hand_strength = {}

for i, r1 in enumerate(ranks):
    for j, r2 in enumerate(ranks):
        value = hand_chart_matrix[i][j]
        if i == j:
            key = f"{r1}{r2}"  # Pair: AA, KK, ...
        elif i < j:
            key = f"{r1}{r2}s"  # Suited: AKs, KQs, ...
        else:
            key = f"{r2}{r1}o"  # Offsuit: AKo, KQo, ...
        hand_strength[key] = value


def get_hand_strength(hand: str):
    """Return strength score for a given starting hand (e.g., 'AKs', 'TTo', 'QJo')"""
    return hand_strength.get(hand.upper(), "Invalid hand")


# Hand categories for easier analysis
hand_categories = {
    "premium": ["AA", "KK", "QQ", "AKs", "AKo"],
    "strong": ["JJ", "TT", "AQs", "AQo", "AJs", "KQs"],
    "medium": ["99", "88", "ATs", "AJo", "KJs", "KQo", "QJs"],
    "speculative": [
        "77",
        "66",
        "A9s",
        "A8s",
        "A7s",
        "A6s",
        "A5s",
        "A4s",
        "A3s",
        "A2s",
        "KTs",
        "KJo",
        "QTs",
        "QJo",
        "JTs",
    ],
    "weak": [
        "55",
        "44",
        "33",
        "22",
        "K9s",
        "K8s",
        "K7s",
        "K6s",
        "K5s",
        "K4s",
        "K3s",
        "K2s",
        "Q9s",
        "Q8s",
        "Q7s",
        "Q6s",
        "Q5s",
        "Q4s",
        "Q3s",
        "Q2s",
        "J9s",
        "J8s",
        "J7s",
        "J6s",
        "J5s",
        "J4s",
        "J3s",
        "J2s",
        "T9s",
        "T8s",
        "T7s",
        "T6s",
        "T5s",
        "T4s",
        "T3s",
        "T2s",
        "98s",
        "97s",
        "96s",
        "95s",
        "94s",
        "93s",
        "92s",
        "87s",
        "86s",
        "85s",
        "84s",
        "83s",
        "82s",
        "76s",
        "75s",
        "74s",
        "73s",
        "72s",
        "65s",
        "64s",
        "63s",
        "62s",
        "54s",
        "53s",
        "52s",
        "43s",
        "42s",
        "32s",
    ],
    "trash": [
        "K9o",
        "K8o",
        "K7o",
        "K6o",
        "K5o",
        "K4o",
        "K3o",
        "K2o",
        "Q9o",
        "Q8o",
        "Q7o",
        "Q6o",
        "Q5o",
        "Q4o",
        "Q3o",
        "Q2o",
        "J9o",
        "J8o",
        "J7o",
        "J6o",
        "J5o",
        "J4o",
        "J3o",
        "J2o",
        "T9o",
        "T8o",
        "T7o",
        "T6o",
        "T5o",
        "T4o",
        "T3o",
        "T2o",
        "98o",
        "97o",
        "96o",
        "95o",
        "94o",
        "93o",
        "92o",
        "87o",
        "86o",
        "85o",
        "84o",
        "83o",
        "82o",
        "76o",
        "75o",
        "74o",
        "73o",
        "72o",
        "65o",
        "64o",
        "63o",
        "62o",
        "54o",
        "53o",
        "52o",
        "43o",
        "42o",
        "32o",
    ],
}


def get_hand_category(hand: str):
    """Return the category of a given hand"""
    hand_upper = hand.upper()
    for category, hands in hand_categories.items():
        if hand_upper in hands:
            return category
    return "unknown"


def get_hand_rank(hand: str):
    """Return a numerical rank for hand strength (higher = stronger)"""
    strength = get_hand_strength(hand)
    if strength == "Invalid hand":
        return 0
    if strength == "∞":
        return 1000  # Aces
    return strength


def compare_hands(hand1: str, hand2: str):
    """Compare two hands and return which is stronger"""
    rank1 = get_hand_rank(hand1)
    rank2 = get_hand_rank(hand2)

    if rank1 > rank2:
        return 1  # hand1 is stronger
    elif rank2 > rank1:
        return -1  # hand2 is stronger
    else:
        return 0  # equal strength


def get_position_adjusted_range(position: str, stack_size: float, pot_size: float):
    """Get recommended hands to play based on position and stack/pot ratios"""

    # Base ranges by position
    position_ranges = {
        "UTG": ["premium", "strong"],
        "UTG+1": ["premium", "strong", "medium"],
        "UTG+2": ["premium", "strong", "medium"],
        "LJ": ["premium", "strong", "medium", "speculative"],
        "HJ": ["premium", "strong", "medium", "speculative"],
        "CO": ["premium", "strong", "medium", "speculative", "weak"],
        "BTN": ["premium", "strong", "medium", "speculative", "weak"],
        "SB": ["premium", "strong", "medium", "speculative", "weak"],
        "BB": ["premium", "strong", "medium", "speculative", "weak", "trash"],
    }

    # Adjust based on stack to pot ratio
    spr = stack_size / pot_size if pot_size > 0 else 10

    if spr < 3:  # Short stack - play tighter
        if position in ["UTG", "UTG+1", "UTG+2"]:
            return ["premium"]
        elif position in ["LJ", "HJ"]:
            return ["premium", "strong"]
        else:
            return ["premium", "strong", "medium"]
    elif spr > 20:  # Deep stack - can play wider
        return position_ranges.get(position, ["premium", "strong"])
    else:  # Normal stack
        return position_ranges.get(position, ["premium", "strong", "medium"])


def should_play_hand(
    hand: str, position: str, stack_size: float, pot_size: float, num_players: int
):
    """Determine if a hand should be played in given situation"""

    # Get recommended range for position
    recommended_categories = get_position_adjusted_range(position, stack_size, pot_size)

    # Check if hand is in recommended range
    hand_category = get_hand_category(hand)

    if hand_category in recommended_categories:
        # Additional adjustments based on number of players
        if num_players <= 3:  # Short-handed - play wider
            return True
        elif num_players >= 7:  # Full ring - play tighter
            if hand_category in ["premium", "strong"]:
                return True
            elif hand_category == "medium" and position in ["BTN", "CO", "SB", "BB"]:
                return True
            else:
                return False
        else:  # 4-6 players (short-handed)
            return True

    return False


def get_hand_action_recommendation(
    hand: str,
    position: str,
    stack_size: float,
    pot_size: float,
    num_players: int,
    action_history: list,
):
    """Get specific action recommendation for a hand"""

    if not should_play_hand(hand, position, stack_size, pot_size, num_players):
        return "fold"

    hand_category = get_hand_category(hand)
    spr = stack_size / pot_size if pot_size > 0 else 10

    # Premium hands - always raise
    if hand_category == "premium":
        if spr < 5:
            return "all_in"
        else:
            return "raise"

    # Strong hands - raise or call depending on position
    elif hand_category == "strong":
        if position in ["BTN", "CO", "SB"]:
            return "raise"
        elif position in ["BB"] and action_history == []:  # No action yet
            return "check"
        else:
            return "call"

    # Medium hands - position dependent
    elif hand_category == "medium":
        if position in ["BTN", "CO"]:
            return "raise"
        elif position in ["SB", "BB"] and action_history == []:
            return "check"
        else:
            return "fold"

    # Speculative hands - mostly fold unless in good position
    elif hand_category == "speculative":
        if position in ["BTN", "CO"] and num_players <= 4:
            return "raise"
        elif position in ["SB", "BB"] and action_history == []:
            return "check"
        else:
            return "fold"

    # Weak and trash hands - mostly fold
    else:
        if position in ["BB"] and action_history == []:
            return "check"
        else:
            return "fold"


def analyze_board_texture(community_cards: list):
    """Analyze the texture of the board"""
    if not community_cards or len(community_cards) < 3:
        return "pre_flop"

    # Extract ranks and suits
    ranks = []
    suits = []

    for card in community_cards:
        if len(card) >= 2:
            ranks.append(card[0])
            suits.append(card[1])

    # Analyze texture
    texture_analysis = {
        "paired": len(set(ranks)) < len(ranks),
        "suited": len(set(suits)) <= 2,  # 2 or fewer suits
        "connected": False,
        "high_cards": 0,
        "low_cards": 0,
    }

    # Check for connected cards
    rank_values = []
    for rank in ranks:
        if rank == "A":
            rank_values.append(14)
        elif rank == "K":
            rank_values.append(13)
        elif rank == "Q":
            rank_values.append(12)
        elif rank == "J":
            rank_values.append(11)
        elif rank == "T":
            rank_values.append(10)
        else:
            rank_values.append(int(rank))

    rank_values.sort()
    for i in range(len(rank_values) - 1):
        if rank_values[i + 1] - rank_values[i] <= 2:
            texture_analysis["connected"] = True
            break

    # Count high vs low cards
    for rank in ranks:
        if rank in ["A", "K", "Q", "J"]:
            texture_analysis["high_cards"] += 1
        else:
            texture_analysis["low_cards"] += 1

    return texture_analysis


def get_post_flop_recommendation(
    hero_cards: list,
    community_cards: list,
    pot_size: float,
    stack_size: float,
    position: str,
    action_history: list,
):
    """Get post-flop action recommendation"""

    if not hero_cards or len(hero_cards) < 2:
        return "fold", "No hole cards detected"

    # Analyze board texture
    board_texture = analyze_board_texture(community_cards)

    # Simple hand strength evaluation (this could be much more sophisticated)
    hero_ranks = [card[0] for card in hero_cards]
    community_ranks = [card[0] for card in community_cards] if community_cards else []

    # Check for pairs, trips, etc.
    all_ranks = hero_ranks + community_ranks
    rank_counts = {}
    for rank in all_ranks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1

    # Determine hand strength
    max_count = max(rank_counts.values()) if rank_counts else 0

    if max_count >= 4:
        hand_strength = "quads"
    elif max_count == 3:
        hand_strength = "trips"
    elif max_count == 2 and list(rank_counts.values()).count(2) >= 2:
        hand_strength = "two_pair"
    elif max_count == 2:
        hand_strength = "pair"
    else:
        hand_strength = "high_card"

    # Action recommendations based on hand strength and position
    if hand_strength in ["quads", "trips"]:
        if position in ["BTN", "CO"]:
            return "raise", f"Strong hand ({hand_strength}) in good position"
        else:
            return "call", f"Strong hand ({hand_strength}) - call to build pot"

    elif hand_strength == "two_pair":
        if position in ["BTN", "CO", "SB"]:
            return "raise", f"Two pair in good position"
        else:
            return "call", f"Two pair - call to see more cards"

    elif hand_strength == "pair":
        # Check if it's top pair or better
        if community_cards:
            highest_community = max(
                community_ranks, key=lambda x: "AKQJT98765432".index(x)
            )
            if any(rank >= highest_community for rank in hero_ranks):
                if position in ["BTN", "CO"]:
                    return "raise", "Top pair in good position"
                else:
                    return "call", "Top pair - call to see more cards"
            else:
                return "fold", "Weak pair - likely behind"
        else:
            return "fold", "Weak pair with no community cards"

    else:  # high card
        return "fold", "No made hand - fold"


# Should return "fold"
