# Healthcheck-bot
![CI Badge](https://github.com/QD-2022/Healthcheck-bot/actions/workflows/ci.yml/badge.svg)

<p align="center">
    <img src="icon.jpeg" alt="logo" width="200">
</p>

A simple Python script to verify if a service is up. Whenever the service falls, a message will be sent to a user/group/channel with Telegram

## How to use?
Just set two env variables:
- `QDBotToken`, your bot token
- `QDBotIDs`, the ID(s) the bot will use to communicate any downtime. It's possible to set multiple IDs, semicolon separated without any space

### Example in bash
```bash
export QDBotToken="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11" # Your bot token
export QDBotIDs="10000000"                                      # Single ID
export QDBotIDs="10000000;10000001;10000002"                    # Multiple IDs
```
