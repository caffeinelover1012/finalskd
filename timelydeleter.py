import os, time, shutil

def deleter():
    for i in os.walk(os.getcwd() + "/static/songs"):
        if i[-1]:
            path = (i[0]+"/" + i[-1][0])
            passedTime = time.time()-os.path.getctime(path)
            if passedTime>=600:
                print("Deleting Path: ",path," coz ",passedTime," seconds have passed.")
                shutil.rmtree(i[0])

