# stooq-webchat-bot
A bot to listen to commands from [webchat](https://github.com/JPBeckner/webchat).

This project uses Django REST Framework to implements an API that communicates as a bot with the webchat.

## Instaling
> It's recommended to use Pipenv to the virtual environment and Python 3.8 to run the project.

Clone or download the project from GitHub. Go to the project directory and install the dependencies.

```shell
pipenv install --python 3.8
```

## Running
Run the project locally.

It's possible in some ways:
```shell
pipenv run execute
```
```shell
pipenv run python manage.py runserver 0.0.0.0:8888
```

## Endpoints

### [POST] /command/
Send a command to the bot. Specificaly to consulte some stock quote.

JSON body parameters:
```json
{
    "command": "string value",
    "parameter": "string value",
    "room": "string value"
}
```
#### Responses:
 * 400 - Bad Request:
  ```json 
  {"error": "Wrong data received."}
  ```
 * 500 - Internal Server Error:
 ```json 
    {"error": "Service unavaliable."}
 ```

 * 200 - OK:
  ```json 
    {"msg": "string value with the stock quote phrase."}
  ```
