# Credits: Tech with Tim tutorial
# YT link:https://youtu.be/Q-__8Xw9KTM

import pygame
import os
import random
import time

pygame.font.init()

WIDTH = 1000
HEIGHT = 700

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "background-black.png")),
    (WIDTH, HEIGHT))

LASER_BLUE = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
LASER_GREEN = pygame.image.load(os.path.join("assets",
                                             "pixel_laser_green.png"))
LASER_RED = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
LASER_YELLOW = pygame.image.load(os.path.join("assets",
                                              "pixel_laser_blue.png"))

SHIP_BLUE = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))
SHIP_GREEN = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))
SHIP_RED = pygame.image.load(os.path.join("assets",
                                          "pixel_ship_red_small.png"))
SHIP_YELLOW = pygame.image.load(os.path.join("assets",
                                             "pixel_ship_yellow.png"))

WHITE = (255, 255, 255)
HEALTHBAR = (255, 0, 0)

class Lasers():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y -= vel

    def off_screen(self):
        return self.y > HEIGHT or self.y < 0

    def collision(self, obj):
        return collide(self, obj)

def collide(obj1, obj2):
    #Apparently obj 2 - obj 1 works pixel perfect
    # #############      BUT        #############
    # Obj1 - obj2 does not collide pixel perfect
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask , (offset_x, offset_y)) != None


class Ship():
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.lasers = []
        self.laser_img = None

    def draw(self, window):
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))
        window.blit(self.ship_img, (self.x, self.y))
        self.healthbar(window)
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, objs: list):
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        self.lasers.remove(laser)
                        obj.health -= 10
                        if obj.health <= 0:
                            objs.remove(obj)


    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def shoot(self):
        laser = Lasers(self.x, self.y, self.laser_img)
        self.lasers.append(laser)

    def healthbar(self, window):
        pygame.draw.rect(window, HEALTHBAR, (self.x + (self.get_width() - self.health)/2, self.y - 10, self.health, 10))
        

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = SHIP_YELLOW
        self.laser_img = LASER_YELLOW
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class Enemy(Ship):
    COLOR_MAP = {
        "red": (SHIP_RED, LASER_RED),
        "blue": (SHIP_BLUE, LASER_GREEN),
        "green": (SHIP_GREEN, LASER_GREEN),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        # self.x += vel
        self.y += vel


def main():
    run = True
    FPS = 60
    level = 1
    lives = 5

    enemies = []
    wave_length = 1
    enemy_vel = 5
    player_vel = enemy_vel + 2
    laser_vel = enemy_vel * 2


    main_font = pygame.font.SysFont("comicsans", 50)
    clock = pygame.time.Clock()

    player = Player(300, 250)

    # ship = Ship(300, 250)

    def redraw_window():
        WIN.blit(BACKGROUND, (0, 0))

        level_label = main_font.render(f"Level: {level}", 1, WHITE)
        lives_label = main_font.render(f"Lives: {lives}", 1, WHITE)

        WIN.blit(level_label, (10, 10))
        WIN.blit(lives_label, ((WIDTH - level_label.get_width() - 10), 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)
        if lives <= 0:
            lost = main_font.render(
                f"GAME OVER\nPress any key to begin new game", 1, WHITE)
            WIN.blit(lost, ((WIDTH - lost.get_width()) / 2,
                            (HEIGHT - lost.get_height()) / 2))

        pygame.display.update()

    while run:
        clock.tick(FPS)

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100),
                              random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green"]),
                              random.randrange(10,50))
                enemies.append(enemy)

        for event in pygame.event.get():
            # print(pygame.key.get_pressed())
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x >= 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player.get_width() <= WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player.get_height() <= HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(-laser_vel, [player])
            if random.randrange(0, FPS * 2) == 1:
                enemy.shoot()
            if collide(player, enemy):
                player.health -= 25
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(laser_vel, enemies)

        # why does this not work outside redraw func?
        # Or without using pygame.display.update?
        # Technically by running the function at the end
        # We do call pygame.display.update AFTER calling all blit funcs
        # if lives <= 0:
        #     lost = main_font.render("GAME OVER Press any key to begin new game", 1, WHITE)
        #     WIN.blit(lost, ((WIDTH - lost.get_width())/2, 100))
        # pygame.display.update()

        redraw_window()


if __name__ == "__main__":
    main()