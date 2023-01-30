platform = [[" "] * 3 for i in range(3)]

def enter():
    print("-------------------")
    print("  Приветсвуем вас  ")
    print("      в игре       ")
    print("  крестики-нолики  ")
    print("-------------------")
    print(" формат ввода: x y ")
    print(" x - номер строки  ")
    print(" y - номер столбца ")
    print()
    print(" X X X  ")
    print(" - - -  - По диагонали, либо вертикали победа!  ")
    print(" - - -  ")
    print()
    print(" X - -  ")
    print(" - X -  - По диагонали, тоже победа!  ")
    print(" - - X  ")
    print('Удачной игры!')

def show_platform():
    print()
    print("     | 0  | 1 | 2 | ")
    print("  ---------------- ")

    for i, row in enumerate(platform):
        row_str = f"  {i}  |  {' | '.join(row)} |"
        print(row_str)
        print("  ----------------")


def ask():
    while True:
        cords = input('Введите координаты:').split()
        if len(cords) != 2:
            print("Введите 2 координаты")
            continue
        x, y = cords

        if not (x.isdigit()) or not (y.isdigit()):
            print(" Введите числа! ")
            continue

        x, y = int(x), int(y)

        if 0 < x > 2 or 0 < y > 2:
            print("Введите число от 0 до 2")
            continue

        if platform[x][y] != " ":
            print(" Клетка занята! ")
            continue
        return x, y


def game_rules():
    win_combination = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                       ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                       ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2))]
    for i in win_combination:
        symbol = []
        for j in i:
            symbol.append(platform[j[0]][j[1]])
        if symbol == ["X", "X", "X"]:
          print("Победил X!!!")
          return True

        if symbol == ["O", "O", "O"]:
          print("Победил О!!!")
          return True
    return False

step = 0
while True:
    step += 1
    enter()
    show_platform()

    if step % 2 == 1:
        print(" Ходит крестик")
    else:
        print(" Ходит нолик")

    x, y = ask()

    if step % 2 == 1:
        platform[x][y] = "X"
    else:
        platform[x][y] = "O"

    if game_rules():
        show_platform()
        break

    if step == 9:
        print("Ничья")
        break