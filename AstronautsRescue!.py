"""
Game by Altinek
feel free to edit the code :D
"""
# import bibliotek
import pygame
import sys
import ctypes
import math
from random import randint, choice


class Score:
    def __init__(self):
        self.time_left = 60
        self.start_time = pygame.time.get_ticks()
        self.paused_time = 0
        self.saved_astronauts = 0
    def time_counter(self):
        seconds = round((pygame.time.get_ticks() - self.start_time - self.paused_time)/1000)-self.saved_astronauts*6
        self.time_left = 10-seconds
        if seconds >10:
            return "TimeEnd"
    def display_score(self):
        print("____________")
        print(self.time_left)
        print(self.saved_astronauts)



class Leaderboard:
    def __init__(self):
        self.text = [font_Arial.render("1.", False, [255, 215, 0]),
                     font_Arial.render("2.", False, [192, 192, 192]),
                     font_Arial.render("3.", False, [205, 127, 50]),
                     font_Arial.render("4.", False, [0, 0, 0]),
                     font_Arial.render("5.", False, [0, 0, 0])]
        try:
            f = open("Content/Data_files/Leaderboard.txt", "r")
            lines = f.readlines()
            #lines.sort(key=lambda x: x.split()[-1])
            self.text = [font_Arial.render(str(1) + "." + (lines[0])[:-1], False, [255, 215, 0]),
                         font_Arial.render(str(2) + "." + (lines[1])[:-1], False, [192, 192, 192]),
                         font_Arial.render(str(3) + "." + (lines[2])[:-1], False, [205, 127, 50]),
                         font_Arial.render(str(4) + "." + (lines[3])[:-1], False, [0, 0, 0]),
                         font_Arial.render(str(5) + "." + (lines[4])[:-1], False, [0, 0, 0])]
            f.close()
        except FileNotFoundError:
            try:
                f = open("Content/Data_files/Leaderboard.txt", "x")
                f.write("\n")
                f.write("\n")
                f.write("\n")
                f.write("\n")
                f.write("\n")
                f.close()
                ctypes.windll.user32.MessageBoxW(None, "You don't have leaderboard file,\n so we created new one.", "Created new leaderboard file", 0)
            except FileExistsError:
                if ctypes.windll.user32.MessageBoxW(None, "Your leaderboard file is probably broken :<,\ndelete it and run game again.\nLoaded default leaderboard", "Error", 0):
                    sys.exit()

    def set_default(self):
        self.text = [font_Arial.render("1.", False, [255, 215, 0]),
                     font_Arial.render("2.", False, [192, 192, 192]),
                     font_Arial.render("3.", False, [205, 127, 50]),
                     font_Arial.render("4.", False, [0, 0, 0]),
                     font_Arial.render("5.", False, [0, 0, 0])]
        open("Content/Data_files/Leaderboard.txt", "w").close()
        f = open("Content/Data_files/Leaderboard.txt", "w")
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.close()


class Options:  # dane do opcji gry
    def __init__(self):
        self.asteroid_speed = 3
        self.asteroid_size = 5
        self.asteroid_amount = 25
        self.astronaut_speed = 10
        self.astronaut_size = 5
        self.point_size = 5
        self.point_amount = 3
        self.spaceship_size = 5

    def set_default(self):
        self.asteroid_speed = 3
        self.asteroid_size = 5
        self.asteroid_amount = 25
        self.astronaut_speed = 10
        self.astronaut_size = 5
        self.point_size = 5
        self.point_amount = 3
        self.spaceship_size = 5

    def options_init(self):  # inicjalizacja opcji do gry, jak nie ma stworzonych to używa podstawowych
        try:
            f = open("Content/Data_files/Options.txt", "r")
            lines = f.readlines()
            self.asteroid_speed = int((lines[0])[17:-1])
            self.asteroid_size = int((lines[1])[16:-1])
            self.asteroid_amount = int((lines[2])[18:-1])
            self.astronaut_speed = int((lines[3])[18:-1])
            self.astronaut_size = int((lines[4])[17:-1])
            self.point_size = int((lines[5])[13:-1])
            self.point_amount = int((lines[6])[15:-1])
            self.spaceship_size = int((lines[7])[17:-1])
            f.close()
        except FileNotFoundError:
            try:
                f = open("Content/Data_files/Options.txt", "x")
                print("\nCreating new options file:")
                f.write("asteroid_speed = 3\n")
                f.write("asteroid_size = 5\n")
                f.write("asteroid_amount = 25\n")
                f.write("astronaut_speed = 10\n")
                f.write("astronaut_size = 5\n")
                f.write("point_size = 5\n")
                f.write("point_amount = 3\n")
                f.write("spaceship_size = 5\n")
                f.close()
                ctypes.windll.user32.MessageBoxW(None, "You don't have options file,\n so we are created new one.", "Created new options file", 0)
            except FileExistsError:
                if ctypes.windll.user32.MessageBoxW(None, "Your save file is probably broken :<,\ndelete it and run game again.\nLoaded default options", "Error", 0):
                    sys.exit()


class Star:
    def __init__(self):
        self.x_speed = randint(-5, 5)
        self.y_speed = randint(-5, 5)
        self.position = [randint(0, width), randint(0, height)]
        self.color = randint(100, 255)
        self.factor = randint(1, 5)

    def moving(self):
        if self.position[0] < 0:
            self.position[0] = width
        if self.position[0] > width:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = height
        if self.position[1] > height:
            self.position[1] = 0
        self.position[0] += self.x_speed * self.factor / 10
        self.position[1] += self.y_speed * self.factor / 10
        pygame.draw.circle(screen, [self.color, self.color, self.color], self.position, self.factor)


class SpaceShip:
    def __init__(self, size):
        self.idle_position = [600, 100]
        self.position = [randint(50, 670), randint(50, 430)]
        self.pos_change = 0
        self.size = size
        self.pos_change_ud = "UP"
        self.ship_origin_img = pygame.image.load("Content/Images/SpaceShip.png")
        self.ship_img = pygame.transform.rotozoom(self.ship_origin_img, 25, self.size / 15)
        self.start_time = pygame.time.get_ticks()
        self.paused_time = 0

    def idle_display(self):
        if self.pos_change_ud == "UP":
            self.pos_change -= 0.2
            if self.pos_change < -10:
                self.pos_change_ud = "DOWN"
        else:
            self.pos_change += 0.2
            if self.pos_change > 10:
                self.pos_change_ud = "UP"
        screen.blit(self.ship_img, [self.idle_position[0] - self.ship_img.get_width() / 2, self.idle_position[1] - self.ship_img.get_width() / 2 + self.pos_change])

    def size_change(self):
        self.ship_img = pygame.transform.rotozoom(self.ship_origin_img, 25, self.size / 15)

    def display(self):
        screen.blit(self.ship_img, [self.position[0] - self.ship_img.get_width() / 2, self.position[1] - self.ship_img.get_height() / 2])

    def station_collision(self):
        global astronauts
        seconds = pygame.time.get_ticks() - self.start_time - self.paused_time
        if seconds < 5000:
            red = 255 * (5000 - seconds) / 5000
            green = 255 - red
            pygame.draw.arc(screen, [red, green, 0],
                            [self.position[0] - self.ship_img.get_width() / 8,
                             self.position[1] - self.ship_img.get_height() / 8,
                             self.ship_img.get_width() / 4,
                             self.ship_img.get_height() / 4], 0, math.pi * 2 * seconds / 5000, 3)
        if len(astronauts) > 1:
            if pygame.Rect(self.position[0] - (self.ship_img.get_width() - 10) / 2,
                           self.position[1] - (self.ship_img.get_height() - 10) / 2,
                           self.ship_img.get_width() - 10,
                           self.ship_img.get_height() - 10).collidepoint(astronauts[-1].position):
                if seconds > 5000:
                    self.start_time = pygame.time.get_ticks()
                    self.paused_time = 0
                    astronauts.pop(-1)
                    score_object.saved_astronauts+=1
                    # todo dodaj punkty do wyniku


class Astronaut:
    def __init__(self, speed, position, size):
        self.position = list(position)
        self.move = [0, 0]
        self.speed = speed
        self.size = size  # todo jak nie potrzeba to wyjeb
        self.astronaut_origin_img = self.astronaut_img = pygame.image.load("Content/Images/Astronaut.png")
        self.astronaut_img = self.astronaut_origin_img = pygame.transform.rotozoom(self.astronaut_origin_img, 0, size / 20)

    def moving(self, mouse_pos):
        self.move[0] = (mouse_pos[0] - self.position[0]) * (self.speed / 100)
        self.move[1] = (mouse_pos[1] - self.position[1]) * (self.speed / 100)
        self.position[0] += self.move[0]
        self.position[1] += self.move[1]

    def display(self, mouse_pos):
        def calculate_angle(a, b, c):
            angle = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
            if angle < 0:
                angle += 360
            return angle

        self.astronaut_img = pygame.transform.rotate(self.astronaut_origin_img, calculate_angle(mouse_pos, self.position, [640, self.position[1]]) - 90)
        screen.blit(self.astronaut_img, [self.position[0] - self.astronaut_img.get_width() / 2, self.position[1] - self.astronaut_img.get_height() / 2])


class AstronautRescuer:
    def __init__(self, speed, position, size):
        self.position = list(position)
        self.move = [0, 0]
        self.speed = speed
        self.size = size  # todo jak nie potrzeba to wyjeb
        self.rescue_astronaut_origin_img = self.rescue_astronaut_img = pygame.image.load("Content/Images/RescueAstronaut.png")
        self.rescue_astronaut_img = self.rescue_astronaut_origin_img = pygame.transform.rotozoom(self.rescue_astronaut_origin_img, 0, size / 20)

    def moving(self, mouse_pos):
        self.move[0] = (mouse_pos[0] - self.position[0]) * (self.speed / 100)
        self.move[1] = (mouse_pos[1] - self.position[1]) * (self.speed / 100)
        self.position[0] += self.move[0]
        self.position[1] += self.move[1]

    def display(self, mouse_pos):
        def calculate_angle(a, b, c):
            angle = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
            if angle < 0:
                angle += 360
            return angle

        self.rescue_astronaut_img = pygame.transform.rotate(self.rescue_astronaut_origin_img, calculate_angle(mouse_pos, self.position, [640, self.position[1]]) - 90)
        screen.blit(self.rescue_astronaut_img, [self.position[0] - self.rescue_astronaut_img.get_width() / 2, self.position[1] - self.rescue_astronaut_img.get_height() / 2])


class LostAstronaut:
    def __init__(self, size):
        self.position = [randint(20, 700), randint(20, 460)]
        self.rotation = 0
        self.rotation_direction = choice([-1, 1])
        self.size = size  # todo jak nie potrzeba to wyjeb
        self.astronaut_origin_img = pygame.image.load("Content/Images/Astronaut.png")
        self.astronaut_origin_img = self.astronaut_img = pygame.transform.rotozoom(self.astronaut_origin_img, 0, self.size / 20)

    def check_collision(self):
        global astronauts
        screen.blit(self.astronaut_img, [self.position[0] - self.astronaut_img.get_width() / 2, self.position[1] - self.astronaut_img.get_height() / 2])
        self.rotation += self.rotation_direction
        self.astronaut_img = pygame.transform.rotate(self.astronaut_origin_img, self.rotation)
        if pygame.Rect(self.position[0] - self.astronaut_origin_img.get_width() / 2,
                       self.position[1] - self.astronaut_origin_img.get_height() / 2,
                       self.astronaut_origin_img.get_width(),
                       self.astronaut_origin_img.get_height()).collidepoint(astronauts[-1].position):
            astronauts.append(Astronaut(options_object.astronaut_speed, self.position, options_object.astronaut_size))
            return "delete"


def menu():  # wyświetlanie menu, wejście do gry, opcji, tabeli wyników i wyjścia z gry
    spaceship_object.size = options_object.spaceship_size
    spaceship_object.size_change()
    text_menu = [font_Arial.render("Play", False, [0, 0, 0]),
                 font_Arial.render("Options", False, [0, 0, 0]),
                 font_Arial.render("Reset scores", False, [0, 0, 0]),
                 font_Arial.render("Exit the game", False, [0, 0, 0]),
                 font_Arial.render("Leaderboard", False, [0, 0, 0]), ]
    screen.fill([0, 0, 0])
    menu_running = True
    while menu_running:
        screen.fill([0, 0, 0])
        display_foreground()
        spaceship_object.idle_display()
        pygame.draw.rect(screen, [0, 255, 0], [30, 30, 200, 60])
        screen.blit(text_menu[0], [40, 45])
        pygame.draw.rect(screen, [255, 255, 255], [30, 100, 200, 60])
        screen.blit(text_menu[1], [40, 115])
        pygame.draw.rect(screen, [255, 0, 0], [30, 170, 200, 60])
        screen.blit(text_menu[2], [40, 185])
        pygame.draw.rect(screen, [255, 0, 0], [30, 400, 200, 60])
        screen.blit(text_menu[3], [40, 415])
        pygame.draw.rect(screen, [255, 255, 255], [width / 2 - 50, 30, 300, 60])
        screen.blit(text_menu[4], [width / 2 + 10, 45])
        pygame.draw.rect(screen, [255, 255, 255], [width / 2 - 50, height - 30, 300, 5])
        for items in range(1, 6):
            pygame.draw.rect(screen, [255, 255, 255], [width / 2 - 25, items * 65 + 50, 250, 50])
            screen.blit(leaderboard_object.text[items - 1], [width / 2 - 18, items * 65 + 58])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(30, 30, 200, 60).collidepoint(pygame.mouse.get_pos()):
                    menu_running = False
                elif pygame.Rect(30, 100, 200, 60).collidepoint(pygame.mouse.get_pos()):
                    options()
                elif pygame.Rect(30, 170, 200, 60).collidepoint(pygame.mouse.get_pos()):
                    leaderboard_object.set_default()
                elif pygame.Rect(30, 400, 200, 60).collidepoint(pygame.mouse.get_pos()):
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)


def play_timer():
    start_ticks = pygame.time.get_ticks()
    text_counter = [font_Arial.render("3", False, [0, 0, 0]),
                    font_Arial.render("2", False, [0, 0, 0]),
                    font_Arial.render("1", False, [0, 0, 0])]
    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        screen.fill([0, 0, 0])
        display_foreground()
        display_objects()

        if seconds <= 1:
            pygame.draw.circle(screen, [255, 0, 0], [360, 240], 30)
            screen.blit(text_counter[0], [352, 225])
        elif 1 < seconds <= 2:
            pygame.draw.circle(screen, [255, 165, 0], [360, 240], 30)
            screen.blit(text_counter[1], [352, 225])
        elif 2 < seconds <= 3:
            pygame.draw.circle(screen, [0, 255, 0], [360, 240], 30)
            screen.blit(text_counter[2], [352, 225])
        else:
            break
        pygame.display.flip()
        clock.tick(60)


def pause():  # pauza gry, wyjście do menu i kontynuacja
    global game_running
    global score_object
    pause_running = True
    text_paused = [font_Arial.render("Paused", False, [255, 255, 255]),
                   font_Arial.render("Leave to menu", False, [0, 0, 0]),
                   font_Arial.render("Quit the game", False, [0, 0, 0])]
    start_time = pygame.time.get_ticks()
    while pause_running:
        screen.fill([0, 0, 0])
        display_foreground()
        display_objects()

        pygame.draw.rect(screen, [255, 0, 0], [150, 300, 200, 50])
        pygame.draw.rect(screen, [255, 0, 0], [370, 300, 200, 50])
        screen.blit(text_paused[0], [310, 100])
        screen.blit(text_paused[1], [150, 310])
        screen.blit(text_paused[2], [375, 310])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(150, 300, 200, 50).collidepoint(pygame.mouse.get_pos()):
                    pause_running = False
                    game_running = False
                elif pygame.Rect(370, 300, 200, 50).collidepoint(pygame.mouse.get_pos()):
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_running = False
                    play_timer()
                    score_object.paused_time += pygame.time.get_ticks() - start_time
                    spaceship_object.paused_time += pygame.time.get_ticks() - start_time
                elif event.key == pygame.K_ESCAPE:
                    pause_running = False
                    game_running = False
            elif event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)


def display_objects():  # wyświetlanie wszystkich min, punktów i węża
    global astronauts
    global lost_astronauts
    spaceship_object.display()
    for items in range(0, len(lost_astronauts)):
        if lost_astronauts[items].check_collision() == "delete":
            lost_astronauts.pop(items)
            for last_items in range(items, len(lost_astronauts)):
                lost_astronauts[last_items].check_collision()
            lost_astronauts.append(LostAstronaut(options_object.point_size))
            break

    astronauts[0].display(pygame.mouse.get_pos())
    for items in range(1, len(astronauts)):
        pygame.draw.line(screen, [255, 255, 255], astronauts[items - 1].position, astronauts[items].position)
        astronauts[items].display(astronauts[items - 1].position)
    score_object.display_score()


def display_foreground():
    for items in range(0, len(stars)):
        stars[items].moving()


def game():  # mechanika gry, obsługa pauzy i wyjścia do menu
    global game_running
    global astronauts
    global lost_astronauts
    global left_game_time
    global score_object
    score_object = Score()
    astronauts = [AstronautRescuer(options_object.astronaut_speed, [360, 240], options_object.astronaut_size),
                  Astronaut(options_object.astronaut_speed, [360, 240], options_object.astronaut_size)]
    lost_astronauts = []
    for amount in range(0, options_object.point_amount):
        lost_astronauts.append(LostAstronaut(options_object.point_size))
    game_running = True
    # play_timer()
    while game_running:
        screen.fill([0, 0, 0])
        display_foreground()
        display_objects()
        astronauts[0].moving(pygame.mouse.get_pos())
        for items in range(1, len(astronauts)):
            astronauts[items].moving(astronauts[items - 1].position)
        spaceship_object.station_collision()
        pygame.display.flip()
        if score_object.time_counter()=="TimeEnd":
            # todo dodaj tutaj zapisywanie wyniku
            game_running=False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                elif event.key == pygame.K_p:
                    pause()
            elif event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)


def options():
    options_running = True
    char_plus = font_Arial.render("+", False, [0, 0, 0])
    char_minus = font_Arial.render("-", False, [0, 0, 0])
    title = (font_Arial.render("Options", False, [255, 255, 255]))
    save = (font_Arial.render("Save to file", False, [0, 0, 0]))
    default = (font_Arial.render("Default", False, [0, 0, 0]))
    quit_text = (font_Arial.render("Back", False, [255, 255, 255]))
    options_text = [font_Arial.render(("Asteroid speed: " + str(options_object.asteroid_speed)), False, [0, 0, 255]),
                    font_Arial.render(("Asteroid size: " + str(options_object.asteroid_size)), False, [0, 0, 255]),
                    font_Arial.render(("Asteroid amount: " + str(options_object.asteroid_amount)), False, [0, 0, 255]),
                    font_Arial.render(("Astronaut speed: " + str(options_object.astronaut_speed)), False, [0, 0, 255]),
                    font_Arial.render(("Astronaut size: " + str(options_object.astronaut_size)), False, [0, 0, 255]),
                    font_Arial.render(("Point size: " + str(options_object.point_size)), False, [0, 0, 255]),
                    font_Arial.render(("Point amount: " + str(options_object.point_amount)), False, [0, 0, 255]),
                    font_Arial.render(("Spaceship size: " + str(options_object.spaceship_size)), False, [0, 0, 255])]
    while options_running:
        screen.fill([0, 0, 0])
        display_foreground()
        spaceship_object.idle_display()
        screen.blit(title, [width / 2 - 60, 15])
        for items in range(1, len(options_text) + 1):
            pygame.draw.rect(screen, [255, 255, 255], [width / 2 - 150, items * 45 + 10, 300, 40])
            screen.blit(options_text[items - 1], [width / 2 - 140, items * 45 + 15])
            pygame.draw.circle(screen, [255, 0, 0], [width / 2 - 180, items * 45 + 30], 20)
            pygame.draw.circle(screen, [0, 255, 0], [width / 2 + 180, items * 45 + 30], 20)
            screen.blit(char_minus, [width / 2 - 185, items * 45 + 10])
            screen.blit(char_plus, [width / 2 + 173, items * 45 + 13])
        pygame.draw.rect(screen, [255, 0, 0], [width / 2 - 200, 420, 180, 40])
        screen.blit(default, [width / 2 - 160, 422])
        pygame.draw.rect(screen, [0, 255, 0], [width / 2 + 20, 420, 180, 40])
        screen.blit(save, [width / 2 + 35, 422])
        screen.blit(quit_text, [10, height - 35])
        pygame.display.flip()
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(0, height - 40, 100, 40).collidepoint(pygame.mouse.get_pos()):
                    options_running = False
                if pygame.Rect(width / 2 - 200, 420, 180, 40).collidepoint(pygame.mouse.get_pos()):  # defaultowe ustawienia
                    options_object.set_default()
                    options_text = [(font_Arial.render(("Asteroid speed: " + str(options_object.asteroid_speed)), False, [0, 0, 255])),
                                    (font_Arial.render(("Asteroid size: " + str(options_object.asteroid_size)), False, [0, 0, 255])),
                                    (font_Arial.render(("Asteroid amount: " + str(options_object.asteroid_amount)), False, [0, 0, 255])),
                                    (font_Arial.render(("Astronaut speed: " + str(options_object.astronaut_speed)), False, [0, 0, 255])),
                                    (font_Arial.render(("Astronaut size: " + str(options_object.astronaut_size)), False, [0, 0, 255])),
                                    (font_Arial.render(("Point size: " + str(options_object.point_size)), False, [0, 0, 255])),
                                    (font_Arial.render(("Point amount: " + str(options_object.point_amount)), False, [0, 0, 255])),
                                    (font_Arial.render(("Spaceship size: " + str(options_object.spaceship_size)), False, [0, 0, 255]))]
                    spaceship_object.size = options_object.spaceship_size
                    spaceship_object.size_change()
                elif pygame.Rect(width / 2 + 20, 420, 180, 40).collidepoint(pygame.mouse.get_pos()):  # zapisywanie ustawień do pliku
                    open("/Content/Data_files/Options.txt", "w").close()
                    f = open("/Content/Data_files/Options.txt", "w")
                    f.write("asteroid_speed = " + str(options_object.asteroid_speed) + "\n")
                    f.write("asteroid_size = " + str(options_object.astronaut_size) + "\n")
                    f.write("asteroid_amount = " + str(options_object.asteroid_amount) + "\n")
                    f.write("astronaut_speed = " + str(options_object.astronaut_speed) + "\n")
                    f.write("astronaut_size = " + str(options_object.astronaut_size) + "\n")
                    f.write("point_size = " + str(options_object.point_size) + "\n")
                    f.write("point_amount = " + str(options_object.point_amount) + "\n")
                    f.write("spaceship_size = " + str(options_object.spaceship_size) + "\n")
                    f.close()  # todo wsm chuj mnie to boli ale jak chcesz to te warunki jakoś skróć by nie było tego spaghetti
                elif pygame.Rect(width / 2 - 200, 55, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    if options_object.asteroid_speed > 1:
                        options_object.asteroid_speed -= 1
                        options_text[0] = (font_Arial.render(("Asteroid speed: " + str(options_object.asteroid_speed)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 - 200, 100, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    if options_object.asteroid_size > 1:
                        options_object.asteroid_size -= 1
                        options_text[1] = (font_Arial.render(("Asteroid size: " + str(options_object.asteroid_size)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 - 200, 145, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    if options_object.asteroid_amount > 1:
                        options_object.asteroid_amount -= 1
                        options_text[2] = (font_Arial.render(("Asteroid amount: " + str(options_object.asteroid_amount)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 - 200, 190, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    if options_object.astronaut_speed > 1:
                        options_object.astronaut_speed -= 1
                        options_text[3] = (font_Arial.render(("Astronaut speed: " + str(options_object.astronaut_speed)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 - 200, 235, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    if options_object.astronaut_size > 1:
                        options_object.astronaut_size -= 1
                        options_text[4] = (font_Arial.render(("Astronaut size: " + str(options_object.astronaut_size)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 - 200, 280, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    if options_object.point_size > 1:
                        options_object.point_size -= 1
                        options_text[5] = (font_Arial.render(("Point size: " + str(options_object.point_size)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 - 200, 325, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    if options_object.point_amount > 1:
                        options_object.point_amount -= 1
                        options_text[6] = (font_Arial.render(("Point amount: " + str(options_object.point_amount)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 - 200, 370, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    if options_object.spaceship_size > 1:
                        options_object.spaceship_size -= 1
                        options_text[7] = (font_Arial.render(("Spaceship size: " + str(options_object.spaceship_size)), False, [0, 0, 255]))
                        spaceship_object.size = options_object.spaceship_size
                        spaceship_object.size_change()
                elif pygame.Rect(width / 2 + 160, 55, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    options_object.asteroid_speed += 1
                    options_text[0] = (font_Arial.render(("Asteroid speed: " + str(options_object.asteroid_speed)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 + 160, 100, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    options_object.asteroid_size += 1
                    options_text[1] = (font_Arial.render(("Asteroid size: " + str(options_object.asteroid_size)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 + 160, 145, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    options_object.asteroid_amount += 1
                    options_text[2] = (font_Arial.render(("Asteroid amount: " + str(options_object.asteroid_amount)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 + 160, 190, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    options_object.astronaut_speed += 1
                    options_text[3] = (font_Arial.render(("Astronaut speed: " + str(options_object.astronaut_speed)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 + 160, 235, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    options_object.astronaut_size += 1
                    options_text[4] = (font_Arial.render(("Astronaut size: " + str(options_object.astronaut_size)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 + 160, 280, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    options_object.point_size += 1
                    options_text[5] = (font_Arial.render(("Point size: " + str(options_object.point_size)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 + 160, 325, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    options_object.point_amount += 1
                    options_text[6] = (font_Arial.render(("Point amount: " + str(options_object.point_amount)), False, [0, 0, 255]))
                elif pygame.Rect(width / 2 + 160, 370, 40, 40).collidepoint(pygame.mouse.get_pos()):
                    options_object.spaceship_size += 1
                    options_text[7] = (font_Arial.render(("Spaceship size: " + str(options_object.spaceship_size)), False, [0, 0, 255]))
                    spaceship_object.size = options_object.spaceship_size
                    spaceship_object.size_change()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    options_running = False
            elif event.type == pygame.QUIT:
                sys.exit()
        clock.tick(60)


def main():  # odpala wszystko
    options_object.options_init()
    while True:
        menu()
        game()
        input()


# włącz pygame itp
pygame.init()
pygame.font.init()
# zmienne do funckji i innych
font_Arial = pygame.font.SysFont("Arial", 30)
width = 720
height = 480
clock = pygame.time.Clock()
screen = pygame.display.set_mode([width, height])
game_running = True
options_object = Options()
astronauts = []
lost_astronauts = []
spaceship_object = SpaceShip(options_object.spaceship_size)
leaderboard_object = Leaderboard()
stars = []
for i in range(0, 20):
    stars.append(Star())

# start gry
main()
# todo jak skonczysz wszystko to zmien wartości width i hight na cyfry zamiast dzielić je w przyciskach, przyspieszy to gre chyba itp
# todo poukładaj te klasy i funkcje by były w jakiejś kolejności
# todo zrób dymki za postacią
'''pojawiają się tylko co jakiś czas, i znikają po sekundzie, pojawiają się przy prędkości wyższej niż ustawiona czyli mouse_rel,mogą się pojawiać np max 5 na sekunde np.
 if predkosc>min_predkosc:
    if czas teraz>zeszły czas + 200ms:
        zrespij randomowo dymek na pozycji astronauty
        zeszły czas=czas teraz'''

