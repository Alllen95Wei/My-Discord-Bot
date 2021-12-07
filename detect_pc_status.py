def pc_status():
    import psutil

    i = 1
    while i > 0:
        msg = "CPU使用率：" + str(psutil.cpu_percent()) + "%" + " / 記憶體使用率：" + str(psutil.virtual_memory().percent) + "%"
        return msg


if __name__ == "__main__":
    print(pc_status())
