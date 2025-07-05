import json
import os
from collections import defaultdict, deque
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple


class PlayerStyle(Enum):
    """Player playing style classifications"""

    UNKNOWN = "Unknown"
    TIGHT_PASSIVE = "Tight-Passive"
    TIGHT_AGGRESSIVE = "Tight-Aggressive"
    LOOSE_PASSIVE = "Loose-Passive"
    LOOSE_AGGRESSIVE = "Loose-Aggressive"
    MANIAC = "Maniac"
    NIT = "Nit"
    CALLING_STATION = "Calling Station"
    ROCK = "Rock"


class PlayerPosition(Enum):
    """Player position classifications"""

    EARLY = "Early"
    MIDDLE = "Middle"
    LATE = "Late"
    BLINDS = "Blinds"


class PlayerAnalyzer:
    """
    Analyzes player behavior and tendencies to create player profiles
    """

    def __init__(self, data_file="player_profiles.json"):
        self.data_file = data_file
        self.player_profiles = self.load_profiles()
        self.current_session = {}
        self.session_start_time = datetime.now()

    def load_profiles(self) -> Dict:
        """Load existing player profiles from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_profiles(self):
        """Save player profiles to file"""
        with open(self.data_file, "w") as f:
            json.dump(self.player_profiles, f, indent=2, default=str)

    def get_or_create_profile(self, player_name: str) -> Dict:
        """Get existing profile or create new one"""
        if player_name not in self.player_profiles:
            self.player_profiles[player_name] = {
                "name": player_name,
                "first_seen": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "total_hands": 0,
                "total_sessions": 0,
                "vpip": 0,  # Voluntarily Put Money In Pot
                "pfr": 0,  # Pre-Flop Raise
                "af": 0,  # Aggression Factor
                "hands_played": [],
                "actions": {
                    "fold": 0,
                    "check": 0,
                    "call": 0,
                    "bet": 0,
                    "raise": 0,
                    "all_in": 0,
                },
                "position_stats": {
                    "early": {"hands": 0, "actions": defaultdict(int)},
                    "middle": {"hands": 0, "actions": defaultdict(int)},
                    "late": {"hands": 0, "actions": defaultdict(int)},
                    "blinds": {"hands": 0, "actions": defaultdict(int)},
                },
                "betting_patterns": {
                    "small_bets": 0,  # < 1/3 pot
                    "medium_bets": 0,  # 1/3 - 2/3 pot
                    "large_bets": 0,  # > 2/3 pot
                    "pot_sized_bets": 0,
                },
                "playing_style": PlayerStyle.UNKNOWN.value,
                "notes": [],
                "session_history": [],
            }
        return self.player_profiles[player_name]

    def update_player_action(
        self,
        player_name: str,
        action: str,
        amount: float = 0,
        pot_size: float = 0,
        position: str = "unknown",
        board_stage: str = "pre_flop",
    ):
        """Update player profile with new action"""
        profile = self.get_or_create_profile(player_name)

        # Update basic stats
        profile["last_seen"] = datetime.now().isoformat()
        profile["actions"][action.lower()] += 1

        # Update position stats
        if position in ["early", "middle", "late", "blinds"]:
            profile["position_stats"][position]["hands"] += 1
            profile["position_stats"][position]["actions"][action.lower()] += 1

        # Update betting patterns
        if action.lower() in ["bet", "raise"] and pot_size > 0:
            bet_ratio = amount / pot_size if pot_size > 0 else 0
            if bet_ratio < 0.33:
                profile["betting_patterns"]["small_bets"] += 1
            elif bet_ratio < 0.67:
                profile["betting_patterns"]["medium_bets"] += 1
            elif bet_ratio < 1.0:
                profile["betting_patterns"]["large_bets"] += 1
            else:
                profile["betting_patterns"]["pot_sized_bets"] += 1

        # Record hand action
        hand_action = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "amount": amount,
            "position": position,
            "board_stage": board_stage,
            "pot_size": pot_size,
        }
        profile["hands_played"].append(hand_action)

        # Keep only last 1000 hands to prevent file bloat
        if len(profile["hands_played"]) > 1000:
            profile["hands_played"] = profile["hands_played"][-1000:]

        self.save_profiles()

    def calculate_player_stats(self, player_name: str) -> Dict:
        """Calculate comprehensive player statistics"""
        profile = self.get_or_create_profile(player_name)

        total_actions = sum(profile["actions"].values())
        if total_actions == 0:
            return profile

        # Calculate VPIP (Voluntarily Put Money In Pot)
        voluntary_actions = (
            profile["actions"]["call"]
            + profile["actions"]["bet"]
            + profile["actions"]["raise"]
            + profile["actions"]["all_in"]
        )
        profile["vpip"] = (
            (voluntary_actions / total_actions) * 100 if total_actions > 0 else 0
        )

        # Calculate PFR (Pre-Flop Raise)
        pre_flop_hands = [
            h for h in profile["hands_played"] if h["board_stage"] == "pre_flop"
        ]
        pre_flop_raises = len(
            [h for h in pre_flop_hands if h["action"].lower() == "raise"]
        )
        profile["pfr"] = (
            (pre_flop_raises / len(pre_flop_hands)) * 100 if pre_flop_hands else 0
        )

        # Calculate Aggression Factor
        aggressive_actions = profile["actions"]["bet"] + profile["actions"]["raise"]
        passive_actions = profile["actions"]["call"] + profile["actions"]["check"]
        profile["af"] = (
            aggressive_actions / passive_actions
            if passive_actions > 0
            else aggressive_actions
        )

        # Determine playing style
        profile["playing_style"] = self.classify_playing_style(profile)

        return profile

    def classify_playing_style(self, profile: Dict) -> str:
        """Classify player's playing style based on VPIP, PFR, and AF"""
        vpip = profile["vpip"]
        pfr = profile["pfr"]
        af = profile["af"]

        # Need minimum hands for reliable classification
        total_hands = len(profile["hands_played"])
        if total_hands < 10:
            return PlayerStyle.UNKNOWN.value

        # Tight vs Loose (based on VPIP)
        tight = vpip < 25
        loose = vpip > 35

        # Passive vs Aggressive (based on AF)
        passive = af < 1.5
        aggressive = af > 2.5

        # Special cases
        if vpip > 50 and af > 3:
            return PlayerStyle.MANIAC.value
        elif vpip < 15 and af < 1:
            return PlayerStyle.NIT.value
        elif vpip > 40 and af < 0.5:
            return PlayerStyle.CALLING_STATION.value
        elif vpip < 10 and af > 2:
            return PlayerStyle.ROCK.value

        # Standard classifications
        if tight and passive:
            return PlayerStyle.TIGHT_PASSIVE.value
        elif tight and aggressive:
            return PlayerStyle.TIGHT_AGGRESSIVE.value
        elif loose and passive:
            return PlayerStyle.LOOSE_PASSIVE.value
        elif loose and aggressive:
            return PlayerStyle.LOOSE_AGGRESSIVE.value

        return PlayerStyle.UNKNOWN.value

    def get_player_summary(self, player_name: str) -> Dict:
        """Get a summary of player's tendencies and recommendations"""
        profile = self.calculate_player_stats(player_name)

        summary = {
            "name": player_name,
            "playing_style": profile["playing_style"],
            "stats": {
                "vpip": round(profile["vpip"], 1),
                "pfr": round(profile["pfr"], 1),
                "af": round(profile["af"], 2),
                "total_hands": len(profile["hands_played"]),
                "sessions": profile["total_sessions"],
            },
            "tendencies": self.analyze_tendencies(profile),
            "exploitation": self.get_exploitation_strategy(profile),
            "notes": profile["notes"][-5:],  # Last 5 notes
        }

        return summary

    def analyze_tendencies(self, profile: Dict) -> List[str]:
        """Analyze specific player tendencies"""
        tendencies = []

        # Betting patterns
        total_bets = (
            profile["betting_patterns"]["small_bets"]
            + profile["betting_patterns"]["medium_bets"]
            + profile["betting_patterns"]["large_bets"]
            + profile["betting_patterns"]["pot_sized_bets"]
        )

        if total_bets > 0:
            small_bet_pct = (
                profile["betting_patterns"]["small_bets"] / total_bets
            ) * 100
            large_bet_pct = (
                profile["betting_patterns"]["large_bets"] / total_bets
            ) * 100

            if small_bet_pct > 60:
                tendencies.append("Prefers small bets - likely weak when betting")
            if large_bet_pct > 50:
                tendencies.append("Makes large bets - strong when betting big")

        # Position tendencies
        for pos, stats in profile["position_stats"].items():
            if stats["hands"] > 5:
                fold_rate = stats["actions"]["fold"] / stats["hands"] * 100
                if fold_rate > 80:
                    tendencies.append(f"Folds frequently from {pos} position")
                elif fold_rate < 40:
                    tendencies.append(f"Plays many hands from {pos} position")

        # Action patterns
        if profile["actions"]["all_in"] > 5:
            tendencies.append("Goes all-in frequently - may be emotional player")

        if profile["actions"]["check"] > profile["actions"]["bet"] * 2:
            tendencies.append("Checks more than bets - passive player")

        return tendencies

    def get_exploitation_strategy(self, profile: Dict) -> List[str]:
        """Get exploitation strategies based on player style"""
        strategies = []
        style = profile["playing_style"]

        if style == PlayerStyle.TIGHT_PASSIVE.value:
            strategies.extend(
                [
                    "Bluff more frequently - they fold to pressure",
                    "Value bet thinly - they call with weak hands",
                    "Steal blinds aggressively - they fold to raises",
                ]
            )
        elif style == PlayerStyle.TIGHT_AGGRESSIVE.value:
            strategies.extend(
                [
                    "Call down with medium hands - they bluff frequently",
                    "Don't bluff - they call with strong hands",
                    "Re-raise with strong hands - they respect aggression",
                ]
            )
        elif style == PlayerStyle.LOOSE_PASSIVE.value:
            strategies.extend(
                [
                    "Value bet heavily - they call with weak hands",
                    "Don't bluff - they call too much",
                    "Isolate them in pots - they play too many hands",
                ]
            )
        elif style == PlayerStyle.LOOSE_AGGRESSIVE.value:
            strategies.extend(
                [
                    "Call down with medium hands - they bluff a lot",
                    "Re-raise with strong hands - they respect aggression",
                    "Avoid marginal situations - they put pressure on",
                ]
            )
        elif style == PlayerStyle.MANIAC.value:
            strategies.extend(
                [
                    "Call down with any pair - they bluff constantly",
                    "Re-raise with strong hands - they don't fold",
                    "Avoid marginal hands - they put too much pressure",
                ]
            )
        elif style == PlayerStyle.NIT.value:
            strategies.extend(
                [
                    "Steal blinds frequently - they fold to pressure",
                    "Bluff when they show weakness - they play very tight",
                    "Value bet thinly - they only play premium hands",
                ]
            )

        return strategies

    def add_note(self, player_name: str, note: str):
        """Add a note about a player"""
        profile = self.get_or_create_profile(player_name)
        timestamp = datetime.now().isoformat()
        profile["notes"].append({"timestamp": timestamp, "note": note})
        self.save_profiles()

    def get_session_summary(self) -> Dict:
        """Get summary of current session"""
        return {
            "start_time": self.session_start_time.isoformat(),
            "duration": (datetime.now() - self.session_start_time).total_seconds() / 60,
            "players_analyzed": len(self.current_session),
            "players": list(self.current_session.keys()),
        }

    def export_player_data(self, player_name: str, filename: str = None):
        """Export player data to JSON file"""
        if filename is None:
            filename = (
                f"player_{player_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

        profile = self.get_or_create_profile(player_name)
        with open(filename, "w") as f:
            json.dump(profile, f, indent=2, default=str)

        return filename
