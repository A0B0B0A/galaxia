from pygame import *
import random

init()  
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.3)

bullet_sound = mixer.Sound("fire.ogg")
bullet_sound.set_volume(1)
font.init()

font1 = font.SysFont('Impact', 100)
font2 = font.SysFont('Impact', 30)

game_over_text = font1.render("Game Over!", True, (255, 0, 0))

screen_info = display.Info()

WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h,
window = display.set_mode((WIDTH, HEIGHT), flags = FULLSCREEN)
FPS = 90
clock = time.Clock()

bg = image.load('infinite_starts.jpg')
bg = transform.scale(bg,(WIDTH, HEIGHT))

bg_y1 = 0
bg_y2 = -HEIGHT

p_img = image.load('images-removebg-preview.png')
warrior_img = image.load('h-removebg-preview.png')
bullet_img = image.load('JSDF-removebg-preview.png')
all_sprites = sprite.Group()

class NPC(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

class Player(NPC):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.speed = 5
        self.bg_speed = 2
        self.max_speed = 20
        self.score = 0 

    def fire(self):
        new_bullet = Bullet(bullet_img, 10, 30, self.rect.right - 30, self.rect.top )
        new_bullet2 = Bullet(bullet_img, 10, 30, self.rect.left + 20, self.rect.top )
        bullet_sound.play()


    def update(self):
        key_pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if key_pressed[K_w] :
            if self.rect.y > 250:
                self.rect.y -= self.speed
            if self.bg_speed < self.max_speed:
                self.bg_speed += 0.1
        if key_pressed[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            if self.bg_speed > 0:
                self.bg_speed -= 0.3
        if key_pressed[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        
        
        bos_hit = sprite.spritecollide(self, boses, False, sprite.collide_mask)
        if len(bos_hit):
            self.hp -= 100

bullets = sprite.Group()

class Bullet(NPC):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.rect.bottom = y
        self.damage = 100
        self.speed = 10
        bullets.add(self)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

            
class Bos(NPC):
    def __init__(self, sprite_img, width, height):
        rand_x = random.randint(0, WIDTH - width)
        super().__init__(sprite_img, width, height, rand_x, - 200)
        self.damage = 100
        self.speed = 4
        boses.add(self)

    def update(self):
        self.rect.y += player.bg_speed +2
        if self.rect.y > HEIGHT:
            self.kill()


player = Player(p_img, 100, 80, 300, 300)
score_aboba_text = font2.render(f"Score: {player.score}", True, (255, 255, 255))

boses = sprite.Group()
alien1 = Bos(warrior_img, 80, 60)

start_time = time.get_ticks()
alien_spawn_time = time.get_ticks()
spawn_interval = random.randint(500, 3000)

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False
            if e.key == K_SPACE:
                player.fire()

    window.blit(bg,(0, bg_y1))
    window.blit(bg,(0, bg_y2))
    bg_y1 += player.bg_speed
    bg_y2 += player.bg_speed
    
    if bg_y1 > HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 > HEIGHT:
        bg_y2 = -HEIGHT
    if player.hp <= 0 :
        finish = True
    
    all_sprites.draw(window)

    if not finish:
        all_sprites.update()
    
    bullets_collide = sprite.groupcollide(bullets, boses, True, True, sprite.collide_mask)
    for bullet in bullets_collide:
        player.score += 10
        score_aboba_text = font2.render(f"Score: {player.score}", True, (255, 255, 255))
    now = time.get_ticks()

    if now - alien_spawn_time > spawn_interval:
        rand_n = random.randint(1, 3)
        for _ in range(rand_n):
            alien1 = Bos(warrior_img, 80, 60)
        alien_spawn_time = time.get_ticks()
        spawn_interval = random.randint(500, 3000)
    if finish:
        window.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2))
    
    window.blit(score_aboba_text, (0, 0))

    display.update()
    clock.tick(FPS)