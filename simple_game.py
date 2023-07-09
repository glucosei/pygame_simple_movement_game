#2219임재욱
# timer
# 모듈 호출
import pygame
import time
import tkinter
#import threading
import random
import tkinter.font
         
global f
global g
global enemy_num

def set_parms():
    window=tkinter.Tk()
    window.title("수치 조절")
    window.geometry("640x400+50+100")
    window.resizable(False, False)

    label=tkinter.Label(window, height=3)
    label.pack()

    def value_check(self):
        global f
        label.config(text="초당 캐릭터에게 가하는 힘을 입력하세요.(단위: N*10)")
        valid = False
        if self.isdigit():
            if (int(self) <= 50 and int(self) >= 0):
                valid = True
        elif self == '':
            valid = True

        if valid:
            f=float(self)*10
        return valid

    def value_error(self):
        label.config(text=str(self) + "를 입력하셨습니다.\n올바른 값을 입력하세요.")

    def go_sim():
        global g
        global enemy_num
        g=float(entry_g.get())
        global enemy_num
        enemy_num=int(entry_enemy.get())
        window.destroy()
        simulate()

    validate_command=(window.register(value_check), '%P')
    invalid_command=(window.register(value_error), '%P')

    spinbox=tkinter.Spinbox(window, from_ = 0, to = 50, validate = 'all', validatecommand = validate_command, invalidcommand=invalid_command)
    spinbox.pack()

    label_g=tkinter.Label(window, height=3, text='중력가속도(단위: m/sec^2)')
    label_g.pack()
    entry_g=tkinter.Entry(window)
    entry_g.pack()

    label_enemy=tkinter.Label(window, height=3, text='적의 수')
    label_enemy.pack()
    entry_enemy=tkinter.Entry(window)
    entry_enemy.pack()
    
    to_sim=tkinter.Button(window, text='시뮬레이션으로', command=go_sim)
    to_sim.pack()
    window.mainloop()






def simulate():
    # 파이게임 초기화(반드시 필요)
    pygame.init()
    
    #parms
    global f
    global g
    global enemy_num
    #print(f)
    char_m=10
    
    
    
    # 화면 크기 설정
    screen_width = 960       #화면 가로 크기
    screen_height = 960         #화면 세로 크기
    screen = pygame.display.set_mode((screen_width, screen_height))  # 튜플 형태=>가로 세로를 1개의 인자로

    # 화면 타이틀 설정
    pygame.display.set_caption("game")

    #배경 이미지 불러오기
    if g<8:
        bg=pygame.image.load("img\\background_moon.jpg")
    elif g<15:
        bg=pygame.image.load("img\\background.jpg")

    elif g<50:
        bg=pygame.image.load("img\\background_jupiter.jpg")
    
    elif g<100:
        bg=pygame.image.load("img\\background_sun.png")
    else:
        bg=pygame.image.load("img\\background_blackhole.jpg")
    #이미지 사이즈 변경
    bg=pygame.transform.scale(bg, (screen_width,screen_height))

    #fps 설정
    clock = pygame.time.Clock()     #프레임 설정

    #폰트 정의
    game_font = pygame.font.Font(None, 70)      #폰트 객체 생성(글꼴, 크기)


    #스크린 대비 캐릭터들 크기
    relativity = 8


    #경과시간: 현재시간 - 시작시간
    start_time= pygame.time.get_ticks()

    #캐릭터 불러오기
    char=pygame.image.load("img\\char.png")
    char=pygame.transform.scale(char, (screen_width/relativity,screen_width/relativity))        #주인공 크기 조정
    char_size=char.get_rect().size     #이미지 크기를 구해옴(리스트 저장: [70, 70])
    char_width=char_size[0]
    char_height=char_size[1]
    #char_pos=((screen_width-char_width)/2,screen_height-char_height)

    char_xpos=(screen_width-char_width)/2
    char_ypos=screen_height-char_height


    #적 불러오기
    #enemy_num=5
    enemy=pygame.image.load("img\\enemy.png")
    enemy=pygame.transform.scale(enemy, (screen_width/relativity,screen_width/relativity))
    enemy_size=enemy.get_rect().size     #이미지 크기를 구해옴(리스트 저장: [70, 70])
    enemy_width=enemy_size[0]
    enemy_height=enemy_size[1]
    #enemies=[enemy for col in range(enemy_num) for row in range(1)]     #이미지, x좌표, y좌표, 현재 속도
    enemies=[[] for col in range(enemy_num)]
    
    for i in range(enemy_num):
        enemies[i].append(enemy)
        enemies[i].append(random.randint(0,screen_width-enemy_width))
        enemies[i].append(i*(-200))
        enemies[i].append(0)
    print(enemies)
    """
    for i in range(enemy_num):
        del enemies[i][0]
        for j in range(4):
            enemies[i][j]=enemies[i][j+1]
    """
    #enemy_pos=((screen_width-enemy_width)/2,(screen_height-enemy_height)/2)
    
    #enemy_xpos=(screen_width-char_width)/2
    #enemy_ypos=0-enemy_height+50
    #enemy_ypos=(screen_height-enemy_height)/2


    #이동 좌표
    fps=120
    dt=1/fps
    f=f*dt
    v=0
    #to_y=0
    #enemy_speed=0
    #g=9.80665
    g_per_frame=g/fps
    flag=0
    #전체 시간
    total_time = 25
    a=f/char_m
    out_of_control=0
    success=False

    x_range=[0,screen_width-char_width]
    #y_range=[0,screen_height-char_height]
    #print(y_range)

    # 이벤트 루프
    running = True  # 게임이 진행중인가?
    while running:
        speed=v/fps             #distance/frame=(distance/sec)/(frame/sec)
        #dt=clock.tick(10)       #1초를 fps로 쪼개기 = 한번 실행하는데 걸리는 시간 = 1/fps
        clock.tick(fps)
        for event in pygame.event.get():  # 어떤 이벤트가 발생하는 동안 반복(큐 자료구조=>FIFO)
            if event.type == pygame.QUIT: # 창닫힘 이벤트 발생하면(x버튼)
                running = False
            
            
            if event.type == pygame.KEYDOWN:    #키가 눌러졌나?
                if event.key==pygame.K_LEFT:    #왼쪽 방향키
                    flag=1
                elif event.key==pygame.K_RIGHT:     #오른쪽 방향키
                    flag=2
            """
                elif event.key==pygame.K_UP:        #위쪽 방향키
                    to_y-=speed
                elif event.key==pygame.K_DOWN:      #아래쪽 방향키
                    to_y+=speed
            """
        
            #elif로 가면 문제가 있음
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_LEFT:
                    flag=0
                if event.key==pygame.K_RIGHT:
                    flag=0
        #print(v)
        if out_of_control>0:
            out_of_control-=1
            print(out_of_control)
        elif flag == 1:
            v-=a
        elif flag ==2:
            v+=a

            """    
                elif event.key==pygame.K_UP:
                    to_y+=speed
                elif event.key==pygame.K_DOWN:
                    to_y-=speed

            """  
            """
            #e.g. right를 누르다가 left를 눌렀다 때면 멈춤
            if event.type == pygame.KEYUP:      #키가 때졌나?
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    to_x=0
                elif event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    to_y=0
            
            """     
        


        char_xpos+=v             #x좌표 위치 지정
        #char_xpos+=to_x*dt         #x좌표 위치 지정
        #char_ypos+=to_y             #x좌표 위치 지정
        #char_ypos+=to_y *dt        #y좌표 위치 지정

        

        #뛰어넘기 방지
        if x_range[0]>=char_xpos:
            char_xpos=x_range[0]
        if char_xpos>=x_range[1]:
            char_xpos=x_range[1]

        """    
        if y_range[0]>=char_ypos:
            char_ypos=y_range[0]
        if char_ypos>=y_range[1]:
            char_ypos=y_range[1]    
        """
        
        #벽과 충돌 
        
        if x_range[0]<=char_xpos+v<=x_range[1]:
            char_xpos+=v         #x좌표 위치 지정
        else:
            out_of_control=fps
            v=-v*0.5
            #char_xpos+=to_x*dt         #x좌표 위치 지정
        """
        if y_range[0]<=char_ypos+to_y<=y_range[1]:
            char_ypos+=to_y         #y좌표 위치 지정
            #char_ypos+=to_y *dt        #y좌표 위치 지정
        """
        #충돌처리
        #충돌 처리하기 위한 rect 정보 업데이트
        char_rect = char.get_rect()     #get_rect의 return = (x 좌표, y좌표, x좌표+width, y좌표+height)
        char_rect.left=char_xpos-30
        char_rect.top=char_ypos-30

        #enemy들
        enemy_rects=[None for i in range(enemy_num)]
        for i in range(enemy_num):
            #땅 감지
            if enemies[i][2] >= screen_height:
                enemies[i][2]=0
                enemies[i][1]=random.randint(0,screen_width-enemy_width)
                enemies[i][3]=0
            
            
            #충돌처리
            #충돌 처리하기 위한 rect 정보 업데이트

            enemy_rects[i] = enemies[i][0].get_rect()
            enemy_rects[i].left=enemies[i][1]-50
            enemy_rects[i].top=enemies[i][2]-60

            
            
            #충돌체크 (char,colliderect)
            if char_rect.colliderect(enemy_rects[i]):
                running=False
                #pass

            #가속도
            enemies[i][2]+=enemies[i][3]
            enemies[i][3]+=g_per_frame
            #print(enemy_ypos)

        
        #경과시간
        elapsed_time = (pygame.time.get_ticks() - start_time)/1000
        #print(int(elapsed_time/1000))
        
        #남은 시간 = 전체 시간 - 경과 시간
        left_time = int(total_time- elapsed_time)
        timer = game_font.render(str(left_time),True,(0,255,0))

        if left_time<=0:
            success=True
            running=False

        
        screen.blit(bg,(0,0))   #배경 그리기
        screen.blit(char,(char_xpos,char_ypos)) #캐릭터 그리기
        for i in range(enemy_num):
            screen.blit(enemies[i][0],(enemies[i][1],enemies[i][2])) #적 그리기
        screen.blit(timer, (30,30))
        pygame.display.update()

    #딜레이
    pygame.time.delay(50)

    if success==1:
        tk=tkinter.Tk()
        literal=tkinter.font.Font(family="궁서", size=50, slant="italic")
        label=tkinter.Label(tk, text='축하합니다!', bg='red',font=literal, width=100,height=25 )
        label.pack()
        
    # pygame 종료
    pygame.quit()
    set_parms()
    

set_parms()
