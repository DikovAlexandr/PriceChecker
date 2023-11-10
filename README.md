## Telegram Price Checker Bot
This is a simple Telegram bot that allows users to add products with their desired prices for automatic price checking. The bot provides a menu with options to add a product, set the checking period, check prices immediately, stop automatic checking, and view all added products.

## Getting Started
- Prerequisites
    Python 3.11.x
- Installation
    Clone the repository:
    ```bash
    git clone https://github.com/DikovAlexandr/PriceChecker
    ```

    Navigate to the project directory:
    ```bash
    cd telegram_price_checker_bot
    ```
    
    Create venv:
    ```bash
    python -m venv venv
    ```

    Activate venv:
    ```bash
    venv\Scripts\activate
    ```

    Install the required packages to venv:
    ```bash
    pip install -r requirements.txt
    ```
## Configuration
Create a new bot on Telegram by talking to BotFather.
Obtain the bot token from BotFather.
Open the bot.py file and replace 'YOUR_BOT_TOKEN' with the obtained bot token.
```python
TOKEN = 'YOUR_BOT_TOKEN'
```
Usage
Run the bot.py with the following command:

```bash
& c:/users/user/PriceChecker/venv/Scripts/python.exe c:/users/user/PriceChecker/bot.py
```
The bot will be active and ready to respond to commands on your Telegram account.
