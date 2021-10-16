def check_size():
    # import module
    import os
    import shutil

    # assign size
    size = 0

    # assign folder path
    folder_path_list = ["C:\\MusicBot\\audio_cache", "C:\\MusicBot - 複製\\audio_cache"]
    for i in range(2):
        folder_path = folder_path_list[i]
        # get size
        for path, dirs, files in os.walk(folder_path):
            for f in files:
                fp = os.path.join(path, f)
                size = os.path.getsize(fp)
        # display size
        print("\"" + folder_path + "\" 大小： " + str(size) + " 位元組")
        if size > 1000000000:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    print("已刪除。")
                except Exception as e:
                    print("刪除 %s失敗。 原因： %s" % (file_path, e))


if __name__ == "__main__":
    check_size()
