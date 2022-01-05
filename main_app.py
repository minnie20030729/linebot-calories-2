#載入LineBot所需要的模組
from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import re

app = Flask(__name__)
 
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('0sgxc4zU4YQBb7n/FnHNs7ksEE1VcCPYUPn6ONSgVYmK9SMn3EHlSf0W5LqT2awT2XmlckW16ARg+vr+eN28Fujt6wmn3Br6glYlplaC8zjjqWlFZ7oa0tX70AePDTWXP+qyZgAeOPBAkyuKuPyWtgdB04t89/1O/w1cDnyilFU=')
 
# 必須放上自己的Channel Secret
handler = WebhookHandler('70a64584bb53162ebe1a5401b3d763b1')



#開啟richMenu
rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=843),
    selected=False,
    name="Nice richmenu",
    chat_bar_text="Tap here",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=843, y=0, width=2500, height=843),
        action=MessageAction(
                    label='主食',
                    text='我餓')),
        RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=843, height=843),
        action=PostbackAction(
                    label='目前卡路里',
                    display_text='我還剩多少大卡?',
                    data='calories'))
                ]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
print(rich_menu_id)
with open("control.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)
line_bot_api.set_default_rich_menu(rich_menu_id)


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
 
    return 'OK'

#測試用食物

class Big_food_type:
    
    def __init__(self, url, title, name, text):
        self.url = url
        self.title = title
        self.name = name
        self.text = text

class Small_food_type:

    def __init__(self, url, title, name, text):
        self.url = url
        self.title = title
        self.name = name
        self.text = text

class Curry:
    
    def __init__(self, url, title, text, calories):
        
        self.url = url
        self.title = title
        self.text = text
        self.calories = int(calories)

rice = Big_food_type('https://i.imgur.com/cL9fa88.png','飯類', 'rice', '攝取澱粉補充熱量')
noodle = Big_food_type('https://i.imgur.com/cL9fa88.png','麵類', 'nnodle', '蘇蘇蘇～吃越大聲就代表越好吃ㄛ！')

curry = Small_food_type('https://i.imgur.com/cL9fa88.png','各種風味的咖哩', 'curry', '香噴噴熱騰騰的好吃咖哩呦～')

indian_curry = Curry('https://i.imgur.com/cL9fa88.png', '印度風咖哩', '微辣但爽口',2)
japenese_curry = Curry('https://i.imgur.com/cL9fa88.png', '日式風咖哩', '香甜可口',3)

test_food = {'我要吃主食!':{rice:{curry:[indian_curry, japenese_curry], '燴飯':['番茄燴飯',' 牛肉燴飯']}, noodle:{'義大利麵':['奶油蕈菇義大利麵','番茄海鮮義大利麵'], '拉麵':['豚骨拉麵']}}, '我想吃甜食!':{}}

'''
test_food = {'我要吃主食!':
        {rice:[
            {curry:[[indian_curry, japenese_curry], ['泰國咖哩', '黑咖哩']],
             '燴飯':['番茄燴飯',' 牛肉燴飯'],'炒飯':[['肉絲炒飯', '蝦仁炒飯'], ['蛋炒飯', '排骨炒飯']]},{'便當':[['奮起湖便當', '排骨便當'],['雞腿便當', '控肉便當']],'火鍋':[['泡菜鍋', '麻辣鍋'],['滷味燙','沙茶鍋']]}
             ],noodle:{'義大利麵':['奶油蕈菇義大利麵','番茄海鮮義大利麵'], '拉麵':['豚骨拉麵']}}, '我想吃甜食!':{}}
'''
#自定義function
def update_calories(calories):
    f = open("calories.txt","w")
    f.write(f'{calories}')
    f.close()
    return

def reset_carlories():
    update_calories("0")
    return

def read_calories():
    f = open("calories.txt","r")
    calories = f.readline()
    f.close()
    return calories




#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        calories = int(event.message.text)
        update_calories(calories)
        buttons_template_message = TemplateSendMessage(
            alt_text='類別選單',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/cL9fa88.png',
                title='今天，我想來點……',
                text='選擇想要的食物類別',
                actions=[
                    MessageAction(
                        label='主食',
                        text='我要吃主食!'
                    ),
                    MessageAction(
                        label='甜食',
                        text='我想吃甜食!'
                    ),
                    MessageAction(
                        label='小點',
                        text='想來點小點!'
                    )
                    
                ]
            ))
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
        
    except ValueError:
        pass

    if event.message.text == '我餓':
        buttons_template_message = TemplateSendMessage(
        alt_text='類別選單',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/cL9fa88.png',
            title='今天，我想來點……',
            text='選擇想要的食物類別',
            actions=[
                MessageAction(
                    label='主食',
                    text='我要吃主食!'
                ),
                MessageAction(
                    label='甜食',
                    text='我想吃甜食!'
                ),
                MessageAction(
                    label='小點',
                    text='想來點小點!'
                )
            ]
        ))
        line_bot_api.reply_message(event.reply_token, buttons_template_message)

        if event.message.text in test_food:
            for i in test_food:
                if event.message.text == i:
                    columns = [
                        CarouselColumn(
                            thumbnail_image_url=j.url,
                            title=j.title,
                            text=j.text,
                            actions=[
                                MessageAction(
                                    label='我要選這個',
                                    text=j.name
                                )
                            ]
                        )
                        for j in test_food[i]
                    ]
                    next_page_column = [
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/cL9fa88.png',
                            title='看看下一頁',
                            text='看看下一頁',
                            actions=[
                                PostbackAction(
                                    label='我要看下一頁',
                                    display_text='next',
                                    data='主食_p2'
                                )
                            ]
                        )
                    ]
                    combine_columns = columns + next_page_column

                    carousel_template_message = TemplateSendMessage(
                    alt_text='類別下的細類',
                    template=CarouselTemplate(
                        columns=combine_columns
                        )
                    )
                    line_bot_api.reply_message(event.reply_token, carousel_template_message)
        
    
    if event.message.text == '剩下的大卡數':
        text_message = TextSendMessage(text=f'你還有{read_calories()}大卡！')
        line_bot_api.reply_message(event.reply_token, text_message)

    

@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == '主食_p2':
        next_page_column = [
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/cL9fa88.png',
                        title='看看下一頁',
                        text='看看下一頁',
                        actions=[
                            PostbackAction(
                                label='我要看下一頁',
                                display_text='next',
                                data='主食_p2'
                            )
                        ]
                    )
                ]
        carousel_template_message = TemplateSendMessage(
                alt_text='類別下的細類',
                template=CarouselTemplate(
                    columns=next_page_column
                        )
                )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    if event.postback.data == 'calories':
        f = open("calories.txt","r")
        calories = f.readline()
        f.close()
        text_message = TextSendMessage(text=f'你還有{calories}大卡')
        line_bot_api.reply_message(event.reply_token, text_message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)