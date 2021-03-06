def check_size(folder_path="C:\\MusicBot\\audio_cache"):
    # 匯入模組
    import os
    # 取得資料夾大小
    total_size = 0
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.stat(fp).st_size
    # 判定
    msg = "`\"" + folder_path + "\"` 大小： " + str(total_size) + " 位元組。"
    return msg


def clean_folder():
    import os
    import shutil
    folder_path = "C:\\MusicBot\\audio_cache"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            msg = "已刪除。"
        except Exception as e:
            msg = "刪除 %s失敗。 原因： %s" % (file_path, e)
        return msg


if __name__ == "__main__":
    print(check_size(folder_path=input("貼上資料夾路徑：")))
