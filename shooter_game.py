#Создай собствен
import pygame
from pygame import mixer
from random import randint


class Sprite(pygame.sprite.Sprite):
    def __init__(self, path, w, h, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(path), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(Sprite):
    def __init__(self, path, w, h, x, y):
        super().__init__(path, w, h, x, y)
        self.dx = 0

    def update(self):
        self.rect.x += self.dx


class Bullet(Sprite):
    def __init__(self, path, w, h, x, y):
        super().__init__(path, w, h, x, y)
        self.speed_y =  5
        
    def update(self):
        self.rect.y -= self.speed_y


class Enemy(Sprite):
    def __init__(self, path, w, h, x, y):
        super().__init__(path, w, h,x, y)
        self.speed = 5
        
    def update(self):
        global lost, state, points
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.y = randint(-200,0)
            lost += 1
        hit_bullets = pygame.sprite.spritecollide(self, bullets, True)
        if hit_bullets:
            self.rect.y = randint(-200, 0)
            points += 1
            for bullet in hit_bullets:
                bullets.remove(bullet)
                del bullet
        if self.rect.colliderect(player):
            state = 'lose'
                    
                
bullets = pygame.sprite.Group()

monsters = pygame.sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', 70, 40, 100 * i, randint(-200, 0))
    monsters.add(monster)


FPS = 30
pygame.init()
pygame.font.init()
font1 = pygame.font.Font(None,36)
font2 = pygame.font.Font(None,50)
window = pygame.display.set_mode((500, 700))
clock = pygame.time.Clock()

mixer.init()
mixer.music.load('space.ogg')

fire_sound = mixer.Sound('fire.ogg')
# mixer.music.load("fire.ogg")
bg = Sprite('galaxy.jpg', 500, 700, 0, 0)

player = Player('rocket.png', 40, 80, 400, 500)
run = True
lost = 0
state = 'game'
points = 0   

mixer.music.play()
counter = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event. key == pygame.K_SPACE and counter == 0:
                counter = 15
                bullet = Bullet('bullet.png', 10, 20, player.rect.x + 15, player.rect.y)
                fire_sound.play()
                bullets.add(bullet)
            if event.key == pygame.K_LEFT:
                player.dx = -5
            if event.key == pygame.K_RIGHT:
                player.dx = 5
        if event.type == pygame.KEYUP:
            player.dx = 0
    #ниже нужно продумать как мы будем писать код котрый будет отвечать за экран победы или поражения
    if counter > 0: 
        counter -= 1
    
    if points == 10:
        state = 'win'
    if lost ==  10:
        state ="lose"
    bg.draw()
    text_lose = font1.render('Пропущено: ' + str(lost), True, (255, 255, 255))
    points_text = font1.render("Счет: " + str(points), True,(255,255,255))
    window.blit(text_lose, (10,40))
    window.blit(points_text, (10, 10))
    if state == 'game':
        bullets.draw(window)
        bullets.update()
        player.draw()   
        player.update()
        monsters.draw(window)
        monsters.update()
    if state == 'win':
        text = font2.render('ПОБЕДА!', True, (0, 255, 0))
        window.blit(text, (140, 300))
    if state == 'lose':
        text = font2.render('ПОРАЖЕНИЕ!', True, (255, 0, 0))
        window.blit(text, (140, 300))
    pygame.display.update()
    clock.tick(FPS)
    


    