import pygame 

# Set Up pygame to work
pygame.init()

# ปรับขนาดหน้าจอ
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Uncle vs Covid-19') # Set ชื่อเกม
icon = pygame.image.load('icon.png') # โหลดภาพเข้ามาใน pygame
pygame.display.set_icon(icon)

pxchange = 1

#--------UNCLE-------#
# 1 - player - uncle.png

psize = 128


pimp = pygame.image.load('person.png')

px = 100 # จุดเริ่มต้นแกน X (แนวนอน)
py = HEIGHT - psize # จุดเริ่มต้นแกน Y (แนวตั้ง)

def Player(x,y):
    screen.blit(pimp, (x,y))


#--------UNCLE-------#
# 2 - enemy - virus.png
#pimp = pygame.image.load('virus.png')


#--------UNCLE-------#
# 1 - player - uncle.png
#pimp = pygame.image.load('uncle.png')


running = True #สั่งให้โปรแกรมทำงาน

clock = pygame.time.Clock()
FPS = 60

while running:
    for event in pygame.event.get():
        # รันลูปเช็คว่ามีการกดปิด pygame[x]
        if event.type == pygame.QUIT:
            running = False

    #px, py จุดเริ่มต้น 
    Player(px,py)
    if px <= 0:
        pxchange = 1
        px += pxchange
    elif px >= WIDTH - psize:
        pxchange = -1
        px += pxchange
    else:
        px += pxchange    
    

    pygame.display.update()
    clock.tick(FPS)



