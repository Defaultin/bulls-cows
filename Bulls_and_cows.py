from itertools import product
from itertools import count
from random import choice


def game(size):
    everything = ["".join(x) for x in product('0123456789', repeat=size) if len(
        set(x)) == len(x)]  # все возможные комбинации без повторяющихся цифр
    pc_secret = choice(everything)  # число, загаданное компьютером

    def bulls_n_cows(guess, answer):  # функция подсчёта быков и коров
        assert guess in everything and answer in everything  # ловля ошибки ввода
        bulls = sum(1 for x, y in zip(guess, answer)
                    if x == y)  # количество быков
        cows = len(set(guess) & set(answer)) - bulls  # количество коров
        return bulls, cows

    def is_compatible(guess, history):  # проверка на совместимость с историей
        # если количество всех быков и коров из истории совпадает с количеством быков и коров какой-то i-ой перебираемой комбинации
        return all(bulls_n_cows(guess, previous_guess) == (bulls, cows) for previous_guess, bulls, cows in history)

    print("Начнём игру! Я загадал число. Попробуйте его удагать, а я попробую угадать ваше!")
    # это множество, из которого мы будем выбирать догадки и вычёркивать уже выбранные или не подходящие
    guess_space = set(everything)
    history = []  # история угадываний
    user_history = []  # исторя угадываний пользователя

    for attempt in count(1):
        while True:
            # выбираем рандомное число из всевозможных комбинаций
            guess = choice(list(guess_space))
            # удаляем его, чтобы больше никогда не выбирать это число
            guess_space.remove(guess)
            # если число совместимо с историей - выбрать его (даст ли оно те же реакции на наши предыдущие ходы)
            if is_compatible(guess, history):
                break

        print(f"\nПопытка №{attempt}. Моя догадка: {guess}.")
        bulls = int(input("Введите количество быков: "))
        cows = int(input("Введите количество коров: "))
        history.append((guess, bulls, cows))
        if bulls == len(guess):
            print("Ха-ха-ха! Я выиграл!")
            break

        user_guess = input("Введите вашу догадку: ")
        if user_guess == pc_secret:
            print("Поздравляю, вы выйграли!")
            break
        user_bulls, user_cows = bulls_n_cows(user_guess, pc_secret)
        user_history.append((user_guess, user_bulls, user_cows))
        print("\n№ | ВАША ДОГАДКА | БЫКИ | КОРОВЫ |")
        print("——|——————————————|——————|————————|")
        for i in range(len(user_history)):
            print("{0} | {1:12} | {2:4} | {3:6} |".format(
                i+1, user_history[i][0], user_history[i][1], user_history[i][2]))
            print("——|——————————————|——————|————————|")


def main():
    tumbler = "да"
    while tumbler == "да":
        number_size = int(
            input("Введите размер числа, которое будете загадывать: "))
        game(number_size)
        tumbler = input("Игра закончена, хотите повторить? (да/нет) ")


if __name__ == "__main__":
    main()