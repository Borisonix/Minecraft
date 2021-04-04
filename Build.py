from mcpi.vec3 import Vec3
from perekritie import *
import time
from settings import *


def build_block(posStart, p_horizon, kod, colA, colB, direction=1):
    '''
    Функция постройки стенового блока
     :param posStart:  стартовая координата, тип: Vec3
     :param p_horizon: признак горизонтальности на плане здания (True - параллельно оси Z, False - параллельно оси X)
     :param kod:  код стенового блока
     :param colA: цвет зоны A
     :param colB: цвет зоны B
     :direction = 1: направление строительства блока:   +1 - вдоль оси X или Z,
                                                        -1 - в противоположную сторону
     :return:   координата следующего стенового блока
    '''

    c1 = kod // 100
    c2 = (kod - c1 * 100) // 10
    c3 = (kod - c1 * 100) % 10

    zona = {}
    pos_st = posStart.clone()  # заготовка для координаты начала кубоида
    pos = posStart.clone()  # заготовка для координаты конца кубоида
    pos_ret = posStart.clone()  # заготовка для координаты, возвращаемой из функции

    if c1 == 1:  # =======   стеновой блок типа 1 (9х8)   ===========================================================
        if c2 == 4:  # строим цоколь?
            pos.y += H_COKOL - 1
            if p_horizon:
                pos.z += (W_B_1 - 1) * direction
                pos_ret.z += W_B_1 * direction
            else:
                pos.x += (W_B_1 - 1) * direction
                pos_ret.x += W_B_1 * direction
            mc.setBlocks(posStart, pos, BROWN_DARK)
            return pos_ret  # выходим
        if c2 == 5:         # ===============    широкий блок с 2 дверьми   ====================================
            pos.y += H_B - 1
            if p_horizon:
                pos.z += (W_B_1 - 1) * direction
                pos_ret.z += W_B_1 * direction
            else:
                pos.x += (W_B_1 - 1) * direction
                pos_ret.x += W_B_1 * direction
            mc.setBlocks(posStart, pos, colA)
            # ----------  первая дверь  ------------------
            pos_st1 = posStart.clone()  # стартовая позиция нижней части двери
            pos_st2 = posStart.clone()  # стартовая позиция верхней части двери
            pos1 = posStart.clone()  # заготовка для конечной позиция нижней части двери
            pos2 = posStart.clone()  # заготовка для конечной позиция верхней части двери
            pos_svet = posStart.clone()  # заготовка для светильника над дверью

            pos_st2.y += H_ZONA_A   # стартовая высота верхней части двери. Нижняя уже готова

            pos1.y += 1
            pos2.y += H_DOOR_1 - 1
            pos_svet.y += H_DOOR_1
            if p_horizon:
                pos_st1.z += 1 * direction
                pos_st2.z += 1 * direction
                pos1.z += (W_DOOR_1) * direction
                pos2.z += (W_DOOR_1) * direction
                pos_svet.z += (W_DOOR_1//2 + 1) * direction
                pos_svet.x -= 1 * direction
            else:
                pos_st1.x += 1 * direction
                pos_st2.x += 1 * direction
                pos1.x += W_DOOR_1 * direction
                pos2.x += W_DOOR_1 * direction
                pos_svet.x += (W_DOOR_1 + W_DOOR_1//2 + 1) * direction
                pos_svet.z -= 1 * direction
            mc.setBlocks(pos_st1, pos1, GREY_GLASS_PAN)
            mc.setBlocks(pos_st2, pos2, GLASS_PAN)
            mc.setBlock(pos_svet, SVET)
            # ----------  вторая дверь  ------------------
            pos_st1 = posStart.clone()  # стартовая позиция нижней части двери
            pos_st2 = posStart.clone()  # стартовая позиция верхней части двери
            pos1 = posStart.clone()  # заготовка для конечной позиция нижней части двери
            pos2 = posStart.clone()  # заготовка для конечной позиция верхней части двери

            pos_st2.y += H_ZONA_A   # стартовая высота верхней части двери. Нижняя уже готова

            pos1.y += 1
            pos2.y += H_DOOR_1 - 1
            if p_horizon:
                pos_st1.z += (W_DOOR_1 + 2) * direction
                pos_st2.z += (W_DOOR_1 + 2) * direction
                pos1.z += (W_DOOR_1 * 2 + 1) * direction
                pos2.z += (W_DOOR_1 * 2 + 1) * direction
                pos_svet.z += (W_DOOR_1 + W_DOOR_1//2) * direction
            else:
                pos_st1.x += (W_DOOR_1 + 2) * direction
                pos_st2.x += (W_DOOR_1 + 2) * direction
                pos1.x += (W_DOOR_1 * 2 + 1) * direction
                pos2.x += (W_DOOR_1 * 2 + 1) * direction
                pos_svet.x += (W_DOOR_1 + W_DOOR_1//2) * direction
            mc.setBlocks(pos_st1, pos1, GREY_GLASS_PAN)
            mc.setBlocks(pos_st2, pos2, GLASS_PAN)
            mc.setBlock(pos_svet, SVET)
            return pos_ret  # выходим

        if p_horizon:       # отмеряем ширину блока по соответствующей оси
            pos.z += (W_B_1 - 1) * direction
            pos_ret.z += W_B_1 * direction
        else:
            pos.x += (W_B_1 - 1) * direction
            pos_ret.x += W_B_1 * direction

        # zona A
        pos.y += H_ZONA_A - 1  # высота зоны А
        pos_st.y += H_ZONA_A
        zona['A'] = {'pos0': posStart.clone(), 'pos1': pos, 'color': colA}

        # zona B
        pos.y = posStart.y
        pos.y += H_B - 1  # высота зоны B
        zona['B'] = {'pos0': pos_st, 'pos1': pos, 'color': colB}

        # zona W - окно
        if (c2 == 1) or (c2 == 3 and c3 == 0):  # какое-то окно есть?
            if c2 == 1:  # 1 окно
                pos_st = zona['B']['pos0'].clone()  # заготовка для координаты начала окна
                pos = pos_st.clone()  # заготовка для координаты конца окна
                pos.y += H_OKNA_1 - 1
                if p_horizon:
                    if c3 == 1:  # код = 111 - свиг окна влево
                        pos_st.z += 1 * direction
                        pos.z = pos_st.z + (W_OKNA_2 - 1) * direction
                    elif c3 == 2:  # код = 112 - свиг окна вправо
                        pos_st.z += ((W_B_1 - W_OKNA_2) - 1) * direction
                        pos.z = pos_st.z + (W_OKNA_2 - 1) * direction
                    else:  # окно в центре
                        pos_st.z += ((W_B_1 - W_OKNA_1) // 2) * direction
                        pos.z = pos_st.z + (W_OKNA_1 - 1) * direction
                else:
                    if c3 == 1:  # код = 111 - свиг окна влево
                        pos_st.x += 1 * direction
                        pos.x = pos_st.x + (W_OKNA_2 - 1) * direction
                    elif c3 == 2:  # код = 112 - свиг окна вправо
                        pos_st.x += ((W_B_1 - W_OKNA_2) - 1) * direction
                        pos.x = pos_st.x + (W_OKNA_2 - 1) * direction
                    else:  # окно в центре
                        pos_st.x += ((W_B_1 - W_OKNA_1) // 2) * direction
                        pos.x = pos_st.x + (W_OKNA_1 - 1) * direction

            elif c2 == 3:  # код 130 - вентиляц. окошечко
                pos_st = zona['B']['pos0'].clone()
                pos = pos_st.clone()
                pos_st.y += 2
                pos.y = (pos_st.y + H_OKNA_4 - 1)
                if p_horizon:
                    pos_st.z += ((W_B_1 - W_OKNA_4) // 2) * direction
                    pos.z = pos_st.z + (W_OKNA_4 - 1) * direction
                else:
                    pos_st.x += ((W_B_1 - W_OKNA_4) // 2) * direction
                    pos.x = pos_st.x + (W_OKNA_4 - 1) * direction
            zona['W'] = {'pos0': pos_st, 'pos1': pos, 'color': OKNO}

    elif c1 == 2:  # стеновой блок типа 2 (7х8) ==============================================================
        if c2 == 4:  # строим цоколь?
            pos.y += (H_COKOL - 1)
            if p_horizon:
                pos.z += (W_B_2 - 1) * direction
                pos_ret.z += W_B_2 * direction
            else:
                pos.x += (W_B_2 - 1) * direction
                pos_ret.x += W_B_2 * direction
            mc.setBlocks(posStart, pos, BROWN_DARK)
            return pos_ret

        if c2 == 5:         # ===============    узкий блок с 1 дверью   ====================================
            pos.y += H_B - 1
            if p_horizon:
                pos.z += (W_B_2 - 1) * direction
                pos_ret.z += W_B_2 * direction
            else:
                pos.x += (W_B_1 - 2) * direction
                pos_ret.x += W_B_2 * direction
            mc.setBlocks(posStart, pos, colA)
            # ----------  дверь  ------------------
            pos_st = posStart.clone()  # стартовая позиция нижней части двери
            pos = posStart.clone()  # заготовка для конечной позиция нижней части двери
            pos_svet = posStart.clone()  # заготовка для светильника над дверью

            pos.y += H_DOOR_1 - 1
            pos_svet.y += H_DOOR_1
            if p_horizon:
                pos_st.z += 2 * direction
                pos.z += (W_DOOR_1 + 1) * direction
                pos_svet.z += (W_B_2//2) * direction
                pos_svet.x -= 1 * direction
            else:
                pos_st.x += 2 * direction
                pos.x += (W_DOOR_1 + 1) * direction
                pos_svet.x += (W_B_2 // 2) * direction
                pos_svet.z += 1 * direction
            mc.setBlocks(pos_st, pos, GREY_GLASS_PAN)
            mc.setBlock(pos_svet, SVET)
            return pos_ret  # выходим

        # обычный стеновой блок узкий
        if p_horizon:
            pos.z += (W_B_2 - 1) * direction
            pos_ret.z += (W_B_2) * direction
        else:
            pos.x += (W_B_2 - 1) * direction
            pos_ret.x += W_B_2 * direction

        # zona A
        pos_st.y += H_ZONA_A
        pos.y += (H_ZONA_A - 1)
        zona['A'] = {'pos0': posStart.clone(), 'pos1': pos, 'color': colA}

        # zona B
        pos.y = posStart.y
        pos.y += (H_B - 1)
        zona['B'] = {'pos0': pos_st, 'pos1': pos, 'color': colB}

        if (c2 == 1) or (c2 == 3 and c3 == 0):
            if c2 == 1:  # код = 210 - 1 окно малое в центре
                pos_st = zona['B']['pos0'].clone()  # заготовка для координаты начала окна
                pos = pos_st.clone()  # заготовка для координаты конца окна
                pos.y += (H_OKNA_2 - 1)
                if p_horizon:
                    pos_st.z += ((W_B_2 - W_OKNA_2) // 2) * direction
                    pos.z = pos_st.z + (W_OKNA_2 - 1) * direction
                else:
                    pos_st.x += ((W_B_2 - W_OKNA_2) // 2) * direction
                    pos.x = pos_st.x + (W_OKNA_2 - 1) * direction
            elif c2 == 3:  # вентиляц. окошечко
                pos_st = zona['B']['pos0'].clone()
                pos = pos_st.clone()
                pos_st.y += 2
                pos.y = (pos_st.y + H_OKNA_4 - 1)
                if p_horizon:
                    pos_st.z += ((W_B_2 - W_OKNA_4) // 2) * direction
                    pos.z = pos_st.z + (W_OKNA_4 - 1) * direction
                else:
                    pos_st.x += ((W_B_2 - W_OKNA_4) // 2) * direction
                    pos.x = pos_st.x + (W_OKNA_4 - 1) * direction
            zona['W'] = {'pos0': pos_st, 'pos1': pos, 'color': OKNO}
    elif c1 == 3:                                                           # стеновой блок типа 3 (7x13)
        if c2 == 5:         # ===============    узкий блок с 1 дверью   ====================================
            pos.y += H_B_3 - 1
            if p_horizon:
                pos.z += (W_B_3 - 1) * direction
                pos_ret.z += W_B_3 * direction
            else:
                pos.x += (W_B_3 - 1) * direction
                pos_ret.x += W_B_3 * direction
            mc.setBlocks(posStart, pos, colA)
            # ----------  дверь  ------------------
            pos_st = posStart.clone()  # стартовая позиция нижней части двери
            pos = posStart.clone()  # заготовка для конечной позиция нижней части двери
            pos_svet = posStart.clone()  # заготовка для светильника над дверью

            pos.y += H_DOOR_1 - 1
            pos_svet.y += H_DOOR_1
            if p_horizon:
                pos_st.z += 2 * direction
                pos.z += (W_DOOR_1 + 1) * direction
                pos_svet.z += (W_B_2//2) * direction
                pos_svet.x -= 1 * direction
            else:
                pos_st.x += 2 * direction
                pos.x += (W_DOOR_1 + 1) * direction
                pos_svet.x += (W_B_2 // 2) * direction
                pos_svet.z += 1 * direction
            mc.setBlocks(pos_st, pos, GREY_GLASS_PAN)
            mc.setBlock(pos_svet, SVET)
            return pos_ret  # выходим

        if p_horizon:
            pos.z += (W_B_3 - 1) * direction
            pos_ret.z += (W_B_3) * direction
        else:
            pos.x += (W_B_3 - 1) * direction
            pos_ret.x += W_B_3 * direction

        # zona A
        pos_st.y += H_ZONA_A
        pos.y += (H_ZONA_A - 1)
        zona['A'] = {'pos0': posStart.clone(), 'pos1': pos, 'color': colA}

        # zona B
        pos.y = posStart.y
        pos.y += (H_B_3 - 1)
        zona['B'] = {'pos0': pos_st, 'pos1': pos, 'color': colB}

        if c2 != 0:
            if c2 == 1:  # код = 310 - 1 окно малое в центре
                pos_st = zona['B']['pos0'].clone()  # заготовка для координаты начала окна
                pos = pos_st.clone()  # заготовка для координаты конца окна
                pos.y += (H_OKNA_5 - 1)
                if p_horizon:
                    pos_st.z += ((W_B_3 - W_OKNA_5) // 2) * direction
                    pos.z = pos_st.z + (W_OKNA_5 - 1) * direction
                else:
                    pos_st.x += ((W_B_3 - W_OKNA_5) // 2) * direction
                    pos.x = pos_st.x + (W_OKNA_5 - 1) * direction
            zona['W'] = {'pos0': pos_st, 'pos1': pos, 'color': OKNO}

    else:
        if p_horizon:
            pos.z += (W_B_4 - 1) * direction
            pos_ret.z += (W_B_4) * direction
        else:
            pos.x += (W_B_4 - 1) * direction
            pos_ret.x += W_B_4 * direction

        # zona A
        pos_st.y += H_ZONA_A
        pos.y += (H_ZONA_A - 2)
        zona['A'] = {'pos0': posStart.clone(), 'pos1': pos, 'color': colA}

        # zona B
        pos.y = posStart.y
        pos.y += (H_B_4 - 1)
        zona['B'] = {'pos0': pos_st, 'pos1': pos, 'color': colB}

    ks = zona.keys()
    for k in sorted(ks):  # постройка подготовленных зон (А, B и W)
        mc.setBlocks(zona[k]['pos0'], zona[k]['pos1'], zona[k]['color'])
    return pos_ret


def build_blocks(pos_Start, p_horizon, kod, colA, colB, amount, direction=1):
    '''
    Строительство группы стеновых блоков
     :param posStart:  стартовая координата, тип: Vec3
     :param p_horizon: признак горизонтальности на плане здания (True - параллельно оси Z, False - параллельно оси X)
     :param kod:  код стенового блока
     :param colA: цвет зоны A
     :param colB: цвет зоны B
     :param amount: кол-во стеновых блоков в группе
     :direction = 1: направление строительства блока:   +1 - вдоль оси X или Z,
                                                        -1 - в противоположную сторону
     :return:
    '''
    pos = pos_Start.clone()
    for i in range(amount):
        pos = build_block(pos, p_horizon, kod, colA, colB, direction)
    if PAUSE > 0:
        time.sleep(PAUSE)
    return pos


def school112():
    def level0():
        # -------------------------------- цоколь -------------------------------
        pos_floor = posMAIN.clone()
        pos_floor.x += 20
        pos_floor.y += H_COKOL - 1
        pos_floor.z += 20
        floor.append(0)
        floor[0] = list()
        floor[0].append(pos_floor)            #  опорная точка для построения пола
        mc.setBlock(pos_floor, FONAR)
        # стена 1
        pos_tek = build_blocks(posMAIN, True, 240, BROWN, BROWN, 3)

        # крыльцо [0] стартовая точка
        pos_kril = pos_tek.clone()
        pos_kril.x -= 1
        pos_kril.y += 1
        krilco.append(pos_kril)
        mc.setBlock(pos_kril, FONAR)

        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 1)
        pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 2)
        # стена 2
        pos_tek = build_blocks(pos_tek, False, 140, BROWN, BROWN, 4)
        # крыльцо [1] стартовая точка
        pos_kril = pos_tek.clone()
        pos_kril.z += 1
        pos_kril.y += 1
        krilco.append(pos_kril)
        mc.setBlock(pos_kril, FONAR)
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 8)
        # стена 3
        pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 1)
        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 4)

        # сохранить точку для крыльца [2] k_main
        pos_kril = pos_tek.clone()
        pos_kril.x -= 1
        pos_kril.y += 1
        krilco.append(pos_kril)
        mc.setBlock(pos_kril, FONAR)

        pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 1)
        # стена 4
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 140, BROWN, BROWN, 2, -1)
        # стена 5
        pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 5)
        # стена 6
        pos_tek = build_blocks(pos_tek, False, 140, BROWN, BROWN, 2)
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 2)
        # стена 7
        pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 1)
        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 4)
        pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 1)
        # стена 8
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 8, -1)
        # крыльцо [3] стартовая точка
        pos_kril = pos_tek.clone()
        pos_kril.x -= 1
        pos_kril.z -= 1
        pos_kril.y += 1
        krilco.append(pos_kril)
        mc.setBlock(pos_kril, FONAR)

        pos_tek = build_blocks(pos_tek, False, 140, BROWN, BROWN, 4, -1)
        # стена 9
        pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 2)
        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 1)
        # крыльцо [4] стартовая точка
        pos_kril = pos_tek.clone()
        pos_kril.x -= 1
        pos_kril.y += 1
        pos_kril.z -= 1
        krilco.append(pos_kril)
        mc.setBlock(pos_kril, FONAR)

        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 3)
        # стена 10
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 18)

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.y += H_COKOL - 1
        floor[0].append(pos_floor)  # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 11
        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 4)
        # стена 12
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 4)
        # стена 13
        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 8, -1)
        # стена 14
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 4, -1)
        # стена 15
        build_blocks(pos_tek, True, 240, BROWN, BROWN, 4)
        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 8, -1)
        build_blocks(pos_tek, True, 240, BROWN, BROWN, 9, -1)
        # стена 16
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 10)
        # стена 17
        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 9, -1)
        # стена 18
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 10, -1)

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.z += 1
        pos_floor.y += H_COKOL - 1
        floor[0].append(pos_floor)              # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 19
        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 8, -1)
        # стена 20
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 4, +1)

        pos_floor = pos_tek.clone()
        pos_floor.x -= 1
        pos_floor.z -= 1
        pos_floor.y += H_COKOL - 1
        floor[0].append(pos_floor)  # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 21
        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 8, -1)
        # стена 22
        pos_tek.x -= 1
        pos_tek.z += 1
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 4, -1)
        # стена 23
        pos_tek.x += 1
        pos_tek.z += 1
        pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 4)
        build_blocks(pos_tek, True, 240, BROWN, BROWN, 4)
        # стена 24
        pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 18, -1)

    def level1():
        # -------------------------------- 1 этаж -------------------------------
        pos_tek = posMAIN.clone()
        pos_tek.y +=  H_COKOL

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.y += H_B
        pos_floor.z += 1
        floor.append(0)
        floor[1] = list()
        floor[1].append(pos_floor)  # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 1
        pos_tek = build_blocks(pos_tek, True, 200, WHITE, WHITE, 3)
        pos_tek = build_blocks(pos_tek, True, 250, ORANGE, ORANGE, 1)
        pos_tek = build_blocks(pos_tek, True, 110, BROWN, WHITE, 2)
        # стена 2
        pos_tek = build_blocks(pos_tek, False, 110, BROWN, BROWN, 4)
        pos_tek = build_blocks(pos_tek, False, 250, WHITE, WHITE, 1)
        pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 3)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 4)
        # стена 3
        pos_tek = build_blocks(pos_tek, True, 112, BROWN, BROWN, 1)
        pos_tek = build_blocks(pos_tek, True, 210, WHITE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, True, 111, BROWN, BROWN, 1)
        # стена 4
        pos_tek = build_blocks(pos_tek, False, 110, BROWN, BROWN, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2, -1)
        # стена 5
        pos_tek = build_blocks(pos_tek, True, 110, BROWN, BROWN, 2)
        pos_tek = build_blocks(pos_tek, True, 150, BROWN, BROWN, 1)
        pos_tek = build_blocks(pos_tek, True, 110, BROWN, BROWN, 2)
        # стена 6
        pos_tek = build_blocks(pos_tek, False, 110, BROWN, BROWN, 2)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2)
        # стена 7
        pos_tek = build_blocks(pos_tek, True, 112, BROWN, BROWN, 1)
        pos_tek = build_blocks(pos_tek, True, 210, WHITE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, True, 111, BROWN, BROWN, 1)
        # стена 8
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 3, -1)
        pos_tek = build_blocks(pos_tek, False, 250, WHITE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, False, 110, BROWN, BROWN, 4, -1)
        # стена 9
        pos_tek = build_blocks(pos_tek, True, 110, BROWN, WHITE, 2)
        pos_tek = build_blocks(pos_tek, True, 250, ORANGE, ORANGE, 1)
        pos_tek = build_blocks(pos_tek, True, 200, WHITE, WHITE, 3)

        # стена 10
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, ORANGE, 2)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2)
        pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 5)
        pos_tek = build_blocks(pos_tek, False, 250, WHITE, WHITE, 2)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 3)

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.y += H_B
        floor[1].append(pos_floor)  # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 11
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 4)
        # стена 12
        pos_tek = build_blocks(pos_tek, False, 200,  WHITE, WHITE, 4)
        # стена 13
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 2, -1)
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 2, -1)
        # стена 14
        pos_tek = build_blocks(pos_tek, False, 200, WHITE, WHITE, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 1, -1)
        # стена 15
        build_blocks(pos_tek, True, 200, WHITE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 210, WHITE, WHITE, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
        build_blocks(pos_tek, True, 200, WHITE, WHITE, 9, -1)
        # стена 16
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2)
        pos_tek = build_blocks(pos_tek, False, 250, BROWN, BROWN, 2)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 3)
        pos_tek = build_blocks(pos_tek, False, 200, BROWN, BROWN, 3)
        # стена 17
        pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 2, -1)
        pos_tek = build_blocks(pos_tek, True, 250, BROWN, BROWN, 1, -1)  # дверь
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 1, -1)
        # стена 18
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 1, -1)
        pos_tek = build_blocks(pos_tek, False, 250, BROWN, BROWN, 1, -1)   # дверь
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 8, -1)

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.z += 1
        pos_floor.y += H_B
        floor[1].append(pos_floor)              # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 19
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 210, WHITE, WHITE, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
        # стена 20
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 1, +1)
        pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 1, +1)
        pos_tek = build_blocks(pos_tek, False, 250, WHITE, WHITE, 1, +1)
        pos_tek = build_blocks(pos_tek, False, 200, WHITE, WHITE, 1, +1)

        pos_floor = pos_tek.clone()
        pos_floor.x -= 1
        pos_floor.z -= 1
        pos_floor.y += H_B
        floor[1].append(pos_floor)              # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 21
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 2, -1)
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 2, -1)
        # стена 22
        pos_tek.x -= 1
        pos_tek.z += 1
        pos_tek = build_blocks(pos_tek, False, 250, WHITE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, False, 200, WHITE, WHITE, 3, -1)
        # стена 23
        pos_tek.x += 1
        pos_tek.z += 1
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 4)
        build_blocks(pos_tek, True, 200, WHITE, WHITE, 4)
        # стена 24
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 3, -1)
        pos_tek = build_blocks(pos_tek, False, 250, WHITE, WHITE, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 5, -1)
        pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, ORANGE, 2, -1)

    def level2():
        # -------------------------------- 2 этаж -------------------------------
        pos_tek = posMAIN.clone()
        pos_tek.y +=  H_COKOL + H_B * 1

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.y += H_B
        pos_floor.z += 1
        floor.append(0)
        floor[2] = list()
        floor[2].append(pos_floor)  # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 1
        pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 3)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1)
        pos_tek = build_blocks(pos_tek, True, 110, WHITE, WHITE, 2)
        # стена 2
        pos_tek = build_blocks(pos_tek, False, 110, BROWN, ORANGE, 4)
        pos_tek = build_blocks(pos_tek, False, 200, BROWN, BROWN, 1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 3)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 4)
        # стена 3
        pos_tek = build_blocks(pos_tek, True, 112, WHITE, WHITE, 1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 4)
        pos_tek = build_blocks(pos_tek, True, 111, WHITE, WHITE, 1)
        # стена 4
        pos_tek = build_blocks(pos_tek, False, 110, WHITE, WHITE, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 2, -1)
        # стена 5
        pos_tek = build_blocks(pos_tek, True, 110, WHITE, WHITE, 2)
        pos_tek = build_blocks(pos_tek, True, 110, BROWN, BROWN, 1)
        pos_tek = build_blocks(pos_tek, True, 110, WHITE, WHITE, 2)
        # стена 6
        pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 2)
        pos_tek = build_blocks(pos_tek, False, 110, WHITE, WHITE, 2)
        # стена 7
        pos_tek = build_blocks(pos_tek, True, 112, WHITE, WHITE, 1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 4)
        pos_tek = build_blocks(pos_tek, True, 111, WHITE, WHITE, 1)
        # стена 8
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 3, -1)
        pos_tek = build_blocks(pos_tek, False, 200, BROWN, BROWN, 1, -1)
        pos_tek = build_blocks(pos_tek, False, 110, BROWN, ORANGE, 4, -1)
        # стена 9
        pos_tek = build_blocks(pos_tek, True, 110, WHITE, WHITE, 2)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1)
        pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 3)
        # стена 10
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, BROWN, 2)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 2)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 4)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 4)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 3)

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.y += H_B_3 - 1
        floor[2].append(pos_floor)  # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 11
        pos_tek = build_blocks(pos_tek, True, 300, BROWN, ORANGE, 4)
        # стена 12
        pos_tek = build_blocks(pos_tek, False, 350, WHITE, WHITE, 1)
        pos_tek = build_blocks(pos_tek, False, 300, WHITE, WHITE, 3)
        # стена 13
        pos_tek = build_blocks(pos_tek, True, 310, ORANGE, WHITE, 2, -1)
        pos_tek = build_blocks(pos_tek, True, 310, ORANGE, BROWN, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 310, ORANGE, WHITE, 2, -1)
        # стена 14
        pos_tek = build_blocks(pos_tek, False, 300, ORANGE, ORANGE, 4, -1)
        # стена 15
        build_blocks(pos_tek, True, 300, WHITE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 200, ORANGE, ORANGE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1, -1)
        build_blocks(pos_tek, True, 300, WHITE, WHITE, 9, -1)
        # стена 16
        pos_tek = build_blocks(pos_tek, False, 300, ORANGE, ORANGE, 5)
        pos_tek = build_blocks(pos_tek, False, 300, WHITE, WHITE, 5)
        # стена 17
        pos_tek = build_blocks(pos_tek, True, 300, ORANGE, WHITE, 2, -1)
        pos_tek = build_blocks(pos_tek, True, 310, ORANGE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 310, ORANGE, BROWN, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 310, BROWN, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 310, ORANGE, WHITE, 1, -1)
        # стена 18
        pos_tek = build_blocks(pos_tek, False, 350, WHITE, WHITE, 1, -1)    # дверь
        pos_tek = build_blocks(pos_tek, False, 300, WHITE, WHITE, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 300, ORANGE, ORANGE, 5, -1)

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.z += 1
        pos_floor.y += H_B_3-1
        floor[2].append(pos_floor)              # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 19
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 200, ORANGE, ORANGE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1, -1)
        # стена 20
        pos_tek = build_blocks(pos_tek, False, 300, ORANGE, ORANGE, 4)

        pos_floor = pos_tek.clone()
        pos_floor.x -= 1
        pos_floor.z -= 1
        pos_floor.y += H_B_3-1
        floor[2].append(pos_floor)              # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 21
        pos_tek = build_blocks(pos_tek, True, 310, ORANGE, WHITE, 2, -1)
        pos_tek = build_blocks(pos_tek, True, 310, ORANGE, BROWN, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 310, ORANGE, WHITE, 2, -1)
        # стена 22
        pos_tek.x -= 1
        pos_tek.z += 1
        pos_tek = build_blocks(pos_tek, False, 300, WHITE, WHITE, 3, -1)
        pos_tek = build_blocks(pos_tek, False, 350, WHITE, WHITE, 1, -1)
        # стена 23
        pos_tek.x += 1
        pos_tek.z += 1
        pos_tek = build_blocks(pos_tek, True, 200, ORANGE, ORANGE, 4)
        build_blocks(pos_tek, True, 300, WHITE, WHITE, 4)
        # стена 24
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 3, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 1, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, BROWN, 2, -1)

    def level3():
        # -------------------------------- 3 этаж -------------------------------
        pos_tek = posMAIN.clone()
        pos_tek.y += H_COKOL + H_B * 2

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.y += H_B
        pos_floor.z += 1
        floor.append(0)
        floor[3] = list()
        floor[3].append(pos_floor)          # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 1
        pos_tek = build_blocks(pos_tek, True, 200, ORANGE, ORANGE, 3)
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1)
        pos_tek = build_blocks(pos_tek, True, 110, ORANGE, ORANGE, 2)
        # стена 2
        pos_tek = build_blocks(pos_tek, False, 110, ORANGE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, False, 200, BROWN, ORANGE, 1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 3)
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 4)
        # стена 3
        pos_tek = build_blocks(pos_tek, True, 112, WHITE, ORANGE, 1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, ORANGE, 4)
        pos_tek = build_blocks(pos_tek, True, 111, WHITE, ORANGE, 1)
        # стена 4
        pos_tek = build_blocks(pos_tek, False, 110, WHITE, ORANGE, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 210, WHITE, ORANGE, 2, -1)
        # стена 5
        pos_tek = build_blocks(pos_tek, True, 110, WHITE, ORANGE, 2)
        pos_tek = build_blocks(pos_tek, True, 110, ORANGE, BROWN, 1)
        pos_tek = build_blocks(pos_tek, True, 110, WHITE, ORANGE, 2)
        # стена 6
        pos_tek = build_blocks(pos_tek, False, 210, WHITE, ORANGE, 2)
        pos_tek = build_blocks(pos_tek, False, 110, WHITE, ORANGE, 2)
        # стена 7
        pos_tek = build_blocks(pos_tek, True, 112, WHITE, ORANGE, 1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, ORANGE, 4)
        pos_tek = build_blocks(pos_tek, True, 111, WHITE, ORANGE, 1)
        # стена 8
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 3, -1)
        pos_tek = build_blocks(pos_tek, False, 200, BROWN, ORANGE, 1, -1)
        pos_tek = build_blocks(pos_tek, False, 110, ORANGE, WHITE, 4, -1)
        # стена 9
        pos_tek = build_blocks(pos_tek, True, 110, WHITE, ORANGE, 2)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, ORANGE, 1)
        pos_tek = build_blocks(pos_tek, True, 200, BROWN, ORANGE, 3)
        # стена 10
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, WHITE, 2)
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 2)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 4)
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2)
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 3)

        pos_tek.y += 5

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.y += H_B_4 - 1
        floor[3].append(pos_floor)               # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 11
        pos_tek = build_blocks(pos_tek, True, 400, WHITE, WHITE, 4)
        # стена 12
        pos_tek = build_blocks(pos_tek, False, 400, ORANGE, ORANGE, 4)
        # стена 13
        pos_tek = build_blocks(pos_tek, True, 400, WHITE, WHITE, 8, -1)
        # стена 14
        pos_tek = build_blocks(pos_tek, False, 400, WHITE, WHITE, 4, -1)
        # стена 15
        build_blocks(pos_tek, True, 400, WHITE, WHITE, 4)
        pos_tek.y -= 5
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 200, ORANGE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, ORANGE, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, WHITE, 1, -1)
        # стена 16
        pos_tek.y += 5
        pos_tek = build_blocks(pos_tek, False, 400, WHITE, WHITE, 10)
        # стена 17
        pos_tek = build_blocks(pos_tek, True, 400, WHITE, WHITE, 9, -1)
        # стена 18
        pos_tek = build_blocks(pos_tek, False, 400, WHITE, WHITE, 10, -1)
        build_blocks(pos_tek, True, 400, WHITE, WHITE, 9)

        # pos_tek.y += 5

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.z += 1
        pos_floor.y += H_B_4 - 1
        floor[3].append(pos_floor)               # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 19
        pos_tek.y -= 5
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 210, BROWN, ORANGE, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 210, ORANGE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 200, ORANGE, WHITE, 2, -1)
        # стена 20
        pos_tek.y += 5
        build_blocks(pos_tek, True, 400, WHITE, WHITE, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 400, ORANGE, ORANGE, 4)

        pos_floor = pos_tek.clone()
        pos_floor.x -= 1
        pos_floor.z -= 1
        pos_floor.y += H_B_4 - 1
        floor[3].append(pos_floor)               # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 21
        pos_tek = build_blocks(pos_tek, True, 400, WHITE, WHITE, 8, -1)
        # стена 22
        pos_tek.x -= 1
        pos_tek.z += 1
        pos_tek = build_blocks(pos_tek, False, 400, ORANGE, ORANGE, 4, -1)
        # стена 23
        pos_tek.y -= 8
        pos_tek.x += 1
        pos_tek.z += 1
        pos_tek = build_blocks(pos_tek, True, 300, ORANGE, WHITE, 4)
        # стена 24
        pos_tek.y += 3
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 3, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 210, BROWN, WHITE, 2, -1)

    def level4():
        # -------------------------------- крыша -------------------------------
        pos_tek = posMAIN.clone()
        pos_tek.y += H_COKOL + H_B * 3

        pos_floor = pos_tek.clone()
        pos_floor.x += 1
        pos_floor.y += H_B - 1
        pos_floor.z += 1
        floor.append(0)
        floor[4] = list()
        floor[4].append(pos_floor)  # опорная точка для построения потолка
        mc.setBlock(pos_floor, FONAR)

        # стена 1
        pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 3)
        pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 1)
        pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 2)
        # стена 2
        pos_tek = build_blocks(pos_tek, False, 130, WHITE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, False, 230, WHITE, WHITE, 4)
        # стена 3
        pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 1)
        pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 1)
        # стена 4
        pos_tek = build_blocks(pos_tek, False, 130, ORANGE, WHITE, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 2, -1)
        # стена 5
        pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 5)
        # стена 6
        pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 2)
        pos_tek = build_blocks(pos_tek, False, 130, ORANGE, WHITE, 2)
        # стена 7
        pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 1)
        pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 1)
        # стена 8
        pos_tek = build_blocks(pos_tek, False, 230, WHITE, WHITE, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 3, -1)
        pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, False, 130, WHITE, WHITE, 4, -1)
        # стена 9
        pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 3)
        pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 1)
        pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 2)
        # стена 10
        pos_tek = build_blocks(pos_tek, False, 230, WHITE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 4)
        pos_tek = build_blocks(pos_tek, False, 230, WHITE, WHITE, 5)
        pos_tek = build_blocks(pos_tek, False, 230, BROWN, WHITE, 2)
        pos_tek = build_blocks(pos_tek, False, 230, WHITE, WHITE, 3)
        # обход пристойки правой
        pos_tek = build_blocks(pos_tek, True, 231, WHITE, WHITE, 4, -1)
        # стена 15
        pos_tek = build_blocks(pos_tek, True, 230, WHITE, WHITE, 3, -1)
        pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 4, -1)
        # обход актового зала
        pos_tek = build_blocks(pos_tek, True, 231, WHITE, WHITE, 10, -1)
        # стена 19
        pos_tek = build_blocks(pos_tek, True, 230, WHITE, WHITE, 1, -1)
        pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 4, -1)
        pos_tek = build_blocks(pos_tek, True, 230, WHITE, WHITE, 3, -1)
        # обход пристойки правой
        pos_tek = build_blocks(pos_tek, True, 231, WHITE, WHITE, 4, -1)
        pos_tek.z += 2              # корректировка для начала стены 24
        # вырезаем излишек
        pos1 = pos_tek.clone()
        pos1.y += 2
        pos2 = pos_tek.clone()
        pos2.y += 8
        pos2.z -= 2
        mc.setBlocks(pos1, pos2, AIR)
        # стена 24
        pos_tek = build_blocks(pos_tek, False, 230, WHITE, WHITE, 3, -1)
        pos_tek = build_blocks(pos_tek, False, 230, BROWN, WHITE, 2, -1)
        pos_tek = build_blocks(pos_tek, False, 230, WHITE, WHITE, 5, -1)
        pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 4, -1)
        pos_tek = build_blocks(pos_tek, False, 230, WHITE, WHITE, 4, -1)


    level0()
    level1()
    level2()
    level3()
    level4()

    krilco_t1(krilco[0])
    krilco_main(krilco[2])
    krilco_t1(krilco[4], -1)

    q = 'N'      # q = input('Будем строить полы и крышу? (Y/N)')
    if q == "Y" or q == "y":
        for i in range(5):
            for j in range(4):
                flooring(floor[i][j], WHITE if i == 0 else KAMEN)




