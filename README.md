# Transport bot for Telegram

1. Install all the dependencies using the bash script
```bash
    $ ./installPackages.sh
```

2. Create a new "telegram bot" using "botfather"
  
  1. Open telegram.
  2. Search in contact: "botfather" (https://core.telegram.org/bots#botfather)
  3. Inside botfather, type: /newbot
  4. Follow the botfather instructions --> Now you have your bot created!!!
  5. Click to the created bot link, example: telegram.me/YOUR_BOT_NAME
  6. Copy the Telegram "TOKEN to access the HTTP API" that botfather gives you in the last message

3. Place your Telegram token (the one you get on point 2.6) into an environment variable

```bash
export TELEGRAM_TOKEN="80141913:AAGnyI4m0KlayTTiswLkrG2w4P39Ifjn75A"
```

4. Run the app!

```bash
python main.py
```
