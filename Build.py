from mcpi.vec3 import Vec3
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

    if c1 == 1:  # стеновой блок типа 1 (9х8)
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

        if p_horizon:
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

        # окна
        if c2 != 0:  # какое-то окно есть?
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
    else:  # стеновой блок типа 2 (7х8)
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

        if c2 != 0:
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

    for k in zona.values():  # постройка подготовленных зон (А, B и W)
        mc.setBlocks(k['pos0'], k['pos1'], k['color'])
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
    time.sleep(PAUSE)
    return pos


def walls4():
    # --------------- цоколь ------------------------
    pos_tek = build_blocks(posMAIN, True, 240, BROWN, BROWN, 4)
    pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 2)

    pos_tek = build_blocks(pos_tek, False, 140, BROWN, BROWN, 4)
    pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 8)

    pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 4, -1)
    pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 1, -1)

    pos_tek = build_blocks(pos_tek, False, 140, BROWN, BROWN, 4, -1)
    pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 8, -1)


    # ---------------------- 1 этаж -----------------
    pos_tek = posMAIN.clone()
    pos_tek.y += H_COKOL
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, WHITE, 1)
    pos_tek = build_blocks(pos_tek, True, 210, WHITE, WHITE, 2)
    pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1)
    pos_tek = build_blocks(pos_tek, True, 110, BROWN, WHITE, 2)

    pos_tek = build_blocks(pos_tek, False, 110, BROWN, BROWN, 4)
    pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 4)

    pos_tek = build_blocks(pos_tek, True, 112, BROWN, BROWN, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 210, WHITE, WHITE, 4, -1)
    pos_tek = build_blocks(pos_tek, True, 111, BROWN, BROWN, 1, -1)

    pos_tek = build_blocks(pos_tek, False, 110, BROWN, BROWN, 4, -1)
    pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 4, -1)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 4, -1)

    # ---------------------- 2 этаж -----------------
    pos_tek = posMAIN.clone()
    pos_tek.y += H_COKOL + H_B * 1  # 2 этаж
    pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 3)
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1)
    pos_tek = build_blocks(pos_tek, True, 110, WHITE, WHITE, 2)

    pos_tek = build_blocks(pos_tek, False, 110, BROWN, ORANGE, 4)
    pos_tek = build_blocks(pos_tek, False, 200, BROWN, BROWN, 1)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 3)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 4)

    pos_tek = build_blocks(pos_tek, True, 112, WHITE, WHITE, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 4, -1)
    pos_tek = build_blocks(pos_tek, True, 111, WHITE, WHITE, 1, -1)

    pos_tek = build_blocks(pos_tek, False, 110, BROWN, ORANGE, 4, -1)
    pos_tek = build_blocks(pos_tek, False, 200, BROWN, BROWN, 1, -1)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 3, -1)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 4, -1)


    # ---------------------- 3 этаж -----------------
    pos_tek = posMAIN.clone()
    pos_tek.y += H_COKOL + H_B * 2  # 3 этаж
    pos_tek = build_blocks(pos_tek, True, 200, ORANGE, ORANGE, 3)
    pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1)
    pos_tek = build_blocks(pos_tek, True, 110, ORANGE, ORANGE, 2)

    pos_tek = build_blocks(pos_tek, False, 110, ORANGE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, False, 200, BROWN, ORANGE, 1)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 3)
    pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 4)

    pos_tek = build_blocks(pos_tek, True, 112, WHITE, ORANGE, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, ORANGE, 4, -1)
    pos_tek = build_blocks(pos_tek, True, 111, WHITE, ORANGE, 1, -1)

    pos_tek = build_blocks(pos_tek, False, 110, ORANGE, WHITE, 4, -1)
    pos_tek = build_blocks(pos_tek, False, 200, BROWN, ORANGE, 1, -1)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 3, -1)
    pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 4, -1)

    # ---------------------- крыша -----------------
    pos_tek = posMAIN.clone()
    pos_tek.y += H_COKOL + H_B * 3
    pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 3)
    pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 1)
    pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 2)

    pos_tek = build_blocks(pos_tek, False, 130, WHITE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 1)
    pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 3)
    pos_tek = build_blocks(pos_tek, False, 230, WHITE, WHITE, 4)

    pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 4, -1)
    pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 1, -1)

    pos_tek = build_blocks(pos_tek, False, 130, WHITE, WHITE, 4, -1)
    pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 1, -1)
    pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 3, -1)
    pos_tek = build_blocks(pos_tek, False, 230, WHITE, WHITE, 4, -1)


def school112():
    # цоколь
    # стена 1
    pos_tek = build_blocks(posMAIN, True, 240, BROWN, BROWN, 4)
    pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 2)
    # стена 2
    pos_tek = build_blocks(pos_tek, False, 140, BROWN, BROWN, 4)
    pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 8)
    # стена 3
    pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 1)
    pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 4)
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
    pos_tek = build_blocks(pos_tek, False, 140, BROWN, BROWN, 4, -1)
    # стена 9
    pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 4)
    pos_tek = build_blocks(pos_tek, True, 140, BROWN, BROWN, 2)
    # стена 10
    pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 18)
    # стена 11
    pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 4)
    # стена 12
    pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 4)
    # стена 13
    pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 8, -1)
    # стена 14
    pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 4, -1)
    # стена 15
    pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 8, -1)
    # стена 16
    pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 10)
    # стена 17
    pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 9, -1)
    # стена 18
    pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 10, -1)
    # стена 19
    pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 8, -1)
    # стена 20
    pos_tek = build_blocks(pos_tek, False, 240, BROWN, BROWN, 4, +1)
    # стена 21
    pos_tek = build_blocks(pos_tek, True, 240, BROWN, BROWN, 8, -1)



    # 1 этаж
    pos_tek = posMAIN.clone()
    pos_tek.y +=  H_COKOL
    # стена 1
    pos_tek = build_blocks(pos_tek, True, 200, WHITE, WHITE, 3)
    pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1)
    pos_tek = build_blocks(pos_tek, True, 110, BROWN, WHITE, 2)
    # стена 2
    pos_tek = build_blocks(pos_tek, False, 110, BROWN, BROWN, 4)
    pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 4)
    # стена 3
    pos_tek = build_blocks(pos_tek, True, 112, BROWN, BROWN, 1)
    pos_tek = build_blocks(pos_tek, True, 210, WHITE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, True, 111, BROWN, BROWN, 1)
    # стена 4
    pos_tek = build_blocks(pos_tek, False, 110, BROWN, BROWN, 2, -1)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2, -1)
    # стена 5
    pos_tek = build_blocks(pos_tek, True, 110, BROWN, BROWN, 5)
    # стена 6
    pos_tek = build_blocks(pos_tek, False, 110, BROWN, BROWN, 2)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2)
    # стена 7
    pos_tek = build_blocks(pos_tek, True, 112, BROWN, BROWN, 1)
    pos_tek = build_blocks(pos_tek, True, 210, WHITE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, True, 111, BROWN, BROWN, 1)
    # стена 8
    pos_tek = build_blocks(pos_tek, False, 110, BROWN, BROWN, 4, -1)
    pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 4, -1)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 4, -1)
    # стена 9
    pos_tek = build_blocks(pos_tek, True, 110, BROWN, WHITE, 2)
    pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1)
    pos_tek = build_blocks(pos_tek, True, 200, WHITE, WHITE, 3)
    # стена 10
    pos_tek = build_blocks(pos_tek, False, 210, ORANGE, ORANGE, 2)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2)
    pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 5)
    pos_tek = build_blocks(pos_tek, False, 200, BROWN, BROWN, 2)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 3)
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
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 210, WHITE, WHITE, 4, -1)
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
    # стена 16
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 2)
    pos_tek = build_blocks(pos_tek, False, 200, BROWN, BROWN, 2)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 3)
    pos_tek = build_blocks(pos_tek, False, 200, BROWN, BROWN, 3)
    # стена 17
    pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 2, -1)
    pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 1, -1)  # дверь
    pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 4, -1)
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 1, -1)
    # стена 18
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 1, -1)
    pos_tek = build_blocks(pos_tek, False, 200, BROWN, BROWN, 1, -1)   # дверь
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 8, -1)
    # стена 19
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 210, WHITE, WHITE, 4, -1)
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 1, -1)
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1, -1)
    # стена 20
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 1, +1)
    pos_tek = build_blocks(pos_tek, False, 210, WHITE, WHITE, 1, +1)
    pos_tek = build_blocks(pos_tek, False, 200, WHITE, WHITE, 2, +1)





    pos_tek = posMAIN.clone()
    pos_tek.y +=  H_COKOL + H_B * 1                                                 # 2 этаж
    pos_tek = build_blocks(pos_tek, True, 200, BROWN, BROWN, 3)
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 1)
    pos_tek = build_blocks(pos_tek, True, 110, WHITE, WHITE, 2)
    pos_tek = build_blocks(pos_tek, False, 110, BROWN, ORANGE, 4)
    pos_tek = build_blocks(pos_tek, False, 200, BROWN, BROWN, 1)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, BROWN, 3)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 4)
    pos_tek = build_blocks(pos_tek, True, 112, WHITE, WHITE, 1)
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, BROWN, 4)
    pos_tek = build_blocks(pos_tek, True, 111, WHITE, WHITE, 1)

    pos_tek = posMAIN.clone()
    pos_tek.y += H_COKOL + H_B * 2                                                # 3 этаж
    pos_tek = build_blocks(pos_tek, True, 200, ORANGE, ORANGE, 3)
    pos_tek = build_blocks(pos_tek, True, 210, ORANGE, ORANGE, 1)
    pos_tek = build_blocks(pos_tek, True, 110, ORANGE, ORANGE, 2)
    pos_tek = build_blocks(pos_tek, False, 110, ORANGE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, False, 200, BROWN, ORANGE, 1)
    pos_tek = build_blocks(pos_tek, False, 210, BROWN, ORANGE, 3)
    pos_tek = build_blocks(pos_tek, False, 210, ORANGE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, True, 112, WHITE, ORANGE, 1)
    pos_tek = build_blocks(pos_tek, True, 210, BROWN, ORANGE, 4)
    pos_tek = build_blocks(pos_tek, True, 111, WHITE, ORANGE, 1)

    pos_tek = posMAIN.clone()
    pos_tek.y += H_COKOL + H_B * 3                                                # крыша
    pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 3)
    pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 1)
    pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 2)
    pos_tek = build_blocks(pos_tek, False, 130, WHITE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 1)
    pos_tek = build_blocks(pos_tek, False, 230, ORANGE, WHITE, 3)
    pos_tek = build_blocks(pos_tek, False, 230, WHITE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 1)
    pos_tek = build_blocks(pos_tek, True, 230, ORANGE, WHITE, 4)
    pos_tek = build_blocks(pos_tek, True, 130, ORANGE, WHITE, 1)

