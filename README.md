# Telegram Phishing Script

## Overview

This Python script is a tool for simulating a phishing campaign on Telegram. It operates a bot that interacts with users to gather information, which is then stored in an encrypted database. The script is configurable with various templates for different scenarios and includes functionality for tracking user engagement.

## Features

- **Environment Setup**: Sets up a Python virtual environment and installs dependencies
- **Phishing Templates**: Includes predefined templates for scenarios such as banking, social media, and government services
- **Data Storage**: Stores captured user data in an encrypted SQLite database
- **Bot Handlers**: Manages user interactions and guides users through a series of prompts
- **Statistics**: Provides a summary of the campaign, including total targets and verified captures
- **Logging**: Records bot operations and user interactions to a log file

## Prerequisites

- Python 3.6 or higher
- A Telegram Bot Token (obtained from BotFather)

## Installation and Usage

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 2. Run the script

```bash
python3 telegram.py
```

The script will set up the virtual environment, install dependencies, and then prompt for the Telegram Bot Token and template selection.

### 3. Bot Interaction

Once the bot is running, send the `/start` command to the bot on Telegram to begin the interaction.

## Dependencies

The script automatically installs the following dependencies:

- `pyTelegramBotApi==4.14.0`
- `colorama==0.4.6`
- `pyfiglet==1.0.2`
- `requests==2.31.0`
- `cryptography==41.0.7`



## Support

[Add support information if applicable]
