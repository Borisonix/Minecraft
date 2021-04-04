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

def ustup(posStart: Vec3, k, d, delta, matirial, direct, p_ossZ = True):
    '''
    Построение группы уступом по диагонали
    :param posStart:        стартовая позиция
    :param k:               кол-во балок
    :param d:               длина балок
    :param delta:           признак подъема = +1, спуска = -1, ровно = 0
    :param matirial:        материал
    :param direct:          направление построения групп +1 - вдоль оси изм. стартовых точек, -1 - против оси
    :p_ossZ:  стартовые точки изменяются вдоль оси Z (балки параллельны оси X) =True. Иначе, все наоборот.
    :return:                позиция следующей группы
    '''
    for i in range(k+1):
        posS = posStart.clone()
        posE = posStart.clone()
        posS.y += i * delta
        if p_ossZ:
            posS.z += i * direct
        else:
            posS.x -= i * direct
        if i < k:
            posE.y += i * delta
            if p_ossZ:
                posS.x -= d-1
                posE.z += i * direct
            else:
                posE.x -= i * direct
                posE.z += d-1
            posE2 = posE.clone()
            posE2.y += 3
            mc.setBlocks(posS, posE2, AIR)  # удаление 5 рядов над тем, что стоим
            mc.setBlocks(posS, posE, matirial)
        else:
            return posS


def stolbik(posStart: Vec3, h, matirial):
    '''
    Построение столбика
    :param posStart:        стартовая позиция
    :param h:               высота столбика
    :param matirial:        материал
    '''
    posS = posStart.clone()
    posE = posStart.clone()
    posE.y += h-1
    mc.setBlocks(posS, posE, matirial)

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
        ustup(posSStup, 2, 4, -1, STUPENI, direction)
    else:
        ustup(posSStup, 2, 4, -1, STUPENI2, direction)
    # столбики
    posS = posStart.clone()
    posS.x -= 3
    posS.y += 1
    stolbik(posS, 5, RED)
    posS.z += 6 * direction
    stolbik(posS, 5, RED)
    # крыша крыльца
    posS = posStart.clone()
    posS.y += 6
    posS = ustup(posS, 2, 4, 1, RED, direction)
    posS = ustup(posS, 2, 4, 0, RED, direction)
    posS = ustup(posS, 3, 4, -1, RED, direction)
    # поручни крыльца
    posS = posStart.clone()
    posS.y += 1
    posS = ustup(posS, 1, 3, 0, ZABOR, direction)
    posS.x -= 3
    posS = ustup(posS, 5, 1, 0, ZABOR2, direction)

def krilco_main(posStart: Vec3):
    # основание крыльца
    posEnd = posStart.clone()
    posEnd.x -= 41
    posEnd.y -= 1
    posEnd.z += 8
    mc.setBlocks(posStart, posEnd, BROWN)

    posS = posStart.clone()
    posS.x -= 31
    posS.z += 9
    posE = posS.clone()
    posE.x -= 10
    posE.y -= 1
    posE.z += 45
    mc.setBlocks(posS, posE, BROWN)

    posS = posStart.clone()
    posS.z += 55
    posE = posS.clone()
    posE.x -= 41
    posE.y -= 1
    posE.z += 9
    mc.setBlocks(posS, posE, BROWN)

    # ступени
    posSStup = posStart.clone()
    posSStup.x -= 40
    posSStup.z += 1
    ustup(posSStup, 2, 8, -1, (156, 0), 1, False)
    posSStup.z += 26
    ustup(posSStup, 2, 9, -1, (156, 0), 1, False)
    posSStup.z += 29
    ustup(posSStup, 2, 8, -1, (156, 0), 1, False)
    # столбики
    posS = posStart.clone()
    posS.x -= 38
    posS.z += 18
    posS.y += 1
    stolbik(posS, 6, RED)
    posS.z += 8
    posS.x -= 3
    stolbik(posS, 6, RED)
    posS.z += 10
    stolbik(posS, 6, RED)
    posS.z += 8
    posS.x += 3
    stolbik(posS, 6, RED)

    # крыша крыльца
    posS = posStart.clone()
    posS.x -= 32
    posS.z += 18
    posS.y += 7
    posS = ustup(posS, 3, 7, 1, RED, 1)
    posS = ustup(posS, 2, 7, 0, RED, 1)
    posS = ustup(posS, 4, 7, -1, RED, 1)
    posS.y += 1
    posS.z -= 1
    posS = ustup(posS, 3, 10, 1, RED, 1)
    posS = ustup(posS, 4, 10, 0, RED, 1)
    posS = ustup(posS, 4, 10, -1, RED, 1)
    posS.y += 1
    posS.z -= 1
    posS = ustup(posS, 3, 7, 1, RED, 1)
    posS = ustup(posS, 2, 7, 0, RED, 1)
    posS = ustup(posS, 4, 7, -1, RED, 1)
    # поручни крыльца
    posS = posStart.clone()
    posS.y += 1
    posS = ustup(posS, 1, 42, 0, ZABOR, 1)
    posS.z += 8
    posS.x -= 40
    posS = ustup(posS, 1, 2, 0, ZABOR, 1)
    posS.x -= 1
    posS = ustup(posS, 16, 1, 0, ZABOR2, 1)
    posS.z += 11
    posS = ustup(posS, 18, 1, 0, ZABOR2, 1)
    posS.x += 1
    posS = ustup(posS, 1, 2, 0, ZABOR, 1)
    posS = posStart.clone()
    posS.y += 1
    posS.z += 64
    posS = ustup(posS, 1, 42, 0, ZABOR, 1)