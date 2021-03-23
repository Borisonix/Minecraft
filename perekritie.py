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
