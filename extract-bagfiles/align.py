#!/usr/bin/env python
import os
import time
import shutil
import threading

class align():
    def alinha_arquivos(self, name):
        if os.path.isfile("pose/"+name):
            diferenca_images = []
            images = [arq for arq in os.listdir("images")]
            for img in sorted(images):
                diferenca_images.append(abs(int(img[0:-5]) - int(name[0:-4])))

            if os.path.isfile("images/" + name[0:-4] + ".jpeg"):
                shutil.copyfile("images/" + name[0:-4] + ".jpeg", "database_images/" + name[0:-4] + ".jpeg")

            elif os.path.isfile("images/" + str(int(name[0:-4]) + int(sorted(diferenca_images)[0])) + ".jpeg"):
                shutil.copyfile("images/" + str(int(name[0:-4]) + int(sorted(diferenca_images)[0])) + ".jpeg", "database_images/" + name[0:-4] + ".jpeg")

            elif os.path.isfile("images/" + str(int(name[0:-4]) - int(sorted(diferenca_images)[0])) + ".jpeg"):
                shutil.copyfile("images/" + str(int(name[0:-4]) - int(sorted(diferenca_images)[0])) + ".jpeg", "database_images/" + name[0:-4] + ".jpeg")

            diferenca_cmdvel = []
            cmdvel = [arq for arq in os.listdir("cmd_vel")]
            for comando in sorted(cmdvel):
                diferenca_cmdvel.append(
                    abs(int(comando[0:-4]) - int(name[0:-4])))

            if os.path.isfile("cmd_vel/" + name[0:-4] + ".txt"):
                shutil.copyfile("cmd_vel/" + name[0:-4] + ".txt", "database_cmdvel/" + name[0:-4] + ".txt")

            elif os.path.isfile("cmd_vel/" + str(int(name[0:-4]) + int(sorted(diferenca_cmdvel)[0])) + ".txt"):
                shutil.copyfile("cmd_vel/" + str(int(name[0:-4]) + int(sorted(diferenca_cmdvel)[0])) + ".txt", "database_cmdvel/" + name[0:-4] + ".txt")

            elif os.path.isfile("cmd_vel/" + str(int(name[0:-4]) - int(sorted(diferenca_cmdvel)[0])) + ".txt"):
                shutil.copyfile("cmd_vel/" + str(int(name[0:-4]) - int(sorted(diferenca_cmdvel)[0])) + ".txt", "database_cmdvel/" + name[0:-4] + ".txt")

            diferenca_joy = []
            joy = [arq for arq in os.listdir("joy")]
            for comandojoy in sorted(joy):
                diferenca_joy.append(
                    abs(int(comandojoy[0:-4]) - int(name[0:-4])))

            if os.path.isfile("joy/" + name[0:-4] + ".txt"):
                shutil.copyfile("joy/" + name[0:-4] + ".txt", "database_joy/" + name[0:-4] + ".txt")

            elif os.path.isfile("joy/" + str(int(name[0:-4]) + int(sorted(diferenca_joy)[0])) + ".txt"):
                shutil.copyfile("joy/" + str(int(name[0:-4]) + int(sorted(diferenca_joy)[0])) + ".txt", "database_joy/" + name[0:-4] + ".txt")

            elif os.path.isfile("joy/" + str(int(name[0:-4]) - int(sorted(diferenca_joy)[0])) + ".txt"):
                shutil.copyfile("joy/" + str(int(name[0:-4]) - int(sorted(diferenca_joy)[0])) + ".txt", "database_joy/" + name[0:-4] + ".txt")

            shutil.copyfile("pose/" + name[0:-4] + ".txt", "database_pose/" + name[0:-4] + ".txt")

    def alinha(self):
        if os.path.isdir("pose"):
            arquivos = [arq for arq in os.listdir("pose")]
            for name in sorted(arquivos):
                #self.alinha_arquivos(name)
                p = threading.Thread(target=self.alinha_arquivos(name))
                p.start()
                #time.sleep(0.1)
            p.join()
        else:
            print("Pasta nao encontrada")
        exit()

if __name__ == '__main__':
    mydata = align()
    mydata.alinha()
