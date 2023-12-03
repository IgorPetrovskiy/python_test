from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = player_width
        self.height = player_height
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('крп.png', self.rect.centerx, self.rect.top, 1, 1, 15)
        bullets.add(bullet)
misseds = 0
goal = 10
max_misseds = 3
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global misseds
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(0, win_width - 80)
            misseds += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
win_width = 700
win_height = 500

player = Player('f-16.png', 5, win_height - 80, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy('mig29.png', randint(0, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)


window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load('field.jpg'), (win_width, win_height))

#Шрифти і написи
font.init()
font = font.Font(None, 25)
win = font.render('YOU WIN!!!', True, (255, 215, 0))
lose = font.render('YOU LOSE!!!', True,(180, 0, 0))



mixer.init()
mixer.music.load('freebird.mp3')
mixer.music.play(-1)
speed = 10

score = 0
run = True
finish = False
clock = time.Clock()
FPS = 60


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if not finish:
        window.blit(background, (0, 0))
        bullets.update()
        bullets.draw(window)
        wallet = font.render('Рахунок' + str(score), 0.25, (255, 255, 255))
        missed = font.render('Пропущено' + str(misseds), 0.25, (255, 255, 255))
        window.blit(missed, (10, 50))
        window.blit(wallet, (10, 20))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        #Перевірка зіткнення куль і мострів
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for s in collides:
            score += 1
            monster = Enemy('mig29.png', randint(0, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or misseds >= max_misseds:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
    else:
        finish = False
        score = 0
        misseds = 0
        for b in bullets:
            b.kill()
        for a in monsters:
            a.kill()
        time.delay(3000)
        for i in range(1, 5):
            monster = Enemy('mig29.png', randint(0, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

    display.update()
    clock.tick(FPS)
