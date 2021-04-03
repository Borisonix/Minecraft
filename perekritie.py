from mcpi.vec3 import Vec3
from queue import Queue
from settings import *

def flooring(posStart: Vec3, matirial):
    mc.setBlock(posStart, AIR)  # замена фонаря на воздух в стартовой точке
    frontier = Queue()  # инициализация стека LIFO. В него будут помещаться координаты точек в формате Vec3
    frontier.put(posStart)
    reached = set()  # инициализация множества обработанных. В него будут помещаться координаты точек заполненных
    # координаты в формате списка, чтобы можно было проверять наличие координаты в множестве
    reached.add(tuple([posStart.x, posStart.y, posStart.z]))

    while not frontier.empty():
        current = frontier.get()  # извлечение из стека последнего
        mc.setBlock(current, matirial)  # заполнение ячейки блоком

        # поиск пустых соседних ячеек, не проверявшихся ранее
        next = current.clone()
        next.x += 1
        if (tuple([next.x, next.y, next.z])) not in reached:
            if mc.getBlock(next) == AIR:
                frontier.put(next)
                reached.add(tuple([next.x, next.y, next.z]))

        next = current.clone()
        next.x -= 1
        if (tuple([next.x, next.y, next.z])) not in reached:
            if mc.getBlock(next) == AIR:
                frontier.put(next)
                reached.add(tuple([next.x, next.y, next.z]))

        next = current.clone()
        next.z += 1
        if (tuple([next.x, next.y, next.z])) not in reached:
            if mc.getBlock(next) == AIR:
                frontier.put(next)
                reached.add(tuple([next.x, next.y, next.z]))

        next = current.clone()
        next.z -= 1
        if (tuple([next.x, next.y, next.z])) not in reached:
            if mc.getBlock(next) == AIR:
                frontier.put(next)
                reached.add(tuple([next.x, next.y, next.z]))

def ustup(posStart: Vec3, k, d, delta,  matirial, direct):
    '''
    Построение группы уступом по диагонали
    :param posStart:        стартовая позиция
    :param k:               кол-во балок
    :param d:               длина балок
    :param delta:           признак подъема = +1, спуска = -1, ровно = 0
    :param matirial:        материал
    :param direct:          направление +1 - вдоль оси Z, -1 - против оси Z
    :return:                позиция следующей группы
    '''
    for i in range(k+1):
        posS = posStart.clone()
        posE = posStart.clone()
        posS.y += i * delta
        posS.z += i * direct
        if i < k:
            posE.y += i * delta
            posS.x -= d
            posE.z += i * direct
            mc.setBlocks(posS, posE, matirial)
        else:
            return posS


def krilco_t1(posStart: Vec3, direction = 1):
    # основание крыльца
    posEnd = posStart.clone()
    posEnd.x -= 3
    posEnd.y -= 1
    posEnd.z += 7 * direction
    mc.setBlocks(posStart, posEnd, WHITE)
    # ступени
    posSStup = posStart.clone()
    posSStup.z += 7 * direction
    if direction == 1:
        ustup(posSStup, 2, 3, -1, STUPENI, direction)
    else:
        ustup(posSStup, 2, 3, -1, STUPENI2, direction)
    # столбики
    posS = posStart.clone()
    posE = posStart.clone()
    posS.x -= 3
    posS.y += 1
    posE.x -= 3
    posE.y += 6
    mc.setBlocks(posS, posE, RED)
    posS.z += 6 * direction
    posE.z += 6 * direction
    mc.setBlocks(posS, posE, RED)
    # крыша крыльца
    posS = posStart.clone()
    posS.y += 6
    posS = ustup(posS, 2, 3, 1, RED, direction)
    posS = ustup(posS, 2, 3, 0, RED, direction)
    posS = ustup(posS, 3, 3, -1, RED, direction)
    # поручни крыльца
    posS = posStart.clone()
    posS.y += 1
    posS = ustup(posS, 1, 2, 0, ZABOR, direction)
    posS.x -= 3
    posS = ustup(posS, 5, 0, 0, ZABOR2, direction)
