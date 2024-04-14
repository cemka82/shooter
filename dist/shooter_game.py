#Создай собственный Шутер!

from pygame import *
from random import randint

#muzikaaa
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()

font1 = font.SysFont('Arial', 80)

win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


#здесь должен быть шрифт
font.init()
font2 = font.SysFont('Arial', 36)

#картинки
img_back = "galaxy.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"

score = 0 #сбито кораблей
goal = 10 #столько кораблей нужно сбить для победы
lost = 0 #пропущено кораблей
max_lost = 3 #проиграли, если пропустили столько



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    #управление
    def update(self): 
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #выстрел
    def fire(self):
        global bullets
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


#класс энеми
class Enemy(GameSprite):
#автоматическое передживение
    def update(self):
        self.rect.y += self.speed
        global lost
#исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       #исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()


#окошечко 
win_height = 500
win_width = 700
window = display.set_mode((win_width, win_height))
display.set_caption("shooter_game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

ship = Player("rocket.png", 5, 400, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

bullets = sprite.Group()

finish = False
run = True
clock = time.Clock()
FPS = 60
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()


    if not finish:
        #нужно обновить фон
        window.blit(background, (0,0))
        #надо написать текст на экране
        score_str = str(score)
        text = font2.render("Счёт: " + score_str, 1, (255, 255, 255))
        window.blit(text, (10, 20))
        lost_str = str(lost)
        text_lose = font2.render("Пропущено: " + lost_str, 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

       #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)



        #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))




    display.update()
    clock.tick(FPS)
'''фор коллидес; иф спрайт коллидес; иф скор гоал;'''