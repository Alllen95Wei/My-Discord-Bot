import time
from random import randint
import discord
import check_folder_size as cfz

client = discord.Client()
localtime = time.localtime()

@client.event
async def on_ready():
    log_file = open("log.txt", mode="a")  # new
    print("登入成功！\n目前登入身份：", client.user)
    print("\n以下為使用紀錄(只要開頭訊息有\"a!\"，則這則訊息和系統回應皆會被記錄)：")
    timestamp = time.strftime("%Y-%m-%d %p %I:%M:%S", localtime)  # new
    login_log = "[" + timestamp + "]" + "登入成功！"  # new
    # new


@client.event
async def on_message(message):  # 有訊息時
    global final_msg
    localtime = time.localtime()
    timestamp = time.strftime("%Y-%m-%d %p %I:%M:%S", localtime)
    if message.author == client.user:  # 排除自己的訊息，避免陷入無限循環
        return
    msg_in = message.content
    if msg_in[:2] == "a!":
        use_log = "[" + timestamp + "]" + str(message.author) + ":\n" + msg_in + "\n\n"
        log_file = open("log.txt", mode="a")
        log_file.write(use_log)
        print(use_log, end="")
        if len(msg_in) == 2:
            final_msg = "我在這！\n如果需要指令協助，請輸入`a!help`"
        elif msg_in[2:5] == "say":
            if msg_in[6:] == "":
                final_msg = "```參數:\nsay <文字>：用大聲公+粗體+斜體+底線說出文字```"
            else:
                msg = "📣📣___**" + str(msg_in[6:]) + "**___"
                final_msg = msg
        elif msg_in[2:6] == "help":  # a! 指令說明
            final_msg = "呼叫機器人：`a!`\n\n參數:\n" \
                        "`say <文字>`：用大聲公+粗體+斜體+底線說出文字\n" \
                        "`ama <問題>`：給你這個問題的隨機回答\n" \
                        "`random <範圍>`：在指定數字範圍隨機取得一數\n" \
                        "`qrcode <文字>`：將輸入的文字轉換為QR Code\n" \
                        "`daily901 <new/channel/fb>`：得到關於「日常901」的資訊\n" \
                        "`rickroll`：？？？" \
                        "\n想得到更詳細的指令參數說明，直接輸入指令而不加參數即可\n試試看吧！"
        elif msg_in[2:5] == "ama":
            final_msg = "```本指令開發中，敬請期待！```"
            if len(msg_in) == 5:
                final_msg = "```參數：\nama <問題>：就是8號球，給你這個問題的隨機回答```"
            else:
                ans1 = ["g", "s", "b"]
                ans_g = ("看起來不錯喔", "肯定的", "我覺得可行", "絕對OK", "是的", "確定", "200 OK", "100 Continue", "Just do it")

                ans_s = (
                    "現在別問我", "404 Not Found", "你的問題超出宇宙的範圍了", "答案仍在變化", "400 Bad Request", "這問題實在沒人答得出來",
                    "Answer=A=Ans=答案",
                    "最好不要現在告訴你", "300 Multiple Choices", "去問瑪卡巴卡更快", "您撥的電話無人接聽，嘟聲後開始計費。", "對不起，您播的號碼是空號，請查明後再撥。")

                ans_b = (
                    "不可能", "否定的", "不值得", "等等等等", "No no no", "我拒絕", "我覺得不行耶", "https://cdn2.ettoday.net/images/4945"
                                                                              "/4945172.jpg", "403 Forbidden",
                    "這樣不好")

                ball_result1 = ans1[randint(0, 2)]
                if ball_result1 == "g":
                    ball_result2 = ans_g[randint(0, len(ans_g) - 1)]
                    ans2 = "```diff\n+✓" + ball_result2
                elif ball_result1 == "s":
                    ball_result2 = ans_s[randint(0, len(ans_s) - 1)]
                    ans2 = "```fix\n□" + ball_result2
                else:
                    ball_result2 = ans_b[randint(0, len(ans_b) - 1)]
                    ans2 = "```diff\n-✗" + ball_result2
                final_msg = ans2 + "```"
        elif msg_in[2:8] == "random":
            if len(msg_in) == 8:
                final_msg = "```參數：\nrandom <範圍>：在指定數字範圍隨機取得一數\n" \
                            "       <範圍>：輸入2個數值，中間以逗號做分隔\n(提示：參數輸入\"%\"就會自動設定範圍為0~100)```"
            else:
                if msg_in[9:] == "%":
                    a = 0
                    b = 100
                else:
                    a = int(msg_in[9:msg_in.find(",")])
                    b = int(msg_in[msg_in.find(",") + 1:])
                r_range_result = randint(a, b)
                final_msg = "結果：```fix\n" + str(r_range_result) + "```"
        elif msg_in[2:8] == "qrcode":
            if len(msg_in) == 8:
                final_msg = "```參數：\nqrcode <文字>：將輸入的文字轉換為QR Code```"
            else:
                text = msg_in[9:]
                text = ascii(text)
                final_msg = "https://chart.apis.google.com/chart?cht=qr&chs=500x500&choe=UTF-8&chld=H|1&chl=" + text.replace(
                    "\'", "")
        elif msg_in[2:10] == "daily901":
            if msg_in[11:] == "":
                final_msg = "```參數：\ndaily901 new：得到「日常901」的最新影片資訊及連結\n         channel：得到「日常901」的連結\n         " \
                            "fb：得到「鮑哥粉絲團！！」的連結``` "
            else:
                path = "daily901-info.txt"
                if msg_in[11:14] == "new":
                    openfile = open(path, mode="r", encoding="utf8")
                    newest_video = openfile.read()
                    openfile.close()
                    final_msg = "目前最新的影片為：\n**" + newest_video + "**\n\n還沒訂閱嗎？\nhttps://www.youtube.com/channel" \
                                                                 "/UCYo6tbHa4AxwStRqWWhaYhw?sub_confirmation=1 "
                if msg_in[11:18] == "channel":
                    final_msg = "日常901的頻道連結：https://www.youtube.com/channel/UCYo6tbHa4AxwStRqWWhaYhw"
                if msg_in[11:13] == "fb":
                    final_msg = "鮑哥粉絲團的連結：https://fb.me/liyuan.baoge"

        elif msg_in[2:10] == "rickroll":
            openfile = open("Never gonna give you up lyrics.txt", mode="r")
            lyrics = openfile.read()
            final_msg = "Never gonna give you up~\nNever gonna let you " \
                        "down~\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ " + "\n\n" \
                                                                                "Lyrics：\n" + lyrics
        elif msg_in[2:11] == "sizecheck":
            cfz.check_size()
        else:
            final_msg = "參數似乎無效...\n輸入`a!help`獲得說明"
        localtime = time.localtime()
        timestamp = time.strftime("%Y-%m-%d %p %I:%M:%S", localtime)
        new_log = "[" + timestamp + "]" + str(client.user) + ":\n" + final_msg + "\n\n"
        print(new_log, end="")
        log_file.write(new_log)
        await message.channel.send(message.author.mention)
        await message.channel.send(final_msg)
        log_file.close()


client.run("ODU4MTcwNDQ4OTM2MzA0NjYw.YNaPgw.xG3Xo8jR_qeVoOn1ondRoeM8zDQ")
