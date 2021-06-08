import slack
import os
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from bot.trivia_questions_answers import Trivia

# get path vars
token = os.getenv('GENOS_BOT_TOKEN')
signing_secret = os.getenv('GENOS_SIGNING_SECRET')

# gets trivia object
trivia = Trivia()

# configure app
app = Flask(__name__)

client = slack.WebClient(token)
BOT_ID = client.api_call('auth.test')['user_id']

slack_event_adapter = SlackEventAdapter(signing_secret, '/slack/events', app)


@slack_event_adapter.on('message')
def message(payload):
    """
    Handles message event
    :param payload: data about the message that was just sent
    :return: None
    """
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')

    # ignores its own messages
    if user_id == BOT_ID:
        return

    text = event.get('text')

    # currently trivia checks for anyone to answer instead of just the user who issued the command
    # I thought this was more fun, but if it becomes annoying to use feel free to change it
    if trivia.was_asked:
        if trivia.is_correct(text):
            client.chat_postMessage(channel=channel_id, text='Congrats! Have a cookie :cookie:')
        else:
            client.chat_postMessage(channel=channel_id, text='pathetic')

    # checks if physics stinks was sent
    if text.lower() == 'physics stinks':
        client.chat_postMessage(channel=channel_id, text='you stink')


@app.route('/trivia', methods=['POST'])
def trivia_command():
    """
    Asks a trivia question to the channel the command was used
    :return: 200 OK response code if it goes through
    """
    # gets data about the command
    data = request.form
    channel_id = data.get('channel_id')

    # gets random question and sends message into the same channel as command was used
    question = trivia.ask_random_question()
    client.chat_postMessage(channel=channel_id, text=question)

    # return 200 OK response
    return Response(), 200
