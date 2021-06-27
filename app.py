from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('OlT1hfNg0JXJ2TUm5Mv9vPKXAB5oFijGRUtHoIP0i4qJ8PC9deKVCskiPvvHkdAu6P4bZUK+e18xYTOOsh5ley7Qvud5gM0+w6GthPov95Rh118Cqyi/k14tMMBBlvRjRgbnrn82yQwzRB09NbDHtwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8919c2b88b453899c7fcf8682a628dd6')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)