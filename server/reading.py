import mysql.connector
import base64
import io
import PIL.Image
import time
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="pioneerpc"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS pioneer;")
mycursor.execute("USE pioneer;")
mycursor.execute("CREATE TABLE IF NOT EXISTS dados (`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY, `VELOCIDADE` varchar(25) NOT NULL, `JOYSTICK` varchar(25) NOT NULL, `imagem` longblob NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;")
mydb.close()

db = mysql.connector.connect(user='root', password='pioneerpc',
                              host='localhost',
                              database='pioneer')

images = [arq for arq in os.listdir("../TG/bag-files/database_images")]
cmd_vel = [arq for arq in os.listdir("../TG/bag-files/database_cmdvel")]
joystick = [arq for arq in os.listdir("../TG/bag-files/database_joy")]

for i in range(len(images)):
    if i % 1000 == 0 and i > 1:
        print 'Train data: {}/{}'.format(i, len(images))
    addr = images[i]

    cmdvel = open("../TG/bag-files/database_cmdvel/" + addr[0:-5] + ".txt", 'r')
    comando = cmdvel.read()
            
    joystick = open("../TG/bag-files/database_joy/" + addr[0:-5] + ".txt", 'r')
    controle = joystick.read()
            
    botao = controle.split()[6]
    botao = botao.replace('0.0)(',"")
    botao = botao.replace(',',"")
    if botao == '1':
        angulo = controle.split()[0]
        velocidade = controle.split()[1]
        angulo = angulo.replace('(',"")
        angulo = angulo.replace(',',"")
        velocidade = velocidade.replace(',',"")
                
        #print('{}'.format(float(angulo)))
        #print('{}'.format(float(velocidade)))
    else:
        angulo = 0.0
        velocidade = 0.0
        #print('{}'.format(float(angulo)))
        #print('{}'.format(float(velocidade)))
        
        #separar informacoes em conteudo de velocidade e de angulo
            
    image = open('../TG/bag-files/database_images/' + addr,'rb').read()
    
    query = "INSERT INTO dados(id,VELOCIDADE,JOYSTICK,imagem) VALUES(%s,%s,%s,%s)"
    cursor=db.cursor()
    cursor.execute(query,(0,velocidade,angulo,image))

    db.commit()
    #time.sleep(10)

db.close()
exit()
sql_fetch_blob_query = """SELECT * from dados where id = 1"""

cursor.execute(sql_fetch_blob_query)
record = cursor.fetchall()
for row in record:
    print("Id = ", row[0], )
    print("velocidade = ", row[1])
    print("joystick = ", row[2])
    image =  row[3]

    print("Storing employee image and bio-data on disk \n")
    salvar = open('teste.jpeg','wb')
    salvar.write(image)
    salvar.close()
    #write_file(image, 'teste.jpeg')

db.close()