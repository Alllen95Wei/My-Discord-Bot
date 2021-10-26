from shutil import copyfile

def change_atpl_to_bgm():
    copyfile("C:\\MusicBot\\config\\autoplaylist.txt",
             "Normal playlist.txt")
    copyfile("BGM playlist.txt",
             "C:\\MusicBot\\config\\autoplaylist.txt")

def change_atpl_to_normal():
    copyfile("Normal playlist.txt",
             "C:\\MusicBot\\config\\autoplaylist.txt")
