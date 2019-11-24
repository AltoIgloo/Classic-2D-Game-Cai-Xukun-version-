import pygame as pg
from sys import exit
from time import sleep
#########################################################以下是初始化
pg.init()
screen = pg.display.set_mode((1200,700))
pg.display.set_caption("落体运动")
width  = 60
height = 110
player1L = pg.image.load("cxk左.png")
player1UL = pg.image.load("cxk上左.png")
player1R = pg.image.load("cxk右.png")
player1UR = pg.image.load("cxk上右.png")
player1L = pg.transform.smoothscale(player1L,(width,height))
player1UL = pg.transform.smoothscale(player1UL,(width,height))
player1R = pg.transform.smoothscale(player1R,(width,height))
player1UR = pg.transform.smoothscale(player1UR,(width,height))
pos = [300,50]
black = 0,0,0
dicLR = {pg.K_a:0,pg.K_d:0}
clock = pg.time.Clock()
rectcolor = [155,155,155]
rectpos = [0,670,1200,10]
rectwid = 10
Dv = 0    #向下分速度
Uv = 0    #向上分速度
g = 1     #重力加速度
posx = 0  #水平位置变化
posy = 0  #竖直位置变化
jumpok = 0#连跳次数限制
rl = 0    #表示左右程度，0是左，1是右
player = player1L

def platform(pfx,pfy,pfl):#定义平台
    global pos,Dv,jumpok,rl,player,playerL,playerR,player1UL,player1UR
    if (pfy-height-30 < pos[1] < pfy-height+20 and pfx-width < pos[0] < pfx+pfl):  #检测平台缓冲区间
            if pos[1] < pfy - height-5:                
                if rl == 0:
                    player = player1UL
                else:
                    player = player1UR
            else:                
                jumpok = 0
                Dv = 0      
                pos = [pos[0],pfy-height+1]
                if rl == 0:                    
                    player = player1L
                else:                    
                    player = player1R
                    
def Lwall(Lwx,Lwy,Lwl):#定义左墙
    global pos,Uv,Dv,g,jumpok,rl,player,playerL,playerR,player1UL,player1UR
    if (Lwx - 20 < pos[0] + width < Lwx + 20 and pos[1] + height > Lwy and pos[1] < Lwy + Lwl):#检测墙壁左侧缓冲区间        
        if pos[0] + width > Lwx:            
            pos[0] = Lwx - width - 5
            
def Rwall(Rwx,Rwy,Rwl):#定义右墙
    global pos,Uv,Dv,g,jumpok,rl,player,playerL,playerR,player1UL,player1UR
    if (Rwx + 20 > pos[0] > Rwx - 20 and pos[1] + height > Rwy and pos[1] < Rwy + Rwl ):#检测墙壁右侧缓冲区间        
        if pos[0] < Rwx:            
            pos[0] = Rwx + 5
        
##########################################################以上是初始化，以下全部是循环体
while True:
    sleep(0.01)
    pg.draw.rect(screen,rectcolor,[0,670,1200,10],rectwid) #地面
    pg.draw.rect(screen,rectcolor,[800,525,200,20],rectwid)#最低平台
    pg.draw.rect(screen,rectcolor,[500,400,200,20],rectwid)#次低平台
    pg.draw.rect(screen,rectcolor,[100,300,200,20],rectwid)#最左平台
    pg.draw.rect(screen,rectcolor,[750,150,350,20],rectwid)#最高平台
    pg.draw.rect(screen,rectcolor,[200,570,300,110],rectwid)#左侧贴地方块
    clock.tick(60)    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key in dicLR:
                dicLR[event.key] = 10
                if event.key == pg.K_a:
                    player = player1L
                    rl = 0
                else:
                    player = player1R
                    rl = 1
            if event.key == pg.K_w:
                jumpok = jumpok + 1
                print(jumpok)
                if jumpok < 2:                    
                    Uv = 14
                    Dv = 0                      
            if event.key == pg.K_s:
                print('squat')
        elif event.type == pg.KEYUP:
            if event.key in dicLR:
                dicLR[event.key] = 0
            if event.key == pg.K_w:
                print('hold')
            if event.key == pg.K_s:
                print('at ease')                
########################################################以上是按键响应，以下是踩踏检测    
    if pos[1] < 555:#检测是否在地面之上
        if rl == 0:
            player = player1UL
        else:
            player = player1UR 
                               
        platform(pfx=100, pfy=300, pfl=200)#最左平台
        platform(pfx=500, pfy=400, pfl=200)#次低平台
        platform(pfx=800, pfy=525, pfl=200)#最低平台
        platform(pfx=750, pfy=150, pfl=350)#最高平台
        platform(pfx=210, pfy=570, pfl=280)#左侧贴地方块顶部平台
        Lwall(Lwx=200, Lwy=570, Lwl=130)   #左侧贴地方块左墙
        Rwall(Rwx=500,Rwy=570,Rwl=130)     #左侧贴地方块右墙
        
        if Uv > 0:
            Uv = Uv - g
        else:
            Dv = Dv + g        
    else:
        jumpok = 0
        Dv = 0      
        pos = [pos[0],556]
        Lwall(Lwx=200, Lwy=570, Lwl=130)   #左侧贴地方块左墙
        Rwall(Rwx=500,Rwy=570,Rwl=130)     #左侧贴地方块右墙
        if rl == 0:
            player = player1L
        else:
            player = player1R 
###########################################################以上是踩踏检测,以下是出界检测
    if pos[0] > 1200:
        pos[0] = -40
    if pos[0] < -50:
        pos[0] = 1190  
##########################################################以上是出界检测                      
    posx = pos[0]+dicLR[pg.K_d]-dicLR[pg.K_a]
    posy = pos[1]-Uv+Dv
    pos = [posx,posy]
    screen.blit(player,pos)
    pg.display.update()
    screen.fill(black)