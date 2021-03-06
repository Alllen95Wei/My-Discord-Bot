import os
import time
from random import randint
import discord
import subprocess
import shlex
from platform import system

import check_folder_size as cfs
import change_autoplaylist as catpl
from dotenv import load_dotenv
import log_writter
from youtube_to_mp3 import main_dl
import detect_pc_status as dps
import update

client = discord.Client()
localtime = time.localtime()
base_dir = os.path.abspath(os.path.dirname(__file__))


@client.event
async def on_ready():
    music = discord.Activity(type=discord.ActivityType.listening, name="YOASOBI is soooooo great")
    await client.change_presence(status=discord.Status.idle, activity=music)
    log_writter.write_log("-------------------------------------------------------------\n", True)
    log_writter.write_log("\n登入成功！\n目前登入身份：" +
                          str(client.user) + "\n以下為使用紀錄(只要開頭訊息有\"a!\"，則這則訊息和系統回應皆會被記錄)：\n\n")
    vc = client.get_channel(888707777659289660)
    await vc.connect()


final_msg = []
msg_author = ""
msg_is_file = False
msg_send_channel = ""
testing = False


@client.event
async def on_message(message):  # 有訊息時
    global final_msg, msg_author, msg_is_file, msg_send_channel, testing
    msg_in = message.content
    if message.author == client.user:  # 排除自己的訊息，避免陷入無限循環
        return
    elif msg_in == "a!test":
        if testing:
            testing = False
            final_msg.append("測試模式已關閉。")
        else:
            testing = True
            final_msg.append("測試模式已開啟。")
        use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
        log_writter.write_log(use_log)
    elif testing:
        return
    elif msg_in[:2] == "a!":
        use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
        log_writter.write_log(use_log)
        if len(msg_in) == 2:
            final_msg.append("我在這！\n如果需要指令協助，請輸入`a!help`")
        elif msg_in[2:5] == "say":
            if msg_in[6:] == "":
                final_msg.append("```參數:\nsay <文字>：用大聲公📣+粗體+斜體+底線說出文字```")
            else:
                msg = "📣📣___**" + str(msg_in[6:]) + "**___"
                final_msg.append(msg)
        elif msg_in[2:6] == "help":  # a! 指令說明
            final_msg.append("呼叫機器人：`a!`\n\n參數:\n"
                             "`say <文字>`：用大聲公📣+**粗體**+___斜體+底線___說出文字\n"
                             "`ama <問題>`：給你這個問題的隨機回答\n"
                             "`random <範圍>`：在指定數字範圍隨機取得一數\n"
                             "`qrcode <文字>`：將輸入的文字轉換為QR Code\n"
                             "`daily901 <new/channel/fb>`：得到關於「日常901」的資訊\n"
                             "`rickroll`：？？？\n"
                             "`sizecheck`：檢查`\"C:\\MusicBot\\audio_cache\"`的大小；當大小超過1500000000位元組時，清空該資料夾\n"
                             "`changeatpl <bgm/normal>`：更換Allen Music Bot的自動播放清單\n"
                             "`ytdl <YouTube連結>`：下載YouTube的影片為mp3\n"
                             "`rc`：重新連接語音頻道「貓娘實驗室ww/音樂 (96kbps)」\n"
                             "`dps`：查詢伺服器電腦的CPU及記憶體使用率\n"
                             "`ping`：查詢機器人的延遲(毫秒)\n"
                             "`cmd <指令>`：在伺服器端執行指令並傳回結果。"
                             "\n想得到更詳細的指令參數說明，直接輸入指令而不加參數即可\n試試看吧！")
        elif msg_in[2:5] == "ama":
            if len(msg_in) == 5:
                final_msg.append("```參數：\nama <問題>：就是8號球，給你這個問題的隨機回答```")
            else:
                ans1 = ("g", "s", "b")
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
                    try:
                        openfile = open(path, mode="r", encoding="utf8")
                        newest_video = openfile.read()
                        openfile.close()
                        final_msg.append("目前最新的影片為：\n**" + newest_video + "**\n\n還沒訂閱嗎？\nhttps://www.youtube.com"
                                                                          "/channel/UCYo6tbHa4AxwStRqWWhaYhw"
                                                                          "?sub_confirmation=1")
                    except Exception as e:
                        final_msg.append("```" + str(e) + "```")
                if msg_in[11:18] == "channel":
                    final_msg.append("日常901的頻道連結：https://www.youtube.com/channel/UCYo6tbHa4AxwStRqWWhaYhw")
                if msg_in[11:13] == "fb":
                    final_msg.append("鮑哥粉絲團的連結：https://fb.me/liyuan.baoge")
        elif msg_in[2:10] == "rickroll":
            channel = message.author.voice.channel
            try:
                await channel.connect()
            except Exception as e:
                final_msg.append("```" + str(e) + "```")
            final_msg.append("ap!p never gonna give you up")
            final_msg.append("ap!skip f")
            msg_send_channel = client.get_channel(891665312028713001)
        elif msg_in[2:11] == "sizecheck":
            if "Direct Message" in str(message.channel):
                final_msg.append("不能在私人訊息使用此指令。請至伺服器使用此指令。")
            elif str(message.author) == "Allen Why#5877" or str(message.guild.owner):
                final_msg.append(cfs.check_size())
                msg_author = message.author
            else:
                final_msg.append("你無權使用此指令。")
        elif msg_in[2:8] == "runmsb":
            if "Direct Message" in str(message.channel):
                final_msg.append("不能在私人訊息使用此指令。請至伺服器使用此指令。")
            elif str(message.author) == "Allen Why#5877" or str(message.guild.owner):
                os.system("C:\\MusicBot\\run.bat")
                final_msg.append("已嘗試執行Allen Music Bot。")
            else:
                final_msg.append("你無權使用此指令。")
        elif msg_in[2:12] == "changeatpl":
            if "Direct Message" in str(message.channel):
                final_msg.append("不能在私人訊息使用此指令。請至伺服器使用此指令。")
            else:
                if str(message.author) == "Allen Why#5877" or str(message.guild.owner):
                    if msg_in[13:16] == "bgm":
                        final_msg.append(catpl.change_atpl_to_bgm())
                    elif msg_in[13:19] == "normal":
                        final_msg.append(catpl.change_atpl_to_normal())
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
                if main_dl(yt_url, file_name, file_name + ".mp3") == "finished":
                    final_msg.append(discord.File(file_name + ".mp3"))
                    msg_is_file = True
        elif msg_in[2:4] == "rc":
            vc = client.get_channel(888707777659289660)
            try:
                await vc.connect()
                final_msg.append("已嘗試加入「貓娘實驗室ww/音樂 (96kbps)」。")
            except Exception as e:
                if str(e) == "Already connected to a voice channel.":
                    final_msg.append("已經連線至語音頻道。")
                else:
                    final_msg.append("```" + str(e) + "```")
        elif msg_in[2:5] == "dps":
            act_msg = dps.pc_status()
            final_msg.append(act_msg)
        elif msg_in[2:6] == "ping":
            final_msg.append("目前延遲：" + str(round(client.latency * 1000)) + "ms")
        elif msg_in[2:3] == "y":
            if message.author == msg_author:
                msg_author = ""
                final_msg.append(cfs.clean_folder())
            else:
                final_msg.append("此回覆無效。")
        elif msg_in[2:5] == "cmd":
            if str(message.author) == "Allen Why#5877":
                if len(msg_in) == 5:
                    final_msg.append("```參數：\ncmd <指令>：在伺服器端執行指令並傳回結果。```")
                else:
                    command = msg_in[6:]
                    if command == "cmd":
                        final_msg.append("不能使用`cmd`指令。")
                    else:
                        try:
                            command = shlex.split(command)
                            command_output = str(subprocess.run(command, capture_output=True, text=True).stdout)
                            if command_output != "":
                                final_msg.append("```" + command_output + "```")
                            else:
                                final_msg.append("終端未傳回回應。")
                        except WindowsError as e:
                            if "WinError 2" in str(e):
                                final_msg.append("似乎沒有這個指令，或指令無法透過Python執行。")
                                final_msg.append("錯誤內容：\n```" + str(e) + "```")
                            else:
                                final_msg.append("```" + str(e) + "```")
            else:
                final_msg.append("你無權使用此指令。")
        elif msg_in[2:8] == "update":
            if str(message.author) == str(client.get_user(657519721138094080)):
                update.update(os.getpid(), system())
                final_msg.append("已嘗試自GitHub取得更新，請稍候。")
            else:
                final_msg.append("你無權使用此指令。")
        else:
            final_msg.append("參數似乎無效...\n輸入`a!help`獲得說明")
    elif message.channel == client.get_channel(891665312028713001):
        if "https://www.youtube.com" == msg_in[:23] or "https://youtu.be" == msg_in[:16] or "https://open.spotify.com" \
                == msg_in[:24]:
            ap_cmd = "ap!p " + msg_in
            final_msg.append(ap_cmd)
            use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
            log_writter.write_log(use_log)
    if msg_send_channel == "":
        msg_send_channel = message.channel
    for i in range(len(final_msg)):
        current_msg = final_msg[i]
        try:
            if isinstance(current_msg, str):
                await msg_send_channel.send(current_msg)
            elif isinstance(current_msg, discord.File):
                await msg_send_channel.send(file=current_msg)
            else:
                await msg_send_channel.send("```" + str(current_msg) + "```")
            new_log = str(msg_send_channel) + "/" + str(client.user) + ":\n" + str(final_msg[i]) + "\n\n"
            log_writter.write_log(new_log)
        except Exception as e:
            if "or fewer in length." in str(e):
                txt_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'full_msg.txt')
                open(txt_file_path, "w").write(str(final_msg[i]))
                await msg_send_channel.send("由於訊息長度過長，因此改以文字檔方式呈現。", file=discord.File(txt_file_path))
                new_log = str(msg_send_channel) + "/" + str(client.user) + ":\n" + "由於訊息長度過長，因此改以文字檔方式呈現。" + "\n\n"
                log_writter.write_log(new_log)
            else:
                final_msg = "發生錯誤。錯誤內容如下：\n```" + str(e) + "```"
                await msg_send_channel.send(final_msg)
                new_log = str(msg_send_channel) + "/" + str(client.user) + ":\n" + str(final_msg) + "\n\n"
                log_writter.write_log(new_log)
    final_msg = []
    msg_is_file = False
    msg_send_channel = ""


@client.event
async def on_member_join(member):
    channel = client.get_channel(857998355082903552)
    welcome_msg = "歡迎<@" + str(member) + ">加入本伺服器！請稍待，直至伺服器管理員分配給你合適的身分組，即可與大家互動~🎵"
    await channel.system_channel.send(welcome_msg)
    new_log = str(channel) + "/" + str(client.user) + ":\n" + str(welcome_msg) + "\n\n"
    log_writter.write_log(new_log)


# 取得TOKEN
load_dotenv(dotenv_path=os.path.join(base_dir, "TOKEN.env"))
TOKEN = str(os.getenv("TOKEN"))
client.run(TOKEN)
