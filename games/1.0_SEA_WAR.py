from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить в доску"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass

#Описание коорд и сравнение
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, l, o):   # s = Ship(Dot(1,2), 4, 0)
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    # определяет точки корабля
    def dots(self):

        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:     # 0 -- X
                cur_x += i

            elif self.o == 1:   # 1 -- Y
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    # попали мы или нет
    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size

        # hid - нужно ли наше поле скрывать
        self.hid = hid

        #кол-во пораженных кораблей
        self.count = 0

        #просто сетку в себе содержит
        self.field = [["0"] * size for _ in range(size)]

        #занятые точки и куда стреляли
        self.busy = []

        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("∎", "0")
        return res

    def out(self, d):
        #проверка, находится ли точка за пределами доски
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    #Нужен для обозначения контура вокруг корабля
    def countour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                # self.field[cur.x][cur.y] = "+"
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)



    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        #Добавляем координаты корабля в busy
        for d in ship.dots:
            self.field[d.x][d.y] = "∎"
            self.busy.append(d)
        #в списочек
        self.ships.append(ship)
        #добавили контур кораблю
        self.countour(ship)

    def shot(self, d):
        """Метод для выстрела со всеми необходимыми проверками и возвратом boolean
         значения для понимания кто делает следующий ход:
         True - ход повторяется.
         False - ход переходит сопернику."""
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            # d - куда стреляют
            # если корабль в списке  (проверяем равенство, если True - то попал)
            if ship.shooten(d):
                ship.lives -= 1
                #по координатам ставим Х (корабль ранен)
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.countour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    #обнуляем список точек рядом с кораблем
    # теперь будет использоваться для хранения точек, куда стрелял игрок
    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy


    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                # возвращает куда будет делать выстрел
                target = self.ask()
                #возвращает булевое значение (принятие кому делать ход)        repeat = self.кто_ходит.метод_выстрела_вернет_bool(координаты_выстрела)
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Введите 2 координаты! ")
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа! ")
                continue
            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)           # Индексы с 0 поэтому -1

### ??????????????????????
class Game:
    def __init__(self, size=6):
        self.size = size
        #Одна доска для компьютера, другая для игрока
        pl = self.random_board()
        co = self.random_board()
        #Скрываем для пк корабли
        co.hid = True

        # и юзеру два окна и боту
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")


    def print_boards(self):
        print("-" * 20)
        print("Доска пользователя:")
        print(self.us.board)
        print("-" * 20)
        print("Доска компьютера:")
        print(self.ai.board)
        print("-" * 20)


    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_boards()
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.defeat():
                self.print_boards()
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()
### ??????????????????????

g = Game()
g.start()