# Thronin: Advanced Automation for Throne and Liberty

## About Thronin

Thronin is an **advanced bot designed to enhance gameplay** in *Throne and Liberty*. Its development focused on providing **convenience, efficiency, and minimal detection risk** for users. It automates various in-game tasks, allowing players to streamline their gameplay and potentially free up time from repetitive grinding.

## Key Features

Thronin offers a wide range of features to automate and optimize your *Throne and Liberty* experience:

- **Automated Fishing**: Effortlessly equips your fishing pole, casts the line, and reels in fish when the bobber indicates a bite. Thronin determines the optimal reel-in time and direction to maximize success. Note that fishing does not currently work with "Famous Fishing Spots" due to color interference with the bobber detection.
- **Classless System**: Thronin works seamlessly with **any class or build** in *Throne and Liberty*, offering **full customization of your skillbar** to tailor combat strategies to your unique playstyle. You can define skill usage, casting, recovery skills, and set repetitions per use.
- **Customizable Farming Locations**: Select and automate farming routines for different in-game locations, enhancing resource collection and maximizing efficiency. Currently, the system **fully supports contracts in Canina Village**.
- **Resource Gathering**: Automates essential tasks like **mining resources**, purchasing daily items from vendors (e.g., Contract Coin Merchant, Sundries Merchant, Guild Merchant), and collecting various in-game rewards from Amitoi, Battle Pass, and Guild collections.
- **Advanced Trackers**: Thronin incorporates sophisticated tracking mechanisms to ensure precise automation:
    - **Amitoi Tracker**: Optimizes collection timing and includes fail-safes to prevent premature travel to the Amitoi house. It also forces the player to face west after teleporting, ensuring consistent character positioning.
    - **Casting Tracker**: Monitors casting times for efficient skill use.
    - **Death Tracker**: Manages respawns and routine restarts after character death, ensuring minimal disruption.
    - **Health & Mana Trackers**: Automates health and mana recovery actions during combat, utilizing potions and skills as needed.
    - **Item Slot Trackers**: Automatically uses items from quick slots, such as potions, to maintain health and mana.
    - **Line of Sight Tracker**: Ensures that actions, particularly combat skills, only occur when the target is visible.
    - **Target & Party Trackers**: Keeps your character engaged with enemies and synchronized with your party leader’s actions in party mode.
- **Item Storage**: Automatically deposits collected items into storage, preventing inventory overflow during farming routines.
- **Contract Completion**: Automates the completion of in-game contracts for rewards and progression, significantly saving manual effort.
- **Crash Detection**: Thronin is designed to **detect when you are kicked or if the game crashes**, attempting to close and restart the game to ensure minimal disruption and uninterrupted gameplay.
- **Advanced Gameplay Modes**:
    - **Assist Mode**: Automates the skills you configure in the Skillbars tab, allowing you to focus on character positioning and strategic movement during combat. It handles health and mana management and skill rotation.
    - **Fishing Mode**: Provides **full automation of the fishing process**, from equipping the pole to reeling in fish.
    - **Party Mode**: Enables your character to follow a party leader in dungeons, daily contracts, or farming activities. It automatically accepts party invites and shared contracts, and engages selected enemies.
    - **Safe Zone Mode**: Collects rewards from Amitoi expeditions, Battle Pass, and Guild rewards without manual intervention. It also handles regular tasks like item deposits at Kastleton and Stonegard Castle to keep your resources organized.

## Installation

To get Thronin up and running, follow these steps:

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python (3.10 or newer)**: Download from [python.org](https://www.python.org/downloads/). Make sure to select the option to "Add Python to PATH" during installation.
- **Git**: Download from [git-scm.com/downloads](https://git-scm.com/downloads/).
- **Tesseract-OCR**: Thronin uses Tesseract for reading contracts.
    - Download the installer for Windows from the [Tesseract installer for Windows section here](https://tesseract-ocr.github.io/tessdoc/Installation.html).
    - Run the installer and follow the prompts.
    - **Important:** You must add the Tesseract installation path to your system's `PATH` environment variables. For easy instructions, refer to [this video tutorial](https://www.youtube.com/watch?v=2kWvk4C1pMo).

### Step 1: Clone the Repository

Open your command prompt (CMD) or PowerShell and navigate to the directory where you want to install Thronin. Then, clone the repository:

```
git clone https://github.com/StevensUneven/thronin-bot.git
cd thronin-bot
```

### Step 2: Set Up the Environment

Navigate into the newly cloned `thronin-bot` directory. This project uses a virtual environment to manage dependencies.

Run the setup batch script:

```
.\1_Create_Environment.bat
```

This script will:

- Create a Python virtual environment (`.venv`).
- Install all necessary Python dependencies.
- Install Thronin as an editable package.

### Step 3: Run Thronin

Once the environment setup is complete, you can run Thronin using the dedicated batch script:

```
.\2_Run_Thronin.bat
```

This script will activate the virtual environment, check for updates, and then launch the Thronin application.

## Resources & Guides

Looking for more help with Thronin? Check out our detailed guides:

- **All Guides Collection**: https://www.patreon.com/collection/1248947
- **Installation Guide**: https://www.patreon.com/posts/installation-119532580
- **Setup Guide**: https://www.patreon.com/posts/setup-guide-119530966
- **Fishing Guide**: https://www.patreon.com/posts/fishing-guide-119865924
- **Contracts Guide**: https://www.patreon.com/posts/contracts-guide-119677060
- **Skillbar Guide**: https://www.patreon.com/posts/skillbars-guide-119531143
- **Routines Explained**: [https://www.patreon.com/posts/routines-126957948](https://www.google.com/search?q=https://www.patreon.com/posts/routines-126953948)
- **FAQ**: https://www.patreon.com/posts/faq-119532301

*New Wiki Coming Soon!*