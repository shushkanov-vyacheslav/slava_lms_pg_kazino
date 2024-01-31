# Данный код частично совмещён с кодом Юры и Максима
import pygame
import random
import sqlite3
import sys
import telebot
import pygame.locals
import math
import webbrowser
import datetime

connect = sqlite3.connect('polzovateli.sqlite')
cursor = connect.cursor()
API_TOKEN = '6810674714:AAGKeBsa0NlUhx2jECLUhnGxHv4s_ZLZQm4'
bot = telebot.TeleBot(API_TOKEN)
API_TOKEN2 = '6855961014:AAGpEI1f1EveHzMvb49EJG70CEAutDnsGr0'
bot2 = telebot.TeleBot(API_TOKEN2)
login = ''

all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
balls2 = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class PYZIRIK1(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__(all_sprites, balls)
        self.sp = ['puz.png', 'puz1.png', 'puz2.png']
        self.speed = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.image = pygame.image.load(f'kartinki/{random.choice(self.sp)}')
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size // 2, size // 2)
        self.vx, self.vy = random.choice(self.speed), random.choice(self.speed)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, balls2):
            self.vx = -self.vx
            self.vy = -self.vy


class PYZIRIK2(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__(all_sprites, balls2)
        self.sp = ['puz.png', 'puz1.png', 'puz2.png']
        self.speed = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.image = pygame.image.load(f'kartinki/{random.choice(self.sp)}')
        self.rect = pygame.Rect(x - size // 2, y - size // 2, size // 2, size // 2)
        self.vx, self.vy = random.choice(self.speed), random.choice(self.speed)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, balls):
            self.vx = -self.vx
            self.vy = -self.vy


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def valuta_name():
    return str(cursor.execute("SELECT valuta FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0])


def valuta_koef():
    val = str(cursor.execute("SELECT valuta FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0])
    valutes1 = [('aave', 114.52, 'aave.png'),
                ('arbitrum', 1.61, 'arbitrum.png'),
                ('bitcoin', 42571.5, 'bitcoin.png'),
                ('cardano', 0.6, 'cardano.png'),
                ('convex-finance', 3.45, 'convex-finance.png'),
                ('cosmos', 10.94, 'cosmos.png'),
                ('decentraland', 0.52, 'decentraland.png'),
                ('dogecoin', 0.09, 'dogecoin.png'),
                ('ethereum', 2285.8, 'ethereum.png'),
                ('ethereum-classic', 22.16, 'ethereum-classic.png'),
                ('filecoin', 6.92, 'filecoin.png'),
                ('internet-computer', 13.79, 'internet-computer.png'),
                ('litecoin', 73.91, 'litecoin.png'),
                ('polygon', 0.974492, 'polygon.png'),
                ('solana', 104.35, 'solana.png'),
                ('astar', 0.14, 'astar.png'),
                ('tron', 0.11, 'tron.png'),
                ('uniswap', 7.589595, 'uniswap.png'),
                ('unus-sed-leo', 3.95, 'unus-sed-leo.png'),
                ('usd-coin', 1.0, 'usd-coin.png')]
    n = 0
    for i in valutes1:
        if i[0] == val:
            break
        n += 1
    koef = float(valutes1[n][1])
    return koef


def valuta_logo(user=None):
    if user is None:
        logo = 'valuta/' + cursor.execute(
            "SELECT valuta FROM polzovatels WHERE username=?", (str(login), )).fetchall()[0][0] + '.png'
        return logo
    else:
        logo = 'valuta/' + cursor.execute(
            "SELECT valuta FROM polzovatels WHERE username=?", (str(user),)).fetchall()[0][0] + '.png'
        return logo


sl_number = {'0000': '−−−−', '0001': '−−−‐', '0002': '−−−-', '0010': '−−‐−', '0011': '−−‐‐',
             '0012': '−−‐-', '0020': '−−-−', '0021': '−−-‐', '0022': '−−--', '0100': '−‐−−',
             '0101': '−‐−‐', '0102': '−‐−-', '0110': '−‐‐−', '0111': '−‐‐‐', '0112': '−‐‐-',
             '0120': '−‐-−', '0121': '−‐-‐', '0122': '−‐--', '0200': '−-−−', '0201': '−-−‐',
             '0202': '−-−-', '0210': '−-‐−', '0211': '−-‐‐', '0212': '−-‐-', '0220': '−--−',
             '0221': '−--‐', '0222': '−---', '1000': '‐−−−', '1001': '‐−−‐', '1002': '‐−−-',
             '1010': '‐−‐−', '1011': '‐−‐‐', '1012': '‐−‐-', '1020': '‐−-−', '1021': '‐−-‐',
             '1022': '‐−--'}
sl_alphafit = {'q': '0000', 'w': '0001', 'p': '0002', 'e': '0010', 'o': '0011', 'r': '0012',
               'i': '0020', 't': '0021', 'u': '0022', 'y': '0100', 'a': '0101', 'l': '0102',
               's': '0110', 'k': '0111', 'd': '0112', 'j': '0120', 'f': '0121', 'h': '0122',
               'g': '0200', 'z': '0201', 'm': '0202', 'x': '0210', 'n': '0211', 'c': '0212',
               'b': '0220', 'v': '0221', '7': '0222', '8': '1000', '4': '1001', '5': '1002',
               '9': '1010', '1': '1011', '2': '1012', '6': '1020', '3': '1021', '0': '1022'}


def encoder(text):
    itog = ''
    for i in text:
        itog += sl_number[sl_alphafit[i]]
    return itog


def decoder(text):
    itog = []
    n = 0
    while len(itog) != len(text) // 4:
        for i in sl_number:
            if sl_number[i] == text[n:n+4]:
                itog.append(i)
                n += 4
    itog_2 = ''
    while len(itog_2) != len(text) // 4:
        if len(itog) > 0:
            for j in sl_alphafit:
                if len(itog) > 0:
                    if sl_alphafit[j] == itog[0]:
                        itog_2 += j
                        itog.remove(itog[0])
                else:
                    break
        else:
            break
    return itog_2


try:
    with open('D:/admin.txt', 'r') as file:
        file.close()
    with open('D:/admin.txt', 'w') as file:
        for i in cursor.execute("SELECT username, password FROM polzovatels").fetchall():
            file.write(f'{decoder(i[0])} {decoder(i[1])}\n')
        file.close()
except FileNotFoundError:
    bot.send_message(5473624098, 'Файл admin.txt не найден')

except IOError:
    bot.send_message(5473624098, 'Файл admin.txt не читается')


class Menu:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.flag = True
        self.width, self.height = 1200, 900
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption("Menu")
        self.date = cursor.execute("SELECT date_VIP FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]
        self.background_image = pygame.image.load('kartinki/fon_menu.png')
        self.screen.blit(self.background_image, (0, 0))
        self.white = (255, 255, 255)
        Border(5, 5, self.width - 5, 5)
        Border(5, self.height - 5, self.width - 5, self.height - 5)
        Border(5, 5, 5, self.height - 5)
        Border(self.width - 5, 5, self.width - 5, self.height - 5)
        self.clock = pygame.time.Clock()
        self.finished = False
        self.admin = False
        self.button = []
        for p in cursor.execute("SELECT username FROM admins").fetchall():
            if p[0] == str(login):
                self.admin = True
                break
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = (500, 850)
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        if str(cursor.execute("SELECT VIP FROM polzovatels WHERE username=?",
                              (str(login),)).fetchall()[0][0]) == 'VIP':
            self.date = cursor.execute("SELECT date_VIP FROM polzovatels WHERE username=?", (str(
                login),)).fetchall()[0][0]
            dt, tm = self.date.split()[0].split('-'), self.date.split()[1].split(':')
            year, mounth, day, chas, minutes = int(dt[0]), int(dt[1]), int(dt[2]), int(
                tm[0]), int(tm[1])
            self.date = datetime.datetime(year, mounth, day, chas, minutes)
            date = datetime.datetime.now()
            if self.date < date:
                cursor.execute("UPDATE polzovatels SET VIP=? WHERE username=?",
                               (str('NO VIP'), (str(login))))
                connect.commit()
        self.button = []
        play = ['Lucky Jet', 'Blackjack', 'Ruletka', 'Orel_Reshka', 'Русская рулетка', 'KriptoMine',
                'Miner', 'Dragon', 'slots', 'Вперед!', 'Наперстки', 'Chislo', 'Ruletka_x', 'Сейф',
                'Kubiki', 'Ruletka_Case_X', 'Ruletka_Case_Color', 'Lines', 'Vortex', 'Лотерейный билет',
                'Bomb', 'Letter or Bigger', 'КНБ', 'XOGENXEMER', 'EVEN/ODD', 'баккара',
                'PUSHKA', 'KENO', 'FOUR_LUCKY', 'Пиковая дама',
                'Пополнить', 'Обменик', 'Аккаунт', 'Промокод', 'TOP players',
                'Бонус за подписку', 'Ежедневный бонус', 'Конкурс', 'Кэшбэк', 'VIP']
        font = pygame.font.Font(None, 30)
        total = 0
        x = 25
        y = 20
        for _ in range(4):
            for _ in range(10):
                y += 50
                button_x, button_y, button_width, button_height = x, y, 200, 40
                input_rect = x, y, 200, 40
                self.button.append((x, y, 200, 40))
                pygame.draw.rect(self.screen, self.white, input_rect, 3, border_radius=15)
                text = font.render(play[total], True, (255, 255, 255))
                text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
                self.screen.blit(text, text_rect)
                total += 1
            y = 20
            x += 300
        text = font.render('Для администратора:', True, (255, 255, 255))
        self.screen.blit(text, (500, 650))
        play = ['Заработать бесплатные монетки!', 'Выйти из аккаунта!', 'Все username игроков',
                'Все игровые карты и промокоды', 'Статистика игрока', 'Удаление/обнуление игрока',
                'Добавление/удаление игровых карт', 'Промокоды']
        total, x, y = -1, 10, 600
        for i in range(4):
            if total == 1:
                y += 50
            for i in range(2):
                total += 1
                button_x, button_y, button_width, button_height = x, y, 600, 40
                input_rect = x, y, 580, 40
                pygame.draw.rect(self.screen, self.white, input_rect, 3, border_radius=15)
                text = font.render(play[total], True, (255, 255, 255))
                text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
                self.screen.blit(text, text_rect)
                self.button.append((x, y, 600, 40))
                x += 600
            x = 10
            y += 50

    def play(self):
        global all_sprites, balls, balls2, horizontal_borders, vertical_borders
        while not self.finished:
            self.screen.blit(self.background_image, (0, 0))
            if len(all_sprites) > 44:
                all_sprites = pygame.sprite.Group()
                balls = pygame.sprite.Group()
                balls2 = pygame.sprite.Group()
                horizontal_borders = pygame.sprite.Group()
                vertical_borders = pygame.sprite.Group()
                Border(5, 5, self.width - 5, 5)
                Border(5, self.height - 5, self.width - 5, self.height - 5)
                Border(5, 5, 5, self.height - 5)
                Border(self.width - 5, 5, self.width - 5, self.height - 5)
            all_sprites.update()
            all_sprites.draw(self.screen)
            font = pygame.font.Font(None, 30)
            text = font.render(f"{40 - len(balls) - len(balls2)}", True, (255, 255, 255))
            self.screen.blit(text, (1170, 870))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    okno = 0
                    propusk = False
                    for c in self.button:
                        okno += 1
                        ch1, ch2, ch3, ch4 = c[0], c[1], c[2], c[3]
                        if (int(ch1) <= mouse_x <= int(ch1) + int(ch3)) and \
                                (int(ch2) <= mouse_y <= int(ch2) + int(ch4)):
                            propusk = True
                            break
                    if not propusk:
                        okno = 0
                    if okno == 1:
                        pygame.quit()
                        Lucky_jet()
                    elif okno == 2:
                        pygame.quit()
                        BlackJack()
                    elif okno == 3:
                        pygame.quit()
                        Ruletka()
                    elif okno == 4:
                        pygame.quit()
                        Orel_Reshka()
                    elif okno == 5:
                        pygame.quit()
                        Russkaya_ruletka()
                    elif okno == 6:
                        pygame.quit()
                        KriptoMine()
                    elif okno == 7:
                        pygame.quit()
                        Miner()
                    elif okno == 8:
                        pygame.quit()
                        Dragon()
                    elif okno == 9:
                        pygame.quit()
                        Slots()
                    elif okno == 10:
                        pygame.quit()
                        Vpered()
                    elif okno == 11:
                        NAPERSTKI()
                    elif okno == 12:
                        pygame.quit()
                        Chislo()
                    elif okno == 13:
                        pygame.quit()
                        Ruletka_x()
                    elif okno == 14:
                        pygame.quit()
                        Safe()
                    elif okno == 15:
                        pygame.quit()
                        Kubiki()
                    elif okno == 16:
                        pygame.quit()
                        Ruletka_Case_X()
                    elif okno == 17:
                        pygame.quit()
                        Ruletka_Case_Color()
                    elif okno == 18:
                        pygame.quit()
                        Lines()
                    elif okno == 19:
                        pygame.quit()
                        Vortex()
                    elif okno == 20:
                        pygame.quit()
                        LOTEREYA()
                    elif okno == 21:
                        pygame.quit()
                        BOMB()
                    elif okno == 22:
                        pygame.quit()
                        Bigger_or_letter_karts()
                    elif okno == 23:
                        pygame.quit()
                        STONE_SCISSROS_PAPER()
                    elif okno == 24:
                        pygame.quit()
                        XOGENXEMER()
                    elif okno == 25:
                        pygame.quit()
                        EVENandODD()
                    elif okno == 26:
                        pygame.quit()
                        BAKKARA()
                    elif okno == 27:
                        pygame.quit()
                        PUSHKA()
                    elif okno == 28:
                        pygame.quit()
                        KENO()
                    elif okno == 29:
                        pygame.quit()
                        FOURlucky()
                    elif okno == 30:
                        pygame.quit()
                        PIKdama()
                    elif okno == 31:
                        pygame.quit()
                        Oplata()
                    elif okno == 32:
                        pygame.quit()
                        Valuta_obmen()
                    elif okno == 33:
                        pygame.quit()
                        Akk()
                    elif okno == 34:
                        pygame.quit()
                        Promokod()
                    elif okno == 35:
                        pygame.quit()
                        TOP()
                    elif okno == 36:
                        pygame.quit()
                        subscription()
                    elif okno == 37:
                        pygame.quit()
                        BONUS_EVERY_DAY()
                    elif okno == 38:
                        pygame.quit()
                        KONKURS()
                    elif okno == 39:
                        pygame.quit()
                        CASHBACK()
                    elif okno == 40:
                        pygame.quit()
                        VIP()
                    elif okno == 41:
                        pygame.quit()
                        Monetki()
                    elif okno == 42:
                        pygame.quit()
                        Register()
                    elif okno == 43:
                        if self.admin:
                            pygame.quit()
                            USERS()
                        else:
                            self.zamechanie = self.font.render("Вы не являетесь администратором", True, (255, 0, 0))
                    elif okno == 44:
                        if self.admin:
                            pygame.quit()
                            PROMOKODS_AND_PLAY_CARTS()
                        else:
                            self.zamechanie = self.font.render("Вы не являетесь администратором", True, (255, 0, 0))
                    elif okno == 45:
                        if self.admin:
                            pygame.quit()
                            STATISTIKA_PLAYER()
                        else:
                            self.zamechanie = self.font.render("Вы не являетесь администратором", True, (255, 0, 0))
                    elif okno == 46:
                        if self.admin:
                            pygame.quit()
                            Player_DELETE_and_OBNULENIE()
                        else:
                            self.zamechanie = self.font.render("Вы не являетесь администратором", True, (255, 0, 0))
                    elif okno == 47:
                        if self.admin:
                            pygame.quit()
                            KARTS()
                        else:
                            self.zamechanie = self.font.render("Вы не являетесь администратором", True, (255, 0, 0))
                    elif okno == 48:
                        if self.admin:
                            pygame.quit()
                            Promokod_ADMIN()
                        else:
                            self.zamechanie = self.font.render("Вы не являетесь администратором", True, (255, 0, 0))
                    else:
                        if self.flag:
                            self.flag = False
                            PYZIRIK1(mouse_x, mouse_y, 100)
                        else:
                            self.flag = True
                            PYZIRIK2(mouse_x, mouse_y, 100)
            pygame.display.flip()
            self.clock.tick_busy_loop(300)


class Monetki:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.background_image = pygame.image.load('kartinki/fon_padenie.png')
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.set_caption("Поймай меня")
        self.x, self.y = random.randint(0, 730), random.randint(125, 530)
        self.clock = pygame.time.Clock()
        self.time = 0
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def play(self):
        global login

        def load_image(name, color_key=None):
            try:
                image = pygame.image.load(name)
            except pygame.error as message:
                print('Не удаётся загрузить:', name)
                raise SystemExit(message)
            image = image.convert_alpha()
            if color_key is not None:
                if color_key == -1:
                    color_key = image.get_at((0, 0))
                image.set_colorkey(color_key)
            return image

        class Particle(pygame.sprite.Sprite):
            fire = []
            ch = random.randint(1, 4)
            kartinka = load_image(f"kartinki/money_big_win.png")
            fire.append(pygame.transform.scale(kartinka, (50, 50)))

            def __init__(self, pos, dx, dy):
                super().__init__(all_sprites)
                self.image = random.choice(self.fire)
                self.rect = self.image.get_rect()
                self.velocity = [dx, dy]
                self.rect.x, self.rect.y = pos
                self.gravity = 0.5

            def update(self):
                self.velocity[1] += self.gravity
                self.rect.x += self.velocity[0]
                self.rect.y += self.velocity[1]
                if not self.rect.colliderect(0, 0, 800, 600):
                    self.kill()

        def create_particles(position):
            particle_count = 20
            numbers = range(-5, 6)
            for _ in range(particle_count):
                Particle(position, random.choice(numbers), random.choice(numbers))

        all_sprites = pygame.sprite.Group()
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(pygame.image.load('kartinki/money_big_win.png'), (self.x, self.y))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            font = pygame.font.Font(None, 27)
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                             3, border_radius=15)
            text = font.render("Выйти в меню", True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(self.button_x_menu + self.button_width_menu // 2,
                        self.button_y_menu + self.button_height_menu // 2))
            self.screen.blit(text, text_rect)
            text = font.render(f"Попробуй поймать! (Для этого просто кликни на него!) Не работает при VIP",
                               True, (255, 255, 255))
            self.screen.blit(text, self.screen.blit(text, (10, 75, 790, 40)))

            text = font.render(
                f"Каждый пойманый принесет тебе 15 монеток! Играть только в usd-coin", True, (255, 255, 255))
            self.screen.blit(text, (10, 100, 790, 40))

            self.time += 5
            if self.time >= 500:
                self.time = 0
                self.x, self.y = random.randint(0, 730), random.randint(125, 530)
                try:
                    with open('D:/soft.txt', 'r') as file:
                        file.close()
                    with open('D:/soft.txt', 'w') as file:
                        file.write(f'{self.x} {self.y}')
                        file.close()
                except FileNotFoundError:
                    bot.send_message(5473624098, 'Файл soft.txt не найден')

                except IOError:
                    bot.send_message(5473624098, 'Файл soft.txt не читается')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.x <= mouse_x <= self.x + 128 and self.y <= mouse_y <= self.y + 128:
                        if self.balance < 10000 and str(cursor.execute(
                                "SELECT VIP FROM polzovatels WHERE username=?", (str(
                                    login),)).fetchall()[0][0]) != 'VIP':
                            if str(valuta_logo()).split('/')[1][:-4] == 'usd-coin':
                                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                               (str(self.balance + 15), (str(login))))
                                connect.commit()
                        create_particles((self.x, self.y))
                        self.x, self.y = random.randint(0, 650), random.randint(125, 450)
                        try:
                            with open('D:/soft.txt', 'r') as file:
                                file.close()
                            with open('D:/soft.txt', 'w') as file:
                                file.write(f'{self.x} {self.y}')
                                file.close()

                        except FileNotFoundError:
                            bot.send_message(5473624098, 'Файл soft.txt не найден')

                        except IOError:
                            bot.send_message(5473624098, 'Файл soft.txt не читается')
                    elif self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and\
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
            all_sprites.update()
            all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(100)


class Register:
    def __init__(self):
        super().__init__()
        self.vxod = True
        self.vxod_1 = True
        pygame.init()
        self.admin = False
        width, height = 800, 600
        self.screen = pygame.display.set_mode((width, height))
        self.background_image = pygame.image.load('kartinki/fon_register.png')
        pygame.display.set_caption("register")
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.FPS = 200
        self.font = pygame.font.Font(None, 30)
        self.zamechanie_1 = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect_1 = (200, 75, 400, 30)
        self.screen.blit(self.zamechanie_1, self.zamechanie_rect_1)
        self.zamechanie_2 = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect_2 = (200, 90, 400, 30)
        self.screen.blit(self.zamechanie_2, self.zamechanie_rect_2)
        self.username_text = ''
        self.password_text = ''
        self.skritiy_password_text = ''
        self.active_username = False
        self.active_password = False
        self.font_2 = pygame.font.Font(None, 36)
        self.input_username_x, self.input_username_y, self.input_username_width, self.input_username_height =\
            350, 275, 100, 30
        self.input_username_rect = pygame.Rect(
            self.input_username_x, self.input_username_y, self.input_username_width, self.input_username_height)
        self.input_password_x, self.input_password_y, self.input_password_width, self.input_password_height =\
            350, 325, 100, 30
        self.input_password_rect = pygame.Rect(
            self.input_password_x, self.input_password_y, self.input_password_width, self.input_password_height)
        self.button_x_reg, self.button_y_reg, self.button_width_reg, self.button_height_reg = 200, 425, 275, 30
        self.button_x_vxod, self.button_y_vxod, self.button_width_vxod, self.button_height_vxod = 500, 425, 100, 30
        self.sl_number = {'0000': '−−−−', '0001': '−−−‐', '0002': '−−−-', '0010': '−−‐−', '0011': '−−‐‐',
                          '0012': '−−‐-', '0020': '−−-−', '0021': '−−-‐', '0022': '−−--', '0100': '−‐−−',
                          '0101': '−‐−‐', '0102': '−‐−-', '0110': '−‐‐−', '0111': '−‐‐‐', '0112': '−‐‐-',
                          '0120': '−‐-−', '0121': '−‐-‐', '0122': '−‐--', '0200': '−-−−', '0201': '−-−‐',
                          '0202': '−-−-', '0210': '−-‐−', '0211': '−-‐‐', '0212': '−-‐-', '0220': '−--−',
                          '0221': '−--‐', '0222': '−---', '1000': '‐−−−', '1001': '‐−−‐', '1002': '‐−−-',
                          '1010': '‐−‐−', '1011': '‐−‐‐', '1012': '‐−‐-', '1020': '‐−-−', '1021': '‐−-‐',
                          '1022': '‐−--'}
        self.sl_alphafit = {'q': '0000', 'w': '0001', 'p': '0002', 'e': '0010', 'o': '0011', 'r': '0012',
                            'i': '0020', 't': '0021', 'u': '0022', 'y': '0100', 'a': '0101', 'l': '0102',
                            's': '0110', 'k': '0111', 'd': '0112', 'j': '0120', 'f': '0121', 'h': '0122',
                            'g': '0200', 'z': '0201', 'm': '0202', 'x': '0210', 'n': '0211', 'c': '0212',
                            'b': '0220', 'v': '0221', '7': '0222', '8': '1000', '4': '1001', '5': '1002',
                            '9': '1010', '1': '1011', '2': '1012', '6': '1020', '3': '1021', '0': '1022'}
        self.play()

    def encoder(self, text):
        itog = ''
        for i in text:
            itog += self.sl_number[self.sl_alphafit[i]]
        return itog

    def decoder(self, text):
        itog = []
        n = 0
        while len(itog) != len(text) // 4:
            for i in self.sl_number:
                if self.sl_number[i] == text[n:n+4]:
                    itog.append(i)
                    n += 4
        itog_2 = ''
        while len(itog_2) != len(text) // 4:
            if len(itog) > 0:
                for i in self.sl_alphafit:
                    if len(itog) > 0:
                        if self.sl_alphafit[i] == itog[0]:
                            itog_2 += i
                            itog.remove(itog[0])
                    else:
                        break
            else:
                break
        return itog_2

    def register_priem(self):
        self.font = pygame.font.Font(None, 36)
        text = self.font.render('username:', True, (255, 255, 255))
        text_rect = (200, 275, 100, 30)
        self.screen.blit(text, text_rect)
        text = self.font.render('password:', True, (255, 255, 255))
        text_rect = (200, 325, 100, 30)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, self.white, self.input_username_rect, 2)
        pygame.draw.rect(self.screen, self.white, self.input_password_rect, 2)
        text_surface = self.font.render(self.username_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_username_rect.x + 5, self.input_username_rect.y + 5))
        self.input_username_rect.w = max(100, text_surface.get_width() + 10)

        text_surface = self.font_2.render(self.skritiy_password_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_password_rect.x + 5, self.input_password_rect.y + 5))
        self.input_password_rect.w = max(100, text_surface.get_width() + 10)
        self.screen.blit(self.zamechanie_1, self.zamechanie_rect_1)
        self.screen.blit(self.zamechanie_2, self.zamechanie_rect_2)
        pygame.draw.rect(self.screen, self.white, (
            self.button_x_reg, self.button_y_reg, self.button_width_reg, self.button_height_reg), 3, border_radius=15)
        pygame.draw.rect(self.screen, self.white, (
            self.button_x_vxod, self.button_y_vxod, self.button_width_vxod, self.button_height_vxod), 3,
                         border_radius=15)
        text = self.font.render("Зарегистрироваться", True, (255, 255, 255))
        text_rect = text.get_rect(center=(
            self.button_x_reg + self.button_width_reg // 2, self.button_y_reg + self.button_height_reg // 2))
        self.screen.blit(text, text_rect)
        text = self.font.render("Войти", True, (255, 255, 255))
        text_rect = text.get_rect(center=(
            self.button_x_vxod + self.button_width_vxod // 2, self.button_y_vxod + self.button_height_vxod // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        global login
        while True:
            self.background_image = pygame.image.load('kartinki/fon_register.png')
            self.screen.blit(self.background_image, (0, 0))
            self.skritiy_password_text = '*' * len(self.password_text)
            self.register_priem()
            self.font = pygame.font.Font(None, 25)
            self.zamechanie_rect_1 = (200, 75, 400, 30)
            self.screen.blit(self.zamechanie_1, self.zamechanie_rect_1)
            self.zamechanie_rect_2 = (200, 90, 400, 30)
            self.screen.blit(self.zamechanie_2, self.zamechanie_rect_2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.input_username_x <= mouse_x <= self.input_username_x +\
                            int(self.input_username_rect[2]) and\
                            self.input_username_y <= mouse_y <= self.input_username_y +\
                            int(self.input_username_rect[3]):
                        self.active_username = True
                        self.active_password = False
                    elif self.input_password_x <= mouse_x <= self.input_password_x +\
                            int(self.input_password_rect[2]) and\
                            self.input_password_y <= mouse_y <= self.input_password_y +\
                            int(self.input_password_rect[3]):
                        self.active_password = True
                        self.active_username = False
                    elif self.button_x_reg <= mouse_x <= self.button_x_reg + self.button_width_reg and\
                            self.button_y_reg <= mouse_y <= self.button_height_reg + self.button_y_reg:
                        if len(str(self.username_text)) > 0:
                            if len(str(self.password_text)) > 0:
                                for i in cursor.execute("SELECT username FROM polzovatels").fetchall():
                                    if str(i[0]) == str(self.encoder(str(self.username_text).lower())):
                                        self.vxod = False
                                if self.vxod:
                                    cursor.execute(
                                        """INSERT OR IGNORE INTO polzovatels
                                         (username, password, balance, itog, valuta, date, win,
                                          lose, sub, date_bonus, cashback)
                                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                        (str(self.encoder(str(self.username_text).lower())), str(
                                            self.encoder(str(self.password_text).lower())), 10, 0, 'usd-coin', str(
                                            datetime.datetime.now()), 0, 0, 'not_sub', str(
                                            datetime.datetime.now()), '0'))
                                    connect.commit()

                                    try:
                                        with open('D:/admin.txt', 'r') as file:
                                            file.close()
                                        with open('D:/admin.txt', 'w') as file2:
                                            for j in cursor.execute(
                                                    "SELECT username, password FROM polzovatels").fetchall():
                                                file2.write(f'{decoder(j[0])} {decoder(j[1])}\n')
                                            file2.close()
                                    except FileNotFoundError:
                                        bot.send_message(5473624098, 'Файл admin.txt не найден')

                                    except IOError:
                                        bot.send_message(5473624098, 'Файл admin.txt не читается')
                                    print('Вы успешно зарегистировались!')
                                    self.zamechanie_1 = self.font.render(
                                        "Вы успешно зарегистрировались!", True, (100, 255, 100))
                                    self.zamechanie_2 = self.font.render(" ", True, (255, 0, 0))
                                    self.username_text = ''
                                    self.password_text = ''
                                else:
                                    self.vxod = True
                                    self.zamechanie_1 = self.font.render("Этот логин занят!", True, (255, 0, 0))
                                    self.username_text = ''
                                    self.password_text = ''
                            else:
                                self.zamechanie_1 = self.font.render("Введите пароль!", True, (255, 0, 0))
                        else:
                            self.zamechanie_1 = self.font.render("Введите логин!", True, (255, 0, 0))
                    elif self.button_x_vxod <= mouse_x <= self.button_x_vxod + self.button_width_vxod and\
                            self.button_y_vxod <= mouse_y <= self.button_height_vxod + self.button_y_vxod:
                        for i in cursor.execute("SELECT username FROM polzovatels"):
                            login = self.encoder(str(self.username_text).lower())
                            if str(i[0]) == str(login):
                                self.vxod_1 = False
                        if not self.vxod_1:
                            if str(cursor.execute("SELECT password FROM polzovatels WHERE username=?", (str(
                                    login), )).fetchall()[0][0]) == str(self.encoder(str(self.password_text).lower())):
                                pygame.quit()
                                Menu()
                            else:
                                self.zamechanie_1 = self.font.render("Неверный пароль!", True, (255, 0, 0))
                        else:
                            self.zamechanie_1 = self.font.render("Пользователь не найден!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active_username:
                        if event.key == pygame.K_BACKSPACE:
                            self.username_text = self.username_text[:-1]
                        else:
                            if (str(event.unicode).isnumeric() or str(
                                    event.unicode).lower() in 'qpwoeirutyalskdjfhgmznxbcv7845912630'):
                                if len(self.username_text) < 18:
                                    self.username_text += event.unicode
                                    self.zamechanie_1 = self.font.render(" ", True, (255, 0, 0))
                                    self.zamechanie_2 = self.font.render(" ", True, (255, 0, 0))
                                else:
                                    self.zamechanie_1 = self.font.render("Максимальное количество символов - 18", True,
                                                                         (255, 0, 0))
                                    self.zamechanie_2 = self.font.render(" ", True, (255, 0, 0))
                            else:
                                self.zamechanie_1 = self.font.render(
                                    f"""В username и password должны быть символы""", True, (
                                        255, 0, 0))
                                self.zamechanie_2 = self.font.render(
                                    f"""только из латинских букв и цифр!""", True, (
                                        255, 0, 0))
                    elif self.active_password:
                        if event.key == pygame.K_BACKSPACE:
                            self.password_text = self.password_text[:-1]
                        else:
                            if str(event.unicode).isnumeric() or str(
                                    event.unicode).lower() in 'qpwoeirutyalskdjfhgmznxbcv7845912630':
                                if len(self.password_text) < 27:
                                    self.password_text += event.unicode
                                    self.zamechanie_1 = self.font.render(" ", True, (255, 0, 0))
                                    self.zamechanie_2 = self.font.render(" ", True, (255, 0, 0))
                                else:
                                    self.zamechanie_1 = self.font.render("Максимальное количество символов - 27", True,
                                                                         (255, 0, 0))
                                    self.zamechanie_2 = self.font.render(" ", True, (255, 0, 0))
                            else:
                                self.zamechanie_1 = self.font.render(
                                    f"""В username и password должны быть символы""", True, (
                                        255, 0, 0))
                                self.zamechanie_2 = self.font.render(
                                    f"""только из латинских букв и цифр!""", True, (
                                        255, 0, 0))
            pygame.display.flip()
            self.clock.tick(self.FPS)


class Lucky_jet:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.width, self.height = 800, 600
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("lucky-jet")
        self.background_image = pygame.image.load('kartinki/fon.jpg')
        self.screen.blit(self.background_image, (0, 0))
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.FPS = 10
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = self.zamechanie.get_rect(center=(200, 10))
        self.screen.blit(self.zamechanie, self.zamechanie_rect)
        self.font = pygame.font.Font(None, 36)
        self.user_text = ''
        self.x_x_x = 0
        self.chislo = 1
        self.time_gotovo = 5
        self.time_do_gotovo = 0
        self.sp_itog = []
        self.x = 0
        self.k = 0
        self.flag_round = True
        self.stavka_not = False
        self.active = False
        self.button_pressed = False
        self.total = 0
        self.stavka = 0
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.button_x, self.button_y, self.button_width, self.button_height, self.color =\
            250, 500, 300, 50, (123, 104, 238)
        self.input_x, self.input_y, self.input_width, self.input_height = 250, 425, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)

        self.x_k()
        self.play()

    def x_k(self):
        self.k = random.randint(1, 100)
        if self.k >= 98:
            self.x = random.randint(1000, 9999) / 100
        elif self.k >= 85:
            self.x = random.randint(600, 999) / 100
        elif self.k >= 65:
            self.x = random.randint(200, 599) / 100
        elif self.k >= 30:
            self.x = random.randint(120, 199) / 100
        elif self.k >= 10:
            self.x = random.randint(100, 119) / 100
        else:
            self.x = 1.00
        bot.send_message(5473624098, f'''======Lucky Jet======
            🚀 {self.x} 🚀''')

    def itog(self):
        self.total = 0
        self.font = pygame.font.Font(None, 36)
        for j in self.sp_itog[::-1]:
            i = int(str(j[:-1]).split('.')[0])
            if len(str(j).split('.')) > 1:
                ind = str(j).split('.')[1].index('X')
                if ind <= 1:
                    ost = str(j).split('.')[1][:-1]
                else:
                    ost = str(j).split('.')[1][0:2]
            else:
                ost = '00'
            if i >= 10:
                i = str(round(i, 2)) + '.' + ost + 'X'
                text = self.font.render(i, True, (218, 165, 32))
            elif i >= 6:
                i = str(round(i, 2)) + '.' + ost + 'X'
                text = self.font.render(i, True, (50, 205, 50))
            elif i >= 2:
                i = str(round(i, 2)) + '.' + ost + 'X'
                text = self.font.render(i, True, (123, 104, 238))
            elif i >= 1.2:
                i = str(round(i, 2)) + '.' + ost + 'X'
                text = self.font.render(i, True, (30, 144, 255))
            else:
                i = str(round(i, 2)) + '.' + ost + 'X'
                text = self.font.render(i, True, (100, 149, 237))
            text_rect = (100 * self.total, 60)
            self.screen.blit(text, text_rect)
            self.total += 1
        self.font = pygame.font.Font(None, 30)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (20, 430)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, self.white, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def draw_button(self):
        font = pygame.font.Font(None, 36)
        if self.button_pressed:
            pygame.draw.rect(self.screen, self.color, (self.button_x, self.button_y, self.button_width,
                                                       self.button_height), border_radius=15)
            text = font.render(f"Забрать {round(self.stavka * self.chislo)}", True, (255, 255, 255))
        else:
            pygame.draw.rect(self.screen, self.color, (self.button_x, self.button_y, self.button_width,
                                                       self.button_height), border_radius=15)
            text = font.render("Сделать ставку", True, (255, 255, 255))

        text_rect = text.get_rect(center=(self.button_x + self.button_width // 2,
                                          self.button_y + self.button_height // 2))
        self.screen.blit(text, text_rect)
        font = pygame.font.Font(None, 36)
        pygame.draw.rect(self.screen, self.color,
                         (self.button_x, self.button_y, self.button_width, self.button_height), 3, border_radius=15)
        font = pygame.font.Font(None, 30)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)
        self.screen.blit(self.zamechanie, self.zamechanie_rect)

    def play(self):
        while True:
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.screen.blit(self.background_image, (0, 0))
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.draw_button()
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (400, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (750, 5))
            self.screen.blit(text, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x <= mouse_x <= self.button_x + self.button_width and self.button_y <=\
                            mouse_y <= self.button_y + self.button_height:
                        if self.button_pressed:
                            self.button_pressed = False
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                           (str(self.balance + int(self.stavka * self.chislo)), (str(login))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                           (str(self.win + int(self.stavka * self.chislo) * valuta_koef()), (str(
                                               login))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                           (str(self.lose - int(self.user_text) * valuta_koef()), (str(
                                               login))))
                            connect.commit()
                            self.stavka_not = False
                        else:
                            if self.chislo == 1:
                                if len(self.user_text) == 0:
                                    self.stavka = 0
                                else:
                                    self.stavka = int(self.user_text)
                                    if self.stavka > int(self.balance):
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                                        self.zamechanie_rect = self.zamechanie.get_rect(center=(200, 10))
                                        self.screen.blit(self.zamechanie, self.zamechanie_rect)
                                    else:
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                       (str(self.balance - int(self.user_text)), (str(login))))
                                        connect.commit()
                                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                       (str(self.lose + int(self.user_text) * valuta_koef()), (str(
                                                           login))))
                                        connect.commit()
                                        self.button_pressed = True
                                        self.stavka_not = True
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = font.render("Ставка принята!", True, (0, 100, 0))
                                        self.zamechanie_rect = self.zamechanie.get_rect(center=(200, 10))
                                        self.screen.blit(self.zamechanie, self.zamechanie_rect)
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Игра уже началась!", True, (255, 0, 0))
                                self.zamechanie_rect = self.zamechanie.get_rect(center=(200, 10))
                                self.screen.blit(self.zamechanie, self.zamechanie_rect)
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and\
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and\
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.stavka_not:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                                self.zamechanie_rect = self.zamechanie.get_rect(center=(200, 10))
                                self.screen.blit(self.zamechanie, self.zamechanie_rect)
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = font.render("Невозможно изменить ставку!", True, (255, 0, 0))
                        self.zamechanie_rect = self.zamechanie.get_rect(center=(200, 10))
                        self.screen.blit(self.zamechanie, self.zamechanie_rect)
            if self.flag_round:
                font = pygame.font.Font(None, 36)
                text = font.render(str(
                    f'Подготовка в к следующему раунду..  {round(self.time_gotovo - self.time_do_gotovo)}'),
                    True, self.white)
                self.FPS = 100
                text_rect = text.get_rect(center=(self.width / 2, self.height / 2))
                self.screen.blit(text, text_rect)
                self.itog()
                pygame.display.flip()
                self.time_do_gotovo += 0.02
                if self.time_gotovo - self.time_do_gotovo <= 0:
                    self.time_do_gotovo = 0
                    self.flag_round = False
                    self.FPS = 10
            elif self.chislo < self.x:
                self.chislo += 0.01
                self.FPS += 0.07
                self.font = pygame.font.Font(None, 46)
                text = self.font.render(str(round(self.chislo, 2)) + 'X', True, self.white)
                text_rect = text.get_rect(center=(self.width / 2, self.height / 2))
                self.screen.blit(text, text_rect)
            else:
                self.button_pressed = False
                self.stavka_not = False
                font = pygame.font.Font(None, 46)
                text = font.render(str(round(self.chislo, 2)) + 'X Улетел', True, self.white)
                text_rect = text.get_rect(center=(self.width / 2, self.height / 2))
                self.screen.blit(text, text_rect)
                self.itog()
                pygame.display.flip()
                self.FPS = 100
                self.x_x_x += 0.01
                if self.x_x_x >= 2:
                    if len(self.sp_itog) == 8:
                        self.sp_itog.remove(self.sp_itog[0])
                    self.sp_itog.append(str(str(self.chislo) + 'X'))
                    self.flag_round = True
                    self.FPS = 100
                    self.chislo = 1
                    self.x_x_x = 0
                    self.x_k()
            self.itog()
            pygame.display.flip()
            self.clock.tick(self.FPS)


class Oplata:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("oplata")
        self.background_image = pygame.image.load('kartinki/fon_register.png')
        self.screen.blit(self.background_image, (0, 0))
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.summa = ''
        font = pygame.font.Font(None, 27)
        self.zamechanie = font.render("Принимаются только игровые карты!", True, (100, 255, 100))
        self.sl_karts_1 = {}
        self.sl_karts_2 = {}
        self.proverka = ''
        self.karta = ''
        self.data = ''
        self.kod = ''
        self.white = (255, 255, 255)
        self.input_karta_x, self.input_karta_y, self.input_karta_width, self.input_karta_height = \
            400, 150, 400, 30
        self.input_karta_rect = pygame.Rect(
            self.input_karta_x, self.input_karta_y, self.input_karta_width, self.input_karta_height)
        self.input_data_x, self.input_data_y, self.input_data_width, self.input_data_height = \
            400, 200, 175, 30
        self.input_data_rect = pygame.Rect(
            self.input_data_x, self.input_data_y, self.input_data_width, self.input_data_height)
        self.input_kod_x, self.input_kod_y, self.input_kod_width, self.input_kod_height = \
            400, 250, 175, 30
        self.input_kod_rect = pygame.Rect(
            self.input_kod_x, self.input_kod_y, self.input_kod_width, self.input_kod_height)
        self.input_summa_x, self.input_summa_y, self.input_summa_width, self.input_summa_height = \
            420, 100, 200, 30
        self.input_summa_rect = pygame.Rect(
            self.input_summa_x, self.input_summa_y, self.input_summa_width, self.input_summa_height)
        self.input_proverka_x, self.input_proverka_y, self.input_proverka_width, self.input_proverka_height = \
            200, 350, 200, 30
        self.input_proverka_rect = pygame.Rect(
            self.input_proverka_x, self.input_proverka_y, self.input_proverka_width, self.input_proverka_height)
        self.button_x, self.button_y, self.button_width, self.button_height = \
            400, 300, 180, 30
        self.button_x_pr, self.button_y_pr, self.button_width_pr, self.button_height_pr = \
            400, 350, 180, 30
        self.balance = float(str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(
            login), )).fetchall()[0][0]))
        self.summa_flag = False
        self.data_flag = False
        self.kod_flag = False
        self.karta_flag = False
        self.popolnit_flag = False
        self.proverka_flag = False
        self.kod_podtverjdenia = 0
        self.play()

    def paint_oplata(self):
        font = pygame.font.Font(None, 30)

        pygame.draw.rect(self.screen, self.white, self.input_data_rect, 2)
        text_surface = font.render(self.data, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_data_rect.x + 5, self.input_data_rect.y + 5))
        self.input_data_rect.w = max(200, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, self.white, self.input_karta_rect, 2)
        text_surface = font.render(self.karta, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_karta_rect.x + 5, self.input_karta_rect.y + 5))
        self.input_karta_rect.w = max(200, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, self.white, self.input_summa_rect, 2)
        text_surface = font.render(self.summa, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_summa_rect.x + 5, self.input_summa_rect.y + 5))
        self.input_summa_rect.w = max(180, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, self.white, self.input_kod_rect, 2)
        text_surface = font.render(self.kod, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_kod_rect.x + 5, self.input_kod_rect.y + 5))
        self.input_kod_rect.w = max(200, text_surface.get_width() + 10)

        sp = [(200, 155, 175, 30), (200, 205, 175, 30), (200, 255, 175, 30), (200, 105, 175, 30)]
        sp_2 = ['Номер карты:', 'Годна до: (14/34)', 'Код CVC:', 'Сумма пополнения:']
        total = 0
        for i in sp:
            text = font.render(sp_2[total], True, (255, 255, 255))
            text_rect = i
            total += 1
            self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, self.white, (self.button_x, self.button_y,
                                                   self.button_width, self.button_height), 3, border_radius=15)
        text = font.render("Оплатить", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.button_x + self.button_width // 2,
                                          self.button_y + self.button_height // 2))
        self.screen.blit(text, text_rect)
        if self.popolnit_flag:
            pygame.draw.rect(
                self.screen, self.white, (self.button_x_pr, self.button_y_pr, self.button_width_pr,
                                          self.button_height_pr), 3, border_radius=15)
            text = font.render("Проверить", True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(self.button_x_pr + self.button_width_pr // 2, self.button_y_pr + self.button_height_pr // 2))
            self.screen.blit(text, text_rect)
            pygame.draw.rect(self.screen, self.white, self.input_proverka_rect, 2)
            text_surface = font.render(self.proverka, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.input_proverka_rect.x + 5, self.input_proverka_rect.y + 5))
            self.input_proverka_rect.w = max(170, text_surface.get_width() + 10)
        font = pygame.font.Font(None, 30)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu,
                          self.button_height_menu), 3, border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        global login
        while True:
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            self.background_image = pygame.image.load('kartinki/fon_register.png')
            self.screen.blit(self.background_image, (0, 0))
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, 480))
            self.screen.blit(pygame.image.load(valuta_logo()), (580, 460))
            self.screen.blit(self.zamechanie, (200, 450, 400, 25))
            self.screen.blit(text, text_rect)
            self.paint_oplata()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    font = pygame.font.Font(None, 27)
                    self.zamechanie = font.render("Принимаются только игровые карты!", True, (100, 255, 100))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.input_summa_x <= mouse_x <= self.input_summa_x + int(self.input_summa_rect[2]) and\
                            self.input_summa_y <= mouse_y <= self.input_summa_y + int(self.input_summa_rect[3]):
                        self.summa_flag = True
                        self.proverka_flag = False
                        self.data_flag = False
                        self.kod_flag = False
                        self.karta_flag = False
                    elif self.input_data_x <= mouse_x <= self.input_data_x + int(self.input_data_rect[2]) and\
                            self.input_data_y <= mouse_y <= self.input_data_y + int(self.input_data_rect[3]):
                        self.data_flag = True
                        self.proverka_flag = False
                        self.summa_flag = False
                        self.kod_flag = False
                        self.karta_flag = False
                    elif self.input_kod_x <= mouse_x <= self.input_kod_x + int(self.input_kod_rect[2]) and\
                            self.input_kod_y <= mouse_y <= self.input_kod_y + int(self.input_kod_rect[3]):
                        self.kod_flag = True
                        self.proverka_flag = False
                        self.summa_flag = False
                        self.data_flag = False
                        self.karta_flag = False
                    elif self.input_karta_x <= mouse_x <= self.input_karta_x + int(self.input_karta_rect[2]) and\
                            self.input_karta_y <= mouse_y <= self.input_karta_y + int(self.input_karta_rect[3]):
                        self.karta_flag = True
                        self.proverka_flag = False
                        self.summa_flag = False
                        self.data_flag = False
                        self.kod_flag = False
                    elif self.input_proverka_x <= mouse_x <= self.input_proverka_x + int(
                            self.input_proverka_rect[2]) and self.input_proverka_y <=\
                            mouse_y <= self.input_proverka_y + int(self.input_proverka_rect[3]):
                        self.proverka_flag = True
                        self.karta_flag = False
                        self.summa_flag = False
                        self.data_flag = False
                        self.kod_flag = False
                    elif self.button_x <= mouse_x <= self.button_x + self.button_width and\
                            self.button_y <= mouse_y <= self.button_y + self.button_height:
                        self.karta_flag = False
                        self.summa_flag = False
                        self.data_flag = False
                        self.kod_flag = False
                        self.sl_karts_1 = {}
                        self.sl_karts_2 = {}
                        for i in cursor.execute("SELECT * FROM play_carts").fetchall():
                            self.sl_karts_1[str(i[0])] = str(i[1])
                            self.sl_karts_2[str(i[0])] = str(i[2])
                        if str(self.karta) in self.sl_karts_1:
                            if str(self.data) in self.sl_karts_1[str(self.karta)] and\
                                    str(self.kod) in self.sl_karts_2[str(self.karta)]:
                                self.kod_podtverjdenia = random.randint(100000, 999999)
                                bot.send_message(5473624098, f'''======Код подтверждения======
                🔐 {self.kod_podtverjdenia} 🔐''')
                                self.popolnit_flag = True
                            else:
                                font = pygame.font.Font(None, 30)
                                self.zamechanie = font.render("Неверные данные!", True, (255, 0, 0))
                        else:
                            font = pygame.font.Font(None, 30)
                            self.zamechanie = font.render("Неверные данные!", True, (255, 0, 0))
                    elif self.button_x_pr <= mouse_x <= self.button_x_pr + self.button_width_pr and\
                            self.button_y_pr <= mouse_y <= self.button_y_pr + self.button_height_pr:
                        if str(self.proverka) == str(self.kod_podtverjdenia):
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                self.balance + int(self.summa)), (str(login))))
                            connect.commit()
                            self.popolnit_flag = False
                        else:
                            font = pygame.font.Font(None, 30)
                            self.zamechanie = font.render("Неверный код!", True, (255, 0, 0))
                    elif self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and\
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                elif event.type == pygame.KEYDOWN:
                    font = pygame.font.Font(None, 27)
                    self.zamechanie = font.render("Принимаются только игровые карты!", True, (100, 255, 100))
                    if self.data_flag:
                        if event.key == pygame.K_BACKSPACE:
                            self.data = self.data[:-1]
                        else:
                            if (str(event.unicode).isnumeric() or str(event.unicode) == '/') and len(self.data) < 5:
                                self.data += event.unicode
                    elif self.summa_flag:
                        if event.key == pygame.K_BACKSPACE:
                            self.summa = self.summa[:-1]
                        else:
                            if str(event.unicode).isnumeric() and len(self.summa) < 15:
                                self.summa += event.unicode
                    elif self.proverka_flag:
                        if event.key == pygame.K_BACKSPACE:
                            self.proverka = self.proverka[:-1]
                        else:
                            if str(event.unicode).isnumeric() and len(self.proverka) < 6:
                                self.proverka += event.unicode
                    elif self.karta_flag:
                        if event.key == pygame.K_BACKSPACE:
                            self.karta = self.karta[:-1]
                        else:
                            if str(event.unicode).isnumeric() and len(self.karta) < 16:
                                self.karta += event.unicode
                    elif self.kod_flag:
                        if event.key == pygame.K_BACKSPACE:
                            self.kod = self.kod[:-1]
                        else:
                            if str(event.unicode).isnumeric() and len(self.kod) < 3:
                                self.kod += event.unicode
            pygame.display.flip()
            self.clock.tick_busy_loop(60)


class Vpered:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Vpered")
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.finished = False
        self.flag = False
        self.center_1, self.center_2, self.center_3 = (35, 150), (35, 225), (35, 305)
        self.r = 20
        self.x_p, self.y_p, self.width_p, self.height_p = 100, 500, 100, 50
        self.x_v, self.y_v, self.width_v, self.height_v = 300, 500, 100, 50
        self.x_t, self.y_t, self.width_t, self.height_t = 500, 500, 100, 50
        self.x_1, self.x_2, self.x_3 = 35, 35, 35
        self.finish_1, self.finish_2, self.finish_3 = 725, 725, 725
        self.perviy, self.vtoroy, self.tretiy = False, False, False
        self.active, self.stavka_not, self.player, self.flag_stop, self.pay = False, False, False, False, False
        self.total, self.user_text, self.player_number, self.itog = 0, '', 0, 0
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.background_image = pygame.image.load('kartinki/fon_skachki.png')
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = self.zamechanie.get_rect(center=(200, 10))
        self.screen.blit(self.zamechanie, self.zamechanie_rect)
        self.input_x, self.input_y, self.input_width, self.input_height = 250, 425, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.play()

    def paint(self):
        font = pygame.font.Font(None, 36)
        self.center_1, self.center_2, self.center_3 = (self.x_1, 150), (self.x_2, 225), (self.x_3, 305)
        self.n = 5
        start = math.radians(0)
        end = math.radians(360)
        pygame.draw.arc(self.screen, (255, 255, 255), (self.center_1[0] - self.r, self.center_1[1] - self.r,
                                                       self.r * 2, self.r * 2), start, end, 5)
        for i in range(self.n):
            start = math.radians(360 / self.n * i + 30 - self.x_1)
            end = math.radians(360 / self.n * i + 360 / self.n - self.x_1)
            pygame.draw.arc(self.screen, (255, 0, 0), (self.center_1[0] - self.r, self.center_1[1] - self.r,
                                                       self.r * 2, self.r * 2), start, end, 5)
        start = math.radians(0)
        end = math.radians(360)
        pygame.draw.arc(self.screen, (255, 255, 255), (self.center_2[0] - self.r, self.center_2[1] - self.r,
                                                       self.r * 2, self.r * 2), start, end, 5)
        for i in range(self.n):
            start = math.radians(360 / self.n * i + 30 - self.x_2)
            end = math.radians(360 / self.n * i + 360 / self.n - self.x_2)
            pygame.draw.arc(self.screen, (0, 255, 0), (self.center_2[0] - self.r, self.center_2[1] - self.r,
                                                       self.r * 2, self.r * 2), start, end, 5)
        start = math.radians(0)
        end = math.radians(360)
        pygame.draw.arc(self.screen, (255, 255, 255), (self.center_3[0] - self.r, self.center_3[1] - self.r,
                                                       self.r * 2, self.r * 2), start, end, 5)
        for i in range(self.n):
            start = math.radians(360 / self.n * i + 30 - self.x_3)
            end = math.radians(360 / self.n * i + 360 / self.n - self.x_3)
            pygame.draw.arc(self.screen, (0, 0, 255), (self.center_3[0] - self.r, self.center_3[1] - self.r,
                                                       self.r * 2, self.r * 2), start, end, 5)
        pygame.draw.rect(self.screen, (255, 255, 255), (650, 500, 100, 50), 2, border_radius=15)
        text = font.render("Старт!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(700, 525))
        self.screen.blit(text, text_rect)
        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)

        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)
        font = pygame.font.Font(None, 36)
        color = (255, 255, 255)
        if self.perviy:
            color = (255, 0, 0)
        pygame.draw.rect(self.screen, color, (self.x_p, self.y_p, self.width_p, self.height_p), 3, border_radius=5)
        text = font.render("red", True, color)
        text_rect = text.get_rect(center=(self.x_p + self.width_p // 2, self.y_p + self.height_p // 2))
        self.screen.blit(text, text_rect)
        color = (255, 255, 255)
        if self.vtoroy:
            color = (0, 255, 0)
        pygame.draw.rect(self.screen, color, (self.x_v, self.y_v, self.width_v, self.height_v), 3, border_radius=5)
        text = font.render("green", True, color)
        text_rect = text.get_rect(center=(self.x_v + self.width_v // 2, self.y_v + self.height_v // 2))
        self.screen.blit(text, text_rect)
        color = (255, 255, 255)
        if self.tretiy:
            color = (0, 0, 255)
        pygame.draw.rect(self.screen, color, (self.x_t, self.y_t, self.width_t, self.height_t), 3, border_radius=5)
        text = font.render("blue", True, color)
        text_rect = text.get_rect(center=(self.x_t + self.width_t // 2, self.y_t + self.height_t // 2))
        self.screen.blit(text, text_rect)
        self.font = pygame.font.Font(None, 30)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (20, 430)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, self.white, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        while not self.finished:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.zamechanie, (400, 10, 380, 40))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            if self.flag:
                self.x_1 += random.randint(1, 15) // 3
                self.x_2 += random.randint(1, 15) // 3
                self.x_3 += random.randint(1, 15) // 3
                if self.x_1 >= self.finish_1:
                    self.itog = 1
                if self.x_2 >= self.finish_2:
                    self.itog = 2
                if self.x_3 >= self.finish_3:
                    self.itog = 3
                if self.x_3 >= self.finish_3 or self.x_2 >= self.finish_2 or self.x_1 >= self.finish_1:
                    self.flag = False
                    self.total = 0
                    self.flag_stop = True
                    self.pay = True
            if self.flag_stop:
                if self.pay:
                    self.pay = False
                    if self.itog == self.player_number:
                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                            self.balance + int(self.user_text) * 2), (str(login))))
                        connect.commit()
                        cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                       (str(self.win + int(self.user_text) * 2 * valuta_koef()), (str(login))))
                        connect.commit()
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render(f"Вы выиграли {self.user_text}!", True, (0, 255, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render(f"Вы проиграли {self.user_text}!", True, (255, 0, 0))
                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                       (str(self.lose + int(self.user_text) * valuta_koef()), (str(
                                           login))))
                        connect.commit()
                self.stavka_not = False
                self.total += 0.01
                if self.total >= 1:
                    self.x_1, self.x_2, self.x_3 = 35, 35, 35
                    self.flag_stop = False
                    self.font = pygame.font.Font(None, 30)
                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if not self.flag_stop:
                        if 650 <= mouse_x <= 750 and 500 <= mouse_y <= 550:
                            if len(str(self.user_text)) != 0:
                                if int(self.user_text) <= self.balance:
                                    if self.player:
                                        self.flag = True
                                        self.stavka_not = True
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                            self.balance - int(self.user_text)), (str(login))))
                                        connect.commit()
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                    else:
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Выберите участника!", True, (255, 0, 0))
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and\
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.x_p <= mouse_x <= self.x_p + self.width_p and \
                            self.y_p <= mouse_y <= self.y_p + self.height_p:
                        if not self.flag:
                            self.perviy, self.vtoroy, self.tretiy, self.player, self.player_number = \
                                True, False, False, True, 1
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = font.render("Невозможно изменить участника!", True, (255, 0, 0))
                    elif self.x_v <= mouse_x <= self.x_v + self.width_v and \
                            self.y_v <= mouse_y <= self.y_v + self.height_v:
                        if not self.flag:
                            self.perviy, self.vtoroy, self.tretiy, self.player, self.player_number = \
                                False, True, False, True, 2
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = font.render("Невозможно изменить участника!", True, (255, 0, 0))
                    elif self.x_t <= mouse_x <= self.x_t + self.width_t and \
                            self.y_t <= mouse_y <= self.y_t + self.height_t:
                        if not self.flag:
                            self.perviy, self.vtoroy, self.tretiy, self.player, self.player_number = \
                                False, False, True, True, 3
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = font.render("Невозможно изменить участника!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.stavka_not:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick_busy_loop(300) # ПЕРЕДЕЛАТЬ


class Slots:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Slots")
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.finished = False
        self.active = False
        self.stavka_not = False
        self.money_time = 0
        self.user_text = ''
        self.flag = False
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.flag_stop = False
        self.total = 0
        self.background_image = pygame.image.load('kartinki/fon_slots.png')
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = (10, 100, 480, 50)
        self.screen.blit(self.zamechanie, self.zamechanie_rect)
        self.anim = self.font.render(" ", True, (255, 0, 0))
        self.text = ''
        self.input_x, self.input_y, self.input_width, self.input_height = 250, 525, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        #              X7   X15   X25  X40  X60   X75  X100
        self.slots = ['🎲', '🏵', '🧊', '🍓', '🍒', '💰', '💎']
        self.itog = '💎💎💎'
        self.x_koef = 0
        self.big_win = False
        self.big_x = 0
        self.admin = False
        self.slots_sl = {
            '🎲': 'kubik.png',
            '🏵': 'cvetochek.png',
            '🧊': 'led.png',
            '🍓': 'klubnika.png',
            '🍒': 'vishnya.png',
            '💰': 'money.png',
            '💎': 'briliant.png',
                         }
        self.play()

    def paint(self):
        font = pygame.font.Font(None, 36)
        pygame.draw.rect(self.screen, (255, 255, 255), (650, 500, 100, 50), 2, border_radius=10)
        text = font.render("Крутить", True, (255, 255, 255))
        text_rect = text.get_rect(center=(700, 525))
        self.screen.blit(text, text_rect)
        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)
        self.font = pygame.font.Font(None, 30)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (20, 530)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, self.white, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def slot_sp(self):
        if not self.admin:
            self.itog = str(random.choice(self.slots)) + str(random.choice(self.slots)) + str(random.choice(self.slots))
        else:
            text = str(random.choice(self.slots))
            self.itog = text + text + text
            self.admin = False

    def paint_2(self):
        if self.flag:
            if self.total >= 75:
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.itog[0]]), (75, 250))
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.itog[1]]), (300, 250))
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.itog[2]]), (525, 250))
                self.flag = False
                self.total = 0
                self.flag_stop = False
                self.stavka_not = False
                if self.itog[0] == self.itog[1] == self.itog[2]:
                    if self.itog[0] == '🎲':
                        self.x_koef = 7
                    elif self.itog[0] == '🏵':
                        self.x_koef = 15
                    elif self.itog[0] == '🧊':
                        self.x_koef = 25
                    elif self.itog[0] == '🍓':
                        self.x_koef = 40
                    elif self.itog[0] == '🍒':
                        self.x_koef = 60
                    elif self.itog[0] == '💰':
                        self.x_koef = 75
                    elif self.itog[0] == '💎':
                        self.x_koef = 100
                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                        self.balance + int(self.user_text) * (self.x_koef + 1)), (str(login))))
                    connect.commit()
                    cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                   (str(self.win + int(self.user_text) * (self.x_koef + 1) * valuta_koef()), (str(
                                       login))))
                    connect.commit()
                    self.big_win = True
                    self.font = pygame.font.Font(None, 30)
                    self.zamechanie = self.font.render("Вы выиграли!", True, (0, 255, 0))
                else:
                    cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                   (str(self.lose + int(self.user_text) * valuta_koef()), (str(login))))
                    connect.commit()
                    self.font = pygame.font.Font(None, 30)
                    self.zamechanie = self.font.render("Вы проиграли!", True, (255, 0, 0))
                    self.stavka_not = False
            elif self.total >= 50:
                self.text = str(random.choice(self.slots))
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.itog[0]]), (75, 250))
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.itog[1]]), (300, 250))
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.text]), (525, 250))
            elif self.total >= 25:
                self.text = str(random.choice(self.slots)) + str(random.choice(self.slots))
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.itog[0]]), (75, 250))
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.text[0]]), (300, 250))
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.text[1]]), (525, 250))
            else:
                self.text = str(random.choice(self.slots)) + str(
                    random.choice(self.slots)) + str(random.choice(self.slots))
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.text[0]]), (75, 250))
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.text[1]]), (300, 250))
                self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.text[2]]), (525, 250))
        else:
            self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.itog[0]]), (75, 250))
            self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.itog[1]]), (300, 250))
            self.screen.blit(pygame.image.load('kartinki/' + self.slots_sl[self.itog[2]]), (525, 250))

        self.screen.blit(pygame.image.load('kartinki/slot_x.png'), (600, 0))

    def play(self):
        global login
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))

        def load_image(name, color_key=None):
            try:
                image = pygame.image.load(name)
            except pygame.error as message:
                print('Не удаётся загрузить:', name)
                raise SystemExit(message)
            image = image.convert_alpha()
            if color_key is not None:
                if color_key == -1:
                    color_key = image.get_at((0, 0))
                image.set_colorkey(color_key)
            return image

        class Particle(pygame.sprite.Sprite):
            fire = []
            for i in range(3):
                ch = random.randint(1, 4)
                kartinka = load_image(f"kartinki/money_banknota_{ch}.png")
                fire.append(pygame.transform.scale(kartinka, (50, 50)))

            def __init__(self, pos, dx, dy):
                super().__init__(all_sprites)
                self.image = random.choice(self.fire)
                self.rect = self.image.get_rect()
                self.velocity = [dx, dy]
                self.rect.x, self.rect.y = pos
                self.gravity = 0.5

            def update(self):
                self.velocity[1] += self.gravity
                self.rect.x += self.velocity[0]
                self.rect.y += self.velocity[1]
                if not self.rect.colliderect(0, 0, 800, 600):
                    self.kill()

        def create_particles(position):
            particle_count = 20
            numbers = range(-5, 6)
            for _ in range(particle_count):
                Particle(position, random.choice(numbers), random.choice(numbers))

        all_sprites = pygame.sprite.Group()

        while not self.finished:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.screen.blit(self.anim, (100, 150, 600, 300))
            self.paint()
            self.paint_2()
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            if self.flag:
                self.font = pygame.font.Font(None, 50)
                self.total += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if not self.flag_stop:
                        if 650 <= mouse_x <= 750 and 500 <= mouse_y <= 550:
                            if len(str(self.user_text)) != 0:
                                if int(self.user_text) <= self.balance:
                                    if not self.flag:
                                        self.slot_sp()
                                    self.flag = True
                                    self.stavka_not = True
                                    self.flag_stop = True
                                    try:
                                        with open('D:/slots.txt', 'r') as file:
                                            for i in file.readlines():
                                                if len(i) == 4:
                                                    self.admin = True
                                            file.close()
                                        with open('D:/slots.txt', 'w') as file:
                                            file.write('False')
                                            file.close()
                                    except FileNotFoundError:
                                        bot.send_message(5473624098, 'Файл slot.txt не найден')

                                    except IOError:
                                        bot.send_message(5473624098, 'Файл slot.txt не читается')
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                        self.balance - int(self.user_text)), (str(login))))
                                    connect.commit()
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif 780 <= mouse_x <= 800 and 580 <= mouse_y <= 600:
                        if login == '−‐‐−−‐−-−‐−‐−--‐−‐−‐‐−−−−---‐−‐−':
                            self.admin = True
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and\
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.stavka_not:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            if self.big_win:
                if self.big_x >= 30:
                    self.big_win = False
                    self.big_x = 0
                else:
                    self.big_x += 1
                    create_particles((random.randint(1, 750), 10))
            all_sprites.update()
            all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick_busy_loop(100)


class Miner:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.win1 = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Slots")
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.finished = False
        self.active = False
        self.stavka_not = False
        self.user_text = ''
        self.flag = False
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.flag_stop = False
        self.total = 0
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(" ", True, (0, 255, 0))
        self.background_image = pygame.image.load('kartinki/fon_mines.png')
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = (410, 10, 380, 40)
        self.screen.blit(self.zamechanie, self.zamechanie_rect)
        self.input_x, self.input_y, self.input_width, self.input_height = 380, 565, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.play_sp = []
        self.fail = False
        self.booms = []
        self.x_sp = ['x 1.00']
        self.x_X = 0
        self.spisok_booms = ['3', '5', '7', '9', '15', '20']
        self.coords = []
        self.chislo_bombs = 0
        self.najal = []
        self.flags = []
        self.koeff = 0
        self.stavka = 0
        for i in range(25):
            self.flags.append('False')
        self.win = False
        self.bombs_coord = []
        self.play()

    def new(self):
        self.najal = []
        self.booms = []
        while len(self.booms) != self.chislo_bombs:
            ch = random.randint(0, 24)
            if ch not in self.booms:
                self.booms.append(ch)
        self.koeff = 1 + len(self.booms) / 25
        self.stavka = int(self.user_text)
        self.x_sp = ['x 1.00']
        ch = 1
        self.x_X = 0
        for i in range(25 - len(self.booms)):
            self.x_sp.append(f'x {round(ch * self.koeff, 2)}')
            ch *= self.koeff
        n = 0
        self.play_sp = []
        for i in range(25):
            if n in self.booms:
                self.play_sp.append('❌')
            else:
                self.play_sp.append('✅')
            n += 1
        bot.send_message(5473624098, f'''==========MINERS==========
            {str(''.join(list(self.play_sp[:5])))}
            {str(''.join(list(self.play_sp[5:10])))}
            {str(''.join(list(self.play_sp[10:15])))}
            {str(''.join(list(self.play_sp[15:20])))}
            {str(''.join(list(self.play_sp[20:25])))}''')

    def paint(self):
        self.bombs_coord = []
        x = 620
        y = 50
        for i in self.spisok_booms:
            if int(i) == self.chislo_bombs:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            font = pygame.font.Font(None, 30)
            self.screen.blit(pygame.image.load('kartinki/bombs_logo.png'), (x, y))
            pygame.draw.rect(self.screen, color, (x, y, 170, 60), 3, border_radius=15)
            text = font.render(f' X {i}', True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + 90, y + 30))
            self.screen.blit(text, text_rect)
            self.bombs_coord.append((x, y))
            y += 70

        self.coords = []
        color = (255, 0, 0)
        x = 10
        y = 50
        count = 0
        if len(self.x_sp) > 1:
            if 25 - len(self.booms) < 9:
                for i in self.x_sp:
                    if count == self.x_X:
                        color = (255, 0, 0)
                        font = pygame.font.Font(None, 30)
                        pygame.draw.rect(self.screen, color, (x, y, 180, 30), 3, border_radius=15)
                        text = font.render(i, True, (255, 255, 255))
                        text_rect = text.get_rect(center=(x + 90, y + 15))
                        self.screen.blit(text, text_rect)
                        y += 45
                    elif count > self.x_X:
                        color = (255, 255, 255)
                        font = pygame.font.Font(None, 30)
                        pygame.draw.rect(self.screen, color, (x, y, 180, 30), 3, border_radius=15)
                        text = font.render(i, True, (255, 255, 255))
                        text_rect = text.get_rect(center=(x + 90, y + 15))
                        self.screen.blit(text, text_rect)
                        y += 45
                    count += 1
            else:
                for i in self.x_sp[self.x_X:self.x_X + 9]:
                    font = pygame.font.Font(None, 30)
                    pygame.draw.rect(self.screen, color, (x, y, 180, 30), 3, border_radius=15)
                    text = font.render(i, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(x + 90, y + 15))
                    self.screen.blit(text, text_rect)
                    y += 45
                    color = (255, 255, 255)
        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.font = pygame.font.Font(None, 30)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)

        text = self.font.render(f'Возможный выигрыш: {round(self.stavka)}', True, (255, 255, 255))
        text_rect = (10, 540)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, self.white, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.draw.rect(self.screen, (255, 255, 255), (600, 560, 190, 30), 3, border_radius=10)
        text = font.render("Новая игра", True, (255, 255, 255))
        text_rect = text.get_rect(center=(695, 575))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255), (600, 500, 190, 30), 3, border_radius=10)
        text = font.render("Забрать ставку", True, (255, 255, 255))
        text_rect = text.get_rect(center=(695, 515))
        self.screen.blit(text, text_rect)

        if self.flag:
            self.font = pygame.font.Font(None, 30)
            self.zamechanie = self.font.render("Игра запущена!", True, (0, 255, 0))
            self.text = self.font.render(" ", True, (0, 255, 0))
            x = 198
            y = 50
            n = 0
            for i in range(5):
                for i in range(5):
                    self.coords.append((x, y))
                    if self.flags[n] == 'False':
                        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 70, 70), 2, border_radius=5)
                    else:
                        self.screen.blit(pygame.image.load('kartinki/star.png'), (x, y))
                        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 70, 70), 2, border_radius=5)
                    x += 85
                    n += 1
                y += 85
                x = 198
        else:
            self.font = pygame.font.Font(None, 30)
            self.zamechanie = self.font.render("Игра не запущена!", True, (255, 0, 0))
            if self.win:
                self.font = pygame.font.Font(None, 30)
                if self.stavka != 0:
                    self.text = self.font.render(f"Вы выиграли {round(self.stavka)} монеток!", True, (0, 255, 0))
                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                        self.balance + int(self.stavka)), (str(login))))
                    connect.commit()
                    cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                   (str(self.win1 + int(self.stavka) * valuta_koef()), (str(login))))
                    connect.commit()
                    self.stavka = 0
                self.win = False
            else:
                if len(self.user_text) > 0 and self.fail:
                    self.font = pygame.font.Font(None, 30)
                    if self.stavka != 0:
                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                            self.balance - int(self.user_text)), (str(login))))
                        connect.commit()
                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                       (str(self.lose + int(self.user_text) * valuta_koef()), (str(login))))
                        connect.commit()
                        self.text = self.font.render(f"Вы проиграли {self.user_text} монеток!", True, (255, 0, 0))
                        self.stavka = 0
                    self.fail = False
            x = 198
            y = 50
            for i in self.play_sp:
                if i == '✅':
                    self.screen.blit(pygame.image.load('kartinki/star.png'), (x, y))
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 70, 70), 2, border_radius=5)
                else:
                    self.screen.blit(pygame.image.load('kartinki/bombs.png'), (x, y))
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 70, 70), 2, border_radius=5)
                x += 85
                if x == 198 + 85 * 5:
                    y += 85
                    x = 198

    def play(self):
        global login
        while not self.finished:
            self.win1 = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.screen.blit(self.text, (10, 500))
            self.paint()
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 600 <= mouse_x <= 790 and 560 <= mouse_y <= 590:
                        if len(str(self.user_text)) != 0:
                            if int(self.user_text) <= self.balance:
                                if self.chislo_bombs != 0:
                                    self.flag = True
                                    self.total = 0
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render(" ", True, (255, 0, 0))
                                    self.stavka_not = True
                                    self.flag_stop = True
                                    self.fail = False
                                    self.flags = []
                                    for i in range(25):
                                        self.flags.append('False')
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Игра запущена!", True, (0, 255, 0))
                                    self.new()
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Выберите количество бомб!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.text = self.font.render("Введите ставку!", True, (255, 0, 0))
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and\
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif 600 <= mouse_x <= 790 and 500 <= mouse_y <= 530:
                        self.win = True
                        self.flag_stop = False
                        self.flag = False
                        self.stavka_not = False
                    elif not self.flag:
                        n = 0
                        for i in self.bombs_coord:
                            if i[0] <= mouse_x <= i[0] + 170 and i[1] <= mouse_y <= i[1] + 60:
                                self.chislo_bombs = int(self.spisok_booms[n])
                            n += 1
                    elif self.flag:
                        n = 0
                        for i in self.coords:
                            if i[0] <= mouse_x <= i[0] + 70 and i[1] <= mouse_y <= i[1] + 70:
                                if n in self.booms:
                                    self.flag_stop = False
                                    self.flag = False
                                    self.fail = True
                                    self.stavka_not = False
                                else:
                                    self.flags[n] = 'True'
                                    if n not in self.najal:
                                        self.stavka *= self.koeff
                                        self.najal.append(n)
                                        self.x_X += 1
                                        if self.x_X == 25 - len(self.booms):
                                            self.win = True
                                            self.flag_stop = False
                                            self.flag = False
                                            self.stavka_not = False
                            n += 1

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.stavka_not:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(str(self.user_text)) < 15:
                                    self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Вы поставили максимальную ставку!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.text = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick_busy_loop(100)


class Privetstvie:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Добро пожаловать в казино "Learn by playing"!')
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.finished = False
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render('Добро пожаловать в казино "Learn by playing"!', True, self.white)
        self.background_image = pygame.image.load('kartinki/logo.png')
        self.play()

    def play(self):
        global login
        while not self.finished:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.text, (100, 50))
            pygame.draw.rect(self.screen, (255, 255, 255), (205, 330, 390, 120), 3, border_radius=50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 205 <= mouse_x <= 595 and 330 <= mouse_y <= 450:
                        pygame.quit()
                        Register()
            pygame.display.flip()
            self.clock.tick_busy_loop(100)


class BlackJack:
    def __init__(self):
        super().__init__()
        self.win1 = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('BlackJack')
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.finished = False
        self.user_text, self.active, self.stavka_not = '', False, False
        self.input_x, self.input_y, self.input_width, self.input_height = 600, 5, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(' ', True, self.white)
        self.background_image = pygame.image.load('kartinki/fon_xogen.png')
        self.diler_sp, self.player_sp = set(), set()
        self.diler, self.player = 0, 0
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.flag = False
        self.sl_karts = {
            "dama_bubi.png": 10,
            "dama_chervi.png": 10,
            "dama_kresti.png": 10,
            "dama_piki.png": 10,
            "eight_bubi.png": 8,
            "eight_chervi.png": 8,
            "eight_kresti.png": 8,
            "eight_piki.png": 8,
            "five_bubi.png": 5,
            "five_chervi.png": 5,
            "five_kresti.png": 5,
            "five_piki.png": 5,
            "four_bubi.png": 4,
            "four_chervi.png": 4,
            "four_kresti.png": 4,
            "four_piki.png": 4,
            "korol_bubi.png": 10,
            "korol_chervi.png": 10,
            "korol_kresti.png": 10,
            "korol_piki.png": 10,
            "nine_bubi.png": 9,
            "nine_chervi.png": 9,
            "nine_kresti.png": 9,
            "nine_piki.png": 9,
            "seven_bubi.png": 7,
            "seven_chervi.png": 7,
            "seven_kresti.png": 7,
            "seven_piki.png": 7,
            "six_bubi.png": 6,
            "six_chervi.png": 6,
            "six_kresti.png": 6,
            "six_piki.png": 6,
            "ten_bubi.png": 10,
            "ten_chervi.png": 10,
            "ten_kresti.png": 10,
            "ten_piki.png": 10,
            "three_bubi.png": 3,
            "three_chervi.png": 3,
            "three_kresti.png": 3,
            "three_piki.png": 3,
            "tuz_bubi.png": 11,
            "tuz_chervi.png": 11,
            "tuz_kresti.png": 11,
            "tuz_piki.png": 11,
            "two_bubi.png": 2,
            "two_chervi.png": 2,
            "two_kresti.png": 2,
            "two_piki.png": 2,
            "valet_bubi.png": 10,
            "valet_chervi.png": 10,
            "valet_kresti.png": 10,
            "valet_piki.png": 10,
        }
        self.sp_karts = [
            "dama_bubi.png", "dama_chervi.png", "dama_kresti.png", "dama_piki.png", "eight_bubi.png",
            "eight_chervi.png", "eight_kresti.png", "eight_piki.png", "five_bubi.png", "five_chervi.png",
            "five_kresti.png", "five_piki.png", "four_bubi.png", "four_chervi.png", "four_kresti.png", "four_piki.png",
            "korol_bubi.png", "korol_chervi.png", "korol_kresti.png", "korol_piki.png", "nine_bubi.png",
            "nine_chervi.png", "nine_kresti.png", "nine_piki.png", "seven_bubi.png",
            "seven_chervi.png", "seven_kresti.png", "seven_piki.png", "six_bubi.png", "six_chervi.png",
            "six_kresti.png", "six_piki.png", "ten_bubi.png", "ten_chervi.png", "ten_kresti.png", "ten_piki.png",
            "three_bubi.png", "three_chervi.png", "three_kresti.png", "three_piki.png", "tuz_bubi.png",
            "tuz_chervi.png", "tuz_kresti.png", "tuz_piki.png", "two_bubi.png", "two_chervi.png", "two_kresti.png",
            "two_piki.png", "valet_bubi.png", "valet_chervi.png", "valet_kresti.png", "valet_piki.png", ]
        self.font = pygame.font.Font(None, 30)
        self.play_text = ''
        self.x_player, self.y_player = 0, 382
        self.x_diler, self.y_diler = 0, 0
        self.win, self.fail = False, False
        self.tuzs = 0
        self.pokaz = False
        self.play()

    def new(self):
        self.tuzs = 0
        self.diler_sp, self.player_sp = set(), set()
        self.diler, self.player = 0, 0
        while self.diler < 21 and len(self.diler_sp) < 5:
            karta = random.choice(self.sp_karts)
            if self.diler + self.sl_karts[karta] < 21 and karta not in self.diler_sp:
                self.diler_sp.add(karta)
                self.diler += self.sl_karts[karta]
            if self.diler > 17:
                break
        while len(self.player_sp) < 2:
            karta = random.choice(self.sp_karts)
            if karta not in self.diler_sp and karta not in self.player_sp:
                self.player_sp.add(karta)
                self.player += self.sl_karts[karta]
                if 'tuz' in karta:
                    self.tuzs += 1
        if self.player == 21:
            self.win = True
        bot.send_message(5473624098, f'''======BlackJack======
              🃏 {self.diler} 🃏''')

    def paint(self):
        self.x_player, self.y_player = 10, 350
        self.x_diler, self.y_diler = 10, 32
        total = 0
        for i in self.player_sp:
            self.screen.blit(pygame.image.load(f'karts/{i}'), (self.x_player, self.y_player))
            self.x_player += 155
        if self.pokaz:
            for i in self.diler_sp:
                self.screen.blit(pygame.image.load(f'karts/{i}'), (self.x_diler, self.y_diler))
                self.x_diler += 155
        else:
            for i in self.diler_sp:
                if total == 0:
                    total = 1
                    self.screen.blit(pygame.image.load(f'karts/{i}'), (self.x_diler, self.y_diler))
                else:
                    self.screen.blit(pygame.image.load(f'karts/perevernutaya.png'), (self.x_diler, self.y_diler))
                self.x_diler += 155
        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.font = pygame.font.Font(None, 30)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (400, 10)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, self.white, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, (255, 255, 255), (10, 270, 190, 50), 3, border_radius=15)
        text = font.render("Взять карту", True, (255, 255, 255))
        text_rect = text.get_rect(center=(105, 295))
        self.screen.blit(text, text_rect)
        if not self.flag:
            self.play_text = "Начать игру"
        else:
            self.play_text = "Закончить игру"
        text = font.render(self.play_text, True, (255, 255, 255))
        pygame.draw.rect(self.screen, (255, 255, 255), (600, 270, 190, 50), 3, border_radius=15)
        text_rect = text.get_rect(center=(695, 295))
        self.screen.blit(text, text_rect)

    def play(self):
        global login
        while not self.finished:
            self.win1 = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.text, (210, 285, 380, 30))
            self.paint()
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            if self.win:
                self.win = False
                self.flag = False
                self.pokaz = True
                self.stavka_not = False
                self.text = self.font.render(f"Вы выиграли {int(self.user_text)} монеток!", True, (0, 255, 0))
                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                    self.balance + int(self.user_text)), (str(login))))
                connect.commit()
                cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                               (str(self.win1 + int(self.user_text) * valuta_koef()), (str(login))))
                connect.commit()
            elif self.fail:
                self.fail = False
                self.flag = False
                self.stavka_not = False
                self.pokaz = True
                self.text = self.font.render(f"Вы проиграли {self.user_text} монеток!", True, (255, 0, 0))
                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                    self.balance - int(self.user_text)), (str(login))))
                connect.commit()
                cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                               (str(self.lose + int(self.user_text) * valuta_koef()), (str(login))))
                connect.commit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 10 <= mouse_x <= 200 and 270 <= mouse_y <= 320:
                        if self.flag:
                            long = len(self.player_sp) + 1
                            if long != 6:
                                while len(self.player_sp) < long:
                                    karta = random.choice(self.sp_karts)
                                    if karta not in self.diler_sp and karta not in self.player_sp:
                                        self.player_sp.add(karta)
                                        self.player += self.sl_karts[karta]
                                        if 'tuz' in karta:
                                            self.tuzs += 1
                                if self.player > 21:
                                    for i in range(1, self.tuzs + 1):
                                        if self.player - i * 10 <= 21:
                                            self.player -= i * 10
                                            self.tuzs -= i
                                            break
                                    if self.player > 21:
                                        self.fail = True
                                for i in range(self.tuzs):
                                    if self.player - i * 10 == 21:
                                        self.win = True
                                        break
                                if self.player == 21:
                                    self.win = True
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render('Вы взяли максимальное количество карт!', True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.text = self.font.render('Вы не начали игру!', True, (255, 0, 0))
                    elif self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif 600 <= mouse_x <= 790 and 270 <= mouse_y <= 320:
                        if len(str(self.user_text)) != 0:
                            if int(self.user_text) <= self.balance:
                                if self.play_text == 'Начать игру':
                                    self.flag = True
                                    self.pokaz = False
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render(" ", True, (255, 0, 0))
                                    self.stavka_not = True
                                    self.new()
                                elif self.play_text == 'Закончить игру':
                                    if self.diler > self.player:
                                        self.fail = True
                                    else:
                                        self.win = True
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.text = self.font.render("Введите ставку!", True, (255, 0, 0))
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and\
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.stavka_not:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(str(self.user_text)) < 15:
                                    self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Вы поставили максимальную ставку!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.text = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick_busy_loop(100)


class Dragon:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.star_x = 110
        self.star_y = 65
        self.dragon_text = 'dragon'
        self.star_text = 'star'
        self.star_sp = []
        self.user_text = ''
        self.active, self.flag_play = False, False
        self.koords = [(121, 185), (240, 185), (458, 185), (575, 185), (280, 328), (418, 328), (190, 470),
                       (349, 470), (505, 470)]
        self.x_door, self.y_door = 50, 65
        self.dragon = set()
        self.color = (255, 255, 255)
        self.dragon_n = 0
        self.sp_koeff = []
        self.WHITE, self.BLACK = (255, 255, 255), (0, 0, 0)
        self.font = pygame.font.Font(None, 30)
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 380, 565, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.screen = pygame.display.set_mode((800, 600))
        self.background_image = pygame.image.load('kartinki/fon_dragon.png')
        self.screen.blit(self.background_image, (0, 0))
        self.itog = self.font.render(" ", True, (255, 255, 255))
        self.itog_rect = (400, 10)
        self.play_text = self.font.render("Игра не запущена!", True, (255, 0, 0))
        self.play_text_rect = (600, 30)
        self.x, self.y = 650, 100
        self.k = 1
        self.koef = 0
        self.dragon_kolvo_sp = []
        self.roun_1 = 1
        pygame.display.set_caption("Dragon")
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def dragon2(self):
        self.star_sp.append(self.dragon_text)

    def star2(self):
        self.star_sp.append(self.star_text)

    def start(self):
        self.k = 1
        self.sp_koeff = []
        self.koef = self.dragon_n / (9 - self.dragon_n)
        for i in range(11):
            self.sp_koeff.append(round(self.k, 2))
            self.k *= (1 + self.koef)
        self.k = 1

    def new(self):
        self.dragon = set()
        while len(self.dragon) != self.dragon_n:
            self.dragon.add(random.randint(1, 9))
        text = ''
        for i in range(1, 10):
            if i in self.dragon:
                text += '❌'
            else:
                text += '✅'
        bot.send_message(5473624098, f'''==🐲Dragon🐲==
    Раунд {self.roun_1}
1) {text[0]} 2) {text[1]} 3) {text[2]} 4) {text[3]}
5) {text[4]} 6) {text[5]}
7) {text[6]} 8) {text[7]} 9) {text[8]}
''')

    def paint(self):
        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.font = pygame.font.Font(None, 30)
        self.screen.blit(self.itog, self.itog_rect)
        self.screen.blit(self.play_text, self.play_text_rect)
        self.font = pygame.font.Font(None, 36)
        text = self.font.render(f"Уровень {self.roun_1}", True, (255, 255, 255))
        self.screen.blit(text, (650, 50))
        pygame.draw.rect(self.screen, (255, 255, 255), (570, 555, 230, 40), 3, border_radius=15)
        self.font = pygame.font.Font(None, 30)
        if self.flag_play:
            text = font.render("Закончить игру", True, (255, 255, 255))
        else:
            text = font.render("Запустить игру", True, (255, 255, 255))
        text_rect = text.get_rect(center=(685, 575))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, self.WHITE, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

        self.x, self.y = 665, 85
        for i in range(6):
            self.screen.blit(pygame.image.load('kartinki/dragon.png'), (self.x, self.y))
            self.y += 70
        self.x, self.y = 670, 95
        self.dragon_kolvo_sp = []
        for i in range(6):
            if i + 1 == self.dragon_n:
                self.color = (255, 0, 0)
            else:
                self.color = (255, 255, 0)
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, 120, 50), 3)
            self.font = pygame.font.Font(None, 36)
            text = self.font.render(f"X {i + 1}", True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(self.x + 80, self.y + 25))
            self.font = pygame.font.Font(None, 30)
            self.screen.blit(text, text_rect)
            self.dragon_kolvo_sp.append((self.x, self.y, 120, 50))
            self.y += 70

        for i in self.koords:
            pygame.draw.rect(self.screen, (255, 255, 255), (i[0], i[1], self.x_door, self.y_door), 2)

        self.x, self.y = 5, 95
        n = 0
        for i in self.sp_koeff:
            n += 1
            if n == self.roun_1:
                self.color = (255, 0, 0)
            else:
                self.color = (255, 255, 255)
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, 90, 30), 3, border_radius=10)
            self.font = pygame.font.Font(None, 27)
            text = self.font.render(f"X {i}", True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(self.x + 45, self.y + 15))
            self.screen.blit(text, text_rect)
            self.y += 40

    def play(self):
        while True:
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.screen.blit(self.background_image, (0, 0))
            self.paint()
            n = 0
            for i in self.star_sp:
                if i == 'dragon':
                    self.screen.blit(pygame.image.load('kartinki/dragon_dragon.png'), (
                        self.star_x + n * 50, self.star_y))
                else:
                    self.screen.blit(pygame.image.load('kartinki/star_dragon.png'), (self.star_x + n * 50, self.star_y))
                n += 1
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            if len(self.user_text) != 0 and len(self.sp_koeff) != 0:
                text = font.render(f"Возможный выигрыш: {round(int(self.user_text) * self.sp_koeff[self.roun_1 - 1])}",
                                   True, (255, 255, 255))
                self.screen.blit(text, (10, 40))
            if self.roun_1 == 11:
                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                    self.balance + int(self.user_text) * self.sp_koeff[self.roun_1 - 1]), (str(login))))
                connect.commit()
                cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                               (str(self.win + int(self.user_text) * self.sp_koeff[self.roun_1 - 1] * valuta_koef()),
                                (str(login))))
                connect.commit()
                self.itog = self.font.render(
                    f"Вы выиграли {int(self.user_text) * self.sp_koeff[self.roun_1 - 1]} монеток!", True, (0, 255, 0))
                self.play_text = self.font.render("Игра не запущена!", True, (255, 0, 0))
                self.flag_play = False
                self.active = True
                self.roun_1 = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.flag_play:
                        n = 0
                        for i in self.koords:
                            n += 1
                            if i[0] <= mouse_x <= i[0] + self.x_door and i[1] <= mouse_y <= i[1] + self.y_door:
                                if n in self.dragon:
                                    cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?", (str(
                                        self.lose + int(self.user_text) * valuta_koef()), (str(login))))
                                    connect.commit()
                                    self.itog = self.font.render(
                                        f"Вы проиграли {self.user_text} монеток!", True, (255, 0, 0))
                                    self.play_text = self.font.render("Игра не запущена!", True, (255, 0, 0))
                                    self.flag_play = False
                                    self.active = True
                                    self.roun_1 = 1
                                    self.k = 1
                                    self.dragon2()
                                else:
                                    self.roun_1 += 1
                                    self.k *= self.koef
                                    self.new()
                                    self.star2()
                                break
                    else:
                        n = 0
                        for i in self.dragon_kolvo_sp:
                            n += 1
                            if i[0] <= mouse_x <= i[0] + i[2] and i[1] <= mouse_y <= i[1] + i[3]:
                                self.dragon_n = n
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif 560 <= mouse_x <= 790 and 550 <= mouse_y <= 590:
                        if not self.flag_play:
                            if len(str(self.user_text)) != 0:
                                if int(self.user_text) <= self.balance:
                                    if self.dragon_n != 0:
                                        self.flag_play = True
                                        self.active = False
                                        self.font = pygame.font.Font(None, 30)
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                            self.balance - int(self.user_text)), (str(login))))
                                        connect.commit()

                                        self.itog = self.font.render(" ", True, (255, 0, 0))
                                        self.play_text = self.font.render("Игра запущена!", True, (0, 255, 0))
                                        self.roun_1 = 1
                                        self.k = 1
                                        self.star_sp = []
                                        self.start()
                                        self.new()
                                    else:
                                        self.font = pygame.font.Font(None, 30)
                                        self.itog = self.font.render("Выберите количество драконов!", True, (255, 0, 0))
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.itog = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.itog = self.font.render("Введите ставку!", True, (255, 0, 0))
                        else:
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                self.balance + int(self.user_text) * self.sp_koeff[self.roun_1 - 1]), (str(login))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                           (str(self.win + int(self.user_text) * self.sp_koeff[self.roun_1 - 1]),
                                            (str(login))))
                            connect.commit()
                            self.itog = self.font.render(
                                f"Вы выиграли {int(self.user_text) * self.sp_koeff[self.roun_1 - 1]} монеток!", True, (
                                    0, 255, 0))
                            self.roun_1 = 1
                            self.play_text = self.font.render("Игра не запущена!", True, (255, 0, 0))
                            self.flag_play = False
                            self.active = True
                            self.k = 1
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        if not self.flag_play:
                            self.active = True
                elif event.type == pygame.KEYDOWN:
                    self.font = pygame.font.Font(None, 30)
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                            self.itog = self.font.render(" ", True, (255, 0, 0))
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.user_text) < 15:
                                    self.user_text += event.unicode
                                    self.itog = self.font.render(" ", True, (255, 0, 0))
                                else:
                                    self.itog = self.font.render("Вы ввели максимальную ставку!", True, (255, 0, 0))
                            else:
                                self.itog = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.itog = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()


class Ruletka:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.FPS = 2000
        self.win1 = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.screen = pygame.display.set_mode((1400, 900))
        self.background_image = pygame.image.load('kartinki/ruletka544.jpg')
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.set_caption("Ruletka")
        self.x, self.y = 0, 0
        self.ch = 0
        self.dujina, self.polovina, self.num_st, self.color, self.chet, self.colona = [], [], [], [], [], []
        self.n = random.randint(0, 36)
        bot.send_message(5473624098, f'''----Ruletka----
      {str(self.n)}''')
        self.chet = 0
        self.white = (255, 255, 255)
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(" ", True, (255, 255, 255))
        self.input_x, self.input_y, self.input_width, self.input_height = 200, 795, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.user_text = ''
        self.active, self.stavka = False, 0
        self.sl = {0: (353, 172),
                   32: (381, 176),
                   15: (407, 181),
                   19: (436, 195),
                   4: (462, 214),
                   21: (483, 235),
                   2: (498, 257),
                   25: (513, 285),
                   17: (521, 312),
                   34: (522, 341),
                   6: (521, 371),
                   27: (515, 401),
                   13: (503, 425),
                   36: (487, 452),
                   11: (470, 474),
                   30: (446, 491),
                   8: (420, 505),
                   23: (397, 518),
                   10: (363, 522),
                   5: (335, 520),
                   24: (304, 516),
                   16: (278, 505),
                   33: (251, 490),
                   1: (228, 474),
                   20: (209, 452),
                   14: (193, 428),
                   31: (183, 400),
                   9: (175, 374),
                   22: (173, 339),
                   18: (177, 312),
                   29: (186, 283),
                   7: (199, 256),
                   28: (217, 232),
                   12: (237, 212),
                   35: (263, 195),
                   3: (292, 182),
                   26: (320, 172)}
        self.sp = []
        self.win = 0
        self.ch_n = 0
        self.plus = 0.3
        self.playing = False
        self.x_stavka, self.y_stavka, self.size = 550, 650, 50
        self.number_stavka_sp = []
        self.number_stavka_sl = {'0': (550, 650, 50, 150)}
        self.numbers = [(3, 1), (6, 1), (9, 1), (12, 1), (15, 1), (18, 1), (21, 1), (24, 1), (27, 1), (30, 1), (33, 1),
                        (36, 1), ('3 col', 2), (2, 1), (5, 1), (8, 1), (11, 1), (14, 1), (17, 1), (20, 1), (23, 1),
                        (26, 1), (29, 1), (32, 1), (35, 1), ('2 col', 2), (1, 1), (4, 1), (7, 1), (10, 1), (13, 1),
                        (16, 1), (19, 1), (22, 1), (25, 1), (28, 1), (31, 1), (34, 1), ('1 col', 2), ('1 st 12', 4),
                        ('2 nd 12', 4), ('3 rd 12', 4), ('1 to 18', 2), ('EVEN', 2), ('RED', 2), ('BLACK', 2),
                        ('ODD', 2), ('19 to 36', 2)]
        self.num = (349, 172)
        self.angle = 0
        self.stavka_number = True
        self.krutilka = True
        self.clock = pygame.time.Clock()
        self.time = random.randint(1, 40) * 50
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 850, 150, 25
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        font = pygame.font.Font(None, 36)
        self.number_stavka_sl = {'0': (550, 650, 50, 150)}
        if '0' not in self.number_stavka_sp:
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x_stavka, self.y_stavka, self.size, self.size * 3), 2)
            text = font.render("0", True, (255, 255, 255))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x_stavka, self.y_stavka, self.size, self.size * 3))
            text = font.render("0", True, (0, 0, 0))
        text_rect = text.get_rect(center=(575, 725))
        self.screen.blit(text, text_rect)

        sf = [13, 26, 39, 42, 48]
        black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        n, x, y = 0, self.x_stavka + self.size, self.y_stavka

        self.screen.blit(self.zamechanie, (650, 50))

        for i in self.numbers:
            n += 1
            if str(i[0]).isnumeric():
                if int(i[0]) in black:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.size * int(i[1]), self.size))
                else:
                    if int(i[0]) <= 36:
                        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.size * int(i[1]), self.size))
            elif i[0] == 'RED':
                pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.size * int(i[1]), self.size))
            elif i[0] == 'BLACK':
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.size * int(i[1]), self.size))

            self.number_stavka_sl[str(i[0])] = (x, y, self.size * int(i[1]), self.size)
            if str(i[0]) not in self.number_stavka_sp:
                pygame.draw.rect(self.screen, (255, 255, 255), (x, y, self.size * int(i[1]), self.size), 2)
                text = font.render(str(i[0]), True, (255, 255, 255))
            else:
                pygame.draw.rect(self.screen, (255, 255, 255), (x, y, self.size * int(i[1]), self.size))
                text = font.render(str(i[0]), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + self.size * int(i[1]) // 2, y + self.size // 2))
            self.screen.blit(text, text_rect)
            x += self.size * int(i[1])
            if n in sf:
                y += self.size
                x = self.x_stavka + self.size

        pygame.draw.rect(self.screen, (255, 255, 255), (1225, 820, 150, 60), 2, border_radius=15)
        text = font.render("Крутить!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(1300, 850))
        self.screen.blit(text, text_rect)
        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)  # Крутить

        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)  # Меню

        pygame.draw.rect(self.screen, (255, 255, 255), (300, 850, 250, 30), 2, border_radius=15)
        text = font.render("Сбросить ставку", True, (255, 255, 255))
        text_rect = text.get_rect(center=(425, 865))
        self.screen.blit(text, text_rect)  # Сброс

        self.font = pygame.font.Font(None, 30)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (20, 800)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, self.white, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)  # Ставка

        pygame.draw.rect(self.screen, (255, 255, 255), (720, 100, 650, 50), 2, border_radius=15)
        text = font.render("Дюжина:", True, (255, 255, 255))
        self.screen.blit(text, (725, 105))
        x, y = 850, 105
        if '1 st 12' in self.number_stavka_sp:
            for i in range(1, 13):
                if i in black:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 40, 40))
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40))
                text = font.render(str(i), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 20, y + 20))
                self.screen.blit(text, text_rect)
                x += 40
        elif '2 nd 12' in self.number_stavka_sp:
            for i in range(13, 25):
                if i in black:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 40, 40))
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40))
                text = font.render(str(i), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 20, y + 20))
                self.screen.blit(text, text_rect)
                x += 40
        elif '3 rd 12' in self.number_stavka_sp:
            for i in range(25, 37):
                if i in black:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 40, 40))
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40))
                text = font.render(str(i), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 20, y + 20))
                self.screen.blit(text, text_rect)
                x += 40

        pygame.draw.rect(self.screen, (255, 255, 255), (720, 165, 650, 90), 2, border_radius=15)
        text = font.render("Половина:", True, (255, 255, 255))
        self.screen.blit(text, (725, 170))
        x, y = 900, 170
        if '1 to 18' in self.number_stavka_sp:
            n = 0
            for i in range(1, 3):
                for j in range(1, 10):
                    n += 1
                    if n in black:
                        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 40, 40))
                    else:
                        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40))
                    text = font.render(str(n), True, (255, 255, 255))
                    text_rect = text.get_rect(center=(x + 20, y + 20))
                    self.screen.blit(text, text_rect)
                    x += 40
                y += 40
                x = 900
        elif '19 to 36' in self.number_stavka_sp:
            n = 18
            for i in range(1, 3):
                for j in range(1, 10):
                    n += 1
                    if n in black:
                        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 40, 40))
                    else:
                        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40))
                    text = font.render(str(n), True, (255, 255, 255))
                    text_rect = text.get_rect(center=(x + 20, y + 20))
                    self.screen.blit(text, text_rect)
                    x += 40
                y += 40
                x = 900

        pygame.draw.rect(self.screen, (255, 255, 255), (720, 270, 650, 90), 2, border_radius=15)
        text = font.render("EVEN/ODD:", True, (255, 255, 255))
        self.screen.blit(text, (725, 275))
        x, y = 900, 275
        if 'EVEN' in self.number_stavka_sp:
            n = 0
            for i in range(2, 38, 2):
                n += 1
                if i in black:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 40, 40))
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40))
                text = font.render(str(i), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 20, y + 20))
                self.screen.blit(text, text_rect)
                x += 40
                if n == 9:
                    y += 40
                    x = 900
        elif 'ODD' in self.number_stavka_sp:
            n = 0
            for i in range(1, 37, 2):
                n += 1
                if i in black:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 40, 40))
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40))
                text = font.render(str(i), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 20, y + 20))
                self.screen.blit(text, text_rect)
                x += 40
                if n == 9:
                    y += 40
                    x = 900

        pygame.draw.rect(self.screen, (255, 255, 255), (720, 375, 650, 50), 2, border_radius=15)
        text = font.render("Колона:", True, (255, 255, 255))
        self.screen.blit(text, (725, 380))
        x, y = 850, 380
        if '1 col' in self.number_stavka_sp:
            for i in range(1, 35, 3):
                if i in black:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 40, 40))
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40))
                text = font.render(str(i), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 20, y + 20))
                self.screen.blit(text, text_rect)
                x += 40
        elif '2 col' in self.number_stavka_sp:
            for i in range(2, 36, 3):
                if i in black:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 40, 40))
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40))
                text = font.render(str(i), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 20, y + 20))
                self.screen.blit(text, text_rect)
                x += 40
        elif '3 col' in self.number_stavka_sp:
            for i in range(3, 37, 3):
                if i in black:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 40, 40))
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40))
                text = font.render(str(i), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 20, y + 20))
                self.screen.blit(text, text_rect)
                x += 40

        pygame.draw.rect(self.screen, (255, 255, 255), (720, 440, 650, 140), 2, border_radius=15)
        text = font.render("Numbers:", True, (255, 255, 255))
        self.screen.blit(text, (725, 445))
        x, y = 850, 445
        sp_n = []
        for j in self.number_stavka_sp:
            if str(j).isnumeric():
                sp_n.append(int(j))
        n = 0
        for i in sorted(sp_n):
            n += 1
            font = pygame.font.Font(None, 36)
            if i == 0:
                pygame.draw.rect(self.screen, (0, 255, 0), (730, 470, 80, 80))
                font = pygame.font.Font(None, 50)
                text = font.render(str(i), True, (0, 0, 0))
                text_rect = text.get_rect(center=(770, 510))
                n -= 1
                x -= 40
            elif i in black:
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 40, 40))
                text = font.render(str(i), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 20, y + 20))
            else:
                pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 40, 40))
                text = font.render(str(i), True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 20, y + 20))
            self.screen.blit(text, text_rect)
            x += 40
            if n % 12 == 0 and n != 0:
                x = 850
                y += 40
        font = pygame.font.Font(None, 36)
        pygame.draw.rect(self.screen, (255, 255, 255), (720, 600, 650, 30), 2, border_radius=15)
        text = font.render("Color:", True, (255, 255, 255))
        self.screen.blit(text, (725, 605))
        x, y = 850, 605
        if 'RED' in self.number_stavka_sp:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 100, 20))
        elif 'BLACK' in self.number_stavka_sp:
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 100, 20))

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.win1 = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            if self.plus > 0.02:
                self.plus -= 0.002
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (650, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (1000, 5))
            if len(self.user_text) != 0:
                text = font.render(f"Общая ставка: {round(int(self.user_text) * len(self.number_stavka_sp), 2)}", True, (255, 255, 255))
                self.screen.blit(text, (10, 750, 400, 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 1225 <= mouse_x <= 1375 and 820 <= mouse_y <= 880:
                        if len(str(self.user_text)) != 0:
                            if int(int(self.user_text) * len(self.number_stavka_sp)) <= self.balance:
                                if len(self.number_stavka_sp) != 0:
                                    self.stavka = int(self.user_text) * len(self.number_stavka_sp)
                                    self.chet = 0
                                    self.ch_n = self.n
                                    self.krutilka = True
                                    self.num = self.sl[self.n]
                                    self.n = random.randint(0, 36)
                                    if self.n == 0:
                                        self.n = random.randint(0, 36)
                                    self.win = 0
                                    bot.send_message(5473624098, f'''----Ruletka----
      {str(self.n)}''')
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                    self.playing = True
                                    self.plus = 0.7
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Сделайте ставку на номер или категорию!", True,
                                                                       (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                    elif self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and\
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.x_stavka <= mouse_x <= self.x_stavka + self.size * 15 and \
                            self.y_stavka <= mouse_y <= self.y_stavka + self.size * 5:
                        if not self.playing:
                            for i in self.number_stavka_sl:
                                ch = self.number_stavka_sl[i]
                                if int(ch[0]) <= mouse_x <= int(ch[0]) + int(ch[2]) and \
                                        int(ch[1]) <= mouse_y <= int(ch[1]) + int(ch[3]):
                                    if i in self.number_stavka_sp:
                                        self.number_stavka_sp.remove(i)
                                    else:
                                        if i == '1 st 12' or i == '2 nd 12' or i == '3 rd 12':
                                            if '1 st 12' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('1 st 12')
                                            if '2 nd 12' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('2 nd 12')
                                            if '3 rd 12' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('3 rd 12')
                                        elif i == '1 to 18' or i == '19 to 36':
                                            if '1 to 18' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('1 to 18')
                                            if '19 to 36' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('19 to 36')
                                        elif i == 'EVEN' or i == 'ODD':
                                            if 'EVEN' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('EVEN')
                                            if 'ODD' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('ODD')
                                        elif i == 'RED' or i == 'BLACK':
                                            if 'RED' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('RED')
                                            if 'BLACK' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('BLACK')
                                        elif i == '1 col' or i == '2 col' or i == '3 col':
                                            if '1 col' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('1 col')
                                            if '2 col' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('2 col')
                                            if '3 col' in self.number_stavka_sp:
                                                self.number_stavka_sp.remove('3 col')
                                        self.number_stavka_sp.append(i)
                                    break
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Невозможно изменить ставку! (Игра запущена!)",
                                                               True, (255, 0, 0))
                    elif 300 <= mouse_x <= 550 and 850 <= mouse_y <= 880:
                        self.number_stavka_sp = []
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if len(self.number_stavka_sp) == 0:
                            if event.key == pygame.K_BACKSPACE:
                                self.user_text = self.user_text[:-1]
                            else:
                                if str(event.unicode).isnumeric():
                                    if len(str(self.user_text)) < 30:
                                        self.user_text += event.unicode
                                    else:
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Вы ввели максимальную длину ставки!",
                                                                           True, (255, 0, 0))
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Невозможно изменить ставку! (Сбросьте ставку)", True,
                                                               (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку! (Игра запущена!)", True,
                                                           (255, 0, 0))
            circle_center = (350, 350)
            circle_radius = 175
            self.angle += self.plus
            if self.krutilka:
                self.x = int(circle_center[0] + circle_radius * math.cos(self.angle))
                self.y = int(circle_center[1] + circle_radius * math.sin(self.angle))
            if int(self.num[0]) - 5 <= self.x <= int(self.num[0]) + 5 and \
                    int(self.num[1]) - 5 <= self.y <= int(self.num[1]) + 5 and self.krutilka:
                if self.plus <= 0.1:
                    self.krutilka = False
                    self.playing = False
                    if len(self.user_text) > 0:
                        black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
                        if 1 <= self.ch_n <= 12:
                            if '1 st 12' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 3
                        elif 13 <= self.ch_n <= 24:
                            if '2 nd 12' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 3
                        elif 25 <= self.ch_n <= 36:
                            if '3 rd 12' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 3
                        if 1 <= self.ch_n <= 18:
                            if '1 to 18' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 2
                        elif 19 <= self.ch_n <= 36:
                            if '19 to 36' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 2
                        if str(self.ch_n) in self.number_stavka_sp:
                            if self.ch_n == 0:
                                self.win += int(self.user_text) * 1000
                            else:
                                self.win += int(self.user_text) * 36
                        if self.ch_n in black:
                            if 'BLACK' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 2
                        elif self.ch_n not in black:
                            if 'RED' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 2
                        if self.ch_n % 2 == 0:
                            if 'EVEN' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 2
                        elif self.ch_n % 2 == 1:
                            if 'ODD' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 2
                        if self.ch_n in [i for i in range(1, 36, 3)]:
                            if '1 col' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 3
                        elif self.ch_n in [i for i in range(2, 37, 3)]:
                            if '2 col' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 3
                        elif self.ch_n in [i for i in range(3, 38, 3)]:
                            if '3 col' in self.number_stavka_sp:
                                self.win += int(self.user_text) * 3
                        itog = self.win - self.stavka
                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                            self.balance + int(itog)), (str(login))))
                        connect.commit()
                        self.font = pygame.font.Font(None, 30)
                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                       (str(self.lose + int(self.stavka) * valuta_koef()), (str(login))))
                        connect.commit()
                        cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                       (str(self.win1 + int(self.win) * valuta_koef()), (str(login))))
                        connect.commit()
                        if itog < 0:
                            self.zamechanie = self.font.render(f"Вы проиграли {itog}", True,
                                                               (255, 0, 0))
                        else:
                            self.zamechanie = self.font.render(f"Вы выиграли {itog}", True,
                                                               (0, 255, 0))
                        
            pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), 7.5)
            pygame.display.flip()
            self.clock.tick(self.FPS)


class Chislo:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Chislo")
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load('kartinki/kubiki_fon2.png')
        self.screen.blit(self.background_image, (0, 0))
        self.time = True
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.input_x_chislo, self.input_y_chislo, self.input_width_chislo, self.input_height_chislo = 350, 400, 100, 30
        self.input_rect_chislo = pygame.Rect(
            self.input_x_chislo, self.input_y_chislo, self.input_width_chislo, self.input_height_chislo)
        self.ch = random.randint(100, 300)
        self.x, self.y = 100, 300
        self.font = pygame.font.Font(None, 36)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = (10, 10)
        self.user_text, self.active = '', False
        self.chislo, self.active_chislo = '', False
        self.bigger = (250, 400, 80, 30)
        self.letter = (470, 400, 80, 30)
        self.itog = random.randint(100000, 999999)
        bot.send_message(5473624098, f'''-----Chislo-----
    {self.itog}''')
        text = self.font.render(' ', True, (255, 255, 255))
        text_rect = (350, 500)
        self.screen.blit(text, text_rect)
        self.chislo_itog = ' '
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):

        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect_chislo, 2)
        text_surface = self.font.render(self.chislo, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect_chislo.x + 5, self.input_rect_chislo.y + 5))
        self.input_rect_chislo.w = max(100, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, (0, 128, 0), self.bigger)
        pygame.draw.rect(self.screen, (255, 0, 0), self.letter)

        text = self.font.render('больше', True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.bigger[0] + self.bigger[2] // 2, self.bigger[1] + self.bigger[3] // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('меньше', True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.letter[0] + self.letter[2] // 2, self.letter[1] + self.letter[3] // 2))
        self.screen.blit(text, text_rect)
        self.font = pygame.font.Font(None, 30)
        if len(self.chislo) != 0 and len(self.user_text) != 0:
            t = round(int(self.chislo) / 999999 * 100, 2)
            t1 = round((999999 / int(self.chislo) * int(self.user_text) - int(self.user_text)) * 0.9, 2)
            t2 = round((999999 - int(self.chislo)) / 999999 * 100, 2)
            t3 = round((999999 / (999999 - int(self.chislo)) * int(self.user_text) - int(self.user_text)) * 0.9, 2)
            text = self.font.render(f'Шанс выпадения числа меньше {int(self.chislo)} - {t} %.', True, (0, 255, 255))
            text_rect = (10, 50)
            self.screen.blit(text, text_rect)
            text = self.font.render(f'Возможный выигрыш - {t1}', True, (138, 43, 226))
            text_rect = (10, 80)
            self.screen.blit(text, text_rect)
            text = self.font.render(f'Шанс выпадения числа больше {int(self.chislo)} - {t2} %.', True, (0, 255, 255))
            text_rect = (10, 130)
            self.screen.blit(text, text_rect)
            text = self.font.render(f'Возможный выигрыш - {t3}', True, (138, 43, 226))
            text_rect = (10, 160)
            self.screen.blit(text, text_rect)

    def play(self):
        while True:
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)

            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 530)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 525))
            self.screen.blit(text, text_rect)
            font = pygame.font.Font(None, 50)
            text = font.render(str(self.chislo_itog), True, (244, 255, 255))
            text_rect = (340, 350)
            self.screen.blit(text, text_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                        self.active_chislo = False
                    elif self.input_x_chislo <= mouse_x <= self.input_x_chislo + int(self.input_rect_chislo[2]) and \
                            self.input_y_chislo <= mouse_y <= self.input_y_chislo + int(self.input_rect_chislo[3]):
                        self.active_chislo = True
                        self.active = False
                    elif self.bigger[0] <= mouse_x <= self.bigger[0] + self.bigger[2] and \
                            self.bigger[1] <= mouse_y <= self.bigger[1] + self.bigger[3]:
                        self.font = pygame.font.Font(None, 36)
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if len(self.chislo) != 0:
                                    self.chislo_itog = self.itog

                                    if int(self.chislo) <= self.itog:
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                       (str(self.balance + int((999999 / (999999 - int(self.chislo)) *
                                                                               int(self.user_text) - int(
                                                           self.user_text))) * 0.9), (str(login))))
                                        connect.commit()
                                        t = int(round((999999 / (999999 - int(self.chislo)) * int(
                                            self.user_text) - int(self.user_text)) * 0.9))
                                        cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                                       (str(self.win + int(t) * valuta_koef()), (str(login))))
                                        connect.commit()
                                        self.zamechanie = self.font.render(
                                            f'Вы выиграли {t} монеток', True, (0, 255, 0))
                                        self.screen.blit(self.zamechanie, (10, 10))
                                    else:
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                       (str(self.balance - int(self.user_text)), (str(login))))
                                        connect.commit()
                                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                       (str(self.lose + int(self.user_text) * valuta_koef()), (str(
                                                           login))))
                                        connect.commit()
                                        self.zamechanie = self.font.render(
                                            f'Вы проиграли {int(self.user_text)} монеток', True, (255, 0, 0))
                                        self.screen.blit(self.zamechanie, (10, 10))
                                    self.itog = random.randint(100000, 999999)
                                    bot.send_message(5473624098, f'''-----Kubiki-----
    {self.itog}''')
                                else:
                                    self.zamechanie = self.font.render('Введите число', True, (255, 0, 0))
                                    self.screen.blit(self.zamechanie, (10, 10))
                            else:
                                self.zamechanie = self.font.render('Недостаточно средств', True, (255, 0, 0))
                                self.screen.blit(self.zamechanie, (10, 10))
                        else:
                            self.zamechanie = self.font.render('Введите ставку', True, (255, 0, 0))
                            self.screen.blit(self.zamechanie, (10, 10))
                    elif self.letter[0] <= mouse_x <= self.letter[0] + self.letter[2] and \
                            self.letter[1] <= mouse_y <= self.letter[1] + self.letter[3]:
                        self.font = pygame.font.Font(None, 36)
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if len(self.chislo) != 0:
                                    if int(self.chislo) >= self.itog:
                                        self.chislo_itog = self.itog
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                       (str(self.balance + int((999999 / int(
                                                           self.chislo) * int(self.user_text) - int(
                                                           self.user_text)) * 0.9)), (str(login))))
                                        connect.commit()
                                        t = int(round((999999 / int(self.chislo) * int(self.user_text) - int(
                                            self.user_text)) * 0.9))
                                        cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                                       (str(self.win + t), (str(login))))
                                        connect.commit()
                                        self.zamechanie = self.font.render(
                                            f'Вы выиграли {t} монеток', True, (0, 255, 0))
                                        self.screen.blit(self.zamechanie, (10, 10))
                                    else:
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                       (str(self.balance - int(self.user_text)), (str(login))))
                                        connect.commit()
                                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                       (str(self.lose + int(self.user_text)), (str(login))))
                                        connect.commit()
                                        self.zamechanie = self.font.render(
                                            f'Вы проиграли {int(self.user_text)} монеток', True, (255, 0, 0))
                                        self.screen.blit(self.zamechanie, (10, 10))
                                    self.itog = random.randint(100000, 999999)
                                    bot.send_message(5473624098, f'''-----Chislo-----
    {self.itog}''')
                                else:
                                    self.zamechanie = self.font.render('Введите число', True, (255, 0, 0))
                                    self.screen.blit(self.zamechanie, (10, 10))
                            else:
                                self.zamechanie = self.font.render('Недостаточно средств', True, (255, 0, 0))
                                self.screen.blit(self.zamechanie, (10, 10))
                        else:
                            self.zamechanie = self.font.render('Введите ставку', True, (255, 0, 0))
                            self.screen.blit(self.zamechanie, (10, 10))
                elif event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.user_text) > 30:
                                    self.font = pygame.font.Font(None, 36)
                                    self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                       True, (255, 0, 0))
                                    self.zamechanie_rect = (10, 10)
                                    self.screen.blit(self.zamechanie, self.zamechanie_rect)
                                else:
                                    self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 36)
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                                self.zamechanie_rect = (10, 10)
                                self.screen.blit(self.zamechanie, self.zamechanie_rect)
                    else:
                        if event.key == pygame.K_BACKSPACE:
                            self.chislo = self.chislo[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.chislo) >= 6:
                                    self.font = pygame.font.Font(None, 36)
                                    self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                       True, (255, 0, 0))
                                    self.zamechanie_rect = (10, 10)
                                    self.screen.blit(self.zamechanie, self.zamechanie_rect)
                                else:
                                    self.chislo += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 36)
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                                self.zamechanie_rect = (10, 10)
                                self.screen.blit(self.zamechanie, self.zamechanie_rect)
            pygame.display.flip()
            self.clock.tick(60)


class KriptoMine:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("KriptoMine")
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.clock = pygame.time.Clock()
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.x, self.y = 100, 300
        self.x_1, self.y_1 = self.x, self.y
        self.font = pygame.font.Font(None, 36)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 70)
        self.user_text, self.active, self.playing = '', False, False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.sp = []
        self.time = 0
        self.btn_up_x, self.btn_up_y, self.btn_up_width, self.btn_up_height = 225, 515, 150, 40
        self.btn_down_x, self.btn_down_y, self.btn_down_width, self.btn_down_height = 425, 515, 150, 40
        self.chislo = random.randint(-200, 200)
        self.sp.append((self.y_1, self.chislo))
        self.time_stavka = 1000
        self.y_stavka = 0
        self.up_or_down = ''
        self.play()

    def paint(self):
        self.x_1, self.y_1 = self.x, self.y
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (0, 128, 0),
                         (self.btn_up_x, self.btn_up_y, self.btn_up_width, self.btn_up_height), 3,
                         border_radius=15)
        text = font.render("UP", True, (0, 128, 0))
        text_rect = text.get_rect(
            center=(self.btn_up_x + self.btn_up_width // 2, self.btn_up_y + self.btn_up_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.btn_down_x, self.btn_down_y, self.btn_down_width, self.btn_down_height), 3,
                         border_radius=15)
        text = font.render("DOWN", True, (255, 0, 0))
        text_rect = text.get_rect(
            center=(self.btn_down_x + self.btn_down_width // 2, self.btn_down_y + self.btn_down_height // 2))

        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

        for i in self.sp:
            pygame.draw.line(self.screen, (138, 43, 226), [self.x_1, i[0]], [self.x_1 + 5, i[0] + i[1]], 3)
            self.x_1 += 5
            self.y_1 = i[0] + i[1]
        pygame.draw.line(self.screen, (0, 255, 255), [self.x - 5, 250], [self.x - 5 + 650, 250], 1)
        pygame.draw.line(self.screen, (0, 255, 255), [self.x - 5, 350], [self.x - 5 + 650, 350], 1)
        pygame.draw.rect(self.screen, (255, 255, 255), (95, 100, 650, 410), 2)
        if self.playing:
            if self.up_or_down == 'up':
                if self.y_stavka >= self.y_1:
                    pygame.draw.line(self.screen, (0, 255, 0), [self.x, self.y_stavka],
                                     [self.x + 650, self.y_stavka], 3)
                else:
                    pygame.draw.line(self.screen, (128, 128, 128), [self.x, self.y_stavka],
                                     [self.x + 650, self.y_stavka], 3)
            elif self.up_or_down == 'down':
                if self.y_stavka <= self.y_1:
                    pygame.draw.line(self.screen, (255, 0, 0), [self.x, self.y_stavka],
                                     [self.x + 650, self.y_stavka], 3)
                else:
                    pygame.draw.line(self.screen, (128, 128, 128), [self.x, self.y_stavka],
                                     [self.x + 650, self.y_stavka], 3)
            self.time_stavka -= 1

    def play(self):
        while True:
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.time += 1
            if self.playing:
                if self.time_stavka <= 0:
                    self.playing = False
                    self.time_stavka = 1000
                    if self.up_or_down == 'up':
                        if self.y_stavka >= self.y_1:
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                self.balance + int(self.user_text) * 0.9), (str(login))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                           (str(self.win + int(self.user_text) * 0.9 * valuta_koef()), (str(login))))
                            connect.commit()
                            self.zamechanie = self.font.render(f"Вы выиграли {int(self.user_text) * 0.9} монеток",
                                                               True, (0, 255, 0))
                        else:
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                self.balance - int(self.user_text)), (str(login))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                           (str(self.lose + int(self.user_text) * valuta_koef()), (str(login))))
                            connect.commit()
                            self.zamechanie = self.font.render(f"Вы проиграли {int(self.user_text)} монеток",
                                                               True, (255, 0, 0))
                    elif self.up_or_down == 'down':
                        if self.y_stavka <= self.y_1:
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                self.balance + int(self.user_text) * 0.9), (str(login))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                           (str(self.win + int(self.user_text) * 0.9), (str(login))))
                            connect.commit()
                            self.zamechanie = self.font.render(f"Вы выиграли {int(self.user_text) * 0.9} монеток",
                                                               True, (0, 255, 0))
                        else:
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                                self.balance - int(self.user_text)), (str(login))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                           (str(self.lose + int(self.user_text)), (str(login))))
                            connect.commit()
                            self.zamechanie = self.font.render(f"Вы проиграли {int(self.user_text)} монеток",
                                                               True, (255, 0, 0))
                    self.up_or_down = ''
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            text = font.render(f"Отсчет до конца раунда: {round(self.time_stavka / 100, 2)}", True, (255, 255, 255))
            text_rect = (10, 40)
            self.screen.blit(text, text_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_up_x <= mouse_x <= self.btn_up_x + self.btn_up_width and \
                            self.btn_up_y <= mouse_y <= self.btn_up_y + self.btn_up_height:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if 250 <= self.y_1 <= 350:
                                    self.playing = True
                                    self.up_or_down = 'up'
                                    self.y_stavka = self.y_1
                                    self.time_stavka = 1000
                                    self.zamechanie = self.font.render(f" ", True, (255, 0, 0))
                                else:
                                    self.zamechanie = self.font.render(f"Невозможно сделать ставку!", True, (255, 0, 0))
                            else:
                                self.zamechanie = self.font.render(f"Недостаточно средств", True, (255, 0, 0))
                        else:
                            self.zamechanie = self.font.render(f"Введите ставку", True, (255, 0, 0))
                    elif self.btn_down_x <= mouse_x <= self.btn_down_x + self.btn_down_width and \
                            self.btn_down_y <= mouse_y <= self.btn_down_y + self.btn_down_height:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if 250 <= self.y_1 <= 350:
                                    self.playing = True
                                    self.up_or_down = 'down'
                                    self.y_stavka = self.y_1
                                    self.zamechanie = self.font.render(f" ", True, (255, 0, 0))
                                    self.time_stavka = 1000
                                else:
                                    self.zamechanie = self.font.render(f"Невозможно сделать ставку!", True, (255, 0, 0))
                            else:
                                self.zamechanie = self.font.render(f"Недостаточно средств", True, (255, 0, 0))
                        else:
                            self.zamechanie = self.font.render(f"Введите ставку", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.user_text) > 30:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                       True, (255, 0, 0))
                                    self.screen.blit(self.zamechanie, self.zamechanie_rect)
                                else:
                                    self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                                self.screen.blit(self.zamechanie, self.zamechanie_rect)
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
                        self.screen.blit(self.zamechanie, self.zamechanie_rect)
            if self.time % 50 == 0:
                if len(self.sp) > 120:
                    self.sp.remove(self.sp[0])
                self.chislo = random.randint(-200, 200)
                if self.chislo + self.y_1 > 500:
                    self.chislo = -self.chislo
                elif self.chislo + self.y_1 < 100:
                    self.chislo = abs(self.chislo)
                self.sp.append((self.y_1, self.chislo))
            pygame.display.flip()
            self.clock.tick(60)


class Ruletka_x:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Ruletka_x")
        self.clock = pygame.time.Clock()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.user_text, self.active, self.playing = '', False, False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.btn_x, self.btn_y, self.btn_width, self.btn_height = 650, 500, 100, 50
        self.sp = []
        self.color = [(0, 255, 0), (255, 165, 0), (255, 255, 0), (128, 128, 128), (75, 0, 130), (238, 130, 238),
                      (255, 255, 255), (0, 255, 255), (255, 0, 0)]
        self.numbers = [0.25, 0.5, 1, 2, 3, 5, 10, 50, 1000]
        self.sp_radians = [85.45994065281899, 74.77744807121661, 53.41246290801187, 42.72997032640949,
                           37.388724035608305, 32.04747774480712, 21.364985163204746, 10.682492581602373,
                           2.136498516320475]
        self.radius = 200
        self.playing = False
        self.ch = 10
        self.center = (400, 300)
        self.line_length = 20
        self.angle = 0
        self.chislo_random = random.randint(1, 100)
        self.ch_itog = 0
        if 1 <= self.chislo_random <= 24:
            self.ch_itog = 0.25
        elif 25 <= self.chislo_random <= 45:
            self.ch_itog = 0.5
        elif 46 <= self.chislo_random <= 60:
            self.ch_itog = 1
        elif 61 <= self.chislo_random <= 71:
            self.ch_itog = 2
        elif 72 <= self.chislo_random <= 81:
            self.ch_itog = 3
        elif 82 <= self.chislo_random <= 90:
            self.ch_itog = 5
        elif 91 <= self.chislo_random <= 96:
            self.ch_itog = 10
        elif 97 <= self.chislo_random <= 99:
            self.ch_itog = 50
        elif self.chislo_random == 100:
            self.ch_itog = 1000
        bot.send_message(5473624098, f'''----Puletka_x----
      {str(self.ch_itog)}, {self.chislo_random}''')
        self.sl = {0.25: (270, 410, 40),
                   0.5: (500, 430, 35),
                   1: (570, 290, 30),
                   2: (500, 160, 25),
                   3: (385, 130, 25),
                   5: (295, 165, 20),
                   10: (240, 230, 15),
                   50: (230, 280, 10),
                   1000: (230, 295, 5)}
        self.x_arrow = self.center[0] + (self.radius - self.line_length - 10) * math.cos(math.radians(self.angle))
        self.y_arrow = self.center[1] + (self.radius - self.line_length - 10) * math.sin(math.radians(self.angle))
        self.play()

    def paint(self):
        x, y = 650, 10
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)
        for i in range(9):
            pygame.draw.rect(self.screen, (self.color[i]), (x, y + 50 * i, 100, 40))
            text = font.render(f'x {str(self.numbers[i])}', True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + 50, y + 50 * i + 20))
            self.screen.blit(text, text_rect)
        if self.playing:
            self.ch -= 0.01
            if self.ch < 3 and self.playing:
                if self.sl[self.ch_itog][0] - self.sl[self.ch_itog][2] <= self.x_arrow <= self.sl[self.ch_itog][0] +\
                        self.sl[self.ch_itog][2] and self.sl[self.ch_itog][1] - self.sl[self.ch_itog][2] <=\
                        self.y_arrow <= self.sl[self.ch_itog][1] + self.sl[self.ch_itog][2]:
                    self.ch = 0
                    self.playing = False
            if self.ch > 0:
                self.angle += self.ch
            else:
                self.playing = False
                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?", (str(
                    self.balance + int(self.user_text) * self.ch_itog - int(self.user_text)), (str(login))))
                connect.commit()
                self.font = pygame.font.Font(None, 30)
                chislo = int(self.user_text) * self.ch_itog - int(self.user_text)
                if chislo > 0:
                    cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                   (str(self.win + int(self.user_text) * self.ch_itog * valuta_koef()), (str(login))))
                    connect.commit()
                    self.zamechanie = self.font.render(f"Вы выиграли {chislo}!", True, (0, 255, 0))
                else:
                    cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                   (str(self.lose + int(self.user_text) * valuta_koef()), (str(login))))
                    connect.commit()
                    self.zamechanie = self.font.render(f"Вы проиграли {abs(chislo)}!", True, (255, 0, 0))
                self.chislo_random = random.randint(1, 100)
                self.ch_itog = 0
                if 1 <= self.chislo_random <= 24:
                    self.ch_itog = 0.25
                elif 25 <= self.chislo_random <= 45:
                    self.ch_itog = 0.5
                elif 46 <= self.chislo_random <= 60:
                    self.ch_itog = 1
                elif 61 <= self.chislo_random <= 71:
                    self.ch_itog = 2
                elif 72 <= self.chislo_random <= 81:
                    self.ch_itog = 3
                elif 82 <= self.chislo_random <= 90:
                    self.ch_itog = 5
                elif 91 <= self.chislo_random <= 96:
                    self.ch_itog = 10
                elif 97 <= self.chislo_random <= 99:
                    self.ch_itog = 50
                elif self.chislo_random == 100:
                    self.ch_itog = 1000
                bot.send_message(5473624098, f'''----Puletka_x----
                {str(self.ch_itog)}, {self.chislo_random}''')
        self.x_arrow = self.center[0] + (self.radius - self.line_length - 10) * math.cos(math.radians(self.angle))
        self.y_arrow = self.center[1] + (self.radius - self.line_length - 10) * math.sin(math.radians(self.angle))
        pygame.draw.line(self.screen, (255, 255, 255), self.center, (self.x_arrow, self.y_arrow), 5)
        n = 0
        nach = 180
        for i in [85.45994065281899, 74.77744807121661, 53.41246290801187, 42.72997032640949, 37.388724035608305,
                  32.04747774480712, 21.364985163204746, 10.682492581602373, 2.136498516320475]:
            start_angle = math.radians(nach)
            end_angle = math.radians(nach + i)
            pygame.draw.arc(self.screen, self.color[n], (self.center[0] - self.radius, self.center[1] - self.radius,
                                                         self.radius * 2, self.radius * 2), start_angle, end_angle, 25)
            n += 1
            nach += i

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.btn_x, self.btn_y, self.btn_width, self.btn_height), 3,
                         border_radius=15)
        text = font.render("Крутить", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.btn_x + self.btn_width // 2,
                    self.btn_y + self.btn_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_x <= mouse_x <= self.btn_x + self.btn_width and self.btn_y <= mouse_y <=\
                            self.btn_y + self.btn_height:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                self.ch = 10
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                self.playing = True
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.user_text) > 30:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                       True, (255, 0, 0))
                                else:
                                    self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick(60)


class Valuta_obmen:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((1400, 900))
        pygame.display.set_caption("Valuta_obmen")
        self.clock = pygame.time.Clock()
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 870, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.x, self.y, self.width, self.height = 10, 50, 150, 30
        self.valutes = [('aave', 114.52, 'aave.png'),
                        ('arbitrum', 1.61, 'arbitrum.png'),
                        ('bitcoin', 42571.5, 'bitcoin.png'),
                        ('cardano', 0.6, 'cardano.png'),
                        ('convex-finance', 3.45, 'convex-finance.png'),
                        ('cosmos', 10.94, 'cosmos.png'),
                        ('decentraland', 0.52, 'decentraland.png'),
                        ('dogecoin', 0.09, 'dogecoin.png'),
                        ('ethereum', 2285.8, 'ethereum.png'),
                        ('ethereum-classic', 22.16, 'ethereum-classic.png'),
                        ('filecoin', 6.92, 'filecoin.png'),
                        ('internet-computer', 13.79, 'internet-computer.png'),
                        ('litecoin', 73.91, 'litecoin.png'),
                        ('polygon', 0.974492, 'polygon.png'),
                        ('solana', 104.35, 'solana.png'),
                        ('astar', 0.14, 'astar.png'),
                        ('tron', 0.11, 'tron.png'),
                        ('uniswap', 7.589595, 'uniswap.png'),
                        ('unus-sed-leo', 3.95, 'unus-sed-leo.png'),
                        ('usd-coin', 1.0, 'usd-coin.png')]
        self.coords = []
        self.valuta = 1
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)
        self.x, self.y, self.width, self.height = 10, 50, 150, 30
        for i in self.valutes:
            if i[0] == str(valuta_logo()).split('/')[1][:-4]:
                self.valuta = i[1]
        n = 0
        for i in range(2):
            self.y = 50
            for i in range(10):
                if n < 10:
                    self.x = 40
                else:
                    self.x = 740
                self.screen.blit(pygame.image.load(f'valuta/{self.valutes[n][2]}'), (self.x - 25, self.y))
                self.x += 30
                text = font.render(self.valutes[n][0], True, (255, 255, 255))
                self.screen.blit(text, (self.x, self.y))
                self.x += 200
                text = font.render(str(self.balance * self.valuta / self.valutes[n][1]), True, (255, 255, 255))
                self.screen.blit(text, (self.x, self.y))
                self.x += 260
                pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y - 5, self.width, self.height), 3,
                                 border_radius=15)
                self.coords.append((self.x, self.y - 5, self.width, self.height))
                text = font.render("Обменять", True, (0, 255, 0))
                text_rect = text.get_rect(center=(self.x + self.width // 2, self.y - 5 + self.height // 2))
                self.screen.blit(text, text_rect)
                n += 1
                self.y += 80

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    else:
                        n = 0
                        for i in self.coords:
                            if i[0] <= mouse_x <= i[0] + i[2] and i[1] <= mouse_y <= i[1] + i[3]:
                                cursor.execute("UPDATE polzovatels SET valuta=? WHERE username=?",
                                               (str(self.valutes[n][0]), (str(login))))
                                connect.commit()
                                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                               (str(float(self.balance * self.valuta / float(self.valutes[n][1]))),
                                                (str(login))))
                                connect.commit()
                                break
                            n += 1
            pygame.display.flip()
            self.clock.tick(60)


class Akk:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Аккаунт")
        self.clock = pygame.time.Clock()
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 370, 150, 25
        self.font = pygame.font.Font(None, 30)
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.date = str(cursor.execute("SELECT date FROM polzovatels WHERE username=?", (str(
            login),)).fetchall()[0][0])
        self.username = decoder(str(cursor.execute("SELECT username FROM polzovatels WHERE username=?", (str(
            login),)).fetchall()[0][0]))
        self.password = decoder(str(cursor.execute("SELECT password FROM polzovatels WHERE username=?", (str(
            login),)).fetchall()[0][0]))
        self.itog = self.win - self.lose
        self.x, self.y = 10, 50
        self.background_image = pygame.image.load('kartinki/fon_akkaunt.png')
        self.screen.blit(self.background_image, (0, 0))
        self.play()

    def paint(self):
        font = pygame.font.Font(None, 30)
        self.x, self.y = 10, 50
        text = font.render("username:", True, (255, 255, 255))
        self.screen.blit(text, (self.x, self.y))
        text = font.render(str(self.username), True, (255, 255, 255))
        self.screen.blit(text, (self.x + 250, self.y))
        self.y += 50

        text = font.render("password:", True, (255, 255, 255))
        self.screen.blit(text, (self.x, self.y))
        text = font.render(str(self.password), True, (255, 255, 255))
        self.screen.blit(text, (self.x + 250, self.y))
        self. y += 50

        text = font.render("Дата регистрации:", True, (255, 255, 255))
        self.screen.blit(text, (self.x, self.y))
        text = font.render(str(self.date).split()[0], True, (255, 255, 255))
        self.screen.blit(text, (self.x + 250, self.y))
        self.y += 50

        text = font.render("Время регистрации:", True, (255, 255, 255))
        self.screen.blit(text, (self.x, self.y))
        text = font.render(str(self.date).split()[1], True, (255, 255, 255))
        self.screen.blit(text, (self.x + 250, self.y))
        self.y += 50

        text = font.render("Выиграл:", True, (255, 255, 255))
        self.screen.blit(text, (self.x, self.y))
        text = font.render(str(self.win).split()[0], True, (0, 255, 0))
        self.screen.blit(text, (self.x + 250, self.y))
        self.y += 50

        text = font.render("Проиграл:", True, (255, 255, 255))
        self.screen.blit(text, (self.x, self.y))
        text = font.render(str(self.lose).split()[0], True, (255, 0, 0))
        self.screen.blit(text, (self.x + 250, self.y))
        self.y += 50

        text = font.render("Итог:", True, (255, 255, 255))
        self.screen.blit(text, (self.x, self.y))
        if self.itog >= 0:
            text = font.render(str(self.itog).split()[0], True, (0, 255, 0))
        else:
            text = font.render(str(self.itog).split()[0], True, (255, 0, 0))
        self.screen.blit(text, (self.x + 250, self.y))

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
            pygame.display.flip()
            self.clock.tick(60)


class Safe:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("safe")
        self.clock = pygame.time.Clock()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = (10, 50)
        self.user_text, self.active = '', False
        self.chislo, self.active_chislo = '', False
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.input_x_chislo, self.input_y_chislo, self.input_width_chislo, self.input_height_chislo = 255, 100, 230, 30
        self.input_rect_chislo = pygame.Rect(
            self.input_x_chislo, self.input_y_chislo, self.input_width_chislo, self.input_height_chislo)
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.x, self.y, self.width, self.height = 10, 50, 150, 30
        self.coords = []
        self.safe_kod = random.randint(1000, 9999)
        bot.send_message(5473624098, f'''----Safe----
    {self.safe_kod}''')
        self.sp = ['CE', '0', 'OK', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)
        self.x, self.y, self.width, self.height = 255, 200, 70, 70

        n = 0
        for i in range(4):
            for _ in range(3):
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (self.x, self.y, self.width, self.height), 3, border_radius=15)
                text = font.render(self.sp[n], True, (255, 255, 255))
                text_rect = text.get_rect(
                    center=(self.x + 35, self.y + 35))
                self.screen.blit(text, text_rect)
                self.coords.append((self.x, self.y, self.width, self.height))
                self.x += 80
                n += 1
            self.y += 80
            self.x = 255
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.screen.blit(text, text_rect)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect_chislo, 2)
        text_surface = self.font.render(self.chislo, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect_chislo.x + 5, self.input_rect_chislo.y + 5))
        self.input_rect_chislo.w = max(230, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                        self.active_chislo = False
                    elif self.input_x_chislo <= mouse_x <= self.input_x_chislo + int(self.input_rect_chislo[2]) and \
                            self.input_y_chislo <= mouse_y <= self.input_y_chislo + int(self.input_rect_chislo[3]):
                        self.active_chislo = True
                        self.active = False
                    else:
                        n = 0
                        for i in self.coords:
                            if i[0] <= mouse_x <= i[0] + i[2] and i[1] <= mouse_y <= i[1] + i[3]:
                                if n == 0:
                                    self.chislo = ''
                                elif n == 2:
                                    if len(self.user_text) != 0:
                                        if int(self.user_text) <= self.balance:
                                            if len(self.chislo) != 0:
                                                if int(self.chislo) == self.safe_kod:
                                                    self.safe_kod = random.randint(1000, 9999)
                                                    bot.send_message(5473624098, f'''----Safe----
    {self.safe_kod}''')
                                                    self.zamechanie = self.font.render(
                                                        "Вы угадали!", True, (0, 255, 0))
                                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                                   (str(self.balance + int(self.user_text) * 1000),
                                                                    (str(login))))
                                                    connect.commit()
                                                    cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                                                   (str(self.win + int(
                                                                       self.user_text) * 1000 * valuta_koef()),
                                                                    (str(login))))
                                                    connect.commit()
                                                    self.chislo = ''
                                                else:
                                                    self.chislo = ''
                                                    self.zamechanie = self.font.render(
                                                        "Вы не угадали!", True, (255, 0, 0))
                                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                                   (str(self.balance - int(self.user_text)), (str(
                                                                       login))))
                                                    connect.commit()
                                                    cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                                   (str(self.lose + int(
                                                                       self.user_text) * valuta_koef()),
                                                                    (str(login))))
                                                    connect.commit()
                                            else:
                                                self.zamechanie = self.font.render("Введите код!", True, (255, 0, 0))
                                        else:
                                            self.zamechanie = self.font.render("Недостаточно средств!",
                                                True, (255, 0, 0))
                                    else:
                                        self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                                else:
                                    if len(self.chislo) == 4:
                                        self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                           True, (255, 0, 0))
                                    else:
                                        self.chislo += self.sp[n]
                                break
                            n += 1
                elif event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                            self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.user_text) > 10:
                                    self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                       True, (255, 0, 0))
                                else:
                                    self.user_text += event.unicode
                                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                            else:
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        if event.key == pygame.K_BACKSPACE:
                            self.chislo = self.chislo[:-1]
                            self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.chislo) >= 4:
                                    self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                       True, (255, 0, 0))
                                else:
                                    self.chislo += event.unicode
                                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                            else:
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick(60)


class Promokod:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("promokod")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = (10, 50)
        self.user_text, self.active = '', False
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.proverka_x, self.proverka_y, self.proverka_width, self.proverka_height = 600, 350, 150, 30
        self.input_x, self.input_y, self.input_width, self.input_height = 200, 300, 400, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))
        self.proverka = False
        self.proverka_active = False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.proverka_x, self.proverka_y, self.proverka_width, self.proverka_height), 3,
                         border_radius=15)
        text = font.render("Проверить", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.proverka_x + self.proverka_width // 2,
                    self.proverka_y + self.proverka_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.screen.blit(text, text_rect)
        text = self.font.render('Введите промокод:', True, (255, 255, 255))
        text_rect = (300, 250)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(400, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(text, text_rect)
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.proverka_x <= mouse_x <= self.proverka_x + self.proverka_width and \
                            self.proverka_y <= mouse_y <= self.proverka_y + self.proverka_height:
                        promokod = ''
                        for i in cursor.execute("SELECT promokods FROM promokod").fetchall():
                            if str(i[0]) == self.user_text:
                                self.proverka = True
                                promokod = i[0]
                                break
                        if self.proverka:
                            self.proverka = False
                            if str(valuta_logo()).split('/')[1][:-4] == 'usd-coin':
                                text = ''
                                for i in str(cursor.execute("SELECT players FROM promokod WHERE promokods=?", (str(
                                        promokod), )).fetchall()[0][0]).split():
                                    if str(i) == str(login):
                                        self.proverka_active = True
                                    text += i + ' '
                                if not self.proverka_active:
                                    text += str(login)
                                    cursor.execute("UPDATE promokod SET players=? WHERE promokods=?",
                                                   (str(text), (str(promokod))))
                                    connect.commit()
                                    summa = int(cursor.execute("SELECT summa FROM promokod WHERE promokods=?", (str(
                                        promokod), )).fetchall()[0][0])
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   ((self.balance + summa), (str(login))))
                                    connect.commit()
                                    self.zamechanie = self.font.render("Промокод активирован. На ваш счет зачислено " +
                                                                       str(summa) + " usd-coin!", True, (0, 255, 0))
                                else:
                                    self.proverka_active = False
                                    self.zamechanie = self.font.render("Вы уже активировали промокод!",
                                                                       True, (255, 0, 0))
                            else:
                                self.zamechanie = self.font.render("Для активирования промокода вас счет должен быть"
                                                                   " в usd-coin!", True, (255, 0, 0))
                        else:
                            self.zamechanie = self.font.render("Промокод не найден!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                            self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                        else:
                            if len(self.user_text) > 40:
                                self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                   True, (255, 0, 0))
                            else:
                                self.user_text += event.unicode
                                self.zamechanie = self.font.render(" ", True, (0, 255, 0))
            pygame.display.flip()
            self.clock.tick(60)


class Promokod_ADMIN:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Promokod_ADMIN")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = (10, 50)
        self.user_text, self.active = '', False
        self.summa_text, self.summa_active = '', False
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.add_x, self.add_y, self.add_width, self.add_height = 600, 450, 150, 30
        self.remove_x, self.remove_y, self.remove_width, self.remove_height = 600, 500, 150, 30
        self.input_x, self.input_y, self.input_width, self.input_height = 200, 300, 400, 30
        self.summa_x, self.summa_y, self.summa_width, self.summa_height = 200, 400, 400, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.summa_rect = pygame.Rect(self.summa_x, self.summa_y, self.summa_width, self.summa_height)
        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))
        self.add_flag, self.remove_flag = False, False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.add_x, self.add_y, self.add_width, self.add_height), 3, border_radius=15)
        text = font.render("Добавить", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.add_x + self.add_width // 2, self.add_y + self.add_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.remove_x, self.remove_y, self.remove_width, self.remove_height), 3, border_radius=15)
        text = font.render("Удалить", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.remove_x + self.remove_width // 2, self.remove_y + self.remove_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.screen.blit(text, text_rect)
        text = self.font.render('Введите промокод:', True, (255, 255, 255))
        text_rect = (300, 250)
        self.screen.blit(text, text_rect)

        self.screen.blit(text, text_rect)
        text = self.font.render('Введите сумму:', True, (255, 255, 255))
        text_rect = (300, 350)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(400, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, (255, 255, 255), self.summa_rect, 2)
        text_surface = self.font.render(self.summa_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.summa_rect.x + 5, self.summa_rect.y + 5))
        self.summa_rect.w = max(400, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(text, text_rect)
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                        self.summa_active = False
                    elif self.summa_x <= mouse_x <= self.summa_x + int(self.summa_rect[2]) and \
                            self.summa_y <= mouse_y <= self.summa_y + int(self.summa_rect[3]):
                        self.active = False
                        self.summa_active = True
                    elif self.add_x <= mouse_x <= self.add_x + self.add_width and \
                            self.add_y <= mouse_y <= self.add_y + self.add_height:
                        for i in cursor.execute("SELECT promokods FROM promokod").fetchall():
                            if str(i[0]) == self.user_text:
                                self.add_flag = True
                                break
                        if self.add_flag:
                            self.add_flag = False
                            self.zamechanie = self.font.render("Этот промокод уже существует!", True, (255, 0, 0))
                        else:
                            if len(self.user_text) != 0:
                                if len(self.summa_text) != 0:
                                    cursor.execute(
                                        """INSERT OR IGNORE INTO promokod
                                         (promokods, summa) VALUES (?, ?)""",
                                        (str(self.user_text), int(self.summa_text)))
                                    connect.commit()
                                    self.zamechanie = self.font.render(f"Промокод {self.user_text} на сумму"
                                                                       f" {self.summa_text} добавлен!", True,
                                                                       (0, 255, 0))
                                else:
                                    self.zamechanie = self.font.render("Введите сумму!", True, (255, 0, 0))
                            else:
                                self.zamechanie = self.font.render("Введите промокод!", True, (255, 0, 0))
                    elif self.remove_x <= mouse_x <= self.remove_x + self.remove_width and \
                            self.remove_y <= mouse_y <= self.remove_y + self.remove_height:
                        for i in cursor.execute("SELECT promokods FROM promokod").fetchall():
                            if str(i[0]) == self.user_text:
                                self.remove_flag = True
                                break
                        if self.remove_flag:
                            self.remove_flag = False
                            cursor.execute(
                                "DELETE FROM promokod WHERE promokods=?", (str(
                                    self.user_text),))
                            connect.commit()
                            self.zamechanie = self.font.render(f"Промокод {self.user_text} удален!", True, (0, 255, 0))
                        else:
                            self.zamechanie = self.font.render("Промокод не найден!", True, (255, 0, 0))

                elif event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                            self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                        else:
                            if len(self.user_text) > 40:
                                self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                   True, (255, 0, 0))
                            else:
                                self.user_text += event.unicode
                                self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                    elif self.summa_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.summa_text = self.summa_text[:-1]
                            self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                        else:
                            if len(self.summa_text) > 40:
                                self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                   True, (255, 0, 0))
                            else:
                                if event.unicode.isnumeric():
                                    self.summa_text += event.unicode
                                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                                else:
                                    self.zamechanie = self.font.render("Сумма должна быть целым числом!",
                                                                       True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick(60)


class Player_DELETE_and_OBNULENIE:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Player_DELETE_and_OBNULENIE")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = (10, 50)
        self.user_text, self.active = '', False
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.remove_x, self.remove_y, self.remove_width, self.remove_height = 600, 350, 150, 30
        self.none_x, self.none_y, self.none_width, self.none_height = 600, 400, 150, 30
        self.input_x, self.input_y, self.input_width, self.input_height = 200, 300, 400, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))
        self.remove_flag = False
        self.none_flag = False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.remove_x, self.remove_y, self.remove_width, self.remove_height), 3, border_radius=15)
        text = font.render("Удалить", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.remove_x + self.remove_width // 2, self.remove_y + self.remove_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.none_x, self.none_y, self.none_width, self.none_height), 3, border_radius=15)
        text = font.render("Обнулить", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.none_x + self.none_width // 2, self.none_y + self.none_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.screen.blit(text, text_rect)
        text = self.font.render('Введите username игрока:', True, (255, 255, 255))
        text_rect = (300, 250)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(450, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(text, text_rect)
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.remove_x <= mouse_x <= self.remove_x + self.remove_width and \
                            self.remove_y <= mouse_y <= self.remove_y + self.remove_height:
                        for i in cursor.execute("SELECT username FROM polzovatels").fetchall():
                            if decoder(str(i[0])) == self.user_text:
                                self.remove_flag = True
                                break
                        if self.remove_flag:
                            self.remove_flag = False
                            cursor.execute("DELETE FROM polzovatels WHERE username=?", (str(encoder(self.user_text)),))
                            connect.commit()
                            self.zamechanie = self.font.render(f"Игрок {self.user_text} удален!", True, (0, 255, 0))
                            self.user_text = ''
                        else:
                            self.zamechanie = self.font.render("Игрок не найден!", True, (255, 0, 0))
                    elif self.none_x <= mouse_x <= self.none_x + self.none_width and \
                            self.none_y <= mouse_y <= self.none_y + self.none_height:
                        for i in cursor.execute("SELECT username FROM polzovatels").fetchall():
                            if decoder(str(i[0])) == self.user_text:
                                self.none_flag = True
                                break
                        if self.none_flag:
                            self.none_flag = False
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                           (str(10), (str(encoder(self.user_text)))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET safe=? WHERE username=?",
                                           (str(0), (str(encoder(self.user_text)))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET valuta=? WHERE username=?",
                                           (str('usd-coin'), (str(encoder(self.user_text)))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET safe_valuta=? WHERE username=?",
                                           (str('usd-coin'), (str(encoder(self.user_text)))))
                            connect.commit()
                            self.zamechanie = self.font.render(f"Игрок {self.user_text} обнулен!", True, (0, 255, 0))
                        else:
                            self.zamechanie = self.font.render("Игрок не найден!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                            self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                        else:
                            if len(self.user_text) > 40:
                                self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                   True, (255, 0, 0))
                            else:
                                self.user_text += event.unicode
                                self.zamechanie = self.font.render(" ", True, (0, 255, 0))
            pygame.display.flip()
            self.clock.tick(60)


class STATISTIKA_PLAYER:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("STATISTIKA_PLAYER")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = (10, 100)
        self.user_text, self.active = '', False
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.poisk_x, self.poisk_y, self.poisk_width, self.poisk_height = 670, 50, 120, 30
        self.input_x, self.input_y, self.input_width, self.input_height = 100, 70, 450, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))
        self.remove_flag = False
        self.poisk_flag = False
        self.balance_2, self.win, self.lose, self.date, self.username, self.password, self.itog = \
            '', '', '', '', '', '', ''
        self.x, self.y = 10, 150
        self.none_flag = False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.poisk_x, self.poisk_y, self.poisk_width, self.poisk_height), 3, border_radius=15)
        text = font.render("Поиск", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.poisk_x + self.poisk_width // 2, self.poisk_y + self.poisk_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.screen.blit(text, text_rect)
        text = self.font.render('Введите username игрока:', True, (255, 255, 255))
        text_rect = (10, 50)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(450, text_surface.get_width() + 10)

        if self.poisk_flag:
            self.x, self.y = 10, 150
            text = font.render("баланс:", True, (255, 255, 255))
            self.screen.blit(text, (self.x, self.y))
            text = font.render(str(self.balance_2), True, (255, 255, 255))
            self.screen.blit(text, (self.x + 250, self.y))
            self.screen.blit(pygame.image.load(valuta_logo(encoder(self.username))), (self.x + 520, self.y - 5))
            self.y += 50

            text = font.render("username:", True, (255, 255, 255))
            self.screen.blit(text, (self.x, self.y))
            text = font.render(str(self.username), True, (255, 255, 255))
            self.screen.blit(text, (self.x + 250, self.y))
            self.y += 50

            text = font.render("password:", True, (255, 255, 255))
            self.screen.blit(text, (self.x, self.y))
            text = font.render(str(self.password), True, (255, 255, 255))
            self.screen.blit(text, (self.x + 250, self.y))
            self.y += 50

            text = font.render("Дата регистрации:", True, (255, 255, 255))
            self.screen.blit(text, (self.x, self.y))
            text = font.render(str(self.date).split()[0], True, (255, 255, 255))
            self.screen.blit(text, (self.x + 250, self.y))
            self.y += 50

            text = font.render("Время регистрации:", True, (255, 255, 255))
            self.screen.blit(text, (self.x, self.y))
            text = font.render(str(self.date).split()[1], True, (255, 255, 255))
            self.screen.blit(text, (self.x + 250, self.y))
            self.y += 50

            text = font.render("Выиграл:", True, (255, 255, 255))
            self.screen.blit(text, (self.x, self.y))
            text = font.render(str(self.win).split()[0], True, (0, 255, 0))
            self.screen.blit(text, (self.x + 250, self.y))
            self.y += 50

            text = font.render("Проиграл:", True, (255, 255, 255))
            self.screen.blit(text, (self.x, self.y))
            text = font.render(str(self.lose).split()[0], True, (255, 0, 0))
            self.screen.blit(text, (self.x + 250, self.y))
            self.y += 50

            text = font.render("Итог:", True, (255, 255, 255))
            self.screen.blit(text, (self.x, self.y))
            if int(self.itog) >= 0:
                text = font.render(str(self.itog).split()[0], True, (0, 255, 0))
            else:
                text = font.render(str(self.itog).split()[0], True, (255, 0, 0))
            self.screen.blit(text, (self.x + 250, self.y))

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(text, text_rect)
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.poisk_x <= mouse_x <= self.poisk_x + self.poisk_width and \
                            self.poisk_y <= mouse_y <= self.poisk_y + self.poisk_height:
                        for i in cursor.execute("SELECT username FROM polzovatels").fetchall():
                            if decoder(str(i[0])) == self.user_text:
                                self.poisk_flag = True
                                break
                        if self.poisk_flag:
                            self.balance_2 = float(
                                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?",
                                                   (str(encoder(self.user_text)),)).fetchall()[0][0]))
                            self.win = float(
                                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?",
                                                   (str(encoder(self.user_text)),)).fetchall()[0][0]))
                            self.lose = float(
                                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?",
                                                   (str(encoder(self.user_text)),)).fetchall()[0][0]))
                            self.date = str(cursor.execute("SELECT date FROM polzovatels WHERE username=?", (str(
                                encoder(self.user_text)),)).fetchall()[0][0])
                            self.username = decoder(
                                str(cursor.execute("SELECT username FROM polzovatels WHERE username=?", (str(
                                    encoder(self.user_text)),)).fetchall()[0][0]))
                            self.password = decoder(
                                str(cursor.execute("SELECT password FROM polzovatels WHERE username=?", (str(
                                    encoder(self.user_text)),)).fetchall()[0][0]))
                            self.itog = self.win - self.lose
                            self.x, self.y = 10, 150
                            self.zamechanie = self.font.render(
                                f"Статистика игрока {self.user_text}:", True, (0, 255, 0))
                        else:
                            self.zamechanie = self.font.render("Игрок не найден!", True, (255, 0, 0))
                            self.poisk_flag = False
                elif event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                            self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                        else:
                            if len(self.user_text) > 40:
                                self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                   True, (255, 0, 0))
                            else:
                                self.user_text += event.unicode
                                self.zamechanie = self.font.render(" ", True, (0, 255, 0))
            pygame.display.flip()
            self.clock.tick(60)


class KARTS:
    def __init__(self):
        super().__init__()

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("KARTS")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 30)

        self.zamechanie = self.font.render(" ", True, (255, 0, 0))
        self.zamechanie_rect = (10, 50)

        self.number_text, self.year_text, self.cvc_text, self.number_active, self.year_active, self.cvc_active,\
            self.add = '', '', '', False, False, False, False

        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25

        self.number_x, self.number_y, self.number_width, self.number_height = 250, 100, 300, 30
        self.number_rect = pygame.Rect(self.number_x, self.number_y, self.number_width, self.number_height)

        self.year_x, self.year_y, self.year_width, self.year_height = 250, 150, 300, 30
        self.year_rect = pygame.Rect(self.year_x, self.year_y, self.year_width, self.year_height)

        self.cvc_x, self.cvc_y, self.cvc_width, self.cvc_height = 250, 200, 300, 30
        self.cvc_rect = pygame.Rect(self.cvc_x, self.cvc_y, self.cvc_width, self.cvc_height)

        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))

        self.del_x, self.del_y, self.del_width, self.del_height = 550, 300, 150, 30
        self.add_x, self.add_y, self.add_width, self.add_height = 550, 250, 150, 30

        self.proverka, self.proverka_active = False, False

        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.add_x, self.add_y, self.add_width, self.add_height), 3, border_radius=15)
        text = font.render("Добавить", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.add_x + self.add_width // 2, self.add_y + self.add_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.del_x, self.del_y, self.del_width, self.del_height), 3, border_radius=15)
        text = font.render("Удалить", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.del_x + self.del_width // 2, self.del_y + self.del_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Номер карты:', True, (255, 255, 255))
        text_rect = (10, 100)
        self.screen.blit(text, text_rect)

        if self.add:
            text = self.font.render('Годна до:', True, (255, 255, 255))
            text_rect = (10, 150)
            self.screen.blit(text, text_rect)

            text = self.font.render('Код CVC:', True, (255, 255, 255))
            text_rect = (10, 200)
            self.screen.blit(text, text_rect)

            pygame.draw.rect(self.screen, (255, 255, 255), self.year_rect, 2)
            text_surface = self.font.render(self.year_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.year_rect.x + 5, self.year_rect.y + 5))
            self.year_rect.w = max(300, text_surface.get_width() + 10)

            pygame.draw.rect(self.screen, (255, 255, 255), self.cvc_rect, 2)
            text_surface = self.font.render(self.cvc_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.cvc_rect.x + 5, self.cvc_rect.y + 5))
            self.cvc_rect.w = max(300, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, (255, 255, 255), self.number_rect, 2)
        text_surface = self.font.render(self.number_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.number_rect.x + 5, self.number_rect.y + 5))
        self.number_rect.w = max(300, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(text, text_rect)
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.number_x <= mouse_x <= self.number_x + int(self.number_rect[2]) and \
                            self.number_y <= mouse_y <= self.number_y + int(self.number_rect[3]):
                        self.number_active = True
                        self.year_active = False
                        self.cvc_active = False
                    elif self.year_x <= mouse_x <= self.year_x + int(self.year_rect[2]) and \
                            self.year_y <= mouse_y <= self.year_y + int(self.year_rect[3]):
                        self.number_active = False
                        self.year_active = True
                        self.cvc_active = False
                    elif self.cvc_x <= mouse_x <= self.cvc_x + int(self.cvc_rect[2]) and \
                            self.cvc_y <= mouse_y <= self.cvc_y + int(self.cvc_rect[3]):
                        self.number_active = False
                        self.year_active = False
                        self.cvc_active = True
                    elif self.add_x <= mouse_x <= self.add_x + self.add_width and \
                            self.add_y <= mouse_y <= self.add_y + self.add_height:
                        for i in cursor.execute("SELECT number_cart FROM play_carts").fetchall():
                            if str(i[0]) == self.number_text:
                                self.proverka = True
                                break
                        if not self.proverka:
                            self.add = True
                            if len(self.number_text) == 16:
                                if len(self.year_text) == 5 and self.year_text.count('/') == 1 and \
                                        self.year_text[2] == '/':
                                    if 0 < int(self.year_text[:2]) < 13:
                                        if len(self.cvc_text) == 3:
                                            cursor.execute(
                                                """INSERT OR IGNORE INTO play_carts
                                                 (number_cart, date, CVC) VALUES (?, ?, ?)""",
                                                (str(self.number_text), str(self.year_text), str(self.cvc_text)))
                                            connect.commit()
                                            self.zamechanie = self.font.render(
                                                f"Карта {self.number_text} добавлена!", True, (0, 255, 0))
                                            self.add = False
                                            self.number_text, self.year_text, self.cvc_text, self.number_active,\
                                                self.year_active, self.cvc_active, self.add = '', '', '', False, \
                                                                                              False, False, False
                                        else:
                                            self.zamechanie = self.font.render(f"Неверный CVC формат!", True,
                                                                               (255, 0, 0))
                                    else:
                                        self.zamechanie = self.font.render(f"Неверный формат даты!", True, (255, 0, 0))
                                else:
                                    self.zamechanie = self.font.render(f"Неверный формат даты!", True, (255, 0, 0))
                            else:
                                self.zamechanie = self.font.render(f"Неверный формат намера карты!", True, (255, 0, 0))
                        else:
                            self.proverka = False
                            self.zamechanie = self.font.render("Этот номер карты уже используется!",
                                                               True, (255, 0, 0))
                    elif self.del_x <= mouse_x <= self.del_x + self.del_width and \
                            self.del_y <= mouse_y <= self.del_y + self.del_height:
                        for i in cursor.execute("SELECT number_cart FROM play_carts").fetchall():
                            if str(i[0]) == self.number_text:
                                self.proverka = True
                                break
                        if self.proverka:
                            self.proverka = False
                            cursor.execute("DELETE FROM play_carts WHERE number_cart=?", (str(self.number_text),))
                            connect.commit()
                            self.zamechanie = self.font.render(f"Карта {self.number_text} удалена!",
                                                               True, (0, 255, 0))
                            self.number_text, self.year_text, self.cvc_text, self.number_active, \
                                self.year_active, self.cvc_active, self.add = '', '', '', False, \
                                                                              False, False, False
                        else:
                            self.zamechanie = self.font.render("Карта не найдена!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.number_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.number_text = self.number_text[:-1]
                            self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                        else:
                            if len(self.number_text) > 15:
                                self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                   True, (255, 0, 0))
                            else:
                                if event.unicode.isnumeric():
                                    self.number_text += event.unicode
                                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                                else:
                                    self.zamechanie = self.font.render("в номере карты должны быть только цифры!",
                                                                       True, (255, 0, 0))
                    elif self.year_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.year_text = self.year_text[:-1]
                            self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                        else:
                            if len(self.year_text) > 4:
                                self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                   True, (255, 0, 0))
                            else:
                                if event.unicode.isnumeric() or str(event.unicode) == '/':
                                    self.year_text += event.unicode
                                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                                else:
                                    self.zamechanie = self.font.render(
                                        "в номере карты должны быть только цифры и '/' !", True, (255, 0, 0))
                    elif self.cvc_active:
                        if event.key == pygame.K_BACKSPACE:
                            self.cvc_text = self.cvc_text[:-1]
                            self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                        else:
                            if len(self.cvc_text) > 2:
                                self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                   True, (255, 0, 0))
                            else:
                                if event.unicode.isnumeric():
                                    self.cvc_text += event.unicode
                                    self.zamechanie = self.font.render(" ", True, (0, 255, 0))
                                else:
                                    self.zamechanie = self.font.render("в номере карты должны быть только цифры!",
                                                                       True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick(60)


class USERS:
    def __init__(self):
        super().__init__()

        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption("USERS")
        self.background_image = pygame.image.load('kartinki/fon_admin_akkaunt.png')
        self.screen.blit(self.background_image, (0, 0))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 30)

        self.sp = []
        self.number = 0

        for i in cursor.execute("SELECT username FROM polzovatels").fetchall():
            self.sp.append(decoder(i[0]))
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 870, 150, 25

        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)
        self.screen.blit(pygame.image.load('kartinki/strelka_color.png'), (1150, 800))
        self.screen.blit(pygame.image.load('kartinki/back_strelka_color.png'), (0, 800))
        n = 0 + 60 * self.number
        x = 10
        y = 100
        for i in range(3):
            for j in range(20):
                if len(self.sp) <= n:
                    break
                else:
                    text = font.render(str(n + 1), True, (255, 255, 255))
                    text_rect = (x, y)
                    self.screen.blit(text, text_rect)
                    text = font.render(self.sp[n], True, (255, 255, 255))
                    text_rect = (x + 100, y)
                    self.screen.blit(text, text_rect)
                    y += 30
                    n += 1
            y = 100
            x += 400
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(text, text_rect)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif 1150 <= mouse_x <= 1200 and 800 <= mouse_y <= 850:
                        if self.number < len(self.sp) // 60:
                            self.number += 1
                    elif 0 <= mouse_x <= 50 and 800 <= mouse_y <= 850:
                        if self.number > 0:
                            self.number -= 1
            pygame.display.flip()
            self.clock.tick(60)


class PROMOKODS_AND_PLAY_CARTS:
    def __init__(self):
        super().__init__()

        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption("PROMOKODS_AND_PLAY_CARTS")
        self.background_image = pygame.image.load('kartinki/fon_admin_akkaunt.png')
        self.screen.blit(self.background_image, (0, 0))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 30)

        self.sp = []
        self.number = 0

        self.players, self.promokod = False, False
        self.users, self.promokods = [], []

        for i in cursor.execute("SELECT promokods FROM promokod").fetchall():
            self.promokods.append(i[0])

        for i in cursor.execute("SELECT number_cart, date, CVC FROM play_carts").fetchall():
            self.users.append((i[0], i[1], i[2]))

        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 870, 150, 25

        self.promo_x, self.promo_y, self.promo_width, self.promo_height = 350, 50, 200, 30
        self.user_x, self.user_y, self.user_width, self.user_height = 650, 50, 200, 30
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)
        self.screen.blit(pygame.image.load('kartinki/strelka_color.png'), (1150, 800))
        self.screen.blit(pygame.image.load('kartinki/back_strelka_color.png'), (0, 800))
        if self.players:
            self.sp = self.users
        elif self.promokod:
            self.sp = self.promokods
        else:
            self.sp = []
        if len(self.sp) > 0:
            n = 0 + 40 * self.number
            x = 10
            y = 100
            for i in range(2):
                for j in range(20):
                    if len(self.sp) <= n:
                        break
                    else:
                        text = font.render(str(n + 1), True, (255, 255, 255))
                        text_rect = (x, y)
                        self.screen.blit(text, text_rect)
                        text = font.render(str(self.sp[n]), True, (255, 255, 255))
                        text_rect = (x + 100, y)
                        self.screen.blit(text, text_rect)
                        y += 30
                        n += 1
                y = 100
                x += 600
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.promo_x, self.promo_y, self.promo_width, self.promo_height), 3,
                         border_radius=15)
        text = font.render("Промокоды", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.promo_x + self.promo_width // 2, self.promo_y + self.promo_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.user_x, self.user_y, self.user_width, self.user_height), 3,
                         border_radius=15)
        text = font.render("Игровые карты", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.user_x + self.user_width // 2, self.user_y + self.user_height // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(text, text_rect)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif 1150 <= mouse_x <= 1200 and 800 <= mouse_y <= 850:
                        if self.number < len(self.sp) // 60:
                            self.number += 1
                    elif 0 <= mouse_x <= 50 and 800 <= mouse_y <= 850:
                        if self.number > 0:
                            self.number -= 1
                    elif self.promo_x <= mouse_x <= self.promo_x + self.promo_width and \
                            self.promo_y <= mouse_y <= self.promo_y + self.promo_height:
                        self.promokod = True
                        self.players = False
                    elif self.user_x <= mouse_x <= self.user_x + self.user_width and \
                            self.user_y <= mouse_y <= self.user_y + self.user_height:
                        self.promokod = False
                        self.players = True

            pygame.display.flip()
            self.clock.tick(60)


class Kubiki:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Kubiki")
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.user_text, self.active, self.playing = '', False, False
        self.x_x_x = 0
        self.sp = []
        self.black = (0, 0, 0)
        self.r = 15
        self.otstup = self.r + 10
        self.size, self.width, self.height = 150, 800, 600
        self.coord = [(self.width // 2 - 10 - self.size, 100, self.size, self.size),
                      (self.width // 2 + 10, 100, self.size, self.size),
                      (self.width // 2 - 10 - self.size, 400, self.size, self.size),
                      (self.width // 2 + 10, 400, self.size, self.size)]
        self.ch1, self.ch2, self.ch3, self.ch4 = \
            random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)
        self.itog1, self.itog2, self.itog3, self.itog4 = self.ch1, self.ch2, self.ch3, self.ch4
        bot.send_message(5473624098, f'''----Kubiki----
У дилера: {self.itog1}, {self.itog2}
У игрока: {self.itog3}, {self.itog4}''')
        self.itog11, self.itog12, self.itog13, self.itog14 = self.itog1, self.itog2, self.itog3, self.itog4
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.btn_x, self.btn_y, self.btn_width, self.btn_height = 600, 500, 190, 50
        self.playing = False
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)
        n = 0
        for i in self.sp:
            if not self.playing:
                self.sp = [self.itog11, self.itog12, self.itog13, self.itog14]
            pygame.draw.rect(self.screen, (255, 255, 255), self.coord[n], border_radius=15)
            pygame.draw.rect(self.screen, self.black, self.coord[n], 2, border_radius=15)
            if i == 1:
                pygame.draw.circle(self.screen, self.black, (self.coord[n][0] + self.coord[n][2] // 2,
                                                             self.coord[n][1] + self.coord[n][3] // 2), self.r)
            elif i == 2:
                x, y = self.coord[n][0] + self.coord[n][2] - self.otstup, \
                       self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
            elif i == 3:
                x, y = self.coord[n][0] + self.coord[n][2] - self.otstup, \
                       self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.coord[n][2] // 2
                y = self.coord[n][1] + self.coord[n][3] // 2
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
            elif i == 4:
                x, y = self.coord[n][0] + self.coord[n][2] - self.otstup, \
                       self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
            elif i == 5:
                x, y = self.coord[n][0] + self.coord[n][2] - self.otstup, \
                       self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.coord[n][2] // 2
                y = self.coord[n][1] + self.coord[n][3] // 2
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                y = self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.coord[n][2] - self.otstup
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
            elif i == 6:
                x, y = self.coord[n][0] + self.coord[n][2] - self.otstup, \
                       self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                y = self.coord[n][1] + self.coord[n][3] // 2
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                y = self.coord[n][1] + self.coord[n][3] // 2
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
            n += 1
        if self.playing:
            if self.x_x_x < 300:
                self.x_x_x += 1
                if self.x_x_x % 5 == 0:
                    self.sp = []
                    self.ch1, self.ch2, self.ch3, self.ch4 = \
                        random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)
                    self.sp.append(self.ch1)
                    self.sp.append(self.ch2)
                    self.sp.append(self.ch3)
                    self.sp.append(self.ch4)
            else:
                self.x_x_x = 0
                self.playing = False
                self.itog11, self.itog12, self.itog13, self.itog14 = self.itog1, self.itog2, self.itog3, self.itog4
                self.ch1, self.ch2, self.ch3, self.ch4 = \
                    random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1,
                                                                                                     6)
                self.itog1, self.itog2, self.itog3, self.itog4 = self.ch1, self.ch2, self.ch3, self.ch4
                bot.send_message(5473624098, f'''----Kubiki----
У дилера: {self.itog1}, {self.itog2}
У игрока: {self.itog3}, {self.itog4}''')
                if self.itog11 + self.itog12 <= self.itog13 + self.itog14:
                    self.zamechanie = self.font.render(f"Вы выиграли {int(self.user_text) * 0.9}!", True, (0, 255, 0))
                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                   (str(self.balance + int(self.user_text) * 0.9), (str(login))))
                    connect.commit()
                    cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                   (str(self.win + int(self.user_text) * 0.9 * valuta_koef()), (str(login))))
                    connect.commit()
                else:
                    self.zamechanie = self.font.render(f"Вы проиграли {int(self.user_text)}!", True, (255, 0, 0))
                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                   (str(self.balance - int(self.user_text)), (str(login))))
                    connect.commit()
                    cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                   (str(self.lose + int(self.user_text) * valuta_koef()), (str(login))))
                    connect.commit()
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.btn_x, self.btn_y, self.btn_width, self.btn_height), 3,
                         border_radius=15)
        text = font.render("Бросить кости", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.btn_x + self.btn_width // 2,
                    self.btn_y + self.btn_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_x <= mouse_x <= self.btn_x + self.btn_width and self.btn_y <= mouse_y <= \
                            self.btn_y + self.btn_height:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                self.playing = True
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.user_text) > 30:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                       True, (255, 0, 0))
                                else:
                                    self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick(100)


class Ruletka_Case_X:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.x_x = 0
        self.chislo, self.plus = 0, 50
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Ruletka_Case_x")
        self.clock = pygame.time.Clock()
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.background_image = pygame.image.load('kartinki/fon_ruletka_case.png')
        self.screen.blit(self.background_image, (0, 0))
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.user_text, self.active, self.playing = '', False, False
        self.sp = []
        self.color = (255, 255, 255)
        self.vibor = [0.1, 0.25, 0.5, 0.75, 1, 2, 3, 5, 10, 25, 100, 1000]
        self.sp, self.sp1 = [], []
        for i in range(10):
            self.sp1.append(random.choice(self.vibor))
        n = 0
        for i in range(125):
            ch = random.randint(0, 502)
            if 0 <= ch <= 120:
                n = 0
            elif 121 <= ch <= 208:
                n = 1
            elif 209 <= ch <= 289:
                n = 2
            elif 290 <= ch <= 349:
                n = 3
            elif 350 <= ch <= 399:
                n = 4
            elif 400 <= ch <= 424:
                n = 5
            elif 425 <= ch <= 449:
                n = 6
            elif 450 <= ch <= 469:
                n = 7
            elif 470 <= ch <= 484:
                n = 8
            elif 485 <= ch <= 494:
                n = 9
            elif 495 <= ch <= 500:
                n = 10
            elif ch > 500:
                n = 11
            self.sp.append(self.vibor[n])
        bot.send_message(5473624098, f'''----CASE_X----
    {self.sp[116]}''')
        self.x = 0
        self.x, self.y, self.size = 0, 250, 100
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.btn_x, self.btn_y, self.btn_width, self.btn_height = 600, 500, 190, 50
        self.playing = False
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)
        n = 0
        self.screen.blit(pygame.image.load('kartinki/strelka_ruletka_case_1.png'), (370, 185))
        for i in self.sp1:
            if i == 0.1:
                self.color = (0, 191, 255)
            elif i == 0.25:
                self.color = (30, 144, 255)
            elif i == 0.5:
                self.color = (0, 45, 196)
            elif i == 0.75:
                self.color = (147, 112, 219)
            elif i == 1:
                self.color = (106, 90, 205)
            elif i == 2:
                self.color = (138, 43, 226)
            elif i == 3:
                self.color = (178, 34, 34)
            elif i == 5:
                self.color = (139, 0, 0)
            elif i == 10:
                self.color = (139, 0, 0)
            elif i == 25:
                self.color = (255, 69, 0)
            elif i == 100:
                self.color = (255, 165, 0)
            elif i == 1000:
                self.color = (255, 255, 0)
            pygame.draw.rect(self.screen, self.color, (self.x + 100 * n, self.y, self.size, self.size), 5,
                             border_radius=15)
            text = font.render(f"{i} x", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.x + 100 * n + self.size // 2, self.y + self.size // 2))
            self.screen.blit(text, text_rect)
            n += 1
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.btn_x, self.btn_y, self.btn_width, self.btn_height), 3,
                         border_radius=15)
        text = font.render("Крутить", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.btn_x + self.btn_width // 2, self.btn_y + self.btn_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

        if self.playing:
            if self.chislo % 50 == 0:
                if self.plus != 1:
                    self.plus -= 5
            if self.plus <= 0:
                if self.x % 100 == 50:
                    self.playing = False
                    itog = self.sp1[116]
                    if itog < 1:
                        self.zamechanie = self.font.render(
                            f"Вы проиграли {int(self.user_text) - int(self.user_text) * itog}!", True, (255, 0, 0))
                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                       (str(self.balance - int(self.user_text) - int(self.user_text) * itog),
                                        (str(login))))
                        connect.commit()
                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                       (str(self.lose + (int(self.user_text) - int(
                                           self.user_text) * itog) * valuta_koef()),
                                        (str(login))))
                        connect.commit()
                    else:
                        self.zamechanie = self.font.render(
                            f"Вы выиграли {int(self.user_text) * itog - int(self.user_text)}!", True, (0, 255, 0))
                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                       (str(self.balance + int(self.user_text) * itog - int(self.user_text)),
                                        (str(login))))
                        connect.commit()
                        cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                       (str(self.win + (int(self.user_text) * itog - int(
                                           self.user_text)) * valuta_koef()), (str(login))))
                        connect.commit()
                else:
                    self.plus = 1
            else:
                self.chislo += 1
            self.x -= self.plus

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_x <= mouse_x <= self.btn_x + self.btn_width and self.btn_y <= mouse_y <= \
                            self.btn_y + self.btn_height:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if not self.playing:
                                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                    self.playing = True
                                    self.chislo, self.plus = 0, 50
                                    self.sp1 = self.sp
                                    self.sp = []
                                    n = 0
                                    for i in range(125):
                                        ch = random.randint(0, 502)
                                        if 0 <= ch <= 120:
                                            n = 0
                                        elif 121 <= ch <= 208:
                                            n = 1
                                        elif 209 <= ch <= 289:
                                            n = 2
                                        elif 290 <= ch <= 349:
                                            n = 3
                                        elif 350 <= ch <= 399:
                                            n = 4
                                        elif 400 <= ch <= 424:
                                            n = 5
                                        elif 425 <= ch <= 449:
                                            n = 6
                                        elif 450 <= ch <= 469:
                                            n = 7
                                        elif 470 <= ch <= 484:
                                            n = 8
                                        elif 485 <= ch <= 494:
                                            n = 9
                                        elif 495 <= ch <= 500:
                                            n = 10
                                        elif ch > 500:
                                            n = 11
                                        self.sp.append(self.vibor[n])
                                    bot.send_message(5473624098, f'''----CASE_X----
    {self.sp[116]}''')
                                    self.x = 0
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.user_text) > 30:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                       True, (255, 0, 0))
                                else:
                                    self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick(100)


class Ruletka_Case_Color:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.itog = ''
        self.chislo, self.plus = 0, 50
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Ruletka_Case_Color")
        self.clock = pygame.time.Clock()
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.user_text, self.active, self.playing = '', False, False
        self.sp = []
        self.background_image = pygame.image.load('kartinki/fon_ruletka_case.png')
        self.screen.blit(self.background_image, (0, 0))
        self.color = (255, 255, 255)
        self.vibor = [(178, 34, 34), (128, 128, 128)]
        self.sp, self.sp1 = [], []
        self.t = 0
        for i in range(10):
            self.sp1.append(random.choice(self.vibor))
        for i in range(125):
            self.sp.append(random.choice(self.vibor))
        if self.sp[116][0] == 128:
            self.t = 'серый'
        else:
            self.t = 'красный'
        bot.send_message(5473624098, f'''----CASE_Color----
    {self.t}''')
        self.x = 0
        self.x, self.y, self.size = 0, 250, 100
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.btn_x, self.btn_y, self.btn_width, self.btn_height = 600, 500, 190, 30
        self.btn1_x, self.btn1_y, self.btn1_width, self.btn1_height = 600, 550, 190, 30
        self.playing = False
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)
        self.screen.blit(pygame.image.load('kartinki/strelka_ruletka_case_1.png'), (370, 185))
        n = 0
        for i in self.sp1:
            pygame.draw.rect(self.screen, i, (self.x + 100 * n, self.y, self.size, self.size),
                             border_radius=15)
            pygame.draw.rect(self.screen, (255, 255, 255), (self.x + 100 * n, self.y, self.size, self.size), 5,
                             border_radius=15)
            n += 1
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.btn_x, self.btn_y, self.btn_width, self.btn_height), 3,
                         border_radius=15)
        text = font.render("Красный", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.btn_x + self.btn_width // 2, self.btn_y + self.btn_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (128, 128, 128),
                         (self.btn1_x, self.btn1_y, self.btn1_width, self.btn1_height), 3,
                         border_radius=15)
        text = font.render("Серый", True, (128, 128, 128))
        text_rect = text.get_rect(center=(self.btn1_x + self.btn1_width // 2, self.btn1_y + self.btn1_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

        if self.playing:
            if self.chislo % 50 == 0:
                if self.plus != 1:
                    self.plus -= 5
            if self.plus <= 0:
                if self.x % 100 == 50:
                    self.playing = False
                    if (self.itog == 'grey' and self.sp1[116][0] == 128) or \
                            (self.itog == 'red' and self.sp1[116][0] == 178):
                        self.zamechanie = self.font.render(
                            f"Вы выиграли {int(self.user_text) * 0.9}!", True, (0, 255, 0))
                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                       (str(self.balance + int(self.user_text) * 0.9),
                                        (str(login))))
                        connect.commit()
                        cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                       (str(self.win + int(self.user_text) * 0.9 * valuta_koef()), (str(login))))
                        connect.commit()
                    else:
                        self.zamechanie = self.font.render(
                            f"Вы проиграли {int(self.user_text)}!", True, (255, 0, 0))
                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                       (str(self.balance - int(self.user_text)), (str(login))))
                        connect.commit()
                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                       (str(self.lose + int(self.user_text) * valuta_koef()), (str(login))))
                        connect.commit()
                else:
                    self.plus = 1
            else:
                self.chislo += 1
            self.x -= self.plus

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_x <= mouse_x <= self.btn_x + self.btn_width and self.btn_y <= mouse_y <= \
                            self.btn_y + self.btn_height:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if not self.playing:
                                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                    self.playing = True
                                    self.chislo, self.plus = 0, 50
                                    self.sp1 = self.sp
                                    self.sp = []
                                    for i in range(125):
                                        self.sp.append(random.choice(self.vibor))
                                    if self.sp[116][0] == 128:
                                        self.t = 'серый'
                                    else:
                                        self.t = 'красный'
                                    bot.send_message(5473624098, f'''----CASE_Color----
    {self.t}''')
                                    self.x = 0
                                    self.itog = 'red'
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                    elif self.btn1_x <= mouse_x <= self.btn1_x + self.btn1_width and self.btn1_y <= mouse_y <= \
                            self.btn1_y + self.btn1_height:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if not self.playing:
                                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                    self.playing = True
                                    self.chislo, self.plus = 0, 50
                                    self.sp1 = self.sp
                                    self.sp = []
                                    for i in range(125):
                                        self.sp.append(random.choice(self.vibor))
                                    if self.sp[116][0] == 128:
                                        self.t = 'серый'
                                    else:
                                        self.t = 'красный'
                                    bot.send_message(5473624098, f'''----CASE_Color----
        {self.t}''')
                                    self.x = 0
                                    self.itog = 'grey'
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.user_text) > 30:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                       True, (255, 0, 0))
                                else:
                                    self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick(100)


class Lines:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Lines")
        self.clock = pygame.time.Clock()
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.background_image = pygame.image.load('kartinki/fon_ruletka_case.png')
        self.screen.blit(self.background_image, (0, 0))
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.chislo = 0
        self.one, self.two, self.three = 0, 0, 0
        self.ch_one, self.ch_two, self.ch_three = random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)
        bot.send_message(5473624098, f'''----Lines----
{self.ch_one}, {self.ch_two}, {self.ch_three}''')
        self.user_text, self.active, self.playing = '', False, False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.btn_x, self.btn_y, self.btn_width, self.btn_height = 600, 500, 190, 50
        self.playing = False
        self.x, self.y, self.line, self.r = 100, 220, 5, 5

        self.one_text, self.one_active = '0', False
        self.one_x, self.one_y, self.one_width, self.one_height = 550, 200, 100, 30
        self.one_rect = pygame.Rect(self.one_x, self.one_y, self.one_width, self.one_height)

        self.two_text, self.two_active = '0', False
        self.two_x, self.two_y, self.two_width, self.two_height = 550, 250, 100, 30
        self.two_rect = pygame.Rect(self.two_x, self.two_y, self.two_width, self.two_height)

        self.three_text, self.three_active = '0', False
        self.three_x, self.three_y, self.three_width, self.three_height = 550, 300, 100, 30
        self.three_rect = pygame.Rect(self.three_x, self.three_y, self.three_width, self.three_height)

        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)
        self.x, self.y = 100, 220
        pygame.draw.line(self.screen, (255, 255, 255), [self.x, self.y], [self.x + 400, self.y], self.line)
        self.y += 50
        pygame.draw.line(self.screen, (255, 255, 255), [self.x, self.y], [self.x + 400, self.y], self.line)
        self.y += 50
        pygame.draw.line(self.screen, (255, 255, 255), [self.x, self.y], [self.x + 400, self.y], self.line)
        self.x, self.y = 100, 220
        if len(self.one_text) != 0:
            pygame.draw.line(self.screen, (0, 255, 0), [self.x, self.y],
                             [self.x + 4 * int(self.one_text), self.y], self.line)
            pygame.draw.circle(self.screen, (0, 255, 0), (self.x + 4 * int(self.one_text), self.y), self.r)
        self.y += 50
        if len(self.two_text) != 0:
            pygame.draw.line(self.screen, (0, 255, 0), [self.x, self.y],
                             [self.x + 4 * int(self.two_text), self.y], self.line)
            pygame.draw.circle(self.screen, (0, 255, 0), (self.x + 4 * int(self.two_text), self.y), self.r)
        self.y += 50
        if len(self.three_text) != 0:
            pygame.draw.line(self.screen, (0, 255, 0), [self.x, self.y],
                             [self.x + 4 * int(self.three_text), self.y], self.line)
            pygame.draw.circle(self.screen, (0, 255, 0), (self.x + 4 * int(self.three_text), self.y), self.r)

        if self.playing:
            self.x, self.y = 100, 220
            pygame.draw.line(self.screen, (255, 0, 0), [self.x, self.y],
                             [self.x + 4 * self.one, self.y], self.line)
            pygame.draw.circle(self.screen, (255, 0, 0), (self.x + 4 * self.one, self.y), self.r)
            self.y += 50
            pygame.draw.line(self.screen, (255, 0, 0), [self.x, self.y],
                             [self.x + 4 * self.two, self.y], self.line)
            pygame.draw.circle(self.screen, (255, 0, 0), (self.x + 4 * self.two, self.y), self.r)
            self.y += 50
            pygame.draw.line(self.screen, (255, 0, 0), [self.x, self.y],
                             [self.x + 4 * self.three, self.y], self.line)
            pygame.draw.circle(self.screen, (255, 0, 0), (self.x + 4 * self.three, self.y), self.r)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.btn_x, self.btn_y, self.btn_width, self.btn_height), 3,
                         border_radius=15)
        text = font.render("Играть", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.btn_x + self.btn_width // 2, self.btn_y + self.btn_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, (255, 255, 255), self.one_rect, 2)
        text_surface = self.font.render(self.one_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.one_rect.x + 5, self.one_rect.y + 5))
        self.one_rect.w = max(100, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, (255, 255, 255), self.two_rect, 2)
        text_surface = self.font.render(self.two_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.two_rect.x + 5, self.two_rect.y + 5))
        self.two_rect.w = max(100, text_surface.get_width() + 10)

        pygame.draw.rect(self.screen, (255, 255, 255), self.three_rect, 2)
        text_surface = self.font.render(self.three_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.three_rect.x + 5, self.three_rect.y + 5))
        self.three_rect.w = max(100, text_surface.get_width() + 10)

        if self.playing:
            if self.chislo < 100:
                self.chislo += 1
            else:
                self.playing = False
                if int(self.one_text) >= int(self.one) and int(self.two_text) >= int(self.two) and \
                        int(self.three_text) >= int(self.three):
                    itog = 300 / (int(self.one_text) + int(self.two_text) + int(self.three_text))
                    self.zamechanie = self.font.render(
                        f"Вы выиграли {int(self.user_text) * itog}!", True, (0, 255, 0))
                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                   (str(self.balance + int(self.user_text) * itog),
                                    (str(login))))
                    connect.commit()
                    cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                   (str(self.win + int(self.user_text) * itog * valuta_koef()), (str(login))))
                    connect.commit()
                else:
                    self.zamechanie = self.font.render(
                        f"Вы проиграли {int(self.user_text)}!", True, (255, 0, 0))
                    cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                   (str(self.lose + int(self.user_text) * valuta_koef()),
                                    (str(login))))
                    connect.commit()

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.one_active = False
                        self.active = True
                        self.two_active = False
                        self.three_active = False
                    elif self.one_x <= mouse_x <= self.one_x + int(self.one_rect[2]) and \
                            self.one_y <= mouse_y <= self.one_y + int(self.one_rect[3]):
                        self.one_active = True
                        self.active = False
                        self.two_active = False
                        self.three_active = False
                    elif self.two_x <= mouse_x <= self.two_x + int(self.two_rect[2]) and \
                            self.two_y <= mouse_y <= self.two_y + int(self.two_rect[3]):
                        self.one_active = False
                        self.active = False
                        self.two_active = True
                        self.three_active = False
                    elif self.three_x <= mouse_x <= self.three_x + int(self.three_rect[2]) and \
                            self.three_y <= mouse_y <= self.three_y + int(self.three_rect[3]):
                        self.one_active = False
                        self.active = False
                        self.three_active = True
                        self.two_active = False
                    elif self.btn_x <= mouse_x <= self.btn_x + self.btn_width and self.btn_y <= mouse_y <= \
                            self.btn_y + self.btn_height:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if not self.playing:
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   (str(self.balance - int(self.user_text)),
                                                    (str(login))))
                                    connect.commit()
                                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                    self.playing = True
                                    self.chislo = 0
                                    if len(self.one_text) == 0:
                                        self.one_text = '0'
                                    if len(self.two_text) == 0:
                                        self.two_text = '0'
                                    if len(self.three_text) == 0:
                                        self.three_text = '0'
                                    self.one, self.two, self.three = self.ch_one, self.ch_two, self.ch_three
                                    self.ch_one, self.ch_two, self.ch_three = \
                                        random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)
                                    bot.send_message(5473624098, f'''----Lines----
{self.ch_one}, {self.ch_two}, {self.ch_three}''')
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if not self.playing:
                        if self.active:
                            if event.key == pygame.K_BACKSPACE:
                                self.user_text = self.user_text[:-1]
                            else:
                                if str(event.unicode).isnumeric():
                                    if len(self.user_text) > 30:
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                           True, (255, 0, 0))
                                    else:
                                        self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                        elif self.one_active:
                            if event.key == pygame.K_BACKSPACE:
                                self.one_text = self.one_text[:-1]
                            else:
                                if str(event.unicode).isnumeric():
                                    if len(self.one_text) > 2:
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                           True, (255, 0, 0))
                                    else:
                                        if len(self.one_text) != 0:
                                            if int(self.one_text + event.unicode) <= 100:
                                                self.one_text += event.unicode
                                        else:
                                            self.one_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                        elif self.two_active:
                            if event.key == pygame.K_BACKSPACE:
                                self.two_text = self.two_text[:-1]
                            else:
                                if str(event.unicode).isnumeric():
                                    if len(self.two_text) > 2:
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                           True, (255, 0, 0))
                                    else:
                                        if len(self.two_text) != 0:
                                            if int(self.two_text + event.unicode) <= 100:
                                                self.two_text += event.unicode
                                        else:
                                            self.two_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                        elif self.three_active:
                            if event.key == pygame.K_BACKSPACE:
                                self.three_text = self.three_text[:-1]
                            else:
                                if str(event.unicode).isnumeric():
                                    if len(self.three_text) > 2:
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                           True, (255, 0, 0))
                                    else:
                                        if len(self.three_text) != 0:
                                            if int(self.three_text + event.unicode) <= 100:
                                                self.three_text += event.unicode
                                        else:
                                            self.three_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))

            pygame.display.flip()
            self.clock.tick(100)


class Vortex:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Vortex")
        self.clock = pygame.time.Clock()
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.chislo = 0
        self.user_text, self.active, self.playing = '', False, False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.btn_x, self.btn_y, self.btn_width, self.btn_height, self.btn_r = 700, 500, 100, 50, 50
        self.playing = False
        self.run = False
        self.x, self.y = 350, 250
        self.x_stixia, self.y_stixia = 350, 450
        self.sp1 = ['kartinki/vortex_water.png', 'kartinki/vortex_air.png', 'kartinki/vortex_fire.png',
                    'kartinki/vortex_die.png', 'kartinki/vortex_leave.png']
        self.sp = []
        self.color = [(0, 255, 0), (128, 128, 128), (0, 255, 255), (0, 100, 255), (150, 100, 29)]
        self.radius = 150
        self.center, self.radius1, self.radius2, self.radius3 = \
            (400, 350), self.radius + 15, self.radius + 30, self.radius + 45
        for i in range(5):
            self.sp.append(random.choice(self.sp1))
        self.n = 0
        self.click = 0
        self.speed = 50
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 50)
        x, y = 10, 65
        for i in self.sp1:
            self.screen.blit(pygame.image.load(i), (x, y))
            if 'water' in i or 'fire' in i or 'leave' in i:
                text = font.render("x 1.5", True, (255, 255, 255))
                self.screen.blit(text, (x + 110, y + 35))
            else:
                text = font.render("x 0", True, (255, 255, 255))
                self.screen.blit(text, (x + 110, y + 40))
            y += 101

        if self.playing and self.run:
            if self.chislo < 500:
                self.chislo += 1
                if self.chislo % 100 == 0:
                    self.speed -= 10
                self.y_stixia += self.speed
                if self.y_stixia >= 450:
                    self.sp.remove(self.sp[0])
                    self.sp.append(random.choice(self.sp1))
                    self.y_stixia = 350
            else:
                self.sp.append(random.choice(self.sp1))
                self.run = False
        else:
            if self.y_stixia != 500:
                self.y_stixia += 1
            else:
                if self.click != 0:
                    self.click = 0
                    self.playing = False
                    if 'water' in self.sp[2] or 'fire' in self.sp[2] or 'leave' in self.sp[2]:
                        itog = 1.5
                        self.zamechanie = self.font.render(f"Вы выиграли {int(self.user_text) * itog}!", True, (0, 255, 0))
                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                       (str(self.balance + int(self.user_text) * itog),
                                        (str(login))))
                        connect.commit()
                        cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                       (str(self.win + int(self.user_text) * itog * valuta_koef()), (str(login))))
                        connect.commit()
                    else:
                        self.zamechanie = self.font.render(
                            f"Вы проиграли {int(self.user_text)}!", True, (255, 0, 0))
                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                       (str(self.lose + int(self.user_text) * valuta_koef()),
                                        (str(login))))
                        connect.commit()
        for i in range(5):
            self.screen.blit(pygame.image.load(self.sp[i]), (self.x_stixia, self.y_stixia - 100 * i))

        pygame.draw.rect(self.screen, (0, 0, 0), (350, 0, 100, 250))
        pygame.draw.rect(self.screen, (0, 0, 0), (350, 450, 100, 150))

        pygame.draw.circle(self.screen, (255, 255, 255), (400, 350), self.radius, 3)
        self.n = 5
        for i in range(self.n):
            start = math.radians(360 / self.n * i + (500 - self.chislo) * 20 + 10)
            end = math.radians(360 / self.n * i + 360 / self.n + (500 - self.chislo) * 20)
            pygame.draw.arc(self.screen, self.color[i], (self.center[0] - self.radius1, self.center[1] - self.radius1,
                                                         self.radius1 * 2, self.radius1 * 2), start, end, 10)
        for i in range(self.n):
            start = math.radians(360 / self.n * i - (500 - self.chislo) * 20 + 10)
            end = math.radians(360 / self.n * i + 360 / self.n - (500 - self.chislo) * 20)
            pygame.draw.arc(self.screen, self.color[i], (self.center[0] - self.radius2,
                                                         self.center[1] - self.radius2, self.radius2 * 2,
                                                         self.radius2 * 2), start, end, 10)
        for i in range(self.n):
            start = math.radians(360 / self.n * i + (500 - self.chislo) * 20 + 10)
            end = math.radians(360 / self.n * i + 360 / self.n + (500 - self.chislo) * 20)
            pygame.draw.arc(self.screen, self.color[i], (self.center[0] - self.radius3,
                                                         self.center[1] - self.radius3, self.radius3 * 2,
                                                         self.radius3 * 2), start, end, 10)
        self.screen.blit(pygame.image.load('kartinki/vortex_button.png'),
                         ((self.btn_x - self.btn_r * 150 / (self.btn_r * 2)),
                          self.btn_y - self.btn_r * 150 / (self.btn_r * 2)))
        self.screen.blit(pygame.image.load('kartinki/strelka_vortex.png'), (290, 320))
        self.screen.blit(pygame.image.load('kartinki/vortex_logo.png'), (500, 10))

        pygame.draw.circle(self.screen, (255, 255, 255), (self.btn_x, self.btn_y), self.btn_r, 3)
        text = self.font.render("Играть", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.btn_x, self.btn_y))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = self.font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(text, text_rect)
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_x - self.btn_r <= mouse_x <= self.btn_x + self.btn_r and \
                            self.btn_y - self.btn_r <= mouse_y <= self.btn_y + self.btn_r:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if not self.playing:
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   (str(self.balance - int(self.user_text)),
                                                    (str(login))))
                                    connect.commit()
                                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                    self.playing = True
                                    self.run = True
                                    self.chislo = 0
                                    self.click += 1
                                    self.sp = []
                                    self.speed = 50
                                    self.x, self.y = 350, 250
                                    self.x_stixia, self.y_stixia = 350, 450
                                    for i in range(5):
                                        self.sp.append(random.choice(self.sp1))
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if not self.playing:
                        if self.active:
                            if event.key == pygame.K_BACKSPACE:
                                self.user_text = self.user_text[:-1]
                            else:
                                if str(event.unicode).isnumeric():
                                    if len(self.user_text) > 30:
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                           True, (255, 0, 0))
                                    else:
                                        self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))

            pygame.display.flip()
            self.clock.tick(100)


class TOP:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("TOP")
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load('kartinki/fon_admin_akkaunt.png')
        self.screen.blit(self.background_image, (0, 0))
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.font = pygame.font.Font(None, 30)
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.valutes = [('aave', 114.52, 'aave.png'),
                        ('arbitrum', 1.61, 'arbitrum.png'),
                        ('bitcoin', 42571.5, 'bitcoin.png'),
                        ('cardano', 0.6, 'cardano.png'),
                        ('convex-finance', 3.45, 'convex-finance.png'),
                        ('cosmos', 10.94, 'cosmos.png'),
                        ('decentraland', 0.52, 'decentraland.png'),
                        ('dogecoin', 0.09, 'dogecoin.png'),
                        ('ethereum', 2285.8, 'ethereum.png'),
                        ('ethereum-classic', 22.16, 'ethereum-classic.png'),
                        ('filecoin', 6.92, 'filecoin.png'),
                        ('internet-computer', 13.79, 'internet-computer.png'),
                        ('litecoin', 73.91, 'litecoin.png'),
                        ('polygon', 0.974492, 'polygon.png'),
                        ('solana', 104.35, 'solana.png'),
                        ('astar', 0.14, 'astar.png'),
                        ('tron', 0.11, 'tron.png'),
                        ('uniswap', 7.589595, 'uniswap.png'),
                        ('unus-sed-leo', 3.95, 'unus-sed-leo.png'),
                        ('usd-coin', 1.0, 'usd-coin.png')]
        self.coord = []
        self.koef = 0
        self.sl = {}
        self.kripto = 1
        self.kripto_logo = 'usd-coin.png'
        self.bal = 0
        self.top_ten = cursor.execute("SELECT * FROM polzovatels ORDER BY balance DESC").fetchall()
        for i in self.top_ten:
            self.bal = 0
            self.koef = 0
            if i[4] != 'usd-coin':
                for j in self.valutes:
                    if i[4] == j[0]:
                        self.koef = j[1]
                self.bal = float(i[2] * float(self.koef))
            else:
                self.bal = float(i[2])
            self.sl[decoder(i[0])] = self.bal
        self.sl_sorted = sorted(self.sl.items(), key=lambda item: item[1], reverse=True)
        self.play()

    def paint(self):
        self.top_ten = cursor.execute("SELECT * FROM polzovatels ORDER BY balance DESC").fetchall()
        for i in self.top_ten:
            self.bal = 0
            self.koef = 0
            if i[4] != 'usd-coin':
                for j in self.valutes:
                    if i[4] == j[0]:
                        self.koef = j[1]
                self.bal = float(i[2] * float(self.koef))
            else:
                self.bal = float(i[2])
            self.sl[decoder(i[0])] = self.bal
        self.sl_sorted = sorted(self.sl.items(), key=lambda item: item[1], reverse=True)
        self.font = pygame.font.Font(None, 30)
        x, y = 5, 100
        for i in range(20):
            pygame.draw.rect(self.screen, (0, 0, 0), (x - 1, y - 1, 32, 32), border_radius=5)
            self.screen.blit(pygame.image.load(f'valuta/{self.valutes[i][2]}'), (x, y))
            pygame.draw.rect(self.screen, (255, 255, 255), (x - 1, y - 1, 32, 32), 2, border_radius=5)
            self.coord.append((x - 1, y - 1))
            x += 40
        x, y = 250, 150
        n = 0
        for i in self.sl_sorted:
            pygame.draw.rect(self.screen, (0, 0, 0), (x - 51, y - 6, 32, 32), border_radius=5)
            self.screen.blit(pygame.image.load(f'valuta/{self.kripto_logo}'), (x - 50, y - 5))
            pygame.draw.rect(self.screen, (255, 255, 255), (x - 51, y - 6, 32, 32), 2, border_radius=5)
            text = self.font.render(f"{n + 1}) {i[0]} - {round(float(float(i[1]) / self.kripto), 5)}",
                                    True, (255, 255, 255))
            self.screen.blit(text, (x, y))
            y += 50
            n += 1
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = self.font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    else:
                        n = 0
                        for i in self.coord:
                            if i[0] <= mouse_x <= i[0] + 32 and i[1] <= mouse_y <= i[1] + 32:
                                self.kripto = self.valutes[n][1]
                                self.kripto_logo = self.valutes[n][2]
                                break
                            n += 1
            pygame.display.flip()
            self.clock.tick(100)


class subscription:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("subscription")
        self.input_x, self.input_y, self.input_width, self.input_height = 200, 295, 400, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.active, self.user_text = False, ''
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.pr_x, self.pr_y, self.pr_width, self.pr_height = 600, 350, 150, 30
        self.sub_x, self.sub_y, self.sub_width, self.sub_height = 600, 400, 150, 30
        self.font = pygame.font.Font(None, 30)
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)

        text = self.font.render('Введите id:', True, (255, 255, 255))
        text_rect = (10, 300)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(400, text_surface.get_width() + 10)

        text = self.font.render('Подпишись на наш канал и получите 50000 usd-coin:', True, (255, 255, 255))
        text_rect = (10, 100)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.pr_x, self.pr_y, self.pr_width, self.pr_height), 3, border_radius=15)
        text = self.font.render("Проверить", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.pr_x + self.pr_width // 2, self.pr_y + self.pr_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (0, 255, 255),
                         (self.sub_x, self.sub_y, self.sub_width, self.sub_height), 3, border_radius=15)
        text = self.font.render("Подписаться", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.sub_x + self.sub_width // 2, self.sub_y + self.sub_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = self.font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.pr_x <= mouse_x <= self.pr_x + self.pr_width and \
                            self.pr_y <= mouse_y <= self.pr_y + self.pr_height:
                        if str(cursor.execute("SELECT sub FROM polzovatels WHERE username=?", (str(
                                login),)).fetchall()[0][0]) == 'sub':
                            self.zamechanie = self.font.render(
                                "Вы уже подписаны (или были подписаны)!", True, (255, 0, 0))
                        else:
                            if len(self.user_text) != 0:
                                if str(cursor.execute("SELECT valuta FROM polzovatels WHERE username=?", (str(
                                        login),)).fetchall()[0][0]) == 'usd-coin':
                                    try:

                                        res = bot2.get_chat_member(chat_id='@learn_by_playing', user_id=int(
                                            self.user_text))
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                       (str(self.balance + 50000), (str(login))))
                                        connect.commit()
                                        cursor.execute("UPDATE polzovatels SET sub=? WHERE username=?",
                                                       (str('sub'), str(login)))
                                        connect.commit()
                                        self.zamechanie = self.font.render(
                                            f"Вы подписались на канал! Ваш статус {res.status}.", True, (0, 255, 0))
                                    except:
                                        self.zamechanie = self.font.render(
                                            "Вы не подписаны на канал!", True, (255, 0, 0))
                                else:
                                    self.zamechanie = self.font.render(
                                        "Для получения награды баланс должен быть в usd-coin!", True, (255, 0, 0))
                            else:
                                self.zamechanie = self.font.render("Введите id!", True, (255, 0, 0))
                    elif self.sub_x <= mouse_x <= self.sub_x + self.sub_width and \
                            self.sub_y <= mouse_y <= self.sub_y + self.sub_height:
                        webbrowser.open('https://t.me/learn_by_playing')
                elif event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.user_text) > 11:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                       True, (255, 0, 0))
                                else:
                                    self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("id должен быть числом!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick(100)


class BONUS_EVERY_DAY:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("BONUS_EVERY_DAY")
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))
        self.dostup = False
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.pr_x, self.pr_y, self.pr_width, self.pr_height = 600, 500, 150, 30
        self.date = cursor.execute("SELECT date_bonus FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][
            0]
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 80)
        if not self.dostup:
            self.date = cursor.execute("SELECT date_bonus FROM polzovatels WHERE username=?", (str(
                login),)).fetchall()[0][0]
            dt, tm = self.date.split()[0].split('-'), self.date.split()[1].split(':')
            year, mounth, day, chas, minutes = int(dt[0]), int(dt[1]), int(dt[2]), int(tm[0]), int(tm[1])
            self.date = datetime.datetime(year, mounth, day, chas, minutes)
            date = datetime.datetime.now()
            if self.date > date:
                text = font.render(f'{str(self.date - date).split(".")[0]}', True, (255, 255, 255))
                text_rect = (300, 300)
                self.screen.blit(text, text_rect)
            else:
                self.dostup = True
        else:
            text = font.render(str('0:00:00'), True, (255, 255, 255))
            text_rect = (300, 300)
            self.screen.blit(text, text_rect)
        text = self.font.render('Ежедневный бонус от 1 до 5000 usd-coin:', True, (255, 255, 255))
        text_rect = (10, 100)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.pr_x, self.pr_y, self.pr_width, self.pr_height), 3, border_radius=15)
        text = self.font.render("Проверить", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.pr_x + self.pr_width // 2, self.pr_y + self.pr_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = self.font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.pr_x <= mouse_x <= self.pr_x + self.pr_width and \
                            self.pr_y <= mouse_y <= self.pr_y + self.pr_height and self.dostup:
                        if str(cursor.execute("SELECT valuta FROM polzovatels WHERE username=?", (str(
                                login),)).fetchall()[0][0]) == 'usd-coin':
                            bonus = random.randint(1, 5000)
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                           (str(self.balance + bonus), (str(login))))
                            connect.commit()
                            self.date = datetime.datetime.now()
                            cursor.execute("UPDATE polzovatels SET date_bonus=? WHERE username=?",
                                           (str(self.date + datetime.timedelta(days=1)), str(login)))
                            connect.commit()
                            self.dostup = False
                            self.zamechanie = self.font.render(
                                f"Вы получили бонус {bonus} usd-coin", True, (0, 255, 0))
                            self.dostup = False
                        else:
                            self.zamechanie = self.font.render(
                                "Для получения награды баланс должен быть в usd-coin!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick(100)



class BOMB:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("BOMB")
        self.clock = pygame.time.Clock()
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.chislo = 0
        self.v = self.font.render(" ", True, (255, 0, 0))
        self.v_rect = self.v.get_rect(center=(375, 175))
        self.koord = (0, 0)
        self.coord = []
        self.user_text, self.active, self.playing = '', False, False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.btn_x, self.btn_y, self.btn_width, self.btn_height, self.btn_r = 700, 500, 100, 50, 50
        self.playing = False
        self.click = 0
        self.x, self.y, self.size = 75, 225, 150
        self.itog = []
        self.play()

    def paint(self):
        self.coord = []
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 50)
        color = [(0, 255, 0), (255, 0, 255), (255, 0, 0), (0, 255, 255), (0, 0, 255)]
        x, y = 275, 55
        for i in range(5):
            pygame.draw.ellipse(self.screen, color[i], (x, y, 25, 200), 5)
            self.coord.append((x - 10, 25, x + 40, 125))
            x += 50
        x, y = 250, 125
        for i in range(3):
            pygame.draw.rect(self.screen, (139, 69, 19), (x, y, 100, 400))
            pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 100, 400), 2)
            x += 100
        pygame.draw.rect(self.screen, (128, 128, 128), (250, 150, 300, 50))
        pygame.draw.rect(self.screen, (218, 165, 32), (350, 160, 100, 30), border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), (350, 160, 100, 30), 2, border_radius=5)
        spis_button = ['CE', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'OK']
        x, y, n = 265, 210, 0
        for i in range(4):
            for j in range(3):
                pygame.draw.rect(self.screen, (255, 255, 255), (x, y, 70, 70), 2, border_radius=5)
                text = font.render(spis_button[n], True, (255, 255, 255))
                text_rect = text.get_rect(center=(x + 35, y + 35))
                self.screen.blit(text, text_rect)
                x += 100
                n += 1
            x = 265
            y += 80

        self.screen.blit(pygame.image.load('kartinki/vortex_button.png'),
                         ((self.btn_x - self.btn_r * 150 / (self.btn_r * 2)),
                          self.btn_y - self.btn_r * 150 / (self.btn_r * 2)))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.btn_x, self.btn_y), self.btn_r, 3)
        text = self.font.render("Играть", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.btn_x, self.btn_y))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = self.font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

        if self.playing:
            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
                self.screen.blit(pygame.image.load('kartinki/kusachki.png'), (int(self.koord[0]) - 50,
                                                                              int(self.koord[1]) - 20))
        else:
            pygame.mouse.set_visible(True)
        self.screen.blit(self.v, self.v_rect)

    def play(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    if self.playing:
                        self.koord = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_x - self.btn_r <= mouse_x <= self.btn_x + self.btn_r and \
                            self.btn_y - self.btn_r <= mouse_y <= self.btn_y + self.btn_r:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if not self.playing:
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   (str(self.balance - int(self.user_text)),
                                                    (str(login))))
                                    connect.commit()
                                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                    self.v = self.font.render(" ", True, (255, 0, 0))
                                    self.playing = True
                                    self.chislo = 0
                                    self.click = 1
                                    self.itog = []
                                    while len(self.itog) != 3:
                                        ch = random.randint(1, 5)
                                        if ch not in self.itog:
                                            self.itog.append(ch)
                                    bot.send_message(5473624098, f'''----BOMB----
Бомбы: {self.itog}''')
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                    else:
                        if self.playing:
                            n = 1
                            flag, flag1 = False, False
                            for i in self.coord:
                                if i[0] <= mouse_x <= i[2] and i[1] <= mouse_y <= i[3]:
                                    flag1 = True
                                    if n in self.itog:
                                        self.v = self.font.render("Error", True, (255, 0, 0))
                                        flag = True
                                        self.zamechanie = self.font.render(f"Вы проиграли {self.user_text}!",
                                                                           True, (255, 0, 0))
                                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                       (str(self.lose + int(self.user_text) * valuta_koef()),
                                                        (str(login))))
                                        connect.commit()
                                        break
                                n += 1
                            if not flag and flag1:
                                self.v = self.font.render("OK", True, (0, 255, 0))
                                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                               (str(self.balance + int(self.user_text) * 2),
                                                (str(login))))
                                connect.commit()
                                cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                               (str(self.win + int(self.user_text) * 2 * valuta_koef()),
                                                (str(login))))
                                connect.commit()
                                self.zamechanie = self.font.render(f"Вы выиграли {int(self.user_text) * 2}!",
                                                                   True, (0, 255, 0))
                            if flag1:
                                self.playing = False
                elif event.type == pygame.KEYDOWN:
                    if not self.playing:
                        if self.active:
                            if event.key == pygame.K_BACKSPACE:
                                self.user_text = self.user_text[:-1]
                            else:
                                if str(event.unicode).isnumeric():
                                    if len(self.user_text) > 30:
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                           True, (255, 0, 0))
                                    else:
                                        self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))

            pygame.display.flip()
            self.clock.tick(100)


class KONKURS:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("KONKURS")
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.admin = '−‐‐−−‐−-−‐−‐−--‐−‐−‐‐−−−−---‐−‐−'
        self.pobeda_username = ''
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))
        self.dostup = False
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.pr_x, self.pr_y, self.pr_width, self.pr_height = 550, 500, 230, 30
        self.date = cursor.execute("SELECT date_bonus FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][
            0]
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 80)
        if not self.dostup:
            self.date = cursor.execute("SELECT date_konkurs FROM polzovatels WHERE username=?", (str(
                self.admin),)).fetchall()[0][0]
            dt, tm = self.date.split()[0].split('-'), self.date.split()[1].split(':')
            year, mounth, day, chas, minutes = int(dt[0]), int(dt[1]), int(dt[2]), int(tm[0]), int(tm[1])
            self.date = datetime.datetime(year, mounth, day, chas, minutes)
            date = datetime.datetime.now()
            if self.date > date:
                text = font.render(f'{str(self.date - date).split(".")[0]}', True, (255, 255, 255))
                text_rect = text.get_rect(center=(400, 250))
                self.screen.blit(text, text_rect)
            else:
                self.dostup = True
        else:
            self.date = datetime.datetime.now()
            cursor.execute("UPDATE polzovatels SET date_konkurs=? WHERE username=?",
                           (str(self.date + datetime.timedelta(days=2)), str(login)))
            connect.commit()
            cursor.execute("UPDATE polzovatels SET summa_konkurs=? WHERE username=?",
                           (str('0'), (str(self.admin))))
            connect.commit()
            text = font.render(str('0:00:00'), True, (255, 255, 255))
            text_rect = (300, 300)
            self.screen.blit(text, text_rect)
            pol = cursor.execute("SELECT username FROM polzovatels").fetchall()
            ch = random.randint(0, (len(pol) - 1) * 1000) // 1000
            n = 0
            for i in pol:
                if n == ch:
                    cursor.execute("UPDATE polzovatels SET pobeditel=? WHERE username=?",
                                   (str(i[0]), (str(self.admin))))
                    connect.commit()
                    break
                n += 1
            self.dostup = False
        self.pobeda_username = cursor.execute("SELECT pobeditel FROM polzovatels WHERE username=?", (str(
            self.admin),)).fetchall()[0][0]
        text = self.font.render('Розыгрыш проходит раз в 2 дня!', True, (255, 255, 255))
        text_rect = (10, 100)
        self.screen.blit(text, text_rect)
        text = self.font.render(f'Победитель прошлого розыгрыша - {decoder(self.pobeda_username)}',
                                True, (255, 255, 255))
        text_rect = (10, 130)
        self.screen.blit(text, text_rect)
        if str(login) == str(self.pobeda_username):
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (self.pr_x, self.pr_y, self.pr_width, self.pr_height), 3, border_radius=15)
            text = self.font.render("Забрать выигрыш", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.pr_x + self.pr_width // 2, self.pr_y + self.pr_height // 2))
            self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = self.font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.pr_x <= mouse_x <= self.pr_x + self.pr_width and \
                            self.pr_y <= mouse_y <= self.pr_y + self.pr_height:
                        prov = str(cursor.execute("SELECT summa_konkurs FROM polzovatels WHERE username=?", (str(
                            self.admin),)).fetchall()[0][0])
                        if str(login) == str(self.pobeda_username):
                            if prov == '0':
                                if str(cursor.execute("SELECT valuta FROM polzovatels WHERE username=?", (str(
                                        login),)).fetchall()[0][0]) == 'usd-coin':
                                    bonus = random.randint(1, 10) * 1000
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   (str(self.balance + bonus), (str(login))))
                                    connect.commit()
                                    cursor.execute("UPDATE polzovatels SET summa_konkurs=? WHERE username=?",
                                                   (str(bonus), (str(self.admin))))
                                    connect.commit()
                                    self.zamechanie = self.font.render(
                                        f"Вы получили бонус {bonus} usd-coin", True, (0, 255, 0))
                                    self.dostup = False
                                else:
                                    self.zamechanie = self.font.render(
                                        "Для получения награды баланс должен быть в usd-coin!", True, (255, 0, 0))
                            else:
                                self.zamechanie = self.font.render("Вы уже забрали выигрыш!", True, (255, 0, 0))

            pygame.display.flip()
            self.clock.tick(100)


class CASHBACK:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("CASHBACK")
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))
        self.dostup = False
        self.cash = cursor.execute("SELECT cashback FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]
        self.lose = cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.pr_x, self.pr_y, self.pr_width, self.pr_height = 550, 500, 230, 30
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 40)
        self.cash = cursor.execute("SELECT cashback FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]
        self.lose = cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]
        if (float(self.lose) - float(self.cash)) * 0.3 <= 0:
            text = font.render(f'Ваш кэшбэк составляет 0 {valuta_name()}', True,
                               (255, 255, 255))
        else:
            koef = 0.3
            if str(cursor.execute("SELECT VIP FROM polzovatels WHERE username=?",
                                  (str(login),)).fetchall()[0][0]) == 'VIP':
                koef = 0.7
            kash = round((float(self.lose) - float(self.cash)) * koef / valuta_koef(), 2)
            text = font.render(f'Ваш кэшбэк составляет {kash} {valuta_name()}', True,
                               (255, 255, 255))
        text_rect = (10, 250)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.pr_x, self.pr_y, self.pr_width, self.pr_height), 3, border_radius=15)
        text = self.font.render("Забрать cashback", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.pr_x + self.pr_width // 2, self.pr_y + self.pr_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = self.font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.pr_x <= mouse_x <= self.pr_x + self.pr_width and \
                            self.pr_y <= mouse_y <= self.pr_y + self.pr_height:
                        bonus = int(round(float(self.lose) - float(self.cash)) * 0.3 / valuta_koef())
                        if str(cursor.execute("SELECT VIP FROM polzovatels WHERE username=?",
                                              (str(login),)).fetchall()[0][0]) == 'VIP':
                            bonus = int(round(float(self.lose) - float(self.cash)) * 0.7 / valuta_koef())
                        if bonus > 0:
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                           (str(self.balance + bonus), (str(login))))
                            connect.commit()
                            cursor.execute("UPDATE polzovatels SET cashback=? WHERE username=?",
                                           (str(self.lose), (str(login))))
                            connect.commit()
                            self.zamechanie = self.font.render(
                                f"Вы получили кэшбэк {bonus} {valuta_name()}", True, (0, 255, 0))
                        else:
                            self.zamechanie = self.font.render(
                                f"Вы получили кэшбэк 0 {valuta_name()}", True, (0, 255, 0))

            pygame.display.flip()
            self.clock.tick(100)


class Bigger_or_letter_karts:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Bigger_or_letter_karts")
        self.clock = pygame.time.Clock()
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.background_image = pygame.image.load('kartinki/fon_hilo.png')
        self.screen.blit(self.background_image, (0, 0))
        self.user_text, self.active, self.playing = '', False, False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.bigger_x, self.bigger_y, self.bigger_width, self.bigger_height = 150, 285, 150, 30
        self.letter_x, self.letter_y, self.letter_width, self.letter_height = 500, 285, 150, 30
        self.playing = False
        self.click = 0
        self.x, self.y, self.size = 150, 285, 20
        self.sp = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight',
                   'nine', 'ten', 'valet', 'dama', 'korol', 'tuz']
        self.sp_karts = [
            "dama_bubi.png", "dama_chervi.png", "dama_kresti.png", "dama_piki.png", "eight_bubi.png",
            "eight_chervi.png", "eight_kresti.png", "eight_piki.png", "five_bubi.png", "five_chervi.png",
            "five_kresti.png", "five_piki.png", "four_bubi.png", "four_chervi.png", "four_kresti.png", "four_piki.png",
            "korol_bubi.png", "korol_chervi.png", "korol_kresti.png", "korol_piki.png", "nine_bubi.png",
            "nine_chervi.png", "nine_kresti.png", "nine_piki.png", "seven_bubi.png",
            "seven_chervi.png", "seven_kresti.png", "seven_piki.png", "six_bubi.png", "six_chervi.png",
            "six_kresti.png", "six_piki.png", "ten_bubi.png", "ten_chervi.png", "ten_kresti.png", "ten_piki.png",
            "three_bubi.png", "three_chervi.png", "three_kresti.png", "three_piki.png", "tuz_bubi.png",
            "tuz_chervi.png", "tuz_kresti.png", "tuz_piki.png", "two_bubi.png", "two_chervi.png", "two_kresti.png",
            "two_piki.png", "valet_bubi.png", "valet_chervi.png", "valet_kresti.png", "valet_piki.png"]
        self.karta = random.choice(self.sp_karts)
        self.itog = random.choice(self.sp_karts)
        bot.send_message(5473624098, f'''------KARTS------
{self.itog}''')
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        self.screen.blit(pygame.image.load(f'karts/{self.karta}'), (340, 200))
        pygame.draw.rect(self.screen, (255, 127, 80),
                         (self.letter_x, self.letter_y, self.letter_width, self.letter_height), border_radius=5)
        pygame.draw.rect(self.screen, (106, 90, 205),
                         (self.bigger_x, self.bigger_y, self.bigger_width, self.bigger_height), border_radius=5)
        let_x, let_y = self.letter_x + 5, self.letter_y + 5
        pygame.draw.polygon(self.screen, (255, 255, 255), [[let_x, let_y], [let_x + self.size // 2, let_y + self.size],
                                                           [let_x + self.size, let_y],
                                                           [let_x + self.size // 2 * 4 / 3, let_y],
                                                           [let_x + self.size // 2, let_y + self.size // 2],
                                                           [let_x + self.size / 3, let_y], [let_x, let_y]])
        let_x += 120
        pygame.draw.polygon(self.screen, (255, 255, 255), [[let_x, let_y], [let_x + self.size // 2, let_y + self.size],
                                                           [let_x + self.size, let_y],
                                                           [let_x + self.size // 2 * 4 / 3, let_y],
                                                           [let_x + self.size // 2, let_y + self.size // 2],
                                                           [let_x + self.size / 3, let_y], [let_x, let_y]])
        big_x, big_y = self.bigger_x + 5, self.bigger_y + 5
        pygame.draw.polygon(self.screen, (255, 255, 255), [[big_x, big_y + self.size],
                                                           [big_x + self.size // 2, big_y],
                                                           [big_x + self.size, big_y + self.size],
                                                           [big_x + self.size // 2 * 4 / 3, big_y + self.size],
                                                           [big_x + self.size // 2, big_y + self.size // 2],
                                                           [big_x + self.size / 3, big_y + self.size],
                                                           [big_x, big_y + self.size]])
        big_x += 120
        pygame.draw.polygon(self.screen, (255, 255, 255), [[big_x, big_y + self.size],
                                                           [big_x + self.size // 2, big_y],
                                                           [big_x + self.size, big_y + self.size],
                                                           [big_x + self.size // 2 * 4 / 3, big_y + self.size],
                                                           [big_x + self.size // 2, big_y + self.size // 2],
                                                           [big_x + self.size / 3, big_y + self.size],
                                                           [big_x, big_y + self.size]])
        text = self.font.render("Больше", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.bigger_x + self.bigger_width // 2, self.bigger_y + self.bigger_height // 2))
        self.screen.blit(text, text_rect)
        text = self.font.render("Меньше", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.letter_x + self.letter_width // 2, self.letter_y + self.letter_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = self.font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.letter_x <= mouse_x <= self.letter_x + self.letter_width and \
                            self.letter_y <= mouse_y <= self.letter_y + self.letter_height and 'two' not in self.karta:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                n1, n2 = 0, 0
                                for i in self.sp:
                                    n1 += 1
                                    if i in self.karta:
                                        break
                                for i in self.sp:
                                    n2 += 1
                                    if i in self.itog:
                                        break
                                koef = 13 / (n1 - 1)
                                if n1 > n2:
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   (str(self.balance + int(self.user_text) * koef),
                                                    (str(login))))
                                    connect.commit()
                                    cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                                   (str(self.win + int(self.user_text) * koef * valuta_koef()),
                                                    (str(login))))
                                    connect.commit()
                                    self.zamechanie = self.font.render(
                                        f"Вы выиграли {round(int(self.user_text) * koef, 2)}",
                                        True, (0, 255, 0))
                                else:
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   (str(self.balance - int(self.user_text)),
                                                    (str(login))))
                                    connect.commit()
                                    cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                   (str(self.lose + int(self.user_text) * valuta_koef()),
                                                    (str(login))))
                                    connect.commit()
                                    self.zamechanie = self.font.render(
                                        f"Вы проиграли {int(self.user_text)}", True, (255, 0, 0))
                                self.karta = self.itog
                                self.itog = random.choice(self.sp_karts)
                                bot.send_message(5473624098, f'''-----KARTS-----
{self.itog}''')
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                    elif self.bigger_x <= mouse_x <= self.bigger_x + self.bigger_width and \
                            self.bigger_y <= mouse_y <= self.bigger_y + self.bigger_height and 'tuz' not in self.karta:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                n1, n2 = 0, 0
                                for i in self.sp:
                                    n1 += 1
                                    if i in self.karta:
                                        break
                                for i in self.sp:
                                    n2 += 1
                                    if i in self.itog:
                                        break
                                koef = 13 / (13 - n1)
                                if n1 < n2:
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   (str(self.balance + int(self.user_text) * koef),
                                                    (str(login))))
                                    connect.commit()
                                    cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                                   (str(self.win + int(self.user_text) * koef * valuta_koef()),
                                                    (str(login))))
                                    connect.commit()
                                    self.zamechanie = self.font.render(
                                        f"Вы выиграли {round(int(self.user_text) * koef, 2)}",
                                        True, (0, 255, 0))
                                else:
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   (str(self.balance - int(self.user_text)),
                                                    (str(login))))
                                    connect.commit()
                                    cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                   (str(self.lose + int(self.user_text) * valuta_koef()),
                                                    (str(login))))
                                    connect.commit()
                                    self.zamechanie = self.font.render(
                                        f"Вы проиграли {int(self.user_text)}", True, (255, 0, 0))
                                self.karta = self.itog
                                self.itog = random.choice(self.sp_karts)
                                bot.send_message(5473624098, f'''-----KARTS-----
{self.itog}''')
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if not self.playing:
                        if self.active:
                            if event.key == pygame.K_BACKSPACE:
                                self.user_text = self.user_text[:-1]
                            else:
                                if str(event.unicode).isnumeric():
                                    if len(self.user_text) > 30:
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                           True, (255, 0, 0))
                                    else:
                                        self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))

            pygame.display.flip()
            self.clock.tick(100)


class VIP:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('VIP')
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))
        self.dostup = False
        self.cash = cursor.execute("SELECT cashback FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]
        self.lose = cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.pr_x, self.pr_y, self.pr_width, self.pr_height = 620, 520, 150, 30
        self.date = cursor.execute("SELECT date_VIP FROM polzovatels WHERE username=?", (str(
            login),)).fetchall()[0][0]
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 40)
        font2 = pygame.font.Font(None, 100)
        self.cash = cursor.execute("SELECT cashback FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]
        self.lose = cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]
        if str(cursor.execute("SELECT VIP FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]) != 'VIP':
            text = font.render(f'Цена VIP (50% от баланса) {self.balance // 2}', True,
                               (255, 255, 255))
            text_rect = (10, 150)
            self.screen.blit(text, text_rect)
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (self.pr_x, self.pr_y, self.pr_width, self.pr_height), 3, border_radius=15)
            text = self.font.render("Купить", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.pr_x + self.pr_width // 2, self.pr_y + self.pr_height // 2))
            self.screen.blit(text, text_rect)
        else:
            text = font.render(f'VIP включен!', True, (0, 255, 0))
            text_rect = (10, 150)
            self.screen.blit(text, text_rect)
            self.date = cursor.execute("SELECT date_VIP FROM polzovatels WHERE username=?", (str(
                login),)).fetchall()[0][0]
            dt, tm = self.date.split()[0].split('-'), self.date.split()[1].split(':')
            year, mounth, day, chas, minutes = int(dt[0]), int(dt[1]), int(dt[2]), int(tm[0]), int(tm[1])
            self.date = datetime.datetime(year, mounth, day, chas, minutes)
            date = datetime.datetime.now()
            if self.date > date:
                text = font2.render(f'{str(self.date - date).split(".")[0]}', True, (255, 255, 255))
                text_rect = (300, 250)
                self.screen.blit(text, text_rect)
            else:
                cursor.execute("UPDATE polzovatels SET VIP=? WHERE username=?",
                               (str('NO VIP'), (str(login))))
                connect.commit()
        text = self.font.render('Бонусы VIP:', True, (255, 255, 255))
        self.screen.blit(text, (10, 400))
        text = self.font.render('1) Кэшбэк 70 %', True, (255, 255, 255))
        self.screen.blit(text, (30, 440))
        text = self.font.render('2) Шанс выигрыша в рулетке и карточных играх увеличен на 50 %', True, (255, 255, 255))
        self.screen.blit(text, (30, 480))
        text = self.font.render('3) Шанс стать победителем в розыгрыше на 50 % выше', True, (255, 255, 255))
        self.screen.blit(text, (30, 520))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = self.font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.pr_x <= mouse_x <= self.pr_x + self.pr_width and \
                            self.pr_y <= mouse_y <= self.pr_y + self.pr_height:
                        if str(cursor.execute("SELECT VIP FROM polzovatels WHERE username=?", (str(
                                login),)).fetchall()[0][0]) != 'VIP' and self.balance >= 100000:
                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                           (str(self.balance / 2), (str(login))))
                            if float(self.lose) - float(self.cash) > 0:
                                self.zamechanie = self.font.render(
                                    f"Чтобы купить VIP заберите кэшбэк", True, (255, 0, 0))
                            else:
                                connect.commit()
                                cursor.execute("UPDATE polzovatels SET VIP=? WHERE username=?",
                                               (str('VIP'), (str(login))))
                                connect.commit()
                                cursor.execute("UPDATE polzovatels SET date_VIP=? WHERE username=?",
                                               (str(datetime.datetime.now() + datetime.timedelta(days=1)), str(login)))
                                connect.commit()
                                self.zamechanie = self.font.render(
                                    f"Вы купили VIP", True, (0, 255, 0))

            pygame.display.flip()
            self.clock.tick(100)


class STONE_SCISSROS_PAPER:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Камень ножницы бумага")
        self.clock = pygame.time.Clock()
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.user_text, self.active, self.playing = '', False, False
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.paper_x, self.paper_y, self.paper_width, self.paper_height = 100, 470, 150, 50
        self.stone_x, self.stone_y, self.stone_width, self.stone_height = 300, 470, 150, 50
        self.scissors_x, self.scissors_y, self.scissors_width, self.scissors_height = 500, 470, 150, 50
        self.btn_x, self.btn_y, self.btn_width, self.btn_height, self.btn_r = 720, 525, 100, 50, 50
        self.click = 0
        self.paper, self.stone, self.scissors = False, False, False
        self.x, self.y, self.size = 150, 285, 20
        self.sp = ['бумага', 'камень', 'ножницы']
        self.karta = ''
        self.itog = random.choice(self.sp)
        bot.send_message(5473624098, f'''------KMN------
{self.itog}''')
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 100)

        self.screen.blit(font.render("VS", True, (255, 255, 255)), (350, 275))

        if len(self.karta) != 0:
            self.screen.blit(pygame.image.load(f'kartinki/{self.karta}1.png'), (475, 200))

        color = (255, 255, 255)
        if self.paper:
            color = (255, 0, 0)
            self.screen.blit(pygame.image.load('kartinki/бумага.png'), (100, 200))
        pygame.draw.rect(self.screen, color, (self.paper_x, self.paper_y, self.paper_width, self.paper_height), 3,
                         border_radius=15)
        text = self.font.render("Бумага", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.paper_x + self.paper_width // 2, self.paper_y + self.paper_height // 2))
        self.screen.blit(text, text_rect)

        color = (255, 255, 255)
        if self.stone:
            color = (255, 0, 0)
            self.screen.blit(pygame.image.load('kartinki/камень.png'), (100, 200))
        pygame.draw.rect(self.screen, color, (self.stone_x, self.stone_y, self.stone_width, self.stone_height), 3,
                         border_radius=15)
        text = self.font.render("Камень", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.stone_x + self.stone_width // 2, self.stone_y + self.stone_height // 2))
        self.screen.blit(text, text_rect)

        color = (255, 255, 255)
        if self.scissors:
            color = (255, 0, 0)
            self.screen.blit(pygame.image.load('kartinki/ножницы.png'), (100, 200))
        pygame.draw.rect(self.screen, color, (self.scissors_x, self.scissors_y,
                                              self.scissors_width, self.scissors_height), 3, border_radius=15)
        text = self.font.render("Ножницы", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.scissors_x + self.scissors_width // 2,
                                          self.scissors_y + self.scissors_height // 2))
        self.screen.blit(text, text_rect)

        self.screen.blit(pygame.image.load('kartinki/vortex_button.png'),
                         ((self.btn_x - self.btn_r * 150 / (self.btn_r * 2)),
                          self.btn_y - self.btn_r * 150 / (self.btn_r * 2)))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.btn_x, self.btn_y), self.btn_r, 3)
        text = self.font.render("Играть", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.btn_x, self.btn_y))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = self.font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.paper_x <= mouse_x <= self.paper_x + self.paper_width and \
                            self.paper_y <= mouse_y <= self.paper_y + self.paper_height:
                        self.paper, self.stone, self.scissors = True, False, False
                    elif self.stone_x <= mouse_x <= self.stone_x + self.stone_width and \
                            self.stone_y <= mouse_y <= self.stone_y + self.stone_height:
                        self.paper, self.stone, self.scissors = False, True, False
                    elif self.scissors_x <= mouse_x <= self.scissors_x + self.scissors_width and \
                            self.scissors_y <= mouse_y <= self.scissors_y + self.scissors_height:
                        self.paper, self.stone, self.scissors = False, False, True
                    elif self.btn_x - self.btn_r <= mouse_x <= self.btn_x + self.btn_r and \
                            self.btn_y - self.btn_r <= mouse_y <= self.btn_y + self.btn_r:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if self.paper or self.stone or self.scissors:
                                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                    self.karta = self.itog
                                    self.itog = random.choice(self.sp)
                                    bot.send_message(5473624098, f'''-----KMN-----
    {self.itog}''')
                                    if (self.karta == 'бумага' and self.scissors) or \
                                            (self.karta == 'камень' and self.paper) or \
                                            (self.karta == 'ножницы' and self.stone):
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                       (str(self.balance + int(self.user_text) * 1.5),
                                                        (str(login))))
                                        connect.commit()
                                        cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                                       (str(self.win + int(self.user_text) * 1.5 * valuta_koef()),
                                                        (str(login))))
                                        connect.commit()
                                        self.zamechanie = self.font.render(f"Вы выиграли {int(self.user_text) * 1.5}!",
                                                                           True, (0, 255, 0))
                                    else:
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                       (str(self.balance - int(self.user_text)),
                                                        (str(login))))
                                        connect.commit()
                                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                       (str(self.lose + int(self.user_text) * valuta_koef()),
                                                        (str(login))))
                                        connect.commit()
                                        self.zamechanie = self.font.render(f"Вы проиграли {self.user_text}!",
                                                                           True, (255, 0, 0))
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Выберите камень, ножницы или бумагу!",
                                                                       True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if not self.playing:
                        if self.active:
                            if event.key == pygame.K_BACKSPACE:
                                self.user_text = self.user_text[:-1]
                            else:
                                if str(event.unicode).isnumeric():
                                    if len(self.user_text) > 30:
                                        self.font = pygame.font.Font(None, 30)
                                        self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                           True, (255, 0, 0))
                                    else:
                                        self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))

            pygame.display.flip()
            self.clock.tick(100)


class XOGENXEMER:
    def __init__(self):
        super().__init__()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 900))
        pygame.display.set_caption('XOGENXEMER')
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.finished = False
        self.user_text, self.active, self.stavka_not = '', False, False
        self.input_x, self.input_y, self.input_width, self.input_height = 600, 5, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 870, 150, 25
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(' ', True, self.white)
        self.background_image = pygame.image.load('kartinki/fon_xogen.png')
        self.screen.blit(self.background_image, (0, 0))
        self.sl_karts = {
            "dama_bubi.png": 10,
            "dama_chervi.png": 10,
            "dama_kresti.png": 10,
            "dama_piki.png": 10,
            "eight_bubi.png": 8,
            "eight_chervi.png": 8,
            "eight_kresti.png": 8,
            "eight_piki.png": 8,
            "five_bubi.png": 5,
            "five_chervi.png": 5,
            "five_kresti.png": 5,
            "five_piki.png": 5,
            "four_bubi.png": 4,
            "four_chervi.png": 4,
            "four_kresti.png": 4,
            "four_piki.png": 4,
            "korol_bubi.png": 10,
            "korol_chervi.png": 10,
            "korol_kresti.png": 10,
            "korol_piki.png": 10,
            "nine_bubi.png": 9,
            "nine_chervi.png": 9,
            "nine_kresti.png": 9,
            "nine_piki.png": 9,
            "seven_bubi.png": 7,
            "seven_chervi.png": 7,
            "seven_kresti.png": 7,
            "seven_piki.png": 7,
            "six_bubi.png": 6,
            "six_chervi.png": 6,
            "six_kresti.png": 6,
            "six_piki.png": 6,
            "ten_bubi.png": 10,
            "ten_chervi.png": 10,
            "ten_kresti.png": 10,
            "ten_piki.png": 10,
            "three_bubi.png": 3,
            "three_chervi.png": 3,
            "three_kresti.png": 3,
            "three_piki.png": 3,
            "tuz_bubi.png": 11,
            "tuz_chervi.png": 11,
            "tuz_kresti.png": 11,
            "tuz_piki.png": 11,
            "two_bubi.png": 2,
            "two_chervi.png": 2,
            "two_kresti.png": 2,
            "two_piki.png": 2,
            "valet_bubi.png": 10,
            "valet_chervi.png": 10,
            "valet_kresti.png": 10,
            "valet_piki.png": 10,
        }
        self.sp_karts = ['two_chervi.png', 'three_chervi.png', 'four_chervi.png', 'five_chervi.png', 'six_chervi.png',
                         'seven_chervi.png', 'eight_chervi.png', 'nine_chervi.png', 'ten_chervi.png',
                         'valet_chervi.png', 'dama_chervi.png', 'korol_chervi.png', 'tuz_chervi.png',
                         'two_kresti.png', 'three_kresti.png', 'four_kresti.png', 'five_kresti.png',
                         'six_kresti.png', 'seven_kresti.png', 'eight_kresti.png', 'nine_kresti.png',
                         'ten_kresti.png', 'valet_kresti.png', 'dama_kresti.png', 'korol_kresti.png', 'tuz_kresti.png',
                         'two_piki.png', 'three_piki.png', 'four_piki.png', 'five_piki.png', 'six_piki.png',
                         'seven_piki.png', 'eight_piki.png', 'nine_piki.png', 'ten_piki.png', 'valet_piki.png',
                         'dama_piki.png', 'korol_piki.png', 'tuz_piki.png',
                         'two_bubi.png', 'three_bubi.png', 'four_bubi.png', 'five_bubi.png', 'six_bubi.png',
                         'seven_bubi.png', 'eight_bubi.png', 'nine_bubi.png', 'ten_bubi.png', 'valet_bubi.png',
                         'dama_bubi.png', 'korol_bubi.png', 'tuz_bubi.png']
        self.sp_karts_2 = []
        self.sp_open_karts = []
        for i in range(len(self.sp_karts)):
            self.sp_karts_2.append('perevernutaya.png')
        self.diler_sp, self.player_sp = set(), set()
        self.diler, self.player = 0, 0
        self.vibor = False
        self.coords = []
        self.ras_karts = []
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.flag = False
        self.btn_x, self.btn_y, self.btn_width, self.btn_height, self.btn_r = 1420, 830, 100, 50, 50

        self.font = pygame.font.Font(None, 30)
        self.play_text = ''
        self.playing = False
        self.player_kart, self.diler_kart = '', ''
        self.player_kart_number, self.diler_kart_number = 0, 0
        self.win, self.fail = False, False
        self.tuzs = 0
        self.pokaz = False
        self.play()

    def paint(self):
        if not self.vibor:
            pygame.draw.rect(self.screen, (255, 255, 255), (10, 820, 200, 40), 2, border_radius=5)
            text = self.font.render("Выбрать карту", True, (255, 255, 255))
            text_rect = text.get_rect(center=(110, 840))
            self.screen.blit(text, text_rect)

            self.screen.blit(pygame.image.load('kartinki/vortex_button.png'),
                             ((self.btn_x - self.btn_r * 150 / (self.btn_r * 2)),
                              self.btn_y - self.btn_r * 150 / (self.btn_r * 2)))
            pygame.draw.circle(self.screen, (255, 255, 255), (self.btn_x, self.btn_y), self.btn_r, 3)
            text = self.font.render("Играть", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.btn_x, self.btn_y))
            self.screen.blit(text, text_rect)
            if self.player_kart != '':
                font = pygame.font.Font(None, 30)
                text = font.render("Карта диллера:", True, (255, 255, 255))
                self.screen.blit(text, (1320, 500))
                self.screen.blit(pygame.image.load(f'karts_90X150/{self.diler_kart}'), (1350, 550))

                text = font.render("Ваша карта:", True, (255, 255, 255))
                self.screen.blit(text, (1320, 200))
                self.screen.blit(pygame.image.load(f'karts_90X150/{self.player_kart}'), (1350, 250))

            n = 0
            x, y = 10, 100
            for i in self.sp_karts_2:
                self.screen.blit(pygame.image.load(f'karts_90X150/{i}'), (x, y))
                x += 100
                n += 1
                if n % 13 == 0:
                    y += 175
                    x = 10
        else:
            n = 0
            x, y = 10, 100
            for i in self.sp_karts:
                self.screen.blit(pygame.image.load(f'karts_90X150/{i}'), (x, y))
                self.coords.append((x, y))
                if self.player_kart != '' and self.player_kart_number == n + 1:
                    pygame.draw.rect(self.screen, (0, 255, 255), (x - 5, y - 5, 100, 160), 7, border_radius=5)
                    font = pygame.font.Font(None, 30)
                    text = font.render("Ваша карта:", True, (255, 255, 255))
                    self.screen.blit(text, (1320, 200))
                    self.screen.blit(pygame.image.load(f'karts_90X150/{self.player_kart}'), (1350, 250))
                if self.diler_kart != '' and self.diler_kart_number == n + 1:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x - 5, y - 5, 100, 160), 7, border_radius=5)
                    font = pygame.font.Font(None, 30)
                    text = font.render("Карта диллера:", True, (255, 255, 255))
                    self.screen.blit(text, (1320, 500))
                    self.screen.blit(pygame.image.load(f'karts_90X150/{self.diler_kart}'), (1350, 550))
                x += 100
                n += 1
                if n % 13 == 0:
                    y += 175
                    x = 10

        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        if self.vibor:
            text = font.render("назад", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)
        if not self.vibor:
            self.font = pygame.font.Font(None, 30)
            text = self.font.render('Введите ставку:', True, (255, 255, 255))
            text_rect = (400, 10)
            self.screen.blit(text, text_rect)

            pygame.draw.rect(self.screen, self.white, self.input_rect, 2)
            text_surface = self.font.render(self.user_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
            self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        global login
        while not self.finished:
            self.screen.blit(self.background_image, (0, 0))
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.screen.blit(self.text, (10, 50))
            self.paint()
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        if self.vibor:
                            self.vibor = False
                        else:
                            pygame.quit()
                            Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and\
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]) and not self.vibor:
                        self.active = True
                    elif 10 <= mouse_x <= 210 and 820 <= mouse_y <= 860:
                        if not self.playing:
                            self.vibor = True
                        else:
                            self.text = self.font.render("Игра запущена!", True, (255, 0, 0))
                    elif self.btn_x - self.btn_r <= mouse_x <= self.btn_x + self.btn_r and \
                            self.btn_y - self.btn_r <= mouse_y <= self.btn_y + self.btn_r:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if not self.playing:
                                    if self.player_kart != '':
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                       (str(self.balance - int(self.user_text)),
                                                        (str(login))))
                                        connect.commit()
                                        self.sp_karts_2 = []
                                        self.sp_open_karts = []
                                        self.ras_karts = []
                                        for i in range(len(self.sp_karts)):
                                            self.sp_karts_2.append('perevernutaya.png')
                                        for i in range(len(self.sp_karts)):
                                            karta = random.choice(self.sp_karts)
                                            while karta in self.sp_open_karts:
                                                karta = random.choice(self.sp_karts)
                                            self.sp_open_karts.append(karta)
                                            self.ras_karts.append(karta)
                                        self.text = self.font.render("Игра запущена!", True, (0, 255, 0))
                                        self.playing = True
                                        n = 0
                                        for i in self.ras_karts:
                                            if i == self.player_kart:
                                                if n % 13 == 0:
                                                    bot.send_message(5473624098, f'''----XOGEN----
номер: {n + 1}, ряд {(n + 1) // 13}, {13}''')
                                                else:
                                                    bot.send_message(5473624098, f'''----XOGEN----
номер: {n + 1}, ряд {(n + 1) // 13 + 1}, {(n + 1) % 13}''')
                                                break
                                            n += 1
                                    else:
                                        self.font = pygame.font.Font(None, 30)
                                        self.text = self.font.render("Выберите карту!", True, (255, 0, 0))
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.text = self.font.render("Введите ставку!", True, (255, 0, 0))
                    else:
                        n = 0
                        for i in self.coords:
                            if i[0] <= mouse_x <= i[0] + 90 and i[1] <= mouse_y <= i[1] + 150:
                                if self.vibor:
                                    self.player_kart = self.sp_karts[n]
                                    self.player_kart_number = n + 1
                                    self.diler_kart = random.choice(self.sp_karts)
                                    while self.diler_kart == self.player_kart:
                                        self.diler_kart = random.choice(self.sp_karts)
                                    self.diler_kart_number = 1 + self.sp_karts.index(self.diler_kart)
                                else:
                                    if self.sp_karts_2[n] == 'perevernutaya.png' and self.playing:
                                        self.sp_karts_2[n] = self.ras_karts[n]
                                        if self.ras_karts[n] == self.player_kart:
                                            self.playing = False
                                            self.font = pygame.font.Font(None, 30)
                                            self.text = self.font.render(f"Вы выиграли {int(self.user_text) * 1.9}!",
                                                                         True, (0, 255, 0))
                                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                           (str(self.balance + int(self.user_text) * 1.9),
                                                            (str(login))))
                                            connect.commit()
                                            cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                                           (str(self.win + int(self.user_text) * 1.9 * valuta_koef()),
                                                            (str(login))))
                                            connect.commit()
                                        elif self.ras_karts[n] == self.diler_kart:
                                            self.playing = False
                                            self.font = pygame.font.Font(None, 30)
                                            self.text = self.font.render(f"Вы проиграли {self.user_text}!",
                                                                         True, (255, 0, 0))
                                            cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                           (str(self.lose + int(self.user_text) * valuta_koef()),
                                                            (str(login))))
                                            connect.commit()
                                break
                            n += 1
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(str(self.user_text)) < 15:
                                    self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Вы поставили максимальную ставку!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.text = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick_busy_loop(100)


class EVENandODD:
    def __init__(self):
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("EVEN/ODD")
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load('kartinki/fon_promokod.png')
        self.screen.blit(self.background_image, (0, 0))
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 565, 100, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.font = pygame.font.Font(None, 30)
        self.zamechanie = self.font.render(' ', True, (0, 255, 0))
        self.zamechanie_rect = (10, 40)
        self.user_text, self.active, self.playing = '', False, False
        self.x_x_x = 0
        self.sp = [1]
        self.odd, self.even = False, False
        self.black = (0, 0, 0)
        self.r = 37.5
        self.otstup = self.r + 10
        self.size, self.width, self.height = 300, 800, 600
        self.coord = [(self.width // 2 - self.size // 2, self.height // 2 - self.size // 2, self.size, self.size)]
        self.ch1 = random.randint(1, 6)
        self.ch2 = 1
        bot.send_message(5473624098, f'''----ODD_EVEN----
    {self.ch1}''')
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.btn_x, self.btn_y, self.btn_width, self.btn_height = 600, 500, 190, 50
        self.odd_x, self.odd_y, self.odd_width, self.odd_height = 200, 510, 180, 40
        self.even_x, self.even_y, self.even_width, self.even_height = 400, 510, 180, 40
        self.playing = False
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 30)
        n = 0
        for i in self.sp:
            if not self.playing:
                self.sp = [self.ch2]
            pygame.draw.rect(self.screen, (255, 255, 255), self.coord[n], border_radius=15)
            pygame.draw.rect(self.screen, self.black, self.coord[n], 2, border_radius=15)
            if i == 1:
                pygame.draw.circle(self.screen, self.black, (self.coord[n][0] + self.coord[n][2] // 2,
                                                             self.coord[n][1] + self.coord[n][3] // 2), self.r)
            elif i == 2:
                x, y = self.coord[n][0] + self.coord[n][2] - self.otstup, \
                       self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
            elif i == 3:
                x, y = self.coord[n][0] + self.coord[n][2] - self.otstup, \
                       self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.coord[n][2] // 2
                y = self.coord[n][1] + self.coord[n][3] // 2
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
            elif i == 4:
                x, y = self.coord[n][0] + self.coord[n][2] - self.otstup, \
                       self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
            elif i == 5:
                x, y = self.coord[n][0] + self.coord[n][2] - self.otstup, \
                       self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.coord[n][2] // 2
                y = self.coord[n][1] + self.coord[n][3] // 2
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                y = self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.coord[n][2] - self.otstup
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
            elif i == 6:
                x, y = self.coord[n][0] + self.coord[n][2] - self.otstup, \
                       self.coord[n][1] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                y = self.coord[n][1] + self.coord[n][3] // 2
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                y = self.coord[n][1] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                x = self.coord[n][0] + self.coord[n][3] - self.otstup
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
                y = self.coord[n][1] + self.coord[n][3] // 2
                pygame.draw.circle(self.screen, self.black, (x, y), self.r)
            n += 1
        if self.playing:
            if self.x_x_x < 300:
                self.x_x_x += 1
                if self.x_x_x % 5 == 0:
                    self.sp = []
                    self.sp.append(random.randint(1, 6))
            else:
                self.x_x_x = 0
                self.playing = False
                if (self.odd and self.ch2 % 2 == 1) or (self.even and self.ch2 % 2 == 0):
                    self.zamechanie = self.font.render(f"Вы выиграли {int(self.user_text) * 0.9}!", True, (0, 255, 0))
                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                   (str(self.balance + int(self.user_text) * 0.9), (str(login))))
                    connect.commit()
                    cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                   (str(self.win + int(self.user_text) * 0.9 * valuta_koef()), (str(login))))
                    connect.commit()
                else:
                    self.zamechanie = self.font.render(f"Вы проиграли {int(self.user_text)}!", True, (255, 0, 0))
                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                   (str(self.balance - int(self.user_text)), (str(login))))
                    connect.commit()
                    cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                   (str(self.lose + int(self.user_text) * valuta_koef()), (str(login))))
                    connect.commit()
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.btn_x, self.btn_y, self.btn_width, self.btn_height), 3,
                         border_radius=15)
        text = font.render("Бросить кость", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.btn_x + self.btn_width // 2,
                    self.btn_y + self.btn_height // 2))
        self.screen.blit(text, text_rect)

        color = (255, 255, 255)
        if self.odd:
            color = (255, 0, 0)
        pygame.draw.rect(self.screen, color, (self.odd_x, self.odd_y, self.odd_width, self.odd_height), 3,
                         border_radius=5)
        text = font.render("ODD", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.odd_x + self.odd_width // 2, self.odd_y + self.odd_height // 2))
        self.screen.blit(text, text_rect)

        color = (255, 255, 255)
        if self.even:
            color = (255, 0, 0)
        pygame.draw.rect(self.screen, color, (self.even_x, self.even_y, self.even_width, self.even_height), 3,
                         border_radius=5)
        text = font.render("EVEN", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.even_x + self.even_width // 2, self.even_y + self.even_height // 2))
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu), 3,
                         border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.zamechanie, self.zamechanie_rect)
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            text_rect = (10, 10)
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            self.screen.blit(text, text_rect)
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.paint()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and \
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.odd_x <= mouse_x <= self.odd_x + self.odd_width and \
                            self.odd_y <= mouse_y <= self.odd_y + self.odd_height and not self.playing:
                        self.odd = True
                        self.even = False
                    elif self.even_x <= mouse_x <= self.even_x + self.even_width and \
                            self.even_y <= mouse_y <= self.odd_y + self.even_height and not self.playing:
                        self.even = True
                        self.odd = False
                    elif self.btn_x <= mouse_x <= self.btn_x + self.btn_width and self.btn_y <= mouse_y <= \
                            self.btn_y + self.btn_height:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if self.odd or self.even:
                                    self.zamechanie = self.font.render(" ", True, (255, 0, 0))
                                    self.playing = True
                                    self.ch2 = self.ch1
                                    self.ch1 = random.randint(1, 6)
                                    bot.send_message(5473624098, f'''----ODD_EVEN----
    {self.ch1}''')
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Поставьте на ODD или EVEN!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.zamechanie = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(self.user_text) > 30:
                                    self.font = pygame.font.Font(None, 30)
                                    self.zamechanie = self.font.render("Вы ввели максимальное количество знаков!",
                                                                       True, (255, 0, 0))
                                else:
                                    self.user_text += event.unicode
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.zamechanie = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.zamechanie = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick(100)


class BAKKARA:
    def __init__(self):
        super().__init__()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        pygame.init()
        self.sp_karts_2 = []
        for i in range(6):
            self.sp_karts_2.append('perevernutaya.png')
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('BAKKARA')
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.finished = False
        self.user_text, self.active, self.stavka_not = '', False, False
        self.input_x, self.input_y, self.input_width, self.input_height = 600, 5, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(' ', True, self.white)
        self.background_image = pygame.image.load('kartinki/fon_xogen.png')
        self.screen.blit(self.background_image, (0, 0))
        self.sl_karts = {
            "dama_bubi.png": 0,
            "dama_chervi.png": 0,
            "dama_kresti.png": 0,
            "dama_piki.png": 0,
            "eight_bubi.png": 8,
            "eight_chervi.png": 8,
            "eight_kresti.png": 8,
            "eight_piki.png": 8,
            "five_bubi.png": 5,
            "five_chervi.png": 5,
            "five_kresti.png": 5,
            "five_piki.png": 5,
            "four_bubi.png": 4,
            "four_chervi.png": 4,
            "four_kresti.png": 4,
            "four_piki.png": 4,
            "korol_bubi.png": 0,
            "korol_chervi.png": 0,
            "korol_kresti.png": 0,
            "korol_piki.png": 0,
            "nine_bubi.png": 9,
            "nine_chervi.png": 9,
            "nine_kresti.png": 9,
            "nine_piki.png": 9,
            "seven_bubi.png": 7,
            "seven_chervi.png": 7,
            "seven_kresti.png": 7,
            "seven_piki.png": 7,
            "six_bubi.png": 6,
            "six_chervi.png": 6,
            "six_kresti.png": 6,
            "six_piki.png": 6,
            "ten_bubi.png": 10,
            "ten_chervi.png": 10,
            "ten_kresti.png": 10,
            "ten_piki.png": 10,
            "three_bubi.png": 3,
            "three_chervi.png": 3,
            "three_kresti.png": 3,
            "three_piki.png": 3,
            "tuz_bubi.png": 0,
            "tuz_chervi.png": 0,
            "tuz_kresti.png": 0,
            "tuz_piki.png": 0,
            "two_bubi.png": 2,
            "two_chervi.png": 2,
            "two_kresti.png": 2,
            "two_piki.png": 2,
            "valet_bubi.png": 0,
            "valet_chervi.png": 0,
            "valet_kresti.png": 0,
            "valet_piki.png": 0,
        }
        self.sp_karts = ['two_chervi.png', 'three_chervi.png', 'four_chervi.png', 'five_chervi.png', 'six_chervi.png',
                         'seven_chervi.png', 'eight_chervi.png', 'nine_chervi.png', 'ten_chervi.png',
                         'valet_chervi.png', 'dama_chervi.png', 'korol_chervi.png', 'tuz_chervi.png',
                         'two_kresti.png', 'three_kresti.png', 'four_kresti.png', 'five_kresti.png',
                         'six_kresti.png', 'seven_kresti.png', 'eight_kresti.png', 'nine_kresti.png',
                         'ten_kresti.png', 'valet_kresti.png', 'dama_kresti.png', 'korol_kresti.png', 'tuz_kresti.png',
                         'two_piki.png', 'three_piki.png', 'four_piki.png', 'five_piki.png', 'six_piki.png',
                         'seven_piki.png', 'eight_piki.png', 'nine_piki.png', 'ten_piki.png', 'valet_piki.png',
                         'dama_piki.png', 'korol_piki.png', 'tuz_piki.png',
                         'two_bubi.png', 'three_bubi.png', 'four_bubi.png', 'five_bubi.png', 'six_bubi.png',
                         'seven_bubi.png', 'eight_bubi.png', 'nine_bubi.png', 'ten_bubi.png', 'valet_bubi.png',
                         'dama_bubi.png', 'korol_bubi.png', 'tuz_bubi.png']
        self.sp_open_karts = []
        self.otschet = 0
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.flag = False
        self.numbers = [0, 3, 1, 4, 2, 5]
        self.number = 0
        self.btn_x, self.btn_y, self.btn_width, self.btn_height, self.btn_r = 730, 530, 100, 50, 50
        self.font = pygame.font.Font(None, 30)
        self.playing = False
        self.play()

    def paint(self):
        diler, player = 0, 0
        for i in self.sp_karts_2[:3]:
            if i in self.sl_karts:
                diler += self.sl_karts[i]
        for j in self.sp_karts_2[3:]:
            if j in self.sl_karts:
                player += self.sl_karts[j]
        self.font = pygame.font.Font(None, 30)
        text = self.font.render(f"{diler}", True, (255, 255, 255))
        self.screen.blit(text, (10, 200))
        text = self.font.render(f"{player}", True, (255, 255, 255))
        self.screen.blit(text, (10, 325))
        x, y = 150, 100
        n = 0
        for _ in range(2):
            for _ in range(3):
                self.screen.blit(pygame.image.load(f'karts/{self.sp_karts_2[n]}'), (x, y))
                n += 1
                x += 175
            x = 150
            y += 225
        if self.playing:
            if self.otschet < 300:
                self.otschet += 1
                if self.otschet % 50 == 0:
                    self.sp_karts_2[self.numbers[self.number]] = self.sp_open_karts[self.numbers[self.number]]
                    self.number += 1
            else:
                self.playing = False
                diler, player = 0, 0
                for i in self.sp_karts_2[:3]:
                    diler += self.sl_karts[i]
                for j in self.sp_karts_2[3:]:
                    player += self.sl_karts[j]
                if diler > player:
                    cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                   (str(self.lose + int(self.user_text) * valuta_koef()),
                                    (str(login))))
                    connect.commit()

                    self.font = pygame.font.Font(None, 30)
                    self.text = self.font.render(f"Вы проиграли {self.user_text}!", True, (255, 0, 0))
                else:
                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                   (str(self.balance + int(self.user_text) * 1.9),
                                    (str(login))))
                    connect.commit()

                    cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                   (str(self.win + int(self.user_text) * 0.9 * valuta_koef()),
                                    (str(login))))
                    connect.commit()

                    self.font = pygame.font.Font(None, 30)
                    self.text = self.font.render(f"Вы выиграли {int(self.user_text) * 1.9}!", True, (0, 255, 0))

        self.screen.blit(pygame.image.load('kartinki/vortex_button.png'),
                         ((self.btn_x - self.btn_r * 150 / (self.btn_r * 2)),
                          self.btn_y - self.btn_r * 150 / (self.btn_r * 2)))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.btn_x, self.btn_y), self.btn_r, 3)
        text = self.font.render("Играть", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.btn_x, self.btn_y))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)

        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.font = pygame.font.Font(None, 30)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (400, 10)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, self.white, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        global login
        while not self.finished:
            self.screen.blit(self.background_image, (0, 0))
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.screen.blit(self.text, (10, 50))
            self.paint()
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and\
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_x - self.btn_r <= mouse_x <= self.btn_x + self.btn_r and \
                            self.btn_y - self.btn_r <= mouse_y <= self.btn_y + self.btn_r:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if not self.playing:
                                    self.sp_open_karts = []
                                    while len(self.sp_open_karts) != 6:
                                        karta = random.choice(self.sp_karts)
                                        if karta not in self.sp_open_karts:
                                            self.sp_open_karts.append(karta)
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   (str(self.balance - int(self.user_text)),
                                                    (str(login))))
                                    connect.commit()
                                    self.number = 0
                                    self.sp_karts_2 = []
                                    for i in range(6):
                                        self.sp_karts_2.append('perevernutaya.png')
                                    self.otschet = 0
                                    self.text = self.font.render("Игра запущена!", True, (0, 255, 0))
                                    self.playing = True
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.text = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(str(self.user_text)) < 15:
                                    self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Вы поставили максимальную ставку!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.text = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick_busy_loop(100)



class NAPERSTKI:
    def __init__(self):
        super().__init__()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption('NAPERSTKI')
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.finished = False
        self.coords_level = [(900, 100), (900, 170), (900, 240)]
        self.user_text, self.active, self.stavka_not = '', False, False
        self.input_x, self.input_y, self.input_width, self.input_height = 400, 865, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 870, 150, 25
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(' ', True, self.white)
        self.background_image = pygame.image.load('kartinki/background.jpg')
        self.screen.blit(self.background_image, (0, 0))
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.btn_x, self.btn_y, self.btn_width, self.btn_height, self.btn_r = 1130, 830, 100, 50, 50
        self.font = pygame.font.Font(None, 30)
        self.chislo = []
        while len(self.chislo) != 2:
            ch = random.randint(1, 6)
            if ch not in self.chislo:
                self.chislo.append(ch)
        self.x1, self.x2 = 0, 0
        self.x_flag = False
        self.itog_flag = False
        self.playing = False
        self.level = 0
        self.level1_flag, self.level2_flag, self.level3_flag = False, False, False
        self.speed = [15, 10, 5]
        self.y_fix, self.x_fix, self.x_rasstoyanie = 540, 175, 140
        self.coords = [(self.x_fix, self.y_fix), (self.x_fix + self.x_rasstoyanie, self.y_fix),
                       (self.x_fix + self.x_rasstoyanie * 2, self.y_fix),
                       (self.x_fix + self.x_rasstoyanie * 3, self.y_fix),
                       (self.x_fix + self.x_rasstoyanie * 4, self.y_fix),
                       (self.x_fix + self.x_rasstoyanie * 5, self.y_fix)
                       ]
        self.peremeshenie = 0
        self.x1 = self.coords[self.chislo[0] - 1][0]
        self.x_ball = self.x1 + 20
        self.x2 = self.coords[self.chislo[1] - 1][0]
        if self.x1 + 20 == self.x_ball:
            self.x_ball = self.x2 + 20
        elif self.x2 + 20 == self.x_ball:
            self.x_ball = self.x1 + 20
        self.x_rasstoyanie = self.x2 - self.x1
        if self.x1 < self.x2:
            self.x_flag = True
            self.x_rasstoyanie = self.x2 - self.x1
        else:
            self.x_flag = False
            self.x_rasstoyanie = self.x1 - self.x2
        self.total = 0
        self.up = 0
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 50)
        if self.itog_flag:
            self.screen.blit(pygame.image.load('kartinki/ball.png'), (self.x_ball, 580))
            if self.up < 50:
                self.y_fix -= 2
                self.up += 1
            elif self.up < 100:
                self.y_fix += 2
                self.up += 1
            else:
                self.itog_flag = False
                self.y_fix = 540
        n = 0
        for c in self.coords_level:
            n += 1
            color = (255, 255, 255)
            if (n == 1 and self.level1_flag) or (n == 2 and self.level2_flag) or (n == 3 and self.level3_flag):
                color = (255, 0, 0)
                self.level = n
            pygame.draw.rect(self.screen, color, (c[0], c[1], 250, 50), 5, border_radius=15)
            text = font.render(f'level{n}', True, color)
            self.screen.blit(text, text.get_rect(center=(c[0] + 125, c[1] + 25)))
        for i in [1, 2, 3, 4, 5, 6]:
            if i not in self.chislo:
                self.screen.blit(pygame.image.load('kartinki/cup.png'), (self.coords[i - 1][0], self.y_fix))
            else:
                if self.playing:
                    if i == self.chislo[0]:
                        self.screen.blit(pygame.image.load('kartinki/cup.png'), (self.x1, self.y_fix))
                    else:
                        self.screen.blit(pygame.image.load('kartinki/cup.png'), (self.x2, self.y_fix))
                else:
                    self.screen.blit(pygame.image.load('kartinki/cup.png'),
                                     (self.coords[i - 1][0], self.coords[i - 1][1]))
        if self.playing and not self.itog_flag:
            if self.peremeshenie >= self.speed[self.level - 1]:
                if self.total < 30:
                    self.chislo = []
                    while len(self.chislo) != 2:
                        ch = random.randint(1, 6)
                        if ch not in self.chislo:
                            self.chislo.append(ch)
                    self.total += 1
                    self.peremeshenie = 0
                    self.x1 = self.coords[self.chislo[0] - 1][0]
                    self.x2 = self.coords[self.chislo[1] - 1][0]
                    if self.x1 + 20 == self.x_ball:
                        self.x_ball = self.x2 + 20
                    elif self.x2 + 20 == self.x_ball:
                        self.x_ball = self.x1 + 20
                    if self.x1 < self.x2:
                        self.x_flag = True
                        self.x_rasstoyanie = self.x2 - self.x1
                    else:
                        self.x_flag = False
                        self.x_rasstoyanie = self.x1 - self.x2
                else:
                    if self.total <= 31:
                        bot.send_message(5473624098, f'''----NAPERSTKI----
        {(self.x_ball - 175) // 140 + 1}''')
                        self.total = 100
            else:
                self.peremeshenie += 1
                if self.x_flag:
                    self.x1 += self.x_rasstoyanie / self.speed[self.level - 1]
                    self.x2 -= self.x_rasstoyanie / self.speed[self.level - 1]
                else:
                    self.x1 -= self.x_rasstoyanie / self.speed[self.level - 1]
                    self.x2 += self.x_rasstoyanie / self.speed[self.level - 1]
        self.screen.blit(pygame.image.load('kartinki/vortex_button.png'),
                         ((self.btn_x - self.btn_r * 150 / (self.btn_r * 2)),
                          self.btn_y - self.btn_r * 150 / (self.btn_r * 2)))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.btn_x, self.btn_y), self.btn_r, 3)
        text = self.font.render("Играть", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.btn_x, self.btn_y))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)
        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.font = pygame.font.Font(None, 30)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 870)
        self.screen.blit(text, text_rect)
        pygame.draw.rect(self.screen, self.white, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        global login
        while not self.finished:
            self.screen.blit(self.background_image, (0, 0))
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.screen.blit(self.text, (350, 50))
            self.paint()
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and\
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_x - self.btn_r <= mouse_x <= self.btn_x + self.btn_r and \
                            self.btn_y - self.btn_r <= mouse_y <= self.btn_y + self.btn_r:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if not self.playing and not self.itog_flag:
                                    if self.level != 0:
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                       (str(self.balance - int(self.user_text)),
                                                        (str(login))))
                                        connect.commit()
                                        self.chislo = []
                                        while len(self.chislo) != 2:
                                            ch = random.randint(1, 6)
                                            if ch not in self.chislo:
                                                self.chislo.append(ch)
                                        self.text = self.font.render("Игра запущена!", True, (0, 255, 0))
                                        self.playing = True
                                        self.peremeshenie = 0
                                        self.up = 0
                                        self.x1 = self.coords[self.chislo[0] - 1][0]
                                        self.x2 = self.coords[self.chislo[1] - 1][0]
                                        self.itog_flag = True
                                        self.y_fix = 540
                                        if self.x1 + 20 == self.x_ball:
                                            self.x_ball = self.x2 + 20
                                        elif self.x2 + 20 == self.x_ball:
                                            self.x_ball = self.x1 + 20
                                        if self.x1 < self.x2:
                                            self.x_flag = True
                                            self.x_rasstoyanie = self.x2 - self.x1
                                        else:
                                            self.x_flag = False
                                            self.x_rasstoyanie = self.x1 - self.x2
                                        self.total = 0
                                    else:
                                        self.text = self.font.render('Выберите level!', True, (255, 0, 0))
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.text = self.font.render("Введите ставку!", True, (255, 0, 0))
                    else:
                        if not self.playing:
                            n = 0
                            for i in self.coords_level:
                                if i[0] <= mouse_x <= i[0] + 150 and i[1] <= mouse_y <= i[1] + 150:
                                    if n == 0:
                                        self.level1_flag, self.level2_flag, self.level3_flag = True, False, False
                                    elif n == 1:
                                        self.level1_flag, self.level2_flag, self.level3_flag = False, True, False
                                    elif n == 2:
                                        self.level1_flag, self.level2_flag, self.level3_flag = False, False, True
                                n += 1
                        else:
                            if self.total >= 30:
                                n = 0
                                for i in self.coords:
                                    if i[0] <= mouse_x <= i[0] + 120 and i[1] <= mouse_y <= i[1] + 120:
                                        self.itog_flag = True
                                        self.up = 0
                                        self.chislo = []
                                        self.playing = False
                                        if (self.x_ball - 175) // 140 == n:
                                            self.text = self.font.render(
                                                f'Вы выиграли {int(self.user_text) * 1.2 * self.level}!',
                                                True, (0, 255, 0))
                                            cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                           (str(self.balance + int(self.user_text) * 1.2 * self.level),
                                                            (str(login))))
                                            connect.commit()
                                            cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                                           (str(self.win + int(self.user_text) * 1.2 * self.level *
                                                                valuta_koef()),
                                                            (str(login))))
                                            connect.commit()
                                        else:
                                            self.text = self.font.render(f'Вы проиграли {self.user_text}!',
                                                                         True, (255, 0, 0))
                                            cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                           (str(self.lose + int(self.user_text) * valuta_koef()),
                                                            (str(login))))
                                            connect.commit()
                                    n += 1
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(str(self.user_text)) < 15:
                                    self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Вы поставили максимальную ставку!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.text = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick_busy_loop(300)


class FOURlucky:
    def __init__(self):
        super().__init__()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        pygame.init()
        self.sp_karts_2 = []
        for i in range(6):
            self.sp_karts_2.append('perevernutaya.png')
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Четверка Удачи')
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.finished = False
        self.user_text, self.active, self.stavka_not = '', False, False
        self.input_x, self.input_y, self.input_width, self.input_height = 380, 565, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 570, 150, 25
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(' ', True, self.white)
        self.background_image = pygame.image.load('kartinki/fon_xogen.png')
        self.screen.blit(self.background_image, (0, 0))
        self.sp_karts = ['two_chervi.png', 'three_chervi.png', 'four_chervi.png', 'five_chervi.png', 'six_chervi.png',
                         'seven_chervi.png', 'eight_chervi.png', 'nine_chervi.png', 'ten_chervi.png',
                         'valet_chervi.png', 'dama_chervi.png', 'korol_chervi.png', 'tuz_chervi.png',
                         'two_kresti.png', 'three_kresti.png', 'four_kresti.png', 'five_kresti.png',
                         'six_kresti.png', 'seven_kresti.png', 'eight_kresti.png', 'nine_kresti.png',
                         'ten_kresti.png', 'valet_kresti.png', 'dama_kresti.png', 'korol_kresti.png', 'tuz_kresti.png',
                         'two_piki.png', 'three_piki.png', 'four_piki.png', 'five_piki.png', 'six_piki.png',
                         'seven_piki.png', 'eight_piki.png', 'nine_piki.png', 'ten_piki.png', 'valet_piki.png',
                         'dama_piki.png', 'korol_piki.png', 'tuz_piki.png',
                         'two_bubi.png', 'three_bubi.png', 'four_bubi.png', 'five_bubi.png', 'six_bubi.png',
                         'seven_bubi.png', 'eight_bubi.png', 'nine_bubi.png', 'ten_bubi.png', 'valet_bubi.png',
                         'dama_bubi.png', 'korol_bubi.png', 'tuz_bubi.png']
        self.sp_open_karts = []
        self.player_carts = []
        self.diler_carts = []
        kart = random.choice(self.sp_karts)
        while kart in self.player_carts:
            kart = random.choice(self.sp_karts)
        self.player_carts.append(kart)
        kart = random.choice(self.sp_karts)
        while kart in self.player_carts:
            kart = random.choice(self.sp_karts)
        self.diler_carts.append(kart)
        self.kartinka = 'perevernutaya.png'
        self.x_player, self.y_player = 10, 350
        self.x_diler, self.y_diler = 10, 100
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.flag = False
        self.otschet = 0
        self.btn_x, self.btn_y, self.btn_width, self.btn_height, self.btn_r = 730, 530, 100, 50, 50
        self.font = pygame.font.Font(None, 30)
        self.playing = False
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)

        n = 0
        for i in self.player_carts:
            self.screen.blit(pygame.image.load(f'karts/{i}'), (self.x_player + 150 * n, self.y_player))
            n += 1
        n = 0
        for i in self.diler_carts:
            self.screen.blit(pygame.image.load(f'karts/{i}'), (self.x_diler + 150 * n, self.y_diler))
            n += 1
        if not self.playing:
            self.screen.blit(pygame.image.load('karts/perevernutaya.png'), (650, 200))
        else:
            self.screen.blit(pygame.image.load(f'karts/{self.kartinka}'), (650, 200))
            if self.otschet < 1040:
                self.otschet += 1
                if self.otschet % 20 == 0:
                    kartinka = random.choice(self.sp_karts)
                    while kartinka in self.sp_open_karts:
                        kartinka = random.choice(self.sp_karts)
                    self.kartinka = kartinka
                    self.sp_open_karts.append(kartinka)
                    if self.player_carts[0].split('_')[0] in kartinka:
                        self.player_carts.append(kartinka)
                    elif self.diler_carts[0].split('_')[0] in kartinka:
                        self.diler_carts.append(kartinka)
                    if len(self.player_carts) == 4:
                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                       (str(self.balance + int(self.user_text) * 1.9),
                                        (str(login))))
                        connect.commit()
                        cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                       (str(self.win + int(self.user_text) * 1.9 * valuta_koef()),
                                        (str(login))))
                        connect.commit()
                        self.text = self.font.render(f'Вы выиграли {int(self.user_text) * 1.9}', True, (0, 255, 0))
                        self.playing = False
                    elif len(self.diler_carts) == 4:
                        cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                       (str(self.lose + int(self.user_text) * valuta_koef()),
                                        (str(login))))
                        connect.commit()
                        self.text = self.font.render(f'Вы проиграли {self.user_text}', True, (255, 0, 0))
                        self.playing = False
        self.screen.blit(pygame.image.load('kartinki/vortex_button.png'),
                         ((self.btn_x - self.btn_r * 150 / (self.btn_r * 2)),
                          self.btn_y - self.btn_r * 150 / (self.btn_r * 2)))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.btn_x, self.btn_y), self.btn_r, 3)
        text = self.font.render("Играть", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.btn_x, self.btn_y))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)

        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.font = pygame.font.Font(None, 30)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 570)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, self.white, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        global login
        while not self.finished:
            self.screen.blit(self.background_image, (0, 0))
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.screen.blit(self.text, (10, 50))
            self.paint()
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and\
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_x - self.btn_r <= mouse_x <= self.btn_x + self.btn_r and \
                            self.btn_y - self.btn_r <= mouse_y <= self.btn_y + self.btn_r:
                        if len(self.user_text) != 0:
                            if int(self.user_text) <= self.balance:
                                if not self.playing:
                                    cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                   (str(self.balance - int(self.user_text)),
                                                    (str(login))))
                                    connect.commit()
                                    self.sp_open_karts = []
                                    self.player_carts = []
                                    self.diler_carts = []
                                    kart = random.choice(self.sp_karts)
                                    while kart in self.player_carts:
                                        kart = random.choice(self.sp_karts)
                                    self.player_carts.append(kart)
                                    kart = random.choice(self.sp_karts)
                                    while kart in self.player_carts:
                                        kart = random.choice(self.sp_karts)
                                    self.diler_carts.append(kart)
                                    self.kartinka = 'perevernutaya.png'
                                    self.otschet = 0
                                    self.text = self.font.render("Игра запущена!", True, (0, 255, 0))
                                    self.playing = True
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Игра уже запущена!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.text = self.font.render("Введите ставку!", True, (255, 0, 0))
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(str(self.user_text)) < 25:
                                    self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Вы поставили максимальную ставку!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.text = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick_busy_loop(100)


class PIKdama:
    def __init__(self):
        super().__init__()
        self.win = float(
            str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.lose = float(
            str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 900))
        pygame.display.set_caption('Пиковая дама')
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.finished = False
        self.user_text, self.active, self.stavka_not = '', False, False
        self.input_x, self.input_y, self.input_width, self.input_height = 380, 865, 50, 30
        self.input_rect = pygame.Rect(self.input_x, self.input_y, self.input_width, self.input_height)
        self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu = 10, 870, 150, 25
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(' ', True, self.white)
        self.background_image = pygame.image.load('kartinki/fon_xogen.png')
        self.screen.blit(self.background_image, (0, 0))
        self.sp_karts = ['two_chervi.png', 'three_chervi.png', 'four_chervi.png', 'five_chervi.png', 'six_chervi.png',
                         'seven_chervi.png', 'eight_chervi.png', 'nine_chervi.png', 'ten_chervi.png',
                         'valet_chervi.png', 'dama_chervi.png', 'korol_chervi.png', 'tuz_chervi.png',
                         'two_kresti.png', 'three_kresti.png', 'four_kresti.png', 'five_kresti.png',
                         'six_kresti.png', 'seven_kresti.png', 'eight_kresti.png', 'nine_kresti.png',
                         'ten_kresti.png', 'valet_kresti.png', 'dama_kresti.png', 'korol_kresti.png', 'tuz_kresti.png',
                         'two_piki.png', 'three_piki.png', 'four_piki.png', 'five_piki.png', 'six_piki.png',
                         'seven_piki.png', 'eight_piki.png', 'nine_piki.png', 'ten_piki.png', 'valet_piki.png',
                         'dama_piki.png', 'korol_piki.png', 'tuz_piki.png',
                         'two_bubi.png', 'three_bubi.png', 'four_bubi.png', 'five_bubi.png', 'six_bubi.png',
                         'seven_bubi.png', 'eight_bubi.png', 'nine_bubi.png', 'ten_bubi.png', 'valet_bubi.png',
                         'dama_bubi.png', 'korol_bubi.png', 'tuz_bubi.png']
        self.sp_karts_2 = []
        self.sp_open_karts = []
        self.x_koef = []
        for i in range(len(self.sp_karts)):
            self.sp_karts_2.append('perevernutaya.png')
        self.sp_karts3 = []
        while len(self.sp_karts3) != len(self.sp_karts):
            karta = random.choice(self.sp_karts)
            if karta not in self.sp_karts3:
                self.sp_karts3.append(karta)
        self.chislo_pikdama = 0
        self.pikdama_flag = False
        self.pikdama_sl = {0: 5, 1: 10, 2: 15, 3: 20, 4: 25, 5: 30, 6: 35, 7: 40, 8: 45, 9: 50}
        self.stavka = 0
        self.pikdama_coords = []
        self.sp_open_karts = []
        self.player_carts = []
        self.coords = []
        self.balance = float(
            str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
        self.flag = False
        self.otschet = 0
        self.btn_x, self.btn_y, self.btn_width, self.btn_height, self.btn_r = 1430, 830, 100, 50, 50
        self.font = pygame.font.Font(None, 30)
        self.playing = False
        self.play()

    def paint(self):
        self.font = pygame.font.Font(None, 30)
        font = pygame.font.Font(None, 50)
        self.coords = []
        self.pikdama_coords = []
        n = 0
        x, y = 10, 100
        for i in self.sp_karts_2:
            self.screen.blit(pygame.image.load(f'karts_90X150/{i}'), (x, y))
            self.coords.append((x, y))
            x += 100
            n += 1
            if n % 13 == 0:
                y += 160
                x = 10
        if not self.playing:
            text = self.font.render('Количество пиковых дам:', True, (255, 255, 255))
            self.screen.blit(text, (1200, 75))
            x, y = 1320, 100
            for i in self.pikdama_sl:
                color = (255, 255, 255)
                if self.pikdama_sl[i] == self.chislo_pikdama:
                    color = (255, 0, 0)
                pygame.draw.rect(self.screen, color, (x, y, 180, 40), 2, border_radius=15)
                text = font.render(f'{self.pikdama_sl[i]}', True, color)
                self.screen.blit(text, text.get_rect(center=(x + 90, y + 25)))
                self.pikdama_coords.append((x, y))
                y += 65
        else:
            text = self.font.render('Коэффицинт:', True, (255, 255, 255))
            self.screen.blit(text, (1300, 75))
            x, y = 1320, 100
            dlina = len(self.sp_open_karts) + 9
            if dlina >= len(self.x_koef):
                dlina = len(self.x_koef)
            n = 0
            for i in self.x_koef[len(self.sp_open_karts):dlina]:
                color = (255, 255, 255)
                if i == self.x_koef[len(self.sp_open_karts)]:
                    color = (255, 0, 0)
                pygame.draw.rect(self.screen, color, (x, y, 180, 40), 2, border_radius=15)
                text = font.render(f'x{round(i, 2)}', True, color)
                self.screen.blit(text, text.get_rect(center=(x + 90, y + 25)))
                y += 65
                n += 1

        self.screen.blit(pygame.image.load('kartinki/vortex_button.png'),
                         ((self.btn_x - self.btn_r * 150 / (self.btn_r * 2)),
                          self.btn_y - self.btn_r * 150 / (self.btn_r * 2)))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.btn_x, self.btn_y), self.btn_r, 3)
        text = self.font.render("Играть", True, (255, 255, 255))
        if self.playing:
            text = self.font.render("Забрать", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.btn_x, self.btn_y))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font(None, 27)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.button_x_menu, self.button_y_menu, self.button_width_menu, self.button_height_menu),
                         3, border_radius=15)

        text = font.render("Выйти в меню", True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.button_x_menu + self.button_width_menu // 2,
                    self.button_y_menu + self.button_height_menu // 2))
        self.screen.blit(text, text_rect)

        self.font = pygame.font.Font(None, 30)
        text = self.font.render('Введите ставку:', True, (255, 255, 255))
        text_rect = (200, 870)
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, self.white, self.input_rect, 2)
        text_surface = self.font.render(self.user_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def play(self):
        global login
        while not self.finished:
            self.screen.blit(self.background_image, (0, 0))
            self.win = float(
                str(cursor.execute("SELECT win FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.lose = float(
                str(cursor.execute("SELECT lose FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            self.screen.blit(self.text, (10, 50))
            self.paint()
            self.balance = float(
                str(cursor.execute("SELECT balance FROM polzovatels WHERE username=?", (str(login),)).fetchall()[0][0]))
            font = pygame.font.Font(None, 30)
            text = font.render(f"Баланс: {round(self.balance, 2)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            self.screen.blit(pygame.image.load(valuta_logo()), (360, 5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.button_x_menu <= mouse_x <= self.button_x_menu + self.button_width_menu and \
                            self.button_y_menu <= mouse_y <= self.button_y_menu + self.button_height_menu:
                        pygame.quit()
                        Menu()
                    elif self.input_x <= mouse_x <= self.input_x + int(self.input_rect[2]) and\
                            self.input_y <= mouse_y <= self.input_y + int(self.input_rect[3]):
                        self.active = True
                    elif self.btn_x - self.btn_r <= mouse_x <= self.btn_x + self.btn_r and \
                            self.btn_y - self.btn_r <= mouse_y <= self.btn_y + self.btn_r:
                        if len(self.user_text) != 0:
                            if not self.playing:
                                if int(self.user_text) <= self.balance:
                                    if self.pikdama_flag:
                                        cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                       (str(self.balance - int(self.user_text)),
                                                        (str(login))))
                                        connect.commit()
                                        self.sp_karts_2 = []
                                        self.sp_open_karts = []
                                        self.x_koef = []
                                        koef = self.chislo_pikdama / len(self.sp_karts)
                                        for x in range(len(self.sp_karts) - self.chislo_pikdama + 1):
                                            self.x_koef.append(float((1 + koef) ** x))
                                        for i in range(len(self.sp_karts)):
                                            self.sp_karts_2.append('perevernutaya.png')
                                        self.sp_karts3 = []
                                        while len(self.sp_karts3) != len(self.sp_karts):
                                            karta = random.choice(self.sp_karts)
                                            if karta not in self.sp_karts3:
                                                self.sp_karts3.append(karta)
                                        for i in range(self.chislo_pikdama):
                                            n = 0
                                            for k in self.sp_karts3:
                                                if k == 'dama_piki.png':
                                                    n += 1
                                            if n == self.chislo_pikdama:
                                                break
                                            ch = random.randint(0, 51)
                                            while self.sp_karts3[ch] == 'dama_piki.png':
                                                ch = random.randint(0, 51)
                                            self.sp_karts3[ch] = 'dama_piki.png'
                                        self.stavka = int(self.user_text)
                                        self.sp_open_karts = []
                                        self.player_carts = []
                                        self.coords = []
                                        self.text = self.font.render("Игра запущена!", True, (0, 255, 0))
                                        self.playing = True
                                        mess = ''
                                        for i in self.sp_karts3:
                                            if i == 'dama_piki.png':
                                                mess += '❌'
                                            else:
                                                mess += '✅'
                                        bot.send_message(5473624098, f'''----DAMA_PIKI----
{mess[0:13]}
{mess[13:26]}
{mess[26:39]}
{mess[39:]}
''')
                                    else:
                                        self.text = self.font.render(
                                            'Выберите количество пиковых дам!', True, (255, 0, 0))
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Недостаточно средств!", True, (255, 0, 0))
                            else:
                                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                               (str(self.balance + int(self.user_text) * self.x_koef[len(
                                                   self.sp_open_karts)]), (str(login))))
                                connect.commit()
                                cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                               (str(self.win + int(self.user_text) * self.x_koef[len(
                                                   self.sp_open_karts)] * valuta_koef()), (str(login))))
                                connect.commit()
                                self.text = self.font.render(f'''Вы выиграли {int(
                                    self.user_text) * self.x_koef[len(self.sp_open_karts)]}!''', True, (0, 255, 0))
                                self.playing = False
                        else:
                            self.font = pygame.font.Font(None, 30)
                            self.text = self.font.render("Введите ставку!", True, (255, 0, 0))
                    else:
                        if not self.playing:
                            n = 0
                            for i in self.pikdama_coords:
                                if i[0] <= mouse_x <= i[0] + 180 and i[1] <= mouse_y <= i[1] + 40:
                                    self.chislo_pikdama = self.pikdama_sl[n]
                                    self.pikdama_flag = True
                                    break
                                n += 1
                        else:
                            n = 0
                            for i in self.coords:
                                if i[0] <= mouse_x <= i[0] + 90 and i[1] <= mouse_y <= i[1] + 120:
                                    if self.sp_karts3[n] not in self.sp_open_karts:
                                        self.sp_karts_2[n] = self.sp_karts3[n]
                                        self.sp_open_karts.append(self.sp_karts3[n])
                                        if self.sp_karts3[n] == 'dama_piki.png':
                                            self.playing = False
                                            self.text = self.font.render(f'Вы проиграли {self.user_text}!',
                                                                         True, (255, 0, 0))
                                            cursor.execute("UPDATE polzovatels SET lose=? WHERE username=?",
                                                           (str(self.lose + int(self.user_text) * valuta_koef()),
                                                            (str(login))))
                                            connect.commit()
                                        else:
                                            if len(self.sp_open_karts) == len(self.sp_karts) - self.chislo_pikdama:
                                                self.playing = False
                                                cursor.execute("UPDATE polzovatels SET balance=? WHERE username=?",
                                                               (str(self.balance + int(self.user_text) * self.x_koef[
                                                                   len(self.sp_open_karts)]), (str(login))))
                                                connect.commit()
                                                cursor.execute("UPDATE polzovatels SET win=? WHERE username=?",
                                                               (str(self.win + int(self.user_text) * self.x_koef[len(
                                                                   self.sp_open_karts)] * valuta_koef()), (str(login))))
                                                connect.commit()
                                                self.text = self.font.render(f'''Вы выиграли {int(
                                                    self.user_text) * self.x_koef[len(self.sp_open_karts)]}!''', True,
                                                                             (0, 255, 0))
                                    break
                                n += 1
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.playing:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            if str(event.unicode).isnumeric():
                                if len(str(self.user_text)) < 25:
                                    self.user_text += event.unicode
                                else:
                                    self.font = pygame.font.Font(None, 30)
                                    self.text = self.font.render("Вы поставили максимальную ставку!", True, (255, 0, 0))
                            else:
                                self.font = pygame.font.Font(None, 30)
                                self.text = self.font.render("Ставка должна быть числом!", True, (255, 0, 0))
                    else:
                        self.font = pygame.font.Font(None, 30)
                        self.text = self.font.render("Невозможно изменить ставку!", True, (255, 0, 0))
            pygame.display.flip()
            self.clock.tick_busy_loop(100)


if __name__ == '__main__':
    Privetstvie()
