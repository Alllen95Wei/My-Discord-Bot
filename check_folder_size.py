def check_size():
    # 匯入模組
    import os
    import shutil
    # 指定資料夾路徑
    folder_path = "C:\\MusicBot\\audio_cache"
    # 取得資料夾大小
    total_size = 0
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.stat(fp).st_size
    # 判定
    msg = "\"" + folder_path + "\" 大小： " + str(total_size) + " 位元組，"
    if total_size > 1500000000:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                msg += "已刪除。"
            except Exception as e:
                msg += "刪除 %s失敗。 原因： %s" % (file_path, e)
    else:
        msg += "未刪除。"
    return msg


if __name__ == "__main__":
    print(check_size())