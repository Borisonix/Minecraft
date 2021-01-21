from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import time

mc = Minecraft.create()

H_B = 8         # высота блока стены
H_COKOL = 2     # высота цоколя
H_ZONA_A = 2    # высота зоны А
W_B_1 = 9       # ширина блока стены тип 1
W_B_2 = 7       # ширина блока стены тип 2

W_OKNA_1, H_OKNA_1 = 5, 5       # ширина и высота окна типа 1
W_OKNA_2, H_OKNA_2 = 4, 5       # ширина и высота окна типа 2
W_OKNA_3, H_OKNA_3 = 2, 5       # ширина и высота окна типа 3 - лестничные площадки
W_OKNA_4, H_OKNA_4 = 1, 2       # ширина и высота окна типа 4 - вентиляция



AIR = 0                 # воздух
STONE = 1               # камень для основы
WHITE = 155
BROWN = 35, 14          # было 159,12
ORANGE = 159,1
BROWN_DARK = 159,12      # темно-коричневый для цоколя было 159,7
OKNO = 160      # 102              тонкое окно

posMAIN = Vec3(122, 67, -961)
posMAIN.x += 20
posMAIN.y += 1
posMAIN.z += 20

def flooring(posStart, matirial):
    f = set()


def build_block(posStart, p_horizon, kod, colA, colB):
    '''
    Функция постройки стенового блока
     :param posStart:  стартовая координата, тип: Vec3
     :param p_horizon: признак горизонтальности на плане здания (True - параллельно оси Z, False - параллельно оси X)
     :param kod:  код стенового блока
     :param colA: цвет зоны A
     :param colB: цвет зоны B
     :return:   координата следующего стенового блока
    '''

    c1 = kod // 100
    c2 = (kod - c1 * 100) // 10
    c3 = (kod - c1 * 100) % 10

    zona = {}
    pos_st = posStart.clone()                                       # заготовка для координаты начала кубоида
    pos = posStart.clone()                                          # заготовка для координаты конца кубоида
    pos_ret = posStart.clone()   # заготовка для координаты, возвращаемой из функции
    

    if c1 == 1:                                                     # стеновой блок типа 1 (9х8)
        if c2 == 4:                                                 # строим цоколь?
            pos.y += H_COKOL - 1
            if p_horizon:
                pos.z += W_B_1 - 1
                pos_ret.z += W_B_1
            else:
                pos.x += W_B_1 - 1
                pos_ret.x += W_B_1
            mc.setBlocks(posStart, pos, BROWN_DARK)
            return pos_ret                                          # выходим
        
        if p_horizon:
            pos.z += W_B_1 - 1
            pos_ret.z += W_B_1
        else:
            pos.x += W_B_1 - 1
            pos_ret.x += W_B_1
        
        # zona A
        pos.y += H_ZONA_A - 1           # высота зоны А
        pos_st.y += H_ZONA_A
        zona['A'] = {'pos0': posStart.clone(), 'pos1': pos, 'color': colA}
        
        # zona B
        pos.y = posStart.y
        pos.y += H_B - 1                # высота зоны B
        zona['B'] = {'pos0': pos_st, 'pos1': pos, 'color': colB}
        
        # окна
        if c2 != 0:                                 # какое-то окно есть?
            if c2 == 1:                 # 1 окно в центре
                pos_st = zona['B']['pos0'].clone()  # заготовка для координаты начала окна
                pos = pos_st.clone()                # заготовка для координаты конца окна
                pos.y += H_OKNA_1 - 1
                if p_horizon:
                    if c3 == 1:                              # код = 111 - свиг окна влево
                        pos_st.z += 1
                        pos.z = pos_st.z + W_OKNA_2 - 1
                    elif c3 == 2:                            # код = 112 - свиг окна вправо
                        pos_st.z += (W_B_1 - W_OKNA_2) - 1
                        pos.z = pos_st.z + W_OKNA_2 - 1
                    else:                                   # окно в центре
                        pos_st.z += (W_B_1 - W_OKNA_1) // 2
                        pos.z = pos_st.z + W_OKNA_1 - 1
                else:
                    if c3 == 1:                                  # код = 111 - свиг окна влево
                        pos_st.x += 1
                        pos.x = pos_st.x + W_OKNA_2 - 1
                    elif c3 == 2:                                # код = 112 - свиг окна вправо
                        pos_st.x += (W_B_1 - W_OKNA_2) - 1
                        pos.x = pos_st.x + W_OKNA_2 - 1
                    else:                                       # окно в центре
                        pos_st.x += (W_B_1 - W_OKNA_1) // 2
                        pos.x = pos_st.x + W_OKNA_1 - 1

            elif c2 == 3:                                                   # код 130 - вентиляц. окошечко
                pos_st = zona['B']['pos0'].clone()
                pos = pos_st.clone()
                pos_st.y += 2
                pos.y = pos_st.y + H_OKNA_4 - 1
                if p_horizon:
                    pos_st.z += (W_B_1 - W_OKNA_4) // 2
                    pos.z = pos_st.z + W_OKNA_4 - 1
                else:
                    pos_st.x += (W_B_1 - W_OKNA_4) // 2
                    pos.x = pos_st.x + W_OKNA_4 - 1
            zona['W'] = {'pos0': pos_st, 'pos1': pos, 'color': OKNO}
    else:                                                               # стеновой блок типа 2 (7х8)
        if c2 == 4:  # строим цоколь?
            pos.y +=  H_COKOL - 1
            if p_horizon:
                pos.z += W_B_2 - 1
                pos_ret.z += W_B_2
            else:
                pos.x += W_B_2 - 1
                pos_ret.x += W_B_2
            mc.setBlocks(posStart, pos, BROWN_DARK)
            return pos_ret

        if p_horizon:
            pos.z += W_B_2 - 1
            pos_ret.z += W_B_2
        else:
            pos.x += W_B_2 - 1
            pos_ret.x += W_B_2

        # zona A
        pos_st.y += H_ZONA_A
        pos.y += H_ZONA_A - 1
        zona['A'] = {'pos0': posStart.clone(), 'pos1': pos, 'color': colA}

        # zona B
        pos.y = posStart.y
        pos.y += H_B -  1
        zona['B'] = {'pos0': pos_st, 'pos1': pos, 'color': colB}

        if c2 != 0:
            if c2 == 1:                                                 # код = 210 - 1 окно малое в центре
                pos_st = zona['B']['pos0'].clone()                      # заготовка для координаты начала окна
                pos = pos_st.clone()                                    # заготовка для координаты конца окна
                pos.y += H_OKNA_2 - 1
                if p_horizon:
                    pos_st.z += (W_B_2 - W_OKNA_2) // 2
                    pos.z = pos_st.z + W_OKNA_2 - 1
                else:
                    pos_st.x += (W_B_2 - W_OKNA_2) // 2
                    pos.x = pos_st.x + W_OKNA_2 - 1
            elif c2 == 3:                                               # вентиляц. окошечко
                pos_st = zona['B']['pos0'].clone()
                pos = pos_st.clone()
                pos_st.y += 2
                pos.y = pos_st.y + H_OKNA_4 - 1
                if p_horizon:
                    pos_st.z += (W_B_2 - W_OKNA_4) // 2
                    pos.z = pos_st.z + W_OKNA_4 - 1
                else:
                    pos_st.x += (W_B_2 - W_OKNA_4) // 2
                    pos.x = pos_st.x + W_OKNA_4 - 1
            zona['W'] = {'pos0': pos_st, 'pos1': pos, 'color': OKNO}

    for k in zona.values():
        mc.setBlocks(k['pos0'], k['pos1'], k['color'])
    return pos_ret


def build_blocks(pos_Start, p_horizon, kod, colA, colB, amount):
    '''
    Строительство группы стеновых блоков
     :param posStart:  стартовая координата, тип: Vec3
     :param p_horizon: признак горизонтальности на плане здания (True - параллельно оси Z, False - параллельно оси X)
     :param kod:  код стенового блока
     :param colA: цвет зоны A
     :param colB: цвет зоны B
     :param amount: кол-во стеновых блоков в группе
     :return:
    '''
    pos = pos_Start.clone()
    for i in range(amount):
        pos = build_block(pos, p_horizon, kod, colA, colB)
    return pos


