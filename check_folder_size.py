def check_size():
    # import module
    import os
    import shutil

    # assign folder path
    msg = ""
    folder_path = "C:\\MusicBot\\audio_cache"
    # get size
    total_size = 0
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.stat(fp).st_size
    # display size
    msg = "\"" + folder_path + "\" 大小： " + str(total_size) + " 位元組，"
    if total_size > 1000000000:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                msg += "已刪除。"
                print("已刪除。")
            except Exception as e:
                msg += "刪除 %s失敗。 原因： %s" % (file_path, e)
                print("刪除 %s失敗。 原因： %s" % (file_path, e))
    else:
        msg += "未刪除。"
    print(msg)
    return msg


if __name__ == "__main__":
    check_size()
