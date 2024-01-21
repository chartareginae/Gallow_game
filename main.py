import pygame
import re
import random
import sqlite3
import requests
from bs4 import BeautifulSoup as Soup
import os
import sys

# вводим цвета по системе RGB
white = (0, 0, 0)
black = (255, 255, 255)
green = (124, 252, 0)
red = (255, 0, 0)
green2 = (0, 153, 0)
sell_size = 50
wight = 1200
height = 600
size = (wight, height)

pygame.init()

# создание плоскости для работы, работа с окном
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ВИСЕЛИЦА")
icon = pygame.image.load('6498720.png')
pygame.display.set_icon(icon)


# рисуем клавиатуру
def draw_keyboard():
    for i in range(1, 5):
        pygame.draw.line(screen, black, (0, height - (sell_size * i)),
                         (wight, height - (sell_size * i)), 1)
    for i in range(1, 9):
        pygame.draw.line(screen, black, (wight / 8 * i, height - (sell_size * 4)),
                         (wight / 8 * i, height), 1)


# работа со шрифтом
font_size = int(sell_size // 2)
font = pygame.font.SysFont('Verdana', font_size)
font2 = pygame.font.SysFont('Verdana', sell_size)


# gallow - виселица
class Gallow:
    def __init__(self):
        self.color = black
        self.coords_begin = ((940, 300), (940, 75), (1075, 75), (1075, 160),
                             (1075, 160), (1075, 160), (1075, 240), (1075, 240))
        self.coords_end = ((940, 75), (1075, 75), (1075, 100), (1075, 240),
                           (1100, 220), (1050, 220), (1100, 300), (1050, 300))
        self.i = 0

    def draw_filed(self):
        pi = 3.14
        pygame.draw.arc(screen, green, (840, 300, 200, 150), 0, pi, 75)

    def draw_head(self):
        pygame.draw.circle(screen, black, (1075, 130), 30, 3)

    def draw_line(self):
        pygame.draw.line(screen, black, self.coords_begin[self.i], self.coords_end[self.i], 3)
        self.i += 1


# работа с буквами
class Letters:
    def __init__(self):
        self.all_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р',
                            'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

    # расставляем буквы на клавиатуре
    def draw_letters(self):
        for i in range(1, 5):
            for j in range(1, 9):
                letter_print = font.render(self.all_letters[(8 * (i - 1) + j) - 1], True, black)
                letter_wight = letter_print.get_width()
                letter_height = letter_print.get_height()
                screen.blit(letter_print, ((wight // 8 * j) - (wight // 16 + letter_wight // 2),
                                           sell_size * i - (sell_size // 2 + letter_height // 2) + height -
                                           (sell_size * 4)))

    # кладем букву на игровое поле (угаданную букву)
    def put_letter_on_filed(self, letter, word):
        result = [_.start() for _ in re.finditer(letter, word)]
        for i in result:
            letter_print = font.render(letter, True, black)
            letter_example = font.render('Щ', True, black)
            letter_wight = letter_example.get_width()
            letter_height = letter_print.get_height()
            distance = 815 // len(word)
            screen.blit(letter_print, (50 + distance * i + letter_wight * 0.8, 250 - letter_height * 1.2))
        all_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р',
                       'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
        index_of_letter = all_letters.index(letter) + 1
        letter_print = font.render(letter, True, green2)
        letter_wight = letter_print.get_width()
        letter_height = letter_print.get_height()
        i = index_of_letter // 8
        j = index_of_letter - (i * 8)
        if j == 0:
            j = 8
            i -= 1
        screen.blit(letter_print, ((wight // 8 * j) - (wight // 16 + letter_wight // 2),
                                   sell_size * i - (sell_size // 2 + letter_height // 2) +
                                   height - (sell_size * 4) + 50))

    # подсвечиваем букву красным
    def wrong_letter(self, letter):
        all_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р',
                       'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
        index_of_letter = all_letters.index(letter) + 1
        letter_print = font.render(letter, True, red)
        letter_wight = letter_print.get_width()
        letter_height = letter_print.get_height()
        i = index_of_letter // 8
        j = index_of_letter - (i * 8)
        if j == 0:
            j = 8
            i -= 1
        screen.blit(letter_print, ((wight // 8 * j) - (wight // 16 + letter_wight // 2),
                                   sell_size * i - (sell_size // 2 + letter_height // 2) +
                                   height - (sell_size * 4) + 50))

    # узнаем куда был выполнен щелчок мышью
    def what_letter(self, coordinate, blocked_letters):
        i = (coordinate[1] - 400) // 50
        j = coordinate[0] // 150
        all_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т',
                       'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
        if coordinate[1] < 400 or all_letters[i * 8 + j] in blocked_letters:
            return ".", blocked_letters
        blocked_letters.append(all_letters[i * 8 + j])
        return all_letters[i * 8 + j], blocked_letters


# убираем лишние html символы
def remove_extraneous_characters(listt, data1):
    for i in listt:
        data1 = data1.replace(str(i), str(i)[str(i)[:-1].rfind('>') + 1:str(i).rfind('<')])
    return data1


# узнаем значение слова
def value(word):
    word_rus = word.lower()
    url_rus = f'https://ru.wikipedia.org/wiki/{word_rus}'
    source = requests.get(url_rus)
    soup = Soup(source.content, 'html.parser')
    symbols = ['b', 'sup', 'span', 'i', 'a', 'small', 'sub']
    data1 = str(soup.find('p'))
    for symbol in symbols:
        data = soup.find('p').find_all(symbol)
        data1 = remove_extraneous_characters(data, data1)
    data1 = data1.replace('<p>', '')
    data1 = data1.replace('</p>', '')
    return data1


# обработка финала
class Finish:
    def __init__(self):
        self.sprite = pygame.sprite.Sprite()
        self.all_sprites = pygame.sprite.Group()
        self.ind = 0

    def you_win_lost(self, leg_right, word, value_word, guessed_letters):
        wight_rect = 700
        if leg_right:
            height_rect = 150
        else:
            height_rect = 200

        if leg_right:
            pygame.draw.rect(screen, white,
                             (wight // 2 - (wight_rect // 2), height // 2 - (height_rect // 2 + 50), wight_rect,
                              height_rect), 150)
            pygame.draw.rect(screen, black, (wight // 2 - (wight_rect // 2), height // 2 - (height_rect // 2 + 50),
                                             wight_rect, height_rect), 3)

            pygame.draw.rect(screen, black, (wight // 2 - 200, height // 2 - 50, 400, 50), 3)
            phrase_print = font.render(f"ВЫ ВЫИГРАЛИ! УГАДАНО {guessed_letters} ИЗ {len(word)} БУКВ", True, black)
            phrase_print2 = font.render("ИГРАТЬ СНОВА", True, black)

            phrase_wight = phrase_print.get_width()
            phrase_wight2 = phrase_print2.get_width()
            phrase_height = phrase_print.get_height()

            screen.blit(phrase_print, (wight // 2 - (phrase_wight // 2), height // 2 - (phrase_height // 2 + 85)))
            screen.blit(phrase_print2, (wight // 2 - phrase_wight2 // 2, height // 2 - 40))

        else:
            self.sprite.image = self.load_image("shot1_arms.png")
            self.all_sprites.add(self.sprite)
            self.sprite.rect = self.sprite.image.get_rect()
            self.all_sprites.add(self.sprite)

            self.sprite.rect.x = 831
            self.sprite.rect.y = 59
            self.up_gallow()

            pygame.draw.rect(screen, white, (wight // 2 - (wight_rect // 2), height // 2 - (height_rect // 2 + 50),
                                             wight_rect, height_rect), 150)
            pygame.draw.rect(screen, black, (wight // 2 - (wight_rect // 2), height // 2 - (height_rect // 2 + 50),
                                             wight_rect, height_rect), 3)
            pygame.draw.rect(screen, black, (wight // 2 - 200, height // 2 - 25, 400, 50), 3)
            phrase_print = font.render(f"ВЫ ПРОИГРАЛИ. УГАДАНО {guessed_letters} ИЗ {len(word)} БУКВ", True, black)
            phrase_print2 = font.render(f"ЭТО СЛОВО {word}", True, black)
            phrase_print3 = font.render("ИГРАТЬ СНОВА", True, black)

            phrase_wight = phrase_print.get_width()
            phrase_height = phrase_print.get_height()
            phrase_wight2 = phrase_print2.get_width()
            phrase_wight3 = phrase_print3.get_width()

            screen.blit(phrase_print, (wight // 2 - (phrase_wight // 2), height // 2 - (phrase_height // 2 + 110)))
            screen.blit(phrase_print2, (wight // 2 - (phrase_wight2 // 2), height // 2 - (phrase_height // 2 + 60)))
            screen.blit(phrase_print3, (wight // 2 - phrase_wight3 // 2, height // 2 - 12.5))

        draw_value(value_word)

    # анимация висельника
    def up_gallow(self):
        clock = pygame.time.Clock()
        running = True
        counter = 0

        while running:
            self.all_sprites.draw(screen)
            self.ind = (self.ind + 1) % 5
            self.re_flash(self.ind)

            self.sprite.rect = self.sprite.image.get_rect()
            self.sprite.rect.x = 831
            self.sprite.rect.y = 59

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            counter += 1
            if counter > 23:
                break
            clock.tick(8)

            pygame.display.flip()

    # обработка спрайтов
    def load_image(self, name):
        fullname = os.path.join(name)
        if not os.path.isfile(fullname):  # если файл не существует, то выходим
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    # работа со спрайтом
    def re_flash(self, ind):
        lis = ['shot3_arms_.png', 'shot4_arms_.png', 'shot5_arms_.png',
               'shot4_arms_.png', 'shot3_arms_.png']
        self.sprite.image = self.load_image(lis[ind])
        self.sprite.rect = self.sprite.image.get_rect()


# выводим значение слова на экран
def draw_value(value_word):
    pygame.draw.rect(screen, white, (0, height - (sell_size * 4), wight, height))
    pygame.draw.line(screen, black, (0, height - (sell_size * 4)),
                     (wight, height - (sell_size * 4)), 1)

    sr = int(len(value_word) / 80 + 1)
    value_word1 = ' '.join(value_word.split())

    if len(value_word) > 560:
        value_word1 = value_word1[:561]
        s = value_word.rfind('.')
        value_word1 = value_word1[:s]

    for i in range(sr):
        if len(value_word) > 80:
            example = font.render(value_word1[:81], True, black)
            value_word1 = value_word1[81:]
        else:
            example = font.render(value_word, True, black)
        screen.blit(example, (0, height - 200 + i * 25))


def play_again(coordinate, leg_right):
    if wight // 2 - 200 <= coordinate[0] <= wight // 2 + 200 and height // 2 - 25 <= coordinate[1] <= height // 2 + 25 \
            and not leg_right:
        main()

    elif wight // 2 - 200 <= coordinate[0] <= wight // 2 + 200 and height // 2 - 50 <= coordinate[1] <= height // 2 \
            and leg_right:
        main()


# стартовое окно
def draw_choice_topic():
    text = font2.render("ВЫБЕРИТЕ ТЕМУ", True, green)
    text_wight = text.get_width()
    screen.blit(text, (wight / 2 - text_wight / 1.9, 100))

    pygame.draw.rect(screen, black, (50, 250, 525, 75), 3)
    pygame.draw.rect(screen, black, (625, 250, 525, 75), 3)
    pygame.draw.rect(screen, black, (312.5, 400, 575, 75), 3)

    topic1 = font2.render("ХИМИЯ", True, black)
    topic1_wight = topic1.get_width()
    topic2 = font2.render("ФИЗИКА", True, black)
    topic2_wight = topic2.get_width()
    topic3 = font2.render("РУССКИЙ ЯЗЫК", True, black)
    topic3_wight = topic2.get_width()

    screen.blit(topic1, (45 + 525 // 2 - topic1_wight // 2, 255))
    screen.blit(topic2, (620 + 525 // 2 - topic2_wight // 2, 255))
    screen.blit(topic3, (230 + 525 // 2 - topic3_wight // 2, 405))


# рисуем игровое поле (расставляем количество букв)
def draw_filed(word):
    count_letters = len(word)
    letter_example = font.render("О", True, black)
    letter_wight = letter_example.get_width()
    distance = 815 // count_letters
    for i in range(count_letters):
        pygame.draw.line(screen, black, (50 + distance * i, 250), (50 + distance * i + letter_wight * 3, 250), 3)


def main():
    global value_word
    game_over = False
    gallow_is_drawn = [True, True, True, True, True, True, True, True, True]
    first_screen = True
    leg_right = True

    screen.fill(white)
    draw_choice_topic()
    pygame.display.update()
    blocked_letters = []
    word = ''
    count_letters = 0

    con = sqlite3.connect("baze.sqlite")
    cur = con.cursor()
    if_you_lost = Gallow()
    letters = Letters()
    win_lost = Finish()
    while not game_over:

        # экстренное закрытие игры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if first_screen and ((50 <= event.pos[0] <= 575 and 250 <= event.pos[1] <= 325)
                                     or (625 <= event.pos[0] <= 1150 and 250 <= event.pos[1] <= 325)
                                     or (312.5 <= event.pos[0] <= 887.5 and 400 <= event.pos[1] <= 475)):
                    if 50 <= event.pos[0] <= 575 and 250 <= event.pos[1] <= 325:
                        result = cur.execute("""SELECT * FROM chemistry""").fetchall()
                        word = random.choice(result)

                    elif 625 <= event.pos[0] <= 1150 and 250 <= event.pos[1] <= 325:
                        result = cur.execute("""SELECT * FROM phis""").fetchall()
                        word = random.choice(result)

                    elif 312.5 <= event.pos[0] <= 887.5 and 400 <= event.pos[1] <= 475:
                        result = cur.execute("""SELECT * FROM all_time""").fetchall()
                        word = random.choice(result)

                    if word[0][0].isdigit():
                        value_word = value(word[1])
                    else:
                        value_word = value('_'.join(word))

                    word = word[1]
                    screen.fill(white)
                    draw_keyboard()
                    letters.draw_letters()
                    count_letters = 0
                    draw_filed(word)
                    first_screen = False
                    pygame.display.update()

                elif first_screen:
                    continue

                else:
                    letter, blocked_letters = letters.what_letter(event.pos, blocked_letters)
                    if letter != '.' and letter in word:
                        letters.put_letter_on_filed(letter, word)
                        pygame.display.update()
                        count_letters += word.count(letter)

                        if count_letters == len(word):
                            blocked_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н',
                                               'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы',
                                               'Ь', 'Э', 'Ю', 'Я']
                            win_lost.you_win_lost(leg_right, word, value_word, count_letters)
                            pygame.display.update()
                            continue

                        pygame.display.update()
                    elif letter != '.':
                        letters.wrong_letter(letter)
                        if gallow_is_drawn[-1]:
                            for line in range(len(gallow_is_drawn)):
                                if gallow_is_drawn[line]:
                                    if line == 0:
                                        if_you_lost.draw_filed()
                                    elif line == 4:
                                        if_you_lost.draw_head()
                                    else:
                                        if_you_lost.draw_line()
                                    gallow_is_drawn[line] = False
                                    break
                                else:
                                    continue
                        elif leg_right:
                            if_you_lost.draw_line()
                            leg_right = False
                            win_lost.you_win_lost(leg_right, word, value_word, count_letters)
                            blocked_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н',
                                               'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы',
                                               'Ь', 'Э', 'Ю', 'Я']
                            pygame.display.update()
                            continue
                        pygame.display.update()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        play_again(event.pos, leg_right)


main()
pygame.quit()
