from shutil import copyfile


def change_atpl_to_bgm():
    try:
        copyfile("C:\\MusicBot\\config\\autoplaylist.txt",
                 "Normal playlist.txt")
        copyfile("BGM playlist.txt",
                 "C:\\MusicBot\\config\\autoplaylist.txt")
        return "已嘗試將自動播放清單換為BGM。\n請將Allen Music Bot重新啟動，才會使變更生效。"
    except Exception as e:
        return_msg = "```" + str(e) + "```"
        return return_msg


def change_atpl_to_normal():
    try:
        copyfile("C:\\MusicBot\\config\\autoplaylist.txt",
                 "BGM playlist.txt")
        copyfile("Normal playlist.txt",
                 "C:\\MusicBot\\config\\autoplaylist.txt")
        return "已嘗試將自動播放清單換為Normal。\n請將Allen Music Bot重新啟動，才會使變更生效。"
    except Exception as e:
        return_msg = "```" + str(e) + "```"
        return return_msg
