import h5py
import os

arquivos = [arq for arq in os.listdir("./log")]
for name in sorted(arquivos):

  info = h5py.File("./log/"+name, "r")

  key = list(info.keys())[0]
  print(info['steering_angle'])
  angulos = []

  for i in range(0, info['steering_angle'].shape[0]):
    angle_steers = info['steering_angle'][i]
    angulos.append(angle_steers)

  print(name,min(angulos),max(angulos))
