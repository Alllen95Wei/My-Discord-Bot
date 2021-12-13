import time


def write_log(content, no_time_stamp=False):
    log = content
    if not no_time_stamp:
        local_time = time.localtime()
        time_stamp = time.strftime("%Y-%m-%d %p %I:%M:%S", local_time)
        log = "[" + time_stamp + "]" + log
    try:
        log_file = open("log.txt", mode="a")
        log_file.write(log)
        log_file.close()
    except Exception as e:
        print("無法寫入記錄檔。(" + str(e) + ")")
    print(log, end="")
