from mysqldb_read import db_fuel_reading
from app import app
from collections import Counter
from datetime import date, datetime
from math import ceil
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask import render_template, request
import random
from flask import Flask, request
from pymessenger.bot import Bot
import os


load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
SEPARATOR = "++"

engine = create_engine(DATABASE_URL)
session = sessionmaker(engine)()

metadata = MetaData()
metadata.reflect(engine)

Base = automap_base(metadata=metadata)
Base.prepare()


def get_data(table, column):
    sa_table = getattr(Base.classes, table)
    col = getattr(sa_table, column)
    rows = session.query(col).all()
    cnt = Counter()
    for row in rows:
        attr = row[0]

        if attr is None:
            continue

        if isinstance(attr, (date, datetime)):
            attr = attr.strftime("%Y-%m")

        cnt[attr] += 1
    return sorted(cnt.items())


def calculate_max_height_graph(values):
    max_value = max(values)
    return int(ceil(max_value / 100.0)) * 100


@app.route('/')
def index():
    tables = sorted(Base.classes.keys())
    print(tables)
    return render_template("index.html", tables=tables)


@app.route('/columns')
def show_columns():
    table_str = request.args["table"]
    # table_str = request.args["fuel_data"]
    table = Base.classes.get(table_str)
    table_columns = {
        col: f"{table_str}{SEPARATOR}{col}" for col in
        table.__table__.columns.keys()
    }
    return render_template('_columns.html',
                           table_columns=sorted(table_columns.items()))


@app.route('/graph')
def build_graph():
    tcolumn = request.args["tcolumn"]
    table, column = tcolumn.split(SEPARATOR)
    data = get_data(table, column)
    labels, values = zip(*data)
    max_height = calculate_max_height_graph(values)
    return render_template('_graph.html',
                           labels=labels,
                           values=values,
                           max_height=max_height)


@app.route("/sp")
def sp():
    return "Hello word"


@app.route('/all_record', methods=("POST", "GET"))
def all_record():
    df = db_fuel_reading()
    return render_template('all_record.html', tables=[df.to_html(classes='Fuel_data')],
                           titles=df.columns.values, index=False)

#bot code

ACCESS_TOKEN = 'ACCESS_TOKEN'   #ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = 'VERIFY_TOKEN'   #VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot (ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/bot", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"