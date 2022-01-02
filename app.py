import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["initial", "search_album_by_song", "intro_album","indtro_album_other_song","recommand_song","recommand_song_by_album","random_collect_song","about_jay"],
    transitions=[
        {
            "trigger": "advance",
            "source": "initial",
            "dest": "search_album_by_song",
            "conditions": "is_going_to_search_album_by_song",
        },
        {
            "trigger": "advance",
            "source": "search_album_by_song",
            "dest": "intro_album",
            "conditions": "is_going_to_intro_album",
        },
        {
            "trigger": "advance",
            "source": "search_album_by_song",
            "dest": "indtro_album_other_song",
            "conditions": "is_going_to_indtro_album_other_song",
        },
        {
            "trigger": "advance",
            "source": "initial",
            "dest": "recommand_song",
            "conditions": "is_going_to_recommand_song",
        },
        {
            "trigger": "advance",
            "source": "recommand_song",
            "dest": "recommand_song_by_album",
            "conditions": "is_going_to_recommand_song_by_album",
        },
        {
            "trigger": "advance",
            "source": "recommand_song",
            "dest": "random_collect_song",
            "conditions": "is_going_to_random_collect_song",
        },
        {
            "trigger": "advance",
            "source": "initial",
            "dest": "about_jay",
            "conditions": "is_going_to_about_jay",
        },
        {"trigger": "advance",
         "source": ["search_album_by_song", "intro_album","indtro_album_other_song","recommand_song","recommand_song_by_album","random_collect_song","about_jay"], 
        "dest": "initial",
        "conditions":"is_going_to_initial"
        }
    ],
    initial="initial",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if machine.state=="initial":
                send_text_message(event.reply_token, "請輸入正確的關鍵字！歌名 或是 “推薦歌曲” 或是 ”關於周杰倫“")
            
            if machine.state=="search_album_by_song":
                send_text_message(event.reply_token, "請輸入正確的關鍵字！“介紹專輯” 或是 ”專輯裡的其他首歌“")

            if machine.state=="intro_album":
                send_text_message(event.reply_token, "查無專輯！")

            if machine.state=="indtro_album_other_song":
                send_text_message(event.reply_token, "查無專輯！")
            
            if machine.state=="recommand_song":
                send_text_message(event.reply_token, "請輸入正確的關鍵字！專輯名稱 或是 “隨機“")
            
            if machine.state=="recommand_song_by_album":
                send_text_message(event.reply_token, "請輸入正確的專輯名稱！")
                
            

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
