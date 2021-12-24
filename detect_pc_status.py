def pc_status():
    try:
        import psutil
        msg = "CPU使用率：" + str(psutil.cpu_percent()) + "%" + " / 記憶體使用率：" + str(psutil.virtual_memory().percent) + "%"
    except Exception as e:
        msg = "```" + str(e) + "```"
    return msg


if __name__ == "__main__":
    print(pc_status())
