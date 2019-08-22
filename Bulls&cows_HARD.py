from itertools import permutations
from random import shuffle
from random import choice
from time import perf_counter
total_score = {'computer': 0, 'user': 0, 'draw': 0}
digits = '0123456789'


def scorecalc(guess, answer):
    bulls = sum(i == j for i, j in zip(guess, answer))
    cows = len(set(guess) & set(answer)) - bulls
    return bulls, cows


def game(size):
    for_cheat = choices = list(permutations(digits, size))
    shuffle(choices); shuffle(for_cheat)
    pc_secret = ''.join(choice(choices))
    attempt = 0
    user_history = []
    print(f"Начнём игру! Загадайте {size}-значное число. \nЯ попытаюсь его угадать, а вы попытайтесь угадать моё.")

    while True:
        guess = choice(choices)
        attempt += 1
        print(f"\nПопытка №{attempt}. Моя догадка: {''.join(guess)}.")
        bulls = int(input("Введите количество быков: "))
        cows = int(input("Введите количество коров: "))
        user_guess = input("Введите вашу догадку: ")
              
        if user_guess == pc_secret and len(for_cheat) > 1:
            for_cheat.remove(tuple(pc_secret))
            pc_secret = ''.join(choice(for_cheat))

        if bulls == size and user_guess == pc_secret:
            print(f"\nНичья! \nВаше число: {''.join(guess)}. \nМоё число: {pc_secret}.")
            total_score['draw'] += 1
            break
        elif bulls == size:
            print(f"\nХа-ха-ха! Вы проиграли! \nЗагаданное мною число — {pc_secret}.")
            total_score['computer'] += 1
            break
        elif user_guess == pc_secret:  
            print("\nПоздравляю, вы выйграли!")
            total_score['user'] += 1
            break

        choices = [c for c in choices if scorecalc(c, guess) == (bulls, cows)]
        if not choices:
            print("Вы где-то мне соврали!")
            break

        user_bulls, user_cows = scorecalc(user_guess, pc_secret)
        user_history.append((user_guess, user_bulls, user_cows))
        for_cheat = [c for c in for_cheat if scorecalc(c, user_guess) == (user_bulls, user_cows)]
        print("\n№ | ВАША ДОГАДКА | БЫКИ | КОРОВЫ |")
        print("——|——————————————|——————|————————|")
        for i in range(len(user_history)):
            print("{0} | {1:12} | {2:4} | {3:6} |".format(
                i+1, user_history[i][0], user_history[i][1], user_history[i][2]))
            print("——|——————————————|——————|————————|")


def main():
    tumbler = "да"
    while tumbler.startswith("да"):
        number_size = int(input("Введите размер числа (1-10), которое будете загадывать: "))
        tick = perf_counter()
        try:
            game(number_size)
        except Exception as e:
            print("Вы где-то мне соврали!")
            print(e)
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