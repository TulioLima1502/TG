#!/usr/bin/env python
import os
import time
import shutil
import threading

class align():
    def alinha_arquivos(self, name, images, cmdvel):
        if os.path.isfile("../bag-files/joy/"+name):
            diferenca_images = []
            #images = [arq for arq in os.listdir("../bag-files/images")]
            for img in sorted(images):
                diferenca_images.append(abs(int(img[0:-5]) - int(name[0:-4])))
                #print(int(img[0:-5]) - int(name[0:-4]))
                if (int(img[0:-5]) - int(name[0:-4])) > 0:
                    break

            if os.path.isfile("../bag-files/images/" + name[0:-4] + ".jpeg"):
                shutil.copyfile("../bag-files/images/" + name[0:-4] + ".jpeg", "../bag-files/database_images/" + name[0:-4] + ".jpeg")

            elif os.path.isfile("../bag-files/images/" + str(int(name[0:-4]) + int(sorted(diferenca_images)[0])) + ".jpeg"):
                shutil.copyfile("../bag-files/images/" + str(int(name[0:-4]) + int(sorted(diferenca_images)[0])) + ".jpeg", "../bag-files/database_images/" + name[0:-4] + ".jpeg")

            elif os.path.isfile("../bag-files/images/" + str(int(name[0:-4]) - int(sorted(diferenca_images)[0])) + ".jpeg"):
                shutil.copyfile("../bag-files/images/" + str(int(name[0:-4]) - int(sorted(diferenca_images)[0])) + ".jpeg", "../bag-files/database_images/" + name[0:-4] + ".jpeg")

            diferenca_cmdvel = []
            #cmdvel = [arq for arq in os.listdir("../bag-files/cmd_vel")]
            for comando in sorted(cmdvel):
                diferenca_cmdvel.append(
                    abs(int(comando[0:-4]) - int(name[0:-4])))
                if (int(comando[0:-4]) - int(name[0:-4])) > 0:
                    break

            if os.path.isfile("../bag-files/cmd_vel/" + name[0:-4] + ".txt"):
                shutil.copyfile("../bag-files/cmd_vel/" + name[0:-4] + ".txt", "../bag-files/database_cmdvel/" + name[0:-4] + ".txt")

            elif os.path.isfile("../bag-files/cmd_vel/" + str(int(name[0:-4]) + int(sorted(diferenca_cmdvel)[0])) + ".txt"):
                shutil.copyfile("../bag-files/cmd_vel/" + str(int(name[0:-4]) + int(sorted(diferenca_cmdvel)[0])) + ".txt", "../bag-files/database_cmdvel/" + name[0:-4] + ".txt")

            elif os.path.isfile("../bag-files/cmd_vel/" + str(int(name[0:-4]) - int(sorted(diferenca_cmdvel)[0])) + ".txt"):
                shutil.copyfile("../bag-files/cmd_vel/" + str(int(name[0:-4]) - int(sorted(diferenca_cmdvel)[0])) + ".txt", "../bag-files/database_cmdvel/" + name[0:-4] + ".txt")

            shutil.copyfile("../bag-files/joy/" + name[0:-4] + ".txt", "../bag-files/database_joy/" + name[0:-4] + ".txt")

    def alinha(self):
        if os.path.isdir("../bag-files/joy"):
            arquivos = [arq for arq in os.listdir("../bag-files/joy")]
            images = [arq for arq in os.listdir("../bag-files/images")]
            cmdvel = [arq for arq in os.listdir("../bag-files/cmd_vel")]

            for name in sorted(arquivos):
                #self.alinha_arquivos(name)
                p = threading.Thread(target=self.alinha_arquivos(name,images,cmdvel))
                p.start()
                #time.sleep(0.1)
            p.join()
        else:
            print("Pasta nao encontrada")
        exit()

if __name__ == '__main__':
    mydata = align()
    mydata.alinha()
