from mcpi.vec3 import Vec3
from queue import Queue
from settings import *

def neighbors(pos):
    ret = []
    pos2 = pos.clone()
    pos2.x += 1
    if mc.getBlock(pos2) == AIR:
        ret.append(pos2)
    pos2 = pos.clone()
    pos2.x -= 1
    if mc.getBlock(pos2) == AIR:
        ret.append(pos2)
    pos2 = pos.clone()
    pos2.z += 1
    if mc.getBlock(pos2) == AIR:
        ret.append(pos2)
    pos2 = pos.clone()
    pos2.z -= 1
    if mc.getBlock(pos2) == AIR:
        ret.append(pos2)
    return ret


def flooring(posStart: Vec3, matirial):
    if mc.getBlock(posStart) == AIR:
        frontier = Queue()
        frontier.put(posStart)
        reached = set()
        reached.add(tuple([posStart.x, posStart.y, posStart.z]))

        while not frontier.empty():
            current = frontier.get()
            mc.setBlock(current, matirial)

            for next in neighbors(current):
                if (tuple([next.x, next.y, next.z])) not in reached:
                    frontier.put(next)
                    reached.add(tuple([next.x, next.y, next.z]))

