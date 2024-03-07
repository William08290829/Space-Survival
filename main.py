import pygame
import random        #引入隨機模組
import os 

FPS = 60                 #這種通常設定好就不會去改變的變數習慣用"大寫"表示
WIDTH = 500
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#遊戲初始化 & 創建視窗
pygame.init()   #把pygame初始化
pygame.mixer.init()    # 把音效初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT))  #畫面的寬度500 & 高度600 (第5、6行)
pygame.display.set_caption("Space Survival")    #命名視窗上面的標題 
clock = pygame.time.Clock()
rock_num = 10

#載入物件圖片
background_img = pygame.image.load(os.path.join("assets", "img", "background.png")).convert()    # os.path = 現在Pthyon 檔案的位置，convert()把圖片轉成pygame比較容易讀取的格式，這樣速度比較快
player_img = pygame.image.load(os.path.join("assets", "img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
# rock_img = pygame.image.load(os.path.join("assets", "img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("assets", "img", "bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("assets", "img", f"rock{i}.png")).convert())  # f"rock{i}.png"  在字串前面加上"f"就可以在字串裡放變數
#載入爆炸圖片
expl_anim = {}           # 用一個字典來表現爆炸
expl_anim['large'] = []
expl_anim['small'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("assets", "img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['large'].append(pygame.transform.scale(expl_img, (75, 75)))  #不同大小石頭爆炸大小不一
    expl_anim['small'].append(pygame.transform.scale(expl_img, (30, 30))) 
    player_expl_img = pygame.image.load(os.path.join("assets", "img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
# 載入寶物圖片
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("assets", "img", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("assets", "img", "gun.png")).convert()

#載入音樂、音效
shoot_sound = pygame.mixer.Sound(os.path.join("assets", "sound", "shoot.wav")) 
shield_sound = pygame.mixer.Sound(os.path.join("assets", "sound", "pow0.wav"))
gunup_sound = pygame.mixer.Sound(os.path.join("assets", "sound", "pow1.wav"))
die_sound = pygame.mixer.Sound(os.path.join("assets", "sound", "rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("assets", "sound", "expl0.wav")), 
    pygame.mixer.Sound(os.path.join("assets", "sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("assets", "sound", "background.ogg"))  #由於背景音樂要重複播放，寫法會不一樣
pygame.mixer.music.set_volume(0.4)      #改背景音樂的大小聲

#載入字體
font_name = os.path.join("assets", "font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

cover_font = os.path.join("assets", "genkai-mincho.ttf")
def draw_cover(surf, text, size, x, y):
    font = pygame.font.Font(cover_font, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect) 

def new_rock():           #撞到再給一顆石頭
    rock = Rock()         
    all_sprite.add(rock)
    rocks.add(rock)

def draw_health(surf, hp, x, y):   # 畫生命條
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if hp <= 40:
        pygame.draw.rect(surf, RED, fill_rect)
    else:
        pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)   # 此為外框，要加像素(2)，讓他空心

def draw_lives(surf, lives, img, x, y):    # 畫生命數
    for i in range(lives):
       img_rect =  img.get_rect()
       img_rect.x = x + 32*i    # 間隔三十二個像素再畫一個
       img_rect.y = y
       surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0, 0))
    draw_cover(screen, '太空生存戰', 72, WIDTH/2, HEIGHT/4)
    draw_text(screen, '<按任意鍵開始>', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)   
        # 取得輸入
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:  
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:  # KEYUP 是等按鈕鬆開才會開始
                waiting = False
                return False

def instr_init():     # 說明介面
    screen.blit(background_img, (0, 0))
    black_background = pygame.Surface((WIDTH,250), pygame.SRCALPHA, 32)
    black_background.fill((0, 0, 0, 80))
    screen.blit(black_background, (0, HEIGHT/4))
    draw_text(screen, '← → 或是 A D鍵 來移動飛船', 30, WIDTH/2, HEIGHT/3)
    draw_text(screen, '空白鍵發射子彈', 30, WIDTH/2, HEIGHT/3 + 30)
    
    shield_instr = power_imgs['shield']
    shield_instr_rect = shield_instr.get_rect()
    shield_instr_rect.x = 175
    shield_instr_rect.y = 300
    shield_instr.set_colorkey(BLACK)
    screen.blit(shield_instr, shield_instr_rect)
    draw_text(screen, ': 加血道具', 18, WIDTH/2, HEIGHT/2)

    gun_instr = power_imgs['gun']
    gun_instr_rect = gun_instr.get_rect()
    gun_instr_rect.x = 180
    gun_instr_rect.y = 340
    gun_instr.set_colorkey(BLACK)
    screen.blit(gun_instr, gun_instr_rect)
    draw_text(screen, ': 加子彈道具', 18, WIDTH/2, HEIGHT/2 + 40)
    
    draw_text(screen, '<按任意鍵開始遊戲>', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)   
        # 取得輸入
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:  
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:  # KEYUP 是等按鈕鬆開才會開始
                waiting = False
                return False


class Player(pygame.sprite.Sprite):   #設立一個類別叫做Player，並繼承pygame.sprite.Sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50, 40))   #建立個平面(寬50、高40)
        # self.image.fill(GREEN)                  #把平面圖上綠色
        self.image = pygame.transform.scale(player_img, (50, 38))  #換上圖片並改圖片的大小
        self.image.set_colorkey(BLACK)    #將飛船的黑色變成透明
        self.rect = self.image.get_rect()    #把這張圖片框起來，就可以設定它
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)   #在飛船上畫出碰撞範圍
        # self.rect.x = 200                    #將這平面的位置移到(200, 200)
        # self.rect.y = 200
        # self.rect.center = (WIDTH/2, HEIGHT/2)    #將它位於中間
        self.rect.centerx = WIDTH / 2        
        self.rect.bottom = HEIGHT - 10       #讓它下面在底部
        self.speedx = 8    #設定速度
        self.health = 100   # 生命條
        self.lives = 3 
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
    
    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now
        
        if self.hidden and now - self.hide_time > 1000:  #1000毫秒
            self.hidden = False
            self.rect.centerx = WIDTH / 2        
            self.rect.bottom = HEIGHT - 10
        
        key_pressed = pygame.key.get_pressed()    #pygame.key.get_pressed()會回傳一堆布林值表示哪些按鈕被按
        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:    #判斷右鍵有沒有被按
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:      #讓它不超出右邊
            self.rect.right = WIDTH
        if self.rect.left < 0:           #讓它不超出左邊
            self.rect.left = 0
        # self.rect.x +=2             #每次跑回圈都往右動2
        # if self.rect.left > WIDTH:   #判斷左邊是不是超出視窗
        #     self.rect.right = 0      #超出則將右邊的座標改成0 (從左邊跑出來)  
    
    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprite.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprite.add(bullet1)
                all_sprite.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):   
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 40))   
        # self.image.fill(RED)                  
        self.image_ori = random.choice(rock_imgs)        # 由於轉動會失帧，所以要放一個原來不會轉的(ori = original)
        self.image_ori.set_colorkey(BLACK) 
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()    #把這張圖片框起來，就可以設定它    
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)   #在石頭上畫出碰撞範圍
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)   #在這兩數字之中隨機回傳一個數字     
        self.rect.y = random.randrange(-180, -100)   #隨機的初始點      
        self.speedy = random.randrange(2, 10)    #掉下來的速度
        self.speedx = random.randrange(-3, 3)    #水平的速度
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3) 

    def rotate(self):   #讓石頭旋轉
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)   # 後面是旋轉幾度
        center = self.rect.center     # 在旋轉時要定位中心點，保存在center
        self.rect = self.image.get_rect()  # 給轉動後的圖片重新定位
        self.rect.center = center
    
    def update(self):
       self.rotate()
       self.rect.y += self.speedy
       self.rect.x += self.speedx 
       if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:    #超出下面or左邊or右邊
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)   #在這兩數字之中隨機回傳一個數字     
            self.rect.y = random.randrange(-100, -40)   #隨機的初始點      
            self.speedy = random.randrange(2, 15)    #掉下來的速度
            self.speedx = random.randrange(-3, 3)    #水平的速度     

class Bullet(pygame.sprite.Sprite):   
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10, 20))   
        # self.image.fill(YELLOW)                  
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()    #把這張圖片框起來，就可以設定它    
        self.rect.centerx = x     
        self.rect.bottom = y
        self.speedy = -10
        
    def update(self):
       self.rect.y += self.speedy
       if self.rect.bottom < 0:
           self.kill()       #如果超出上面，將它刪掉

class Explosion(pygame.sprite.Sprite):   
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)                  
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center     
        self.frame = 0
        self.last_update = pygame.time.get_ticks()  # pygame.time.get_tick 會給我們從初始化到現在的毫秒數
        self.frame_rate = 50   # 至少要經過50毫秒才會到下一張圖片

    def update(self):
       now = pygame.time.get_ticks()
       if now - self.last_update > self.frame_rate:     # 讓他更新率
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):     # 如果已經數到最後一張，消滅它
               self.kill()
            else: 
                self.image = expl_anim[self.size][self.frame]   # 換下一張
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):   
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)       
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()    #把這張圖片框起來，就可以設定它    
        self.rect.center = center    
        self.speedy = 3      # 寶物掉落速度
        
    def update(self):
       self.rect.y += self.speedy
       if self.rect.top > HEIGHT:
           self.kill()       #如果超出上面，將它刪掉



#播放背景音樂
pygame.mixer.music.play(-1)    # ( )裡面要寫說要撥放幾次，要無限播放寫-1


#遊戲迴圈
show_init = True
show_instr = True
running = True
while running :
    if show_init:    #遊戲初始畫面
        close = draw_init()
        if close:
            break
        if show_instr:
            close = instr_init()
            if close:
                break

            show_init = False
            all_sprite = pygame.sprite.Group()    #創建sprite的群組
            rocks = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powers = pygame.sprite.Group()
            player = Player()
            all_sprite.add(player)           #把Player加入all_sprite
            for i in range(rock_num):
                new_rock()
            #分數
            score = 0
    
    clock.tick(FPS)     #為解決不同電腦好壞跑迴圈的速度差，限制迴圈能跑的次數(FPS 次)
    # 取得輸入
    for event in pygame.event.get():   #pygame.event.get()會回傳所有的發生事件(回傳列表)
        if event.type == pygame.QUIT:  #事件的類型是不是"把遊戲關閉"
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()  
    
    #更新遊戲
    all_sprite.update()    #這樣寫會執行這個群組裡面每一個update函式
    # 判斷石頭 & 子彈相撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)  #兩個群組碰撞，後面再加上兩個布林值，決定說撞到要不要刪掉
    for hit in hits:          #hits 會回傳碰到的石頭和子彈
        random.choice(expl_sounds).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'large')
        all_sprite.add(expl)
        if random.random() > 0.95:   # random.random() 會回傳 0~1 之間隨機的值
            pow = Power(hit.rect.center)
            all_sprite.add(pow)
            powers.add(pow)
        new_rock()

    # 判斷石頭 & 飛船相撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)  #將碰撞用圓形判斷
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'small')
        all_sprite.add(expl)
        if player.health <= 0:   
            death_expl = Explosion(player.rect.center, 'player')
            all_sprite.add(death_expl)
            die_sound.play()
            player.lives -= 1     #扣一命
            player.health = 100   #回滿血
            player.hide()         #讓他藏起來一段時間  
    
    # 判斷寶物 & 飛船相撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health +=20
            if player.health > 100:
                player.health = 100
                shield_sound.play()
        elif hit.type == 'gun':
            player.gunup()    #加槍數的函式
            gunup_sound.play()

    if player.lives == 0 and not(death_expl.alive()):  # 等die不存在(也就是動畫跑完)才結束
            show_init = True
    
    #畫面顯示
    screen.fill(BLACK)  #畫面填滿顏色，用元組表達R、G、B(第4行)
    screen.blit(background_img, (0, 0))  # blit 就是畫的意思，後面是座標
    all_sprite.draw(screen)     #把all_sprite全部畫在screen上面
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    pygame.display.update() 

pygame.quit()    #把遊戲關掉