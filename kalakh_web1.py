# Игра "Калах" для двух игроков

# Основные константы
BOTTOM_PLAYER = 0
TOP_PLAYER = 1
HUMAN_PLAYER = 0
COMPUTER_PLAYER = 1
GAME_OVER = -1
GO_ON = 1

# Класс Board - реализация простого циклического контейнера, описывающего доску для игры в калах
# Соотнесение лунок игроков c ячейками списка:
# Лунка              | 5 | 4 | 3 | 2 | 1 | 0 |                обращение к лункам игрока TOP_PLAYER
# Ячейка               12  11  10  9   8   7
# Калах       |/\| 13                         6 |\/|
# Ячейка               0   1   2   3   4   5
# Лунка              | 0 | 1 | 2 | 3 | 4 | 5 |                обращение к лункам игрока BOTTOM_PLAYER
# № на доске           1   2   3   4   5   6                  един для обоих игроков, если ход делает человек
#

class Board(list):
    # Конструктор, по умолчанию заполняющий стартовую позицию
    # holes         - исходное состояние ячеек, по умолчанию - стартовая доска
    #                 если holes принадлежит к классу Board, доски копируются
    # the_hole      - номер ячейки, из которой делается ход сразу после создания нового экземпляро доски
    #                 если the_hole == -1 (значение по умолчанию), то ход не делатся
    # which_player  - указывает, с какой стороны доски делается ход
    def __init__(self, holes = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0], the_hole = -1, which_player = TOP_PLAYER):
        # Инициализация родительского класса list
        super().__init__(holes)

        # Сделать ход, если указана лунка
        if the_hole >= 0 :
            self.move(the_hole, which_player )

    # Вывод игрового поля
    def draw_board(self):
        print(f'      |', end='')

        # Камни в верхних лунках
        for i in range(6):  
            print(' %2d |' % (self[12-i]), end='')
        # Камни в калахах
        print('\n  %2d  |                             |  %2d' % (self[13], self[6]))
        print(f'      |', end='')
        # Камни в нихних лунках
        for i in range(6):
            print(' %2d |' % (self[i]), end='')
        # Номера лунок на доске (для обеих сторон при ходе игрока-человека)
        print(f'\n\n       ', end='')
        for i in range(6):
            print(' %2d  ' % (i+1), end='')

        print('\n\n')
        print(self.position_estimate(TOP_PLAYER))


    # Раскладывает камни из ячейки hole в следующие ячейки по кругу, против часовой стрелки, исключая калах противника.
    # Возвращает номер ячейки списка, в которую попал последний камень
    def simple_move(self, hole):

        # Число камней в лунке
        n = self[hole]
        # Камни забрали из лунки
        self[hole] = 0

        # Счетчик лунок
        current_hole = hole

        while n > 0 :
            # Если исходная лунка на нижней стороне
            if hole < 6 :
                # Увеличить номер лунки на 1, либо пропустиь калах противника и продолжить с лунки 0
                current_hole = 0 if current_hole == 12 else current_hole + 1
            # Если исходная лунка на верхней стороне
            else :
                # Если это калах противника - пропустить его
                if current_hole == 5 :
                    current_hole = current_hole + 2
                # Увеличить номер лунки на 1, либо, дойдя до 13, продолжить с лунки 0
                else :
                    current_hole = 0 if current_hole == 13 else current_hole + 1

            # Увеличить число камней в текущей лунке на 1
            self[current_hole] = self[current_hole] + 1
            # Уменьшить счетчик камней на 1
            n = n - 1

        # Вернуть номер поледней ячейки
        return current_hole

    # Делает ход и реализовывает дополнительные правила игры
    # hole          - номер лунки, из которой делается ход (от 0 до 5)
    # which_player  - игрок, сделавший ход
    # Возвращает True если последний камень попал в свой калах
    def move(self, hole, which_player):

        # Перевод номера лунки в номер ячейки списка
        start_hole = hole if which_player == BOTTOM_PLAYER else hole + 7
        # Разложить камни и узнать последнюю ячейку
        end_hole = self.simple_move(start_hole)

        # Если последний камень попал в пустую лунку и противолежащая лунка на стороне противника не пуста
        if end_hole != 6 and end_hole != 13 and self[end_hole] == 1 and self[12 - end_hole] != 0 :
            # Если ход начался и завершился на одной стороне
            if (start_hole < 6 and end_hole < 6) or (start_hole > 6 and end_hole > 6):
                # Положить камни из обеих лунок в калах игрока, сделавшего ход
                self[6 if start_hole < 6 else 13] = self[6 if start_hole < 6 else 13] + self[end_hole] + self[12 - end_hole]
                self[end_hole] = 0
                self[12 - end_hole] = 0

        # Вернуть True если последний камень попал в свой калах
        return (end_hole == 6 and start_hole < 6) or (end_hole == 13 and start_hole > 6)

    # Оценочная функция позиции для указанного игрока - разность камней в калахах
    def position_estimate(self, which_player):
        sum_bottom = 0
        sum_top = 0
        for i in range(7) :
            sum_bottom = sum_bottom + self[i]
            sum_top = sum_top + self[7+i]

        return sum_top - sum_bottom if which_player == TOP_PLAYER else sum_bottom - sum_top
        #return self[13] - self[6] if which_player == TOP_PLAYER else self[6] - self[13]

    # Возвращает True если последний камень попадает в калах игрока which_player после хода из лунки hole
    def to_kalakh(self, hole, which_player) :
        if which_player == BOTTOM_PLAYER :
            return (hole + self[hole] - 6) % 13 == 0
        else :
            return (hole + self[hole + 7] - 6) % 13 == 0

    # Возвращает количетво камней в лунке hole на стороне игрока which_player
    def in_hole(self, hole, which_player) :
        return self[hole] if which_player == BOTTOM_PLAYER else self[hole + 7]

    # Возвращает True если это первый ход (оба калаха пусты)
    def initial_board(self) :
        return self[6] == 0 and self[13] == 0

    # Возвращает True если на стороне игрока which_player не осталось камней
    def is_side_empty(self, which_player) :
        return max(self[0:6]) == 0 if which_player == BOTTOM_PLAYER else max(self[7:13]) == 0

    # Перемещает все оставшиеся в игре камни в калахи игроков, обнуляя игровые лунки
    def finalise(self) :
        self[6] = self[6] + sum(self[0:6])
        self[13] = self[13] + sum(self[7:13])

        self[0:6] = [0, 0, 0, 0, 0, 0]
        self[7:13] = [0, 0, 0, 0, 0, 0]

    def max_kalakh(self) :
        return max(self[6], self[13]);


# Класс "Player" - инкапсуляция основных параметров игрока и реализация алгоритма игры
# Игрок не привязан к конкретной доске и может играть на любой, описанной классом Board
class Player :
    # Конструктор, задает параметры игрока
    # which_player     - задает половину доски, верхнюю или нижнюю (ТОР_PLAYER или BOTTOM_PLAYER), принадлежащую игроку
    # strength         - сила игрока-компьютера, глубина, на которую делается оценка ходов.
    def __init__(self, which_player = BOTTOM_PLAYER, strength = 5 ) :
        self.player_side = which_player
        self.player_strength = strength

    # Возвращает сторону доски противоположную стороне игрока
    def opponent_side(self) :
        return TOP_PLAYER if self.player_side == BOTTOM_PLAYER else BOTTOM_PLAYER

    # Возвращает оптимальный ход из позиции board
    # Возвращает флаг окончания игры если дальнейшие ходы невозможны
    def best_move(self, board) :

        # Если в одном из калахов больше 36 камней или нет больше ходов закончить игру
        if board.max_kalakh() > 36 or board.is_side_empty(self.player_side):
             return GAME_OVER

        hole = -1

        # Минимальное значение оценки
        estimation = -50

        # Определение диапазона лунок, из которых возможны ходы
        from_hole = 0
        # Если это начало игры, ход из самой дальней от своего калаха лунки запрещен
        if board.initial_board() : from_hole = 1

        # Далее аналог функции max_estimate, но с запоминанием хода с высшей оценкой
        # Ходы по-очереди из всех лунок
        for i in range(from_hole, 6) :
            # Если лунка не пустая
            if board.in_hole(i, self.player_side) > 0 :
                # Если после этого хода последний камень попадет в свой калах...
                if board.to_kalakh(i, self.player_side) :
                    # Оценить свои ходы после хода из лунки i. Сделать ход, создав Board(board, i, player_side),
                    # и вызвать функцию max_estimate для получившейся позиции
                    hole_estimation = self.max_estimate(Board(board, i, self.player_side), self.player_strength, 50)
                else :
                    # Оценить ответ противника на ход из лунки i. Сделать ход, создав Board(board, i, player_side),
                    # и вызвать функцию min_estimate для оценки получившейся позиции
                    hole_estimation = self.min_estimate(Board(board, i, self.player_side), self.player_strength, estimation)

                # Если этот ход лучше предыдущих
                if hole_estimation > estimation :
                    # Сохранить параметры хода
                    estimation = hole_estimation
                    hole = i

        if hole < 0 :
            return GAME_OVER

        return hole

    # Рекурсивные функции для реализации MinMax алгоритма поиска оптимальной стратегии
    # max_estimate поочередно делает все ходы игрока и вызывает для оценки каждого из них функцию
    # min_estimate, которая делает поочередно все следующие ходы оппонента и вызывает для их оценки
    # снова функцию max_estimate и т.д, до достижения заданной глубины ходов

    # Оценка ходов игрока из позиции board
    # board    - позиция, ходы из которой нужно оценить
    # depth    - глубина анализа - количество последовательных ходов
    # Возвращает резуьтат лучшего хода (ход с максимальной оценкой)
    def max_estimate(self, board, depth, preliminary_estimation) :
        # Минимальная возможная оценка
        estimation = -50

        # Если в одном из калахов больше 36 камней или нет больше ходов, пренести содержимое игровых лунок в калах
        if board.max_kalakh() > 36 or board.is_side_empty(self.player_side):
            board.finalise()
            # Вернуть оценку позиции
            return board.position_estimate(self.player_side)

        # Если уже сделано заданное число ходов в глубину, просто вернуть оценку позиции
        if depth == 0:
            return board.position_estimate(self.player_side)

        # Сделать все ходы и найти позицию с максимальной оценкой
        for i in range(6) :
            # Если текущая лунка не пуста
            if board.in_hole(i, self.player_side) > 0 :
                # Если последний камень попал в свой калах
                if board.to_kalakh(i, self.player_side) :
                    # Оценить свои ходы после хода из лунки i. Сделать ход, создав Board(board, i, player_side),
                    # и вызвать функцию max_estimate для оценки получившейся позиции, уменьшив глубину анализа на 1
                    estimation = max(estimation, self.max_estimate(Board(board, i, self.player_side), depth - 1, 50) )
                else :
                    # Оценить ответ противника на ход из лунки i. Сделать ход,  создав Board(board, i, player_side),
                    # и вызвать функцию min_estimate для оценки получившейся позиции, уменьшив глубину анализа на 1
                    estimation = max(estimation, self.min_estimate(Board(board, i, self.player_side), depth - 1, estimation ) )

            if ( estimation > preliminary_estimation ) :
                return estimation

        if depth <= 0 :
            print(depth)
        # Вернуть полученную оценку позиции
        return estimation


    # Оценка позиции board с точки зрения оппонента
    # board    - позиция, ходы оппонента из которой нужно оценить
    # depth    - глубина анализа, количество последовательных ходов
    # Выбирается резуьтат лучшего хода с точки зрения оппонента (ход с минимальной оценкой)
    def min_estimate(self, board, depth, preliminary_estimation) :
        # Максимальная возможная оценка
        estimation = 50

        # Если у оппонента нет больше ходов, перенести содержимое игровых лунок в калах
        if board.max_kalakh() > 36 or board.is_side_empty(self.opponent_side()) :
            board.finalise()
            # Вернуть оценку позиции
            return board.position_estimate(self.player_side)

        # Если сделано максимальное число ходов в глубину, просто вернуть оценку позиции
        if depth == 0 :
            return board.position_estimate(self.player_side)

        # Сделать все ходы оппонента и найти позицию с минимальной оценкой
        for i in range(6) :
            # Если текущая лунка оппонента не пуста
            if board.in_hole(i, self.opponent_side()) > 0 :
                # Если последний камень оппонента попадает в его калах
                if board.to_kalakh(i, self.opponent_side()) :
                    # Оценить повторные ходы противника после его хода из лунки i, создав Board(board, i, opponent_side)
                    # и снова вызвав функцию min_estimate для получившейся позиции, уменьшив глубину анализа на 1
                    estimation = min(estimation, self.min_estimate(Board(board, i, self.opponent_side()), depth - 1, -50 ) )
                else :
                    # Оценить ходы после хода противника из лунки i, сделав этот ход (Board(board, i, opponent_side)
                    # и вызвав функцию mах_estimate для получившейся позиции, уменьшив глубину анализа на 1
                    estimation = min(estimation, self.max_estimate(Board(board, i, self.opponent_side()), depth - 1, estimation ) )

            if ( estimation < preliminary_estimation ) :
                return estimation

        # Вернуть полученную оценку позиции
        if depth == 0 :
            print(depth)
        return estimation

    # Делает оптимальный ход из позиции board
    # Возвращает флаг окончания игры если дальнейшие ходы невозможны или поступила команда на остановку
    def make_move(self, board) :

        hole = self.best_move(board)

        if hole < 0 :
            board.finalise()
            return GAME_OVER;

        # Если последний камень игрока, делавшего ход, попал в свой калах
        if board.move(hole, self.player_side) :
            # Нарисовать поле
            board.draw_board()
            # Сделать еще один ход
            return self.make_move(board)

        # Если все лунки противника пусты
        if board.is_side_empty(self.opponent_side()):
            # Очистить игровые лунки
            board.finalise()
            return GAME_OVER

        return GO_ON


wells = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
my_board = Board(wells)
player = Player(BOTTOM_PLAYER, 2)

print(player.best_move(my_board ))







