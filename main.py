from pygame import *
from GameSprite import *
from Player import *
from enemy import *
from time import time as timer

def main():
    #фоновая музыка
    mixer.init()
    mixer.music.load('space.ogg')
    mixer.music.play()
    fire_sound = mixer.Sound('fire.ogg')


    font.init()
    font1 = font.SysFont('Arial', 40)

    win = font1.render('YOU WIN:(', True, (255,255,255))
    lose = font1.render('YOU LOSE:)', True, (255,255,255))

    # нам нужны такие картинки:
    img_back = "galaxy.jpg" # фон игры
    img_hero = "rocket.png" # герой
    img_enemy = "ufo.png"

    # Создаем окошко
    win_width = 1200
    win_height = 900
    display.set_caption("Shooter")
    window = display.set_mode((win_width, win_height))
    background = transform.scale(image.load(img_back), (win_width, win_height))

    # создаем спрайты
    ship = Player(img_hero, 5, win_height - 100, 80, 100, 10, win_width, win_height, window)
    monsters = sprite.Group()
    for i in range(1, 6):
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5), win_width, win_height, window)
        monsters.add(monster)

    asteroids = sprite.Group()
    for i in range(1, 3):
        asteroid = Enemy('asteroid.png', randint(80, win_width - 80), -40, 50, 50, randint(1,5), win_width, win_height, window)
        asteroids.add(asteroid)





    bullets = sprite.Group()
    clock = time.Clock()
    lost = 0
    score = 0
    ammo = 30
    reload = False
    # переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
    finish = False
    # Основной цикл игры:
    run = True # флаг сбрасывается кнопкой закрытия окна
    while run:
        # событие нажатия на кнопку Закрыть
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == MOUSEBUTTONDOWN and ammo > 0:
                if e.button == 1:
                    fire_sound.play()
                    bullets.add(ship.fire())
                    ammo = ammo - 1

        new_time = timer()

        if ammo <= 0 and reload == False:
            reload = True
            old_time = timer()

        if reload == True:
            if new_time - old_time >= 1:
                ammo = 30
                reload = False

        if not finish:
            # обновляем фон
            window.blit(background,(0,0))
            lost_text = font1.render('Пропущено:' + str(lost), True, (255,255,255))
            window.blit(lost_text,(10, 10))
            score_text = font1.render('Сбито:' + str(score), True, (255,255,255))
            window.blit(score_text,(10, 40))
            score_text = font1.render('Патронов:' + str(ammo), True, (255,255,255))
            window.blit(score_text,(10, 70))

            # производим движения спрайтов
            ship.update()
            for m in monsters:
                lost += m.update()

            collides = sprite.groupcollide(monsters, bullets, True, True)
            collides1 = sprite.groupcollide(asteroids, bullets, False, True)
            for c in collides:

                score = score + 1
                monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5), win_width, win_height, window)
                monsters.add(monster)
            if sprite.spritecollide(ship, monsters, False) or lost >= 5 or sprite.spritecollide(ship, asteroids, False):
                finish = True
                window.blit(lose, (200, 200))
            
            if score >= 100:
                finish = True
                window.blit(win, (200, 200))

            # обновляем их в новом местоположении при каждой итерации цикла
            asteroids.update()
            bullets.update()
            ship.reset()
            monsters.draw(window)
            bullets.draw(window)
            asteroids.draw(window)

            display.update()
        # цикл срабатывает каждую 0.05 секунд
        clock.tick(60)

if __name__ == '__main__':
    main()