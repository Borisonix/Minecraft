from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

H_B = 8         # высота блока стены
H_B_3 = 13      # высота высокого блока стены
H_B_4 = 5       # высота широкого блока стены

H_COKOL = 2     # высота цоколя
H_ZONA_A = 2    # высота зоны А
W_B_1 = 9       # ширина блока стены тип 1
W_B_2 = 7       # ширина блока стены тип 2
W_B_3 = 7       # ширина блока стены тип 3
W_B_4 = 7       # ширина блока стены тип 4

W_OKNA_1, H_OKNA_1 = 5, 5       # ширина и высота окна типа 1
W_OKNA_2, H_OKNA_2 = 4, 5       # ширина и высота окна типа 2
W_OKNA_3, H_OKNA_3 = 2, 5       # ширина и высота окна типа 3 - лестничные площадки
W_OKNA_4, H_OKNA_4 = 1, 2       # ширина и высота окна типа 4 - вентиляция
W_OKNA_5, H_OKNA_5 = 4, 10      # ширина и высота окна типа 5 - спорт залы

W_DOOR_1, H_DOOR_1 = 3, 6       # ширина и высота двери главный вход

AIR = 0                 # воздух
STONE = 1               # камень для основы
WHITE = 155
BROWN = 159, 12          # было 35,14
ORANGE = 159, 1
BROWN_DARK = 159, 12      # темно-коричневый для цоколя было 159,7
OKNO = 160      # 102              тонкое окно
PAUSE = 0
KAMEN = 44
FONAR = 89   # отмечены точки начала строительства перекрытий. Для построения заменить на 0!!!
SVET = 89
GREY_GLASS_PAN = 160, 7
GLASS_PAN = 102
STUPENI = 156, 3
STUPENI2 = 156, 2
RED = 35, 14
ZABOR = 85, 1
ZABOR2 = 85, 0

mc = Minecraft.create()

posMAIN = Vec3(122, 67, -1011)

''' для первичного позиционирования игрока в новом мире разкомментарить
posMy = posMAIN.clone()
posMy.y += 5
mc.player.setTilePos(posMy)
#'''

floor = list()      # список опорных точек для построения полов и крыши
krilco = list()