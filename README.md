# PokerGPT - AI-Powered Poker Analysis Tool

PokerGPT is a sophisticated poker analysis tool designed to help you improve your online poker game on PokerStars. It provides real-time analysis, hand strength evaluation, opponent range estimation, and strategic recommendations to enhance your poker skills through education and learning.

## 🚀 **Key Features**

### 🎯 **Real-time Game Analysis**

- **Live Game State Monitoring**: Continuously reads the poker table using OCR and computer vision
- **Dynamic Player Support**: Supports 2-9 players at the table (configurable)
- **Position Tracking**: Automatically calculates your position relative to the dealer
- **Action History**: Tracks all player actions and betting patterns

### 🤖 **AI-Powered Insights**

- **GPT-4o Integration**: Uses OpenAI's latest GPT-4o (Omni) for advanced poker analysis
- **Strategic Recommendations**: Provides detailed analysis of game situations
- **Player Tendency Analysis**: Identifies opponent playing styles and patterns
- **Hand Strength Evaluation**: Analyzes your hand relative to the board and opponent ranges

### 📊 **Professional Hand Strength Analysis**

- **Complete Hand Rankings**: Based on professional poker hand charts
- **Hand Categories**: Premium, Strong, Medium, Speculative, Weak, Trash
- **Position-Adjusted Ranges**: Different hand ranges for different positions
- **Hand Notation**: Converts cards to poker notation (e.g., 'AKs', 'TTo')
- **Strength Scoring**: Numerical strength ratings for all starting hands

### 🎲 **Advanced Range Analysis**

- **Action-Based Ranges**: Estimate opponent hands based on their actions
- **Position-Based Ranges**: Different ranges for different positions
- **Bet Sizing Analysis**: Adjust ranges based on bet sizes
- **Exploitation Opportunities**: Identify how to exploit opponent tendencies

### 👥 **Player Tendency Analysis**

- **Real-time Player Profiling**: Track player behavior and tendencies
- **Playing Style Classification**: Tight-Passive, Loose-Aggressive, Maniac, etc.
- **VPIP/PFR/AF Tracking**: Professional poker statistics
- **Betting Pattern Analysis**: Small, medium, large bet preferences
- **Position-Based Tendencies**: How players act from different positions
- **Exploitation Strategies**: Specific advice for each player type
- **Session History**: Persistent player profiles across sessions

### 🃏 **Board Texture Analysis**

- **Board Evaluation**: Analyze paired, suited, connected boards
- **Draw Analysis**: Identify flush draws, straight draws, and outs
- **Post-Flop Recommendations**: Action recommendations for post-flop play
- **Hand Strength Evolution**: How your hand strength changes with the board

### 📊 **Comprehensive Dashboard**

- **Real-time GUI**: Live updates every 500ms for fast response
- **Player Information Table**: Shows all players' cards, actions, stack sizes, and playing styles
- **Game State Display**: Current board stage, pot size, dealer position, and more
- **Hand Strength Analysis**: Detailed analysis of your hand strength and playability
- **Opponent Range Analysis**: Estimated hand ranges for all opponents
- **Player Tendency Analysis**: Real-time player profiling and exploitation strategies
- **Board Texture Analysis**: How the board affects hand strength
- **Quick Strategic Tips**: Position-based and situation-based advice
- **Live Notifications**: Real-time text alerts for game events
- **Game Log**: Complete history of all actions and events

### 🔔 **Text-Based Notifications**

- **Live Notifications**: Real-time text notifications for game events
- **Action Alerts**: Immediate display of player actions and amounts
- **Board Stage Updates**: Clear indication of game progression
- **Hero Role Notifications**: Your position and role updates
- **Fast Response**: 500ms update frequency for immediate feedback

### 🛡️ **Educational Focus**

- **No Automated Actions**: Completely safe - only provides analysis and recommendations
- **Learning Tool**: Designed to help you understand poker concepts and improve your game
- **Professional Standards**: Based on widely-used poker hand strength charts and strategies

## Prerequisites

- Python 3.8 or higher
- Access to OpenAI GPT-4o API
- Tesseract OCR for text recognition
- PokerStars client

## Installation

1. **Clone or download** the project files
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Set up OpenAI API key** in the `pokergpt.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. **Ensure Tesseract OCR** is installed (included in the project)

## PokerStars Setup

1. **Open PokerStars client** and ensure it's visible on screen
2. **Disable animations** in table settings for better detection
3. **Use standard table layout** for optimal detection

## Usage

### Starting the Analyzer

```bash
python poker_analyzer.py
```

### Configuration

1. **Enter your player number** (1-9, starting from bottom of table)
2. **Specify maximum players** at the table (2-9)
3. **The analyzer will automatically**:
   - Locate the PokerStars window
   - Resize it to optimal dimensions
   - Start monitoring the game
   - Provide comprehensive analysis

### Understanding the Interface

#### **Player Information Table**

- **Player**: Player number/name
- **Status**: Active/Inactive
- **Role**: Dealer, Small Blind, Big Blind, etc.
- **Cards**: Visible cards (if any)
- **Turn**: Whether it's their turn
- **Action**: Last action taken
- **Amount**: Bet/raise amount
- **Stack Size**: Current chip stack
- **Play Style**: Identified playing style
- **Strategy**: Exploitation strategy

#### **Game State Information**

- **Total Players**: Number of active players
- **Hero Cards**: Your hole cards
- **Community Cards**: Board cards (flop, turn, river)
- **Board Stage**: Pre-flop, Flop, Turn, or River
- **Total Pot Size**: Current pot amount
- **Dealer Position**: Which player is dealer
- **Hero Position**: Your position relative to dealer
- **Rounds**: Number of hands played

#### **Analysis Sections**

- **AI Analysis & Recommendations**: Detailed GPT-4o analysis with hand strength
- **Hand Strength Analysis**: Professional hand evaluation and recommendations
- **Opponent Range Analysis**: Estimated hand ranges for all opponents
- **Player Tendency Analysis**: Real-time player profiling and exploitation strategies
- **Board Texture Analysis**: How the board affects hand strength
- **Quick Strategic Tips**: Position-based advice
- **Game Log**: Complete action history

## Hand Strength Analysis Features

### 🎯 **Pre-Flop Analysis**

- **Hand Notation**: Converts your cards to poker notation (e.g., 'AKs', 'TTo')
- **Strength Rating**: Numerical strength score based on professional charts
- **Category Classification**: Premium, Strong, Medium, Speculative, Weak, Trash
- **Playability Assessment**: Should you play this hand in current situation?
- **Position-Based Ranges**: Different recommendations for different positions
- **Stack-to-Pot Analysis**: Adjusts recommendations based on SPR

### 🎲 **Opponent Range Analysis**

- **Action-Based Estimation**: Estimates opponent hands based on their actions
- **Position-Based Ranges**: Different ranges for different positions
- **Bet Sizing Impact**: Adjusts ranges based on bet sizes
- **Exploitation Opportunities**: Identifies how to exploit opponent tendencies
- **Range Descriptions**: Human-readable descriptions of opponent ranges

### 🃏 **Post-Flop Analysis**

- **Board Texture Evaluation**: Analyzes paired, suited, connected boards
- **Hand Strength Evolution**: How your hand strength changes with the board
- **Draw Analysis**: Identifies flush draws, straight draws, and calculates outs
- **Action Recommendations**: Specific actions based on hand strength and position
- **Pot Odds Calculation**: Calculates pot odds for calling decisions

## How It Helps Improve Your Game

### 📈 **Learning Opportunities**

- **Understand Hand Strength**: Learn professional hand rankings and categories
- **Position Play**: Learn how position affects hand playability
- **Range Analysis**: Learn to think in terms of hand ranges
- **Board Texture**: Understand how board texture affects hand strength
- **Pot Odds**: Learn when calls are profitable
- **Exploitation**: Develop strategies against different player types

### 🎯 **Strategic Development**

- **Hand Selection**: Learn which hands to play in which positions
- **Bet Sizing**: Understand optimal bet sizing based on hand strength
- **Range vs Range**: Learn to think about hand ranges rather than specific hands
- **Board Reading**: Analyze how the board affects your hand and opponents' ranges
- **Draw Evaluation**: Understand drawing hands and implied odds

### 🧠 **Decision Making**

- **Real-time Feedback**: Get analysis as the game happens
- **Historical Context**: Track how your decisions perform over time
- **Pattern Recognition**: Identify recurring situations and optimal responses
- **Professional Standards**: Learn from professional hand strength charts

## Technical Features

### 🔧 **Hand Strength Engine**

- **Professional Charts**: Based on widely-used poker hand strength charts
- **Dynamic Ranges**: Adjusts based on position, stack size, and number of players
- **Real-time Analysis**: Updates analysis as game state changes
- **Comprehensive Coverage**: Handles all 169 possible starting hands

### 📊 **Range Analysis Engine**

- **Action-Based Estimation**: Uses opponent actions to estimate ranges
- **Position-Based Adjustments**: Different ranges for different positions
- **Bet Sizing Analysis**: Considers bet sizes in range estimation
- **Exploitation Identification**: Finds opportunities to exploit opponent tendencies

### 🎲 **Board Analysis Engine**

- **Texture Recognition**: Identifies board characteristics (paired, suited, connected)
- **Draw Calculation**: Calculates potential draws and outs
- **Hand Evolution**: Tracks how hand strength changes with the board
- **Post-Flop Strategy**: Provides specific recommendations for post-flop play

## Limitations

- **Screen Resolution**: Tested on 1920x1080, may need adjustments for other resolutions
- **Table Layout**: Requires specific PokerStars table settings
- **OCR Accuracy**: Depends on screen clarity and text recognition
- **API Dependencies**: Requires active internet connection for GPT-4o analysis
- **Hand Strength**: Based on general charts, may not account for specific game dynamics

## Troubleshooting

### Common Issues

1. **"Poker client window NOT Found"**

   - Ensure PokerStars is open and visible
   - Check that the window title contains "No Limit" and "$" or "Money"

2. **Poor text recognition**

   - Disable animations in PokerStars settings
   - Ensure good screen contrast
   - Check Tesseract installation

3. **Analysis not updating**

   - Verify OpenAI API key is set correctly
   - Check internet connection
   - Ensure API credits are available

4. **Hand strength analysis errors**
   - Ensure hero cards are properly detected
   - Check card format (should be like "Ah", "Ks", etc.)
   - Verify position calculation

### Performance Tips

- **Close unnecessary applications** to improve OCR speed
- **Use SSD storage** for faster file operations
- **Ensure adequate RAM** for smooth operation
- **Update regularly** for best hand strength analysis

## Educational Use

This tool is perfect for:

- **Poker beginners** learning hand strength fundamentals
- **Intermediate players** improving their range analysis
- **Advanced players** fine-tuning their game theory
- **Coaches** teaching poker concepts with professional charts
- **Students** studying game theory and hand ranges

## Legal Notice

This tool is for **educational and analysis purposes only**. It does not:

- Automate any poker actions
- Interfere with game play
- Violate PokerStars terms of service
- Provide unfair advantages

## Support

For questions or issues:

1. Check the troubleshooting section above
2. Ensure all prerequisites are properly installed
3. Verify hand strength analysis is working correctly

## Contributing

Contributions are welcome! Focus areas:

- Improved hand strength algorithms
- Enhanced range analysis
- Better board texture recognition
- UI/UX improvements
- Educational content
- Additional hand strength charts

---

**Remember**: This tool is designed to help you learn and improve your poker skills through comprehensive analysis and education, not to play the game for you. Use it responsibly and always make your own decisions at the poker table.
