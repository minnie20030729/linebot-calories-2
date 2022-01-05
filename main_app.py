# 載入LineBot所需要的模組
from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import re
import csv

app = Flask(__name__)
 
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('5uqC6REb69jMZ6cvEJEm2UfjrWTS3VfCUjrcNeLfbG1aYhkRZwGgN2LWdrO1P960bF0Q46YsabvneGoIyxHUcXLTR14LFYWJD29kYqi3YPuKN2+vFZ0KYduImkd6VB98OIHdbhlNTb4TY+X0t17i/wdB04t89/1O/w1cDnyilFU=0sgxc4zU4YQBb7n/FnHNs7ksEE1VcCPYUPn6ONSgVYmK9SMn3EHlSf0W5LqT2awT2XmlckW16ARg+vr+eN28Fujt6wmn3Br6glYlplaC8zjjqWlFZ7oa0tX70AePDTWXP+qyZgAeOPBAkyuKuPyWtgdB04t89/1O/w1cDnyilFU=')
 
# 必須放上自己的Channel Secret
handler = WebhookHandler('70a64584bb53162ebe1a5401b3d763b1')

'''
# 開啟richMenu
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
'''

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

# 建立儲存食物資料的類別

class BigFoodGroup:
    
    def __init__(self, title, text, url):
        self.title = title
        self.text = text
        self.url = url

class SmallFoodGroup:

    def __init__(self, title, text, url):
        self.title = title
        self.text = text
        self.url = url

class Food:
    
    def __init__(self, title, text, url, calories):
        
        self.title = title
        self.text = text
        self.url = url
        self.calories = int(calories)


# 自定義function

## 計算卡路里用 ##
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

## 「下一頁」資料用 ##
def build_nextpage_info(food_lst):
    f = open("next_page.txt","w")
    for item in food_lst:
        print(item, file=f)
    f.close()

def update_nextpage_info():
    f_1 = open("next_page.txt","r")
    food_lst = []
    for line in f_1:
        food_lst.append(line.strip())
    if len(food_lst) > 9:
        show_lst = food_lst[0:9]
        others = food_lst[9:]
        f_1.close()
        f_2 = open("next_page.txt","w")
        for item in others:
            print(item, file=f_2)
        f_2.close()
    else:
        show_lst = food_lst[0:]
        f_1.close()
        f_2 = open("next_page.txt","w")
        f_2.close()
        
    return show_lst

# 讀取 database 並導入其資料

food_data = {}
    
big_food_group_class = []
big_food_group_text = []
    
small_food_group_class = []
small_food_group_text = []
    
food_class = []
food_text = []

with open('food_data.csv', 'r', encoding = 'UTF-8-sig') as f:
    csvFile = csv.DictReader(f)
    
    for row in csvFile:
        
        # 判斷食物大類是否已存在，若不存在，貼進大類的 list 中，並創建成 class 資訊存起來
        if row['food_cate'] not in big_food_group_text:
            
            big_food_group_text.append(row['food_cate'])
            temp_1 = BigFoodGroup(row['food_cate'], row['food_cate_dis'], row['food_cate_url'])
            big_food_group_class.append(temp_1)
            
        # 判斷食物小類是否已存在，若不存在，貼進小類的 list 中，並創建成 class 資訊存起來
        if row['food_type'] not in small_food_group_text:
            
            small_food_group_text.append(row['food_type'])
            temp_2 = SmallFoodGroup(row['food_type'], row['food_type_dis'], row['food_type_url'])
            small_food_group_class.append(temp_2)
        
        # 判斷食物品項是否已存在，若不存在，貼進品項的 list 中，並創建成 class 資訊存起來
        if row['food'] not in food_text:
            
            food_text.append(row['food'])
            temp_3 = Food(row['food'], row['food_dis'], row['food_url'], row['calories'])
            food_class.append(temp_3)
        
        # 判斷食物大類是否在 dict 中
        # 若不在，新增食物大類、細項、品項
        if row['food_cate'] not in food_data:
            food_data[row['food_cate']] = {row['food_type']: [row['food']]}
            
        # 若在，判斷細項是否於食物大類中
            # 若不在，新增食物細項、品項
        elif row['food_type'] not in food_data.get(row['food_cate']):
            food_data[row['food_cate']].update({row['food_type']:[row['food']]})
            
            # 若在，新增食物、品項
        else:
            food_data[row['food_cate']][row['food_type']] += [row['food']]


# 主程式碼重複應用的 elements 存放區
next_page_column = [
    CarouselColumn(
        thumbnail_image_url='https://i.imgur.com/cL9fa88.png',
        title='看看下一頁',
        text='看看下一頁',
        actions=[
            PostbackAction(
                label='我要看下一頁',
                display_text='',
                data='下一頁'
            )
        ]
    )
]


#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # 開頭觸發文字
    if event.message.text == '我餓':
        calories_request_message = TextSendMessage(text='今天想吃多少大卡呢~\n請輸入"XXXX大卡"')
        line_bot_api.reply_message(event.reply_token, calories_request_message)

    # 請使用者輸入大卡數
    if "大卡" in event.message.text:
        try:
            calories = int(event.message.text[:-2])
            update_calories(calories)

            inform_message = TextSendMessage(text=f'您有{read_calories()}大卡，想吃哪類食物呢？')

            mainMenu_flex_message = FlexSendMessage(
                alt_text='主選單',
                contents={
                        "type": "bubble",
                        "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                          {
                            "type": "text",
                            "text": "想吃哪一類食物呢?",
                            "weight": "bold",
                            "size": "lg",
                            "gravity": "center"
                          },
                          {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                              {
                                "type": "button",
                                "action": {
                                  "type": "message",
                                  "label": "輕食",
                                  "text": "輕食"
                                },
                                "height": "sm",
                                "style": "secondary",
                                "gravity": "center",
                                "color": "#f1eddf"
                              },
                              {
                                "type": "text",
                                "text": "沙拉、三明治、漢堡、捲餅、包子",
                                "size": "xs",
                                "align": "center",
                                "gravity": "top"
                              },
                              {
                                "type": "button",
                                "action": {
                                  "type": "message",
                                  "label": "麵包",
                                  "text": "麵包"
                                },
                                "height": "sm",
                                "style": "secondary",
                                "gravity": "center",
                                "color": "#f1eddf"
                              },
                              {
                                "type": "text",
                                "text": "甜、鹹",
                                "size": "xs",
                                "align": "center",
                                "gravity": "top"
                              },
                              {
                                "type": "button",
                                "action": {
                                  "type": "message",
                                  "label": "御飯糰",
                                  "text": "御飯糰"
                                },
                                "height": "sm",
                                "style": "secondary",
                                "gravity": "center",
                                "color": "#f1eddf"
                              },
                              {
                                "type": "text",
                                "size": "xs",
                                "align": "center",
                                "gravity": "top",
                                "text": "三角、圓形、加熱、壽司"
                              },
                              {
                                "type": "button",
                                "action": {
                                  "type": "message",
                                  "label": "關東煮",
                                  "text": "關東煮"
                                },
                                "height": "sm",
                                "style": "secondary",
                                "gravity": "center",
                                "color": "#f1eddf"
                              },
                              {
                                "type": "text",
                                "size": "xs",
                                "align": "center",
                                "gravity": "top",
                                "text": "蔬菜、肉類、海鮮、其他"
                              },
                              {
                                "type": "button",
                                "action": {
                                  "type": "message",
                                  "label": "飯類",
                                  "text": "飯類"
                                },
                                "height": "sm",
                                "style": "secondary",
                                "gravity": "center",
                                "color": "#f1eddf"
                              },
                              {
                                "type": "text",
                                "text": "咖哩飯、燴飯、便當、炒飯、粥、燉飯",
                                "size": "xs",
                                "align": "center",
                                "gravity": "top"
                              },
                              {
                                "type": "button",
                                "action": {
                                  "type": "message",
                                  "label": "麵類",
                                  "text": "麵類"
                                },
                                "height": "sm",
                                "style": "secondary",
                                "gravity": "center",
                                "color": "#f1eddf"
                              },
                              {
                                "type": "text",
                                "text": "涼麵、義大利麵、牛肉麵、拌麵",
                                "size": "xs",
                                "align": "center",
                                "gravity": "top"
                              },
                              {
                                "type": "button",
                                "action": {
                                  "type": "message",
                                  "label": "湯滷類",
                                  "text": "湯滷類"
                                },
                                "height": "sm",
                                "style": "secondary",
                                "gravity": "center",
                                "color": "#f1eddf"
                              },
                              {
                                "type": "text",
                                "text": "火鍋、滷味、湯品、鍋物",
                                "size": "xs",
                                "align": "center",
                                "gravity": "top"
                              }
                            ]
                          }
                        ]
                      }
                    }
            )
         
            line_bot_api.reply_message(event.reply_token,[inform_message, mainMenu_flex_message])

        except ValueError:
            pass

    # 當使用者輸入大類
    if event.message.text in big_food_group_text:

        # 找出其之下的小類並記憶
        temp_small_group_lst = list(food_data[event.message.text].keys())
        build_nextpage_info(temp_small_group_lst)
        small_group_lst = update_nextpage_info()
        

        # 製作成輸出的旋轉 columns 格式
        output_carousel_columns = []
        for small in small_group_lst:
            info_index = small_food_group_text.index(small)
            output_carousel_columns.append(
                CarouselColumn(
                    thumbnail_image_url=small_food_group_class[info_index].url,
                    title=small_food_group_class[info_index].title,
                    text=small_food_group_class[info_index].text,
                    actions=[
                        MessageAction(
                            label='我要選這個',
                            text=small_food_group_class[info_index].title
                        )
                    ]
                )
            )

        combine_columns = output_carousel_columns + next_page_column

        carousel_template_message = TemplateSendMessage(
            alt_text='大類下的小類',
            template=CarouselTemplate(
            columns=combine_columns
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)


    # 當使用者輸入小類
    if event.message.text in small_food_group_text:
                
        # 先找出其所屬的大類
        for key in food_data:
            if event.message.text in food_data[key]:
                big_group_name = key
                break
            
        # 再找出其之下的品項並記憶
        temp_food_lst = food_data[big_group_name][event.message.text]
        build_nextpage_info(temp_food_lst)
        food_lst = update_nextpage_info()

        # 製作成輸出的旋轉 columns 格式
        output_carousel_columns = []
        for food in food_lst:
            info_index = food_lst.index(food)
            output_carousel_columns.append(
                CarouselColumn(
                    thumbnail_image_url=food_class[info_index].url,
                    title=food_class[info_index].title,
                    text=food_class[info_index].text,
                    actions=[
                        MessageAction(
                            label='我要選這個',
                            text=food_class[info_index].title
                        )
                    ]
                )
            )

        combine_columns = output_carousel_columns + next_page_column

        carousel_template_message = TemplateSendMessage(
            alt_text='細類下的食物',
            template=CarouselTemplate(
            columns=combine_columns
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

'''
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
                                text=j.title
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
        
'''


    

@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == '下一頁':

        next_page_lst = update_nextpage_info()

        output_carousel_columns = []
        if next_page_lst[0] in big_food_group_text:
            for big in next_page_lst:
                info_index = big_food_group_text.index(big)
                output_carousel_columns.append(
                    CarouselColumn(
                        thumbnail_image_url=big_food_group_class[info_index].url,
                        title=big_food_group_class[info_index].title,
                        text=big_food_group_class[info_index].text,
                        actions=[
                            MessageAction(
                                label='我要選這個',
                                text=big_food_group_class[info_index].title
                            )
                        ]
                    )
                )

        elif next_page_lst[0] in small_food_group_text:
            for small in next_page_lst:
                info_index = small_food_group_text.index(small)
                output_carousel_columns.append(
                    CarouselColumn(
                        thumbnail_image_url=small_food_group_class[info_index].url,
                        title=small_food_group_class[info_index].title,
                        text=small_food_group_class[info_index].text,
                        actions=[
                            MessageAction(
                                label='我要選這個',
                                text=small_food_group_class[info_index].title
                            )
                        ]
                    )
                )

        else:
            for food in next_page_lst:
                info_index = food_text.index(food)
                output_carousel_columns.append(
                    CarouselColumn(
                        thumbnail_image_url=food_class[info_index].url,
                        title=food_class[info_index].title,
                        text=food_class[info_index].text,
                        actions=[
                            MessageAction(
                                label='我要選這個',
                                text=food_class[info_index].title
                            )
                        ]
                    )
                )

        combine_columns = output_carousel_columns + next_page_column

        carousel_template_message = TemplateSendMessage(
                alt_text='類別下的細類',
                template=CarouselTemplate(
                    columns=combine_columns
                        )
                )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    if event.postback.data == 'calories':
        text_message = TextSendMessage(text=f'你還有{read_calories()}大卡')
        line_bot_api.reply_message(event.reply_token, text_message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)