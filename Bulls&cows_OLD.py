from itertools import product
from itertools import count
from random import choice
from time import perf_counter
total_score = {'computer': 0, 'user': 0, 'draw': 0}


def game(size):
    everything = ["".join(x) for x in product('0123456789', repeat=size) if len(set(x)) == len(x)]  # все возможные комбинации без повторяющихся цифр
    pc_secret = choice(everything)  # число, загаданное компьютером

    def bulls_n_cows(guess, answer):  # функция подсчёта быков и коров
        assert guess in everything and answer in everything  # ловля ошибки ввода
        bulls = sum(1 for x, y in zip(guess, answer) if x == y)  # количество быков
        cows = len(set(guess) & set(answer)) - bulls  # количество коров
        return bulls, cows

    def is_compatible(guess, history):  # проверка на совместимость с историей
        # если количество всех быков и коров из истории совпадает с количеством быков и коров какой-то i-ой перебираемой комбинации
        return all(bulls_n_cows(guess, previous_guess) == (bulls, cows) for previous_guess, bulls, cows in history)

    print(f"Начнём игру! Загадайте {size}-значное число. \nЯ попытаюсь его угадать, а вы попытайтесь угадать моё.")
    guess_space = set(everything)  # это множество, из которого мы будем выбирать догадки и вычёркивать уже выбранные или не подходящие
    history = []  # история угадываний
    user_history = []  # исторя угадываний пользователя

    for attempt in count(1):
        while True:
            guess = choice(list(guess_space))  # выбираем рандомное число из всевозможных комбинаций
            guess_space.remove(guess)  # удаляем его, чтобы больше никогда не выбирать это число
            if is_compatible(guess, history):   # если число совместимо с историей - выбрать его (даст ли оно те же реакции на наши предыдущие ходы)
                break

        print(f"\nПопытка №{attempt}. Моя догадка: {guess}.")
        bulls = int(input("Введите количество быков: "))
        cows = int(input("Введите количество коров: "))
        history.append((guess, bulls, cows))
        user_guess = input("Введите вашу догадку: ")
        
        if bulls == len(guess) and user_guess == pc_secret:
            print(f"\nНичья! \nВаше число: {guess}. \nМоё число: {pc_secret}.")
            total_score['draw'] += 1
            break
        elif bulls == len(guess):
            print(f"\nХа-ха-ха! Вы проиграли! \nЗагаданное мною число — {pc_secret}.") 
            total_score['computer'] += 1
            break
        elif user_guess == pc_secret:
            print("\nПоздравляю, вы выйграли!")
            total_score['user'] += 1
            break
            
        user_bulls, user_cows = bulls_n_cows(user_guess, pc_secret)
        user_history.append((user_guess, user_bulls, user_cows))
        print("\n№ | ВАША ДОГАДКА | БЫКИ | КОРОВЫ |")
        print("——|——————————————|——————|————————|")
        for i in range(len(user_history)):
            print("{0} | {1:12} | {2:4} | {3:6} |".format(i+1, user_history[i][0], user_history[i][1], user_history[i][2]))
            print("——|——————————————|——————|————————|")


def main():
    tumbler = "да"
    while tumbler.startswith("да"):
        number_size = int(input("Введите размер числа (1-6), которое будете загадывать: "))
        tick = perf_counter()
        game(number_size)
        total_time = perf_counter() - tick
        print("\n|================================================|")
        print("|  ИГРОК  |  ВРЕМЯ  | ПОБЕДЫ | ПОРАЖЕНИЯ | НИЧЬИ |")
        print("|—————————|—————————|————————|———————————|———————|")
        print("| {0} | {1:7} | {2:6} | {3:9} | {4:5} |".format(
            'Виталий', f"{round(total_time // 60)}м {round(total_time % 60)}c", total_score['user'], total_score['computer'], total_score['draw']))
        print("|================================================|")
        tumbler = input("\nХотите начать новую игру? (да/нет) ")


if __name__ == "__main__":
    main()