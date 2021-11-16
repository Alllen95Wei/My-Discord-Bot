import os
import time
from random import randint
import discord
import check_folder_size as cfs
import change_autoplaylist as catpl
from dotenv import load_dotenv
from youtube_to_mp3 import main_dl


client = discord.Client()
localtime = time.localtime()


@client.event
async def on_ready():
    music = discord.Activity(type=discord.ActivityType.listening, name="YOASOBI is soooooo great")
    await client.change_presence(status=discord.Status.dnd, activity=music)
    print("登入成功！\n目前登入身份：", client.user)
    print("\n以下為使用紀錄(只要開頭訊息有\"a!\"，則這則訊息和系統回應皆會被記錄)：")
    timestamp = time.strftime("%Y-%m-%d %p %I:%M:%S", localtime)
    try:
        log_file = open("log.txt", mode="a")
        login_log = "-------------------------------------------------------------\n[" + timestamp + "]" + "登入成功！\n"
        log_file.write(login_log)
        log_file.close()
    except Exception as e:
        print(e)
    vc = client.get_channel(888707777659289660)
    await vc.connect()


final_msg = []
msg_author = ""
msg_count = 1
msg_is_file = False
msg_send_channel = ""


@client.event
async def on_message(message):  # 有訊息時
    global final_msg, msg_author, msg_count, msg_is_file, msg_send_channel
    local_time = time.localtime()
    timestamp = time.strftime("%Y-%m-%d %p %I:%M:%S", local_time)
    if message.author == client.user:  # 排除自己的訊息，避免陷入無限循環
        return
    msg_in = message.content
    if msg_in[:2] == "a!":
        use_log = "[" + timestamp + "]" + str(message.author) + ":\n" + msg_in + "\n\n"
        try:
            log_file = open("log.txt", mode="a")
            log_file.write(use_log)
        except Exception as e:
            print("無法寫入記錄檔。(" + str(e) + ")")
        print(use_log, end="")
        if len(msg_in) == 2:
            final_msg.append("我在這！\n如果需要指令協助，請輸入`a!help`")
        elif msg_in[2:5] == "say":
            if msg_in[6:] == "":
                final_msg.append("```參數:\nsay <文字>：用大聲公+粗體+斜體+底線說出文字```")
            else:
                msg = "📣📣___**" + str(msg_in[6:]) + "**___"
                final_msg.append(msg)
        elif msg_in[2:6] == "help":  # a! 指令說明
            final_msg.append("呼叫機器人：`a!`\n\n參數:\n"
                             "`say <文字>`：用大聲公+粗體+斜體+底線說出文字\n"
                             "`ama <問題>`：給你這個問題的隨機回答\n"
                             "`random <範圍>`：在指定數字範圍隨機取得一數\n"
                             "`qrcode <文字>`：將輸入的文字轉換為QR Code\n"
                             "`daily901 <new/channel/fb>`：得到關於「日常901」的資訊\n"
                             "`rickroll`：？？？\n"
                             "`sizecheck`：檢查\"C:\\MusicBot\\audio_cache\"的大小；當大小超過1500000000位元組時，清空該資料夾\n"
                             "`changeatpl <bgm/normal>`：更換Allen Music Bot的自動播放清單\n"
                             "`ytdl <YouTube連結>`：下載YouTube的影片為mp3"
                             "\n想得到更詳細的指令參數說明，直接輸入指令而不加參數即可\n試試看吧！")
        elif msg_in[2:5] == "ama":
            if len(msg_in) == 5:
                final_msg.append("```參數：\nama <問題>：就是8號球，給你這個問題的隨機回答```")
            else:
                ans1 = ["g", "s", "b"]
                ans_g = ("看起來不錯喔", "肯定的", "我覺得可行", "絕對OK", "是的", "確定", "200 OK", "100 Continue", "Just do it")

                ans_s = (
                    "現在別問我", "404 Not Found", "你的問題超出宇宙的範圍了", "答案仍在變化", "400 Bad Request", "這問題實在沒人答得出來",
                    "Answer=A=Ans=答案",
                    "最好不要現在告訴你", "300 Multiple Choices", "去問瑪卡巴卡更快", "您撥的電話無人接聽，嘟聲後開始計費。", "對不起，您播的號碼是空號，請查明後再撥。")

                ans_b = (
                    "不可能", "否定的", "不值得", "等等等等", "No no no", "我拒絕", "我覺得不行耶",
                    "https://cdn2.ettoday.net/images/4945/4945172.jpg",
                    "403 Forbidden", "這樣不好")

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
                final_msg.append(ans2 + "```")
        elif msg_in[2:8] == "random":
            if len(msg_in) == 8:
                final_msg.append("```參數：\nrandom <範圍>：在指定數字範圍隨機取得一數\n"
                                 "       <範圍>：輸入2個數值，中間以逗號做分隔\n(提示：參數輸入\"%\"就會自動設定範圍為0~100)```")
            else:
                if msg_in[9:] == "%":
                    a = 0
                    b = 100
                else:
                    a = int(msg_in[9:msg_in.find(",")])
                    b = int(msg_in[msg_in.find(",") + 1:])
                r_range_result = randint(a, b)
                final_msg.append("結果：```fix\n" + str(r_range_result) + "```")
        elif msg_in[2:8] == "qrcode":
            if len(msg_in) == 8:
                final_msg.append("```參數：\nqrcode <文字>：將輸入的文字轉換為QR Code```")
            else:
                text = msg_in[9:]
                final_msg.append(
                    "https://chart.apis.google.com/chart?cht=qr&chs=500x500&choe=UTF-8&chld=H|1&chl=" + text.replace(
                        "\'", ""))
        elif msg_in[2:10] == "daily901":
            if msg_in[11:] == "":
                final_msg.append("```參數：\ndaily901 new：得到「日常901」的最新影片資訊及連結\n         channel：得到「日常901」的連結\n         "
                                 "fb：得到「鮑哥粉絲團！！」的連結``` ")
            else:
                path = "daily901-info.txt"
                if msg_in[11:14] == "new":
                    openfile = open(path, mode="r", encoding="utf8")
                    newest_video = openfile.read()
                    openfile.close()
                    final_msg.append("目前最新的影片為：\n**" + newest_video + "**\n\n還沒訂閱嗎？\nhttps://www.youtube.com/channel"
                                                                      "/UCYo6tbHa4AxwStRqWWhaYhw?sub_confirmation=1 ")
                if msg_in[11:18] == "channel":
                    final_msg.append("日常901的頻道連結：https://www.youtube.com/channel/UCYo6tbHa4AxwStRqWWhaYhw")
                if msg_in[11:13] == "fb":
                    final_msg.append("鮑哥粉絲團的連結：https://fb.me/liyuan.baoge")
        elif msg_in[2:10] == "rickroll":
            channel = message.author.voice.channel
            try:
                await channel.connect()
            except Exception as e:
                print(e)
            final_msg.append("ap!pn never gonna give you up")
            final_msg.append("ap!skip f")
            msg_count = 2
            msg_send_channel = client.get_channel(891665312028713001)
        elif msg_in[2:11] == "sizecheck":
            if str(message.author) == str(message.guild.owner) or "Allen Why#5877":
                final_msg.append(cfs.check_size())
                msg_author = message.author
            else:
                final_msg.append("你無權使用此指令。")
        elif msg_in[2:8] == "runmsb":
            if str(message.author) == str(message.guild.owner) or "Allen Why#5877":
                os.system("C:\\MusicBot\\run.bat")
                final_msg.append("已嘗試執行Allen Music Bot。")
            else:
                final_msg.append("你無權使用此指令。")
        elif msg_in[2:12] == "changeatpl":
            print(message.author)
            if str(message.author) == str(message.guild.owner) or "Allen Why#5877":
                if msg_in[13:16] == "bgm":
                    catpl.change_atpl_to_bgm()
                    final_msg.append("已嘗試將自動播放清單換為BGM。\n請將Allen Music Bot重新啟動，才會使變更生效。")
                elif msg_in[13:19] == "normal":
                    catpl.change_atpl_to_normal()
                    final_msg.append("已嘗試將自動播放清單換為原狀。\n請將Allen Music Bot重新啟動，才會使變更生效。")
                else:
                    final_msg.append("```參數：\nchangeatpl bgm：將Allen Music Bot的自動播放清單換為BGM playlist。\n"
                                     "           normal：將Allen Music Bot的自動播放清單回歸原狀。```")
            else:
                final_msg.append("你無權使用此指令。")
        elif msg_in[2:6] == "ytdl":
            if len(msg_in) == 6:
                final_msg.append("```參數：\nytdl <YouTube連結>：將該YouTube影片下載為mp3，再傳回Discord。由於Discord有"
                                 "檔案大小限制，因此有時可能會失敗。```")
            else:
                yt_url = msg_in[7:]
                file_name = str(message.author) + yt_url[-11:]
                print(file_name)
                if main_dl(yt_url, file_name, file_name + ".mp3") == "finished":
                    final_msg = discord.File(file_name + ".mp3")
                    msg_is_file = True
        elif msg_in[2:3] == "y":
            if message.author == msg_author:
                msg_author = ""
                final_msg.append(cfs.clean_folder())
            else:
                final_msg.append("此回覆無效。")
        else:
            final_msg.append("參數似乎無效...\n輸入`a!help`獲得說明")
        local_time = time.localtime()
        timestamp = time.strftime("%Y-%m-%d %p %I:%M:%S", local_time)
    elif message.channel == client.get_channel(891665312028713001):
        if "https://www.youtube.com" == msg_in[:23] or "https://youtu.be" == msg_in[:16]:
            final_msg.append("ap!p " + msg_in)
            use_log = "[" + timestamp + "]" + str(message.author) + ":\n" + msg_in + "\n\n"
            try:
                log_file = open("log.txt", mode="a")
                log_file.write(use_log)
            except Exception as e:
                print("無法寫入記錄檔。(" + str(e) + ")")
            print(use_log, end="")
    else:
        return
    if msg_send_channel == "":
        msg_send_channel = message.channel
    await msg_send_channel.send(message.author.mention)
    for i in range(msg_count):
        if not msg_is_file:
            await msg_send_channel.send(final_msg[i])
            new_log = "[" + timestamp + "]" + str(client.user) + ":\n" + final_msg[i] + "\n\n"
        else:
            await msg_send_channel.send(file=final_msg)
            new_log = "[" + timestamp + "]" + str(client.user) + ":\n" + str(final_msg) + "\n\n"
        print(new_log, end="")
        try:
            log_file = open("log.txt", mode="a")
            log_file.write(new_log)
            log_file.close()
        except Exception as e:
            print("無法寫入記錄檔。(" + str(e) + ")")
    final_msg = []
    msg_count = 1
    msg_is_file = False
    msg_send_channel = ""


# 取得TOKEN
env_path = "TOKEN.env"
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
