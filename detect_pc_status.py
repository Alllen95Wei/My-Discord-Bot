def pc_status():
    try:
        import psutil
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        ram_total = round(psutil.virtual_memory().total / (1024^3))
        ram_free = round(psutil.virtual_memory().free / (1024^3))
        msg = "CPU使用率：" + str(cpu_usage) + "%" + " / 記憶體使用率：" + str(ram_usage) + "%" + "`(" + str(ram_free) + "MB / " + str(ram_total) + "MB)`"
    except Exception as e:
        msg = "```" + str(e) + "```"
    return msg


if __name__ == "__main__":
    from time import sleep
    while True:
        print(pc_status())
        sleep(1)
