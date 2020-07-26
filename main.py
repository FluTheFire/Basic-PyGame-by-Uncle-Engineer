import pygame
import math
import random
import time
import csv
from pygame import mixer



# Set Up pygame to work
pygame.init()

# ปรับขนาดหน้าจอ
WIDTH = 1000
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Uncle vs Covid-19') # Set ชื่อเกม
icon = pygame.image.load('icon.png') # โหลดภาพเข้ามาใน pygame
pygame.display.set_icon(icon)

background = pygame.image.load('background.jpg')


p_speed = 5
pxchange = 0


#--------UNCLE-------#
# 1 - player - uncle.png
psize = 128

pimp = pygame.image.load('person.png')

px = 100 # จุดเริ่มต้นแกน X (แนวนอน)
py = HEIGHT - psize # จุดเริ่มต้นแกน Y (แนวตั้ง)

def Player(x,y):
    screen.blit(pimp, (x,y)) # bilt = วางภาพในหน้าจอ


#--------Apple-------#
# 2 - item - apple.png
esize = 64

aimg = pygame.image.load('apple.png')
ex = 50
ey = 0
eychange = 5

# เช็คว่า apple ตกยังจะได้ไม่ตกซ้ำ
Aple_Fall = False

def Apple(x, y):
    screen.blit(aimg, (x,y))

def reset_Apple():
    global ex, ey, allscore
    ey = -20
    ex = random.randint(esize, WIDTH - esize)

#--------Multi-Enemy-----#
# 3 - enemy - virus.png
eimg = pygame.image.load('virus.png')
exlist = [] #ตำแหน่งแกน x ของ enemy
eylist = [] #ตำแหน่งแกน y ของ enemy
ey_change_list = []
allenemy = 4

def Enemy(x, y):
    screen.blit(eimg, (x,y))

def reset_Multi_Enemy(i):
    global exlist, eylist
    eylist[i] = -20
    exlist[i] = random.randint(esize, WIDTH - esize)
    ey_change_list[i] = random.randint(1,5)


for i in range(allenemy):
    exlist.append(random.randint(esize, WIDTH - esize))
    eylist.append(-20)
    ey_change_list.append(random.randint(1,5)) #สุ่มความเร้วให้ enemy

#--------Boss-------#
b_coming = False
bsize = 64

bimg = pygame.image.load('boss.png')
bx = 50
by = 0
bychange = 5

def Boss(x, y):
    screen.blit(bimg, (x,y))

def reset_Boss():
    global bx, by, b_coming
    by = -20
    bx = random.randint(esize, WIDTH - esize)
    b_coming = False

#--------Mask-------#
# 3 - mask - mask.png
msize = 64

mimg = pygame.image.load('sword.png')
mx = 100
my = HEIGHT - psize
mychange = 20
mstate = 'ready'

def fire_mask(x, y):
    global mstate
    mstate = 'fire'
    screen.blit(mimg, (mx,my))


#-------COLLISION-------#

def isCollision(ecx, ecy, mcx, mcy):
    # isCollision เช็คว่าชนกันหรือไม่? หากชนกันให้บอกว่า ชน (True)
    distance = math.sqrt(math.pow(ecx - mcx, 2) + math.pow(ecy - mcy, 2))
    
    if distance < (esize / 2) + (msize / 2):
        return True
    else:
        return False

#-------SOUND-------------
sound_shot = pygame.mixer.Sound('shot.wav')
sound_damage = pygame.mixer.Sound('damage.wav')
sound_reload = pygame.mixer.Sound('reload.wav')
    
#-------SCORE----------#
allscore = 0
font = pygame.font.Font('angsa.ttf', 60)

def showscore():
    score = font.render(f'Score: {allscore}',True, (255,255,255))
    screen.blit(score,(30,20))


#-------Ammo------------#
# จำนวนกระสุน
ammo_count = 10

def showammo():
    ammo = font.render(f'{ammo_count}/inf.',True, (0,0,0))
    screen.blit(ammo,(HEIGHT - 40, 20))

def reload():
    global ammo_count
    sound_reload.play()
    ammo_count = 10


#--------High Score-----#

highscore = 0

def readHighScore():
    global highscore
    with open('highscore.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            highscore = int(row[0])

def showHighscore():
    highscorebar = font.render(f'HighScore: {highscore}',True, (255,0,255))
    screen.blit(highscorebar,(30,65))

readHighScore()

#--------Heart---------#
# player health
health = 3

def showhealth():
    healthbar = font.render(f'Health: {health}',True, (255,0,0))
    screen.blit(healthbar,(30,110))


#-------Game Over------#
fontover = pygame.font.Font('angsa.ttf',120)
fontrestart = pygame.font.Font('angsa.ttf', 90)
gameover = False

def GameOver():
    global gameover
    overtext = fontover.render('Game Over',True, (255,0,0))
    screen.blit(overtext,(WIDTH / 2 - 170, HEIGHT / 2 - 100))

    overtext = fontrestart.render('Press \'N\' to Restart',True, (255,255,0))
    screen.blit(overtext,(WIDTH / 2 - 170 - 35, HEIGHT / 2 - 100 + 80))

    gameover = True



running = True #สั่งให้โปรแกรมทำงาน

clock = pygame.time.Clock() # game clock
FPS = 60 # frame rate

It_Down = False


#---------GAME LOOP----------------
while running:

    screen.blit(background, (0, 0))
    showscore()
    showammo()
    showhealth()
    showHighscore()
    

    for event in pygame.event.get():
        # รันลูปเช็คว่ามีการกดปิด pygame[x]
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            It_Down = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                pxchange = -p_speed
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                pxchange = p_speed
            if event.key == pygame.K_SPACE and not gameover:
                if mstate == 'ready' and ammo_count > 0:
                    sound_shot.play()
                    mx = px
                    ammo_count -= 1
                    fire_mask(mx, my)
            if event.key == pygame.K_r and not gameover and ammo_count < 10:
                reload()
            if event.key == pygame.K_n and gameover:
                gameover = False
                for i in range(allenemy):
                    reset_Multi_Enemy(i)
                reset_Apple()
                health = 3
                ammo_count = 10
                allscore = 0
                readHighScore()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or  event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                It_Down = False

    
    #---------------Game Over----------------
    #ถ้าเลือดเหลือ 0 Gameover
    if health <= 0:
        health = 0
        if allscore > highscore:
            with open('highscore.csv', 'w', newline='') as f:
                thewriter = csv.writer(f)

                thewriter.writerow([f'{allscore}'])
        GameOver()

    #----------------Run Player---------------------
    #px, py จุดเริ่มต้น 
    #--> ทำให้ player ขยับซ้ายขวาเมื่อชนขอบจอ
    Player(px,py)

    # Move Player
    if not gameover:
        px += pxchange
        if px <= 0:
            # หากชนขอบจอว้าย ให้ปรับค่า pxchange = 1
            pxchange = 0
            px = 1
            
        elif px >= WIDTH - psize:
            # หากชนขอบจอขวา ให้ปรับค่า pxchange = -1
            pxchange = 0
            px = WIDTH - psize - 1    

    if not It_Down:
        pxchange = 0
   
    
   

    

    #---------------Run Apple-----------------------
    if not gameover and allscore % 5 == 0 and allscore != 0:
        Apple(ex, ey)
        ey += eychange

    # เข็คว่าชนศัตรูยัง
    collision = isCollision(ex, ey, px, py)
    if collision:
        reset_Apple()
        #กิน apple แล้วเพิ่ม speed
        p_speed += 20
        
    if ey >= WIDTH:
        reset_Apple()

    

    
    #---------------Run Multi Enemy------------------
    for i in range(allenemy):
        # เพิ่มความเร็วของ enemy
        eylist[i] += ey_change_list[i]
        colissionmulit = isCollision(exlist[i], eylist[i], mx ,my)

        if gameover:
            break

        if colissionmulit:
            my = HEIGHT - psize
            mstate = 'ready'
            sound_damage.play()
            reset_Multi_Enemy(i)
            allscore += 1
        
        if eylist[i] >= WIDTH:
            health -= 1;
            reset_Multi_Enemy(i)

        Enemy(exlist[i], eylist[i])
    
    
    #-------------Run Boss-----------------------
    if allscore % 5 == 0 and allscore != 0:
        b_coming = True
    
    if b_coming and not gameover:
        Boss(bx, by)
        by += bychange

        collision = isCollision(bx, by, mx, my)
        if collision:
            my = HEIGHT - psize
            mstate = 'ready'
            # ฆ่าบอส heal เลือด 1
            health += 1
            reset_Boss()
            

        if by >= WIDTH:
            allscore -= 2
            reset_Boss()


    #--------------Fire Mask------------------------
    if mstate == 'fire':
        fire_mask(mx, my)
        my -= mychange
    
    # เช็คว่า Mask วิ่งไปชนขอบบนแล้วยัง? ถ้าชนให้ state เปลี่ยนเป็นพร้อมยิง
    if my <= 0:
        my = HEIGHT - psize
        mstate = 'ready'

    pygame.display.update()
    screen.fill((0,0,0))
    clock.tick(FPS)



