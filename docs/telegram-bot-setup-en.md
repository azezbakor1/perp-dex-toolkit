# How to Create a Telegram Bot from Scratch

This guide walks you through creating a Telegram bot end-to-end, including bot creation, securing your token, retrieving your chat ID, and wiring credentials into your application.

### Step 1: Start a chat with BotFather

1. Open Telegram and search for `@BotFather`
2. Start a chat with BotFather
3. Send `/start` to begin

### Step 2: Create a new bot

1. Send the `/newbot` command
2. Choose a display name for your bot
3. Choose a username for your bot (must end with `bot`, e.g., `my_trading_bot`)
4. BotFather will return a **bot token** — store it securely

### Step 3: Get your bot token

After creating the bot, BotFather will provide a token similar to:
```
123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

**Security best practices**
- Never share this token publicly
- Store it in environment variables or a secret manager
- Use a `.env` file for local development
- Rotate the token immediately if it is ever exposed

### Step 4: Obtain your chat ID

1. Send any message to your newly created bot on Telegram
2. Replace `{bot_token}` in the URL below with your token and open it in a browser:
   https://api.telegram.org/bot{bot_token}/getUpdates

For example, if your token is `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`, open:
`https://api.telegram.org/bot123456789:ABCdefGHIjklMNOpqrsTUVwxyz/getUpdates`

You will see a JSON payload similar to:
```
{"ok":true,"result":[{"update_id":880712345,
"message":{"message_id":1,"from":{"id":5586512345,"is_bot":false,"first_name":"yourQuantGuy","username":"yourquantguy","language_code":"en","is_premium":true},"chat":{"id":5586512345,"first_name":"yourQuantGuy","username":"yourquantguy","type":"private"},"date":1759103123,"text":"/start","entities":[{"offset":0,"length":6,"type":"bot_command"}]}}]}
```
Locate `"chat":{"id": ... }` and copy the value — in this example, `5586512345`.

Optional (CLI example):
```bash
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates" | jq
```

### Step 5: Update your .env file

Add your Telegram bot token and chat ID to the `.env` file used by the app:
```
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Example:
```
TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
TELEGRAM_CHAT_ID=5586512345
LANGUAGE=EN
```

Tips
- If messages do not arrive, ensure you have sent at least one message to the bot to initialize the chat
- If your bot is added to a group, the chat ID will be different (negative IDs are common in groups)
- Consider limiting permissions and enabling privacy mode if using your bot in groups
