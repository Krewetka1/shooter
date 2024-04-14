#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
class GameSprite (sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,played_speed):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(player_image),(size_x,size_y))
        self.speed=played_speed
        self.rect=self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x<win_width-80:
            self.rect.x+=self.speed  
        if keys[K_UP] and self.rect.y>5:
            self.rect.y-=self.speed
        if keys[K_DOWN] and self.rect.y<win_height-80:
            self.rect.y+=self.speed

    def fire(self):
        bullet=Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global lost 

        if self.rect.y>win_height:
            self.rect.x=randint(80,win_height-80)
            self.rect.y=0
            lost+=1

class Bullet(GameSprite):
    def update(self): 
        self.rect.y+=self.speed
        if self.rect.y<0:
            self.kill()
            
            
img_bullet='bullet.png'
img_monsters='ufo.png'
win_width=700
win_height=500


monsters = sprite.Group()
for i in range(1,6):
    monster=Enemy(img_monsters,randint(80,win_width-80),-40,80,50,randint(1,5))
    monsters.add(monster)

bullets=sprite.Group()
asteroids=sprite.Group()
for i in range(1,4):
    asteroid = Enemy('asteroid.png',randint(80,win_width-80),-40,80,50,randint(1,4))
    asteroids.add(asteroid)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play

fire_sound=mixer.Sound('fire.ogg')

lost=0
score=0
goal=10
max_lost=3

img_back='galaxy.jpg'
img_hero='rocket.png'

window=display.set_mode((win_width,win_height))
display.set_caption('Шутер')

background=transform.scale(
    image.load(img_back), (win_width,win_height)
)


ship=Player(img_hero,5,win_height-100,80,100,5)
font.init()
font2=font.Font(None,36)

font1=font.Font(None,80)

win=font1.render('YOU WIN!',True,(0,255,0))
lose=font1.render('YOU LOSE!',True,(255,0,0))

life=3
life_color=(0,255,0)
text_life=font2.render(str(life),1,life_color)
window.blit(text_life,(650,10))
ammo=5
text_ammo=font2.render(str(ammo),1,(255,255,255))
window.blit(text_ammo,(650,10))
clock=time.Clock()
FPS=60
run=True 
finish=False
rel_time=False
num_fire=0
while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
        
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                if num_fire <5 and rel_time==False:
                    fire_sound.play()
                    ship.fire()
                    num_fire+=1
                if num_fire >=5 and rel_time ==False:
                    last_time=timer()
                    rel_time=True


    if not finish:
        window.blit(background,(0,0))
        ship.update()
        ship.reset()
        text = font2.render('Счёт:'+ str(score),1,(255,255,255))
        window.blit(text,(10,20))

        if rel_time == True:
            now_time=timer()
            if now_time-last_time <3:
                reload = font2.render('Reload...',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire=0
                rel_time=False


        collides = sprite.groupcollide(monsters,bullets,True,True)
        
        for collide in collides:
            score +=1
            monster=Enemy(img_monsters,randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship,asteroids,False) or sprite.spritecollide(ship,monsters,False):
            life -=1
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)

        if lost>=max_lost or life==0:
            finish=True
            window.blit(lose,(200,200))

        if score >= goal:
            finish=True
            window.blit(win,(200,200))
            

        text_lose=font2.render('Пропущено:'+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        asteroids.draw(window)
        asteroids.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        display.update()

    else:
        finish=False
        score=0
        lost=0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(1,6):
            monster=Enemy (img_monsters,randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)
            
window.blit(background,(0,0))
clock.tick(FPS)
display.update()
