# Healthcheck-bot
![CI Badge](https://github.com/QD-2022/Healthcheck-bot/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/QD-2022/Healthcheck-bot/branch/main/graph/badge.svg?token=G54CHQRYTC)](https://codecov.io/gh/QD-2022/Healthcheck-bot)

<p align="center">
    <img src="icon.jpeg" alt="logo" width="200">
</p>

A simple Python script to verify if a service is up. Whenever the service falls, a message will be sent to a user/group/channel with Telegram

## How to use?
**Make a copy** of the file `config/settings.yaml.dist` in the same directory and rename it to `settings.yaml`:
- Set `bot_token`, your bot token
- Set `chat_ids`, the ID(s) the bot will use to communicate any downtime. It's possible to set multiple IDs, semicolon separated without any space
- Set the urls you'd like to check in `urls.json`

### Telegram bots
This is bot is now able to contact other bots and check if their running correctly!
In order to setup this module, obtain an `api_id` and `api_hash` following the [Telegram guide](https://core.telegram.org/api/obtaining_api_id), now add them your `settings.yaml`. 
The last step is to add the bot(s) to check in the same settings file, completing the value for each key:
- Set `username`, the bot to be checked username without the prepending '@'
- Set `command`, the command that will be sent to your bot
- Set `expected_response`, the expected response from your bot. Any special character should be replaced with their equivalent character (a new line should be replaced with `\n`)
Multiple bots could be added by added just by repeating the same structure of a sequence of objects in yaml. 

### Example
```yaml
bot_token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11" # Your bot token
chat_ids: ["10000000", "10000001", "10000002"]  # Single ID or Multiple IDs
api_id: "123456"
api_hash: "123456:ABC-DEF1234ghIkl-zyx57W2v"
bots_to_check:
  - username: "@WebpageBot"
    command: "/start"
    expected_response: "Hello, I'm the Webpage Bot!\nPlease send me up to 10 links and I will update previews for them."
```

### Run it every 5 minutes using crontab
- Open crontab using:
```bash
$ crontab -e
```
- Add the following line
```bash
*/5 * * * * cd /path/to/Healthcheck-bot/ && python3 src/main.py > checks.log 2> errors.log    
```

## Write Unit Tests
In order to write Unit Tests, you have to put it inside `tests`.
There are many possibilities, 

### Unit Tests without mocking
To add a new unit test without mocking, there are some examples at the beginning of `tests`, but let's inspect how they're implemented:
- `func`: simply the function to mock
- `expected_res`: the expected returned value of the function to test
- `arg`: a tuple that contains the argument(s) of the function to test (the one previously defined in `func`). In case there are no passing arguments, just add an empty tuple object (`tuple()`)
- `is_async`: this is not a compulsory key, should be added and set to `True` only if the function is asynchronous

### Unit Tests with mocking
If is necessary one or more mock(s), it's possible to append three more keys to the unit test.
In case an async function needs to be mocked, its result can be wrapped in an `AsyncMock` and its return value set as a constructor element in the constructor. 
The test should have the same keys with three more keys:
- `mock_obj`: it's a list of the objects in which there are the functions to mock. In our examples they often refer to the main object (the one imported from src.main)
- `mock_func`: an array of strings, it indicates the functions to mock
- `mock_ret`: a list of the returned values