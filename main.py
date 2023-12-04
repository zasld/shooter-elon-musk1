from os import remove
import pygame as pg
from other import set_text
from sprites import *
from config import *
from other import *
from random import randint
from time import time
pg.init()

pg.display.set_caption("Elon Sus")
mw = pg.display.set_mode(WINDOWS_SIZE)
mw.fill(BACK_COLOR)
clock = pg.time.Clock()

background = pg.transform.scale(pg.image.load('pic\\teslas.jpg'),(WINDOWS_SIZE))
ship = Ship('pic\\elon.png', WINDOWS_SIZE[0]/2,WINDOWS_SIZE[1]/2,70,100)

sound_fon = pg.mixer.Sound('snd\\fon1.mp3')
sound_fire = pg.mixer.Sound('snd\\fire1.mp3')
sound_fon.play(-1)

stars = pg.sprite.Group()
fiers = pg.sprite.Group()
aliens = pg.sprite.Group()
meteor = pg.sprite.Group()
for i in range(20): stars.add(Star(True))




# aliens = []
play = True

key_wait = 0

SCORE = 0
TICKS = 0
ticks = 0
fps = 0
t = time()
gameover = False

while play:
    for e in pg.event.get():            
            if e.type == pg.QUIT or \
                    (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                play  = False    
    
    

    if gameover:
        game_over(mw)        
    else:
        mw.blit(background,(0,0))

        

        if pg.key.get_pressed()[pg.K_s]:
            ship.movey = 'down'
        if pg.key.get_pressed()[pg.K_w]:
            ship.movey = 'up'
        if pg.key.get_pressed()[pg.K_d]:
            ship.movex = 'right'
        if pg.key.get_pressed()[pg.K_a]:
            ship.movex = 'left'
        if pg.key.get_pressed()[pg.K_SPACE]: # ОГОНЬ
            ship.fire(fiers, sound_fire, FIRE_WAIT)  

        if pg.key.get_pressed()[pg.K_1]: # скорость корабля -
            ship.speed -= 1        
        if pg.key.get_pressed()[pg.K_2]: # скорость корабля +
            ship.speed += 1
        if pg.key.get_pressed()[pg.K_3]: # скорость стрельбы +        
            if FIRE_WAIT > 2:  FIRE_WAIT -= 1 
            else: FIRE_WAIT =  1
        if pg.key.get_pressed()[pg.K_4]: # скорость стрельбы -
            FIRE_WAIT += 1    
        if pg.key.get_pressed()[pg.K_5]: # скорость НЛО +
            for alien in aliens:
                alien.speed += 1        
        if pg.key.get_pressed()[pg.K_6]: # скорость НЛО -
            for alien in aliens:            
                if alien.speed > 2:  alien.speed -= 1 
                else: alien.speed =  1
        
        if pg.key.get_pressed()[pg.K_q]:    # Добавить НЛО
            alien_add(aliens, ALIEN_SPEED)
            alien_wait = 5
        if pg.key.get_pressed()[pg.K_9]:  # включить/выключить появление НЛО
            if key_wait == 0:
                ALIEN = not ALIEN
                key_wait = KEY_WAIT
            else:
                key_wait -= 1 
        
        
        

        # добавляем НЛО через заданный период
        if TICKS % NEW_ALIEN_WAIT == 1 :
            if ALIEN and len(aliens) < ALIENS_LIMIT:  alien_add(aliens, ALIEN_SPEED)


        # попаднаия пуль в НЛО
        collisions = pg.sprite.groupcollide(aliens, fiers, True, True)
        for a, f in collisions.items():       
            #print(a.rect.x, f[0].rect.x)
            SCORE += 1
            if SCORE % FIRE_BONUS == 0: 
                # каждые десять очков бонус к стрельбе
                FIRE_WAIT -= 2
                if FIRE_WAIT<2:FIRE_WAIT = 2
            NEW_ALIEN_WAIT -= 2
            if NEW_ALIEN_WAIT <= 0 : NEW_ALIEN_WAIT = 4
            ALIEN_SPEED += 0.05

        # столкновение игрока и НЛО
        if pg.sprite.spritecollide(ship, aliens, False):
            gameover = True
    
        

        aliens.update(ship)
        aliens.draw(mw)
        
        fiers.update()
        fiers.draw(mw)            
                    
        ship.update()
        ship.draw(mw)
        
        # подсчет FPS
        t2 = time()
        if t2-t > 1:                        
            t = t2        
            fps = TICKS-ticks
            ticks = TICKS

        # текст
        set_text(mw, f"Скорость - {ship.speed}", 30, (10,10))    
        set_text(mw, f"Огонь - {int(FIRE_WAIT)}", 30, (870,10))
        set_text(mw, int(ALIEN), 30, (960,680))
        set_text(mw, f"Чужих - {len(aliens)}", 30, (10,680))
        set_text(mw,f"ОЧКИ - {SCORE}", 40, (500,10))
        set_text(mw,f"звезд-{len(stars)}", 30, (500,680))
        set_text(mw, f"x-{ship.rect.x} y-{ship.rect.y}", 30, (150,680))
        set_text(mw,f"fps-{fps}", 30, (700,680))

    
    # добавляем звезды через заданный период
    if TICKS % STAR_WAIT == 0:        
        stars.add(Star())
    stars.update()
    stars.draw(mw)

    pg.display.update()
    clock.tick(FPS)
    pg.event.pump()
    TICKS += 1

pg.quit()