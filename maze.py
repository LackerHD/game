from pygame import *
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 10:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_h - 80:
            self.rect.y += self.speed
        if keys[K_d] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 10:
            self.rect.x -= self.speed

class Enemy(GameSprite):
    nap = 'left'
    def update(self):
        if self.rect.x <= 450:
            self.nap = 'right'
        if self.rect.x >= win_w-80:
            self.nap = 'left'
        if self.nap == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

class Wall(sprite.Sprite):
    def __init__(self, color1, color2,color3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color1, color2, color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

        
win_w = 700
win_h = 500
window = display.set_mode((win_w, win_h))
display.set_caption('Лабиринт')
background = transform.scale(image.load('background.jpg'),(win_w,win_h))
player = Player('heoro.png',5,win_w - 80,4)
monster  = Enemy('pydj.png',3,win_w - 80,280)
gold = GameSprite('chafg.png',0,win_w - 120, win_h - 80)

wall1 = Wall(218, 112, 214, 20, 100, 100, 10)
wall2 = Wall(255, 0, 255, 100, 20, 100, 10)
wall3 = Wall(186, 85, 211, 20, 100,200, 10)


game = True
finish = False
FPS = 60
clock = time.Clock()

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

font.init()
font = font.Font(None, 70)
win = font.render('Сигма', True, (100, 189, 251))

lose = font.render('Не Сигма', True, (251, 189, 251))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        
        window.blit(background, (0,0))

        player.update()
        monster.update()

        player.reset()
        monster.reset()
        gold.reset()

        wall1.draw()
        wall2.draw()
        wall3.draw()
    
    if sprite.collide_rect(player, monster) or sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2) or sprite.collide_rect(player, wall3):
        finish = True
        kick.play()
        window.blit(lose, (200, 200))
    if sprite.collide_rect(player, gold):
        finish = True
        money.play()
        window.blit(win, (200, 200))
    display.update()
    clock.tick(FPS)