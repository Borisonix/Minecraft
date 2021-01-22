from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from settings import *
from Build import *
# import time

# mc = Minecraft.create()

posZACHISTKA = posMAIN.clone()
posZACHISTKA.x += 300
posZACHISTKA.y += 150
posZACHISTKA.z += 400
mc.setBlocks(posMAIN, posZACHISTKA, AIR)    # зачистка территории

posZACHISTKA.y = posMAIN.y
mc.setBlocks(posMAIN, posZACHISTKA, STONE)  # каменная площадка

posMAIN.x += 20
posMAIN.y += 1
posMAIN.z += 70

# school112()         # постройка школы
walls4()