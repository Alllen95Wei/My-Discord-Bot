def update(PID):
    import os
    os.system("git_clone.bat")
    os.kill(PID, 9)
