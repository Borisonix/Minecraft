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


def flooring(posStart, matirial):
    if mc.getBlock(posStart) == AIR:
        frontier = Queue()
        frontier.put(posStart)
        # reached = set()
        # reached.add(hash(posStart))

        while not frontier.empty():
            current = frontier.get()
            mc.setBlock(current, matirial)

            for next in neighbors(current):
                frontier.put(next)
                    # reached.add(hash(next))

