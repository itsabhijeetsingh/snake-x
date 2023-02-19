from typing import Counter
import pygame
from pygame import key
from pygame.locals import*
from pygame import mixer
import random
import math
import time
import sys
import os
import mysql.connector

mixer.init()
pygame.init()

# Accessing Database 'score_record'

mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = 'omkar@2004')
mycursor = mydb.cursor()
mycursor.execute('show databases')

db_exist = 'F'

for i in mycursor:
    if i ==('snake_x_db',):
        db_exist = 'T'


if db_exist == 'F':
    mycursor.execute('CREATE DATABASE snake_x_db;')
    mycursor.execute('use snake_x_db')
    mycursor.execute('CREATE TABLE normal(\
        Scores int)')
    mycursor.execute('INSERT INTO normal(Game_Number, Scores) VALUES(1,10)')
    mydb.commit()
    mycursor.execute('CREATE TABLE hard(\
        Game_Number int Primary key, \
        Scores int)')
    mycursor.execute('INSERT INTO hard(Game_Number, Scores) VALUES(1,10)')
    mydb.commit()
    mycursor.execute('CREATE TABLE extreme(\
        Game_Number int Primary key, \
        Scores int)')
    mycursor.execute('INSERT INTO extreme(Game_Number, Scores) VALUES(1,10)')
    mydb.commit()

if db_exist == 'T':
    mydb = mysql.connector.connect(host = 'localhost',
                               user = 'root',
                               passwd = 'omkar@2004',
                               database = 'snake_x_db')

# database cursor
mycursor = mydb.cursor()

# defining resolution
res = (720, 720)
screen = pygame.display.set_mode(res, pygame.RESIZABLE)
pygame.display.set_caption('SnakeX')
width, height = screen.get_width(), screen.get_height()

# defining colors
black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)
green = pygame.Color(0,255,0)
blue = pygame.Color(0,0,255)
light_blue = pygame.Color(110,155,255)
light_green  = pygame.Color(100,255,0)
cyan = pygame.Color(88,188,188)
bg = pygame.Color(85, 185, 50)
color_quit_btn = pygame.Color(170,0,0)
color_rock = pygame.Color(50,50,50)

# loading sound/music/audio
mixer.music.load('sound_pack/sound_bg.mp3')

sound_bg = pygame.mixer.Sound('sound_pack/sound_bg.wav')
sound_bg.set_volume(0.2)
sound_character_death = pygame.mixer.Sound('sound_pack/sound_character_death.mp3')
sound_character_death.set_volume(0.5)
sound_item_collect = pygame.mixer.Sound('sound_pack/sound_select.mp3')
sound_item_collect.set_volume(0.5)
sound_select = pygame.mixer.Sound('sound_pack/sound_item_collect.wav')
sound_select.set_volume(0.5)

# defining variables
start_game = False
running = True
level_1 = 'level_1'
level_2 = 'level_2'
level_3 = 'level_3'

# sound variables
sound_play = 'TRUE'
sound_sfx = 'TRUE'

# score variable
score = 0

# defining functions

# accessing records in database
def records():
    
    record_normal = []
    record_hard = []
    record_extreme = []
    record_settings = []
    record_normal_last = []
    record_hard_last = []
    record_extreme_last = []
    for i in range(1):
        # accessing records in snake_x_db
        mycursor.execute('select*from normal')
        for i in mycursor:
            record_normal.append(i)
        record_normal_last.append(i)
        mycursor.execute('select*from hard')
        for i in mycursor:
            record_hard.append(i)
        record_hard_last.append(i)
        mycursor.execute('select*from extreme')
        for i in mycursor:
            record_extreme.append(i)
        record_extreme_last.append(i)
    
    record_list = (record_normal, \
        record_hard, record_extreme, record_normal_last, record_hard_last, record_extreme_last)
    return record_list


# accessing maximum records in database
def game_db_records(records):
    i = 0
    temp = []
    for j in records[0]:
        temp.append(records[0][i][1])
        i +=1
    max_normal = max(temp)
    i = 0
    temp = []
    for j in records[1]:
        temp.append(records[1][i][1])       
        i += 1
    max_hard = max(temp)
    i = 0
    temp = []
    for j in records[2]:
        temp.append(records[2][i][1])    
        i += 1
    max_extreme = max(temp)
    max_game = max(max_normal, max_hard, max_extreme)
    
    max_list = (max_game,max_normal, max_hard, max_extreme)
    return max_list
        
# updating database
def db_update(level,record_last,score):
    if level == 'normal':
        new_record = record_last[3][0][0] + 1
    if level == 'hard':
        new_record = record_last[4][0][0] + 1
    if level == 'extreme':
        new_record = record_last[5][0][0] + 1
    mycursor.execute(f'INSERT INTO {level} VALUES ({new_record}, {score})')
    mydb.commit()

    
# game menu function
def game_menu():
    color_C_play = False
    color_C_high_score = False
    color_C_instruction = False
    color_C_settings = False
    color_C_quit = False
    click = False 
    
    while True:
        
        screen.fill(bg)
         
        # defining x and y
        x, y = pygame.mouse.get_pos()
        
        # defining font
        font_1 = pygame.font.SysFont('times new roman', 70)
        
        #defining heading
        font = pygame.font.SysFont('times new roman', 30)
        
        txt_heading = font_1.render(
            'MAIN MENU', True, black
        )
        txt_heading_rect = txt_heading.get_rect()
        txt_heading_rect = (width/6+40,20)
        
        # defining text
        txt_play = font.render(
            'PLAY', True, black
        )
        txt_high_score = font.render(
            'HIGH SCORE', True, black
        )
        txt_instructions = font.render(
            'INSTRUCTIONS', True, black
        )
        txt_settings = font.render(
            'SETTINGS', True, black
        )
        txt_quit = font.render(
            'QUIT', True, black
        )
        
        # text
        txt_play_rect = txt_play.get_rect()
        txt_play_rect = (315,208)
        txt_high_score_rect = txt_high_score.get_rect()
        txt_high_score_rect = (265,308)
        txt_instructions_rect = txt_instructions.get_rect()
        txt_instructions_rect = (245,408)
        txt_settings_rect = txt_settings.get_rect()
        txt_settings_rect = (280,508)
        txt_quit_rect = txt_quit.get_rect()
        txt_quit_rect = (315,608)
        
        # button
        btn_play = pygame.Rect(230,200, 250, 50)
        btn_high_score = pygame.Rect(230,300, 250,50)
        btn_instruction = pygame.Rect(230, 400, 250,50)
        btn_settings = pygame.Rect(230,500, 250,50)
        btn_quit = pygame.Rect(230,600, 250,50)
        
        # button conditions     
        if btn_play.collidepoint(x, y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    game_level_menu()
                else:
                    game_level_menu()
        if btn_high_score.collidepoint(x, y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    game_high_score()
                else:
                    game_high_score()
        if btn_instruction.collidepoint(x, y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    game_instructions()
                else:
                    game_instructions()
                    
        if btn_settings.collidepoint(x, y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    game_settings()
                else:
                    game_settings()
        if btn_quit.collidepoint(x, y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    sys.exit()       
                else:
                    sys.exit()
        # drawing button
        if color_C_play:
            pygame.draw.rect(screen, blue, btn_play)
        else:
            pygame.draw.rect(screen, light_blue, btn_play)
        if color_C_high_score:
            pygame.draw.rect(screen, blue, btn_high_score)
        else:
            pygame.draw.rect(screen, light_blue, btn_high_score)
        if color_C_instruction:
            pygame.draw.rect(screen, blue, btn_instruction)
        else:
            pygame.draw.rect(screen, light_blue, btn_instruction)
        if color_C_settings:
            pygame.draw.rect(screen, blue, btn_settings)
        else:
            pygame.draw.rect(screen, light_blue,  btn_settings)
        if color_C_quit:
            pygame.draw.rect(screen, red, btn_quit)
        else:
            pygame.draw.rect(screen, light_blue, btn_quit)
        
        # displaying the text
        screen.blit(txt_heading, txt_heading_rect)
        screen.blit(txt_play, txt_play_rect)
        screen.blit(txt_high_score, txt_high_score_rect)
        screen.blit(txt_instructions, txt_instructions_rect)
        screen.blit(txt_settings, txt_settings_rect)
        screen.blit(txt_quit, txt_quit_rect)
        
        
        # defining conditions
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == K_ESCAPE:
                    sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    click = True 
            if 230 < x < 230+250 and 200 < y <250:
                color_C_play = True
            else:
                color_C_play = False
            if 230<x<230+250 and 300<y<350:
                color_C_high_score = True
            else:
                color_C_high_score =  False
            if 230<x<230+250 and 400<y<450:
                color_C_instruction = True
            else:
                color_C_instruction = False
            if 230<x<230+250 and 500<y<550:
                color_C_settings = True
            else:
                color_C_settings = False
            if 230<x<230+250 and 600<y<650:
                color_C_quit = True
            else:
                color_C_quit = False

        pygame.display.update()
        

# game level screen function
def game_level_menu(level = None):
    level = level
    click = False
    while True:
        # filling color in background
        screen.fill(bg)
        
        # mouse live cursorarray/list
        x, y = pygame.mouse.get_pos()
        
        # defining heading
        font_heading = pygame.font.SysFont('times new roman', 50, bold = True)
        txt_heading = font_heading.render(
            'LEVEL(S)', True, black
        )
        txt_heading_rect = (width//3, 30)
        
        # defining content
        font = pygame.font.SysFont('times new roman', 30)
        txt_1 = font.render(
            'NORMAL', True, black
        )
        txt_2 = font.render(
            'HARD', True, black
        )
        txt_3 = font.render(
            'EXTREME', True, black
        )
        
        txt_1_rect = (width//3+55, 205)
        txt_2_rect = (width//3+75, 305)
        txt_3_rect = (width//3+50, 405) 
        
        
        # defining and drawing buttons
        btn_1 = pygame.draw.rect(screen, light_blue,
                pygame.Rect(width//3, 200,width//3, 50))
        btn_2 = pygame.draw.rect(screen, light_blue,
                pygame.Rect(width//3, 300,width//3, 50))
        btn_3 = pygame.draw.rect(screen, light_blue,
                pygame.Rect(width//3, 400,width//3, 50))
        
        # defining button collition conditions
        if btn_1.collidepoint(x, y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    game_loop_1()
                else:
                    game_loop_1()
        if btn_2.collidepoint(x, y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    game_loop_2()
                else:
                    game_loop_2()
        if btn_3.collidepoint(x,y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    game_loop_3()
                else:
                    game_loop_3() 
    
        # changing color at hover
        if width//3 < x < width//3 + width//3 and 200 < y < 250 :
            pygame.draw.rect(screen, blue,
                pygame.Rect(width//3, 200,width//3, 50))
        else:
            pygame.draw.rect(screen, light_blue,
                pygame.Rect(width//3, 200,width//3, 50))
        if width//3 < x < width//3 + width//3 and 300 < y < 350 :
            pygame.draw.rect(screen, blue,
                pygame.Rect(width//3, 300,width//3, 50))
        else:
            pygame.draw.rect(screen, light_blue,
                pygame.Rect(width//3, 300,width//3, 50))
        if width//3 < x < width//3 + width//3 and 400 < y < 450 :
            pygame.draw.rect(screen, blue,
                pygame.Rect(width//3, 400,width//3, 50))
        else:
            pygame.draw.rect(screen, light_blue,
                pygame.Rect(width//3, 400,width//3, 50))
            
        # defining funtion conditions
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == K_ESCAPE:
                    game_menu()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    click = True
            if level == level_1:
                game_loop_1()
            if level == level_2:
                game_loop_2()
            if level == level_3:
                game_loop_3()
            
                    
        # screen blit(s)
        screen.blit(txt_heading, txt_heading_rect)
        screen.blit(txt_1, txt_1_rect)
        screen.blit(txt_2, txt_2_rect)
        screen.blit(txt_3, txt_3_rect)
        
        
        # screen updating
        pygame.display.update()
        

# game score
def game_score():
    font = pygame.font.SysFont('times new roman', 20)
    txt = font.render(
        'SCORE : ' + str(score), True, white
    )
    txt_rect = txt.get_rect()
    screen.blit(txt, txt_rect)

# game over
def game_over(level):
    color_c_restart = False
    color_c_menu = False
    color_c_quit = False
    click = False
    level = level
    global score
    score = score
    while True:
        screen.fill(black)
        
        x,y = pygame.mouse.get_pos()
        
        font_heading = pygame.font.SysFont('times new roman', 60)
        txt_heading = font_heading.render(
            'GAME OVER', True, red
        )
        txt_heading_rect = txt_heading.get_rect()
        txt_heading_rect = (width/4, height/4-50)        
        
        font = pygame.font.SysFont('times new roman', 20)
        txt = font.render(
            'FINAL SCORE : ' + str(score), True, white
        )
        txt_rect = txt.get_rect()
        txt_rect = (width/3 + 40, height/4 + 70)
        
        txt_restart = font.render(
            'RESTART', True, white            
        )
        txt_menu = font.render(
            'MENU', True, white
        )
        txt_quit = font.render(
            'QUIT', True, white
        )
        
        # text
        txt_restart_rect = txt_restart.get_rect()
        txt_restart_rect = (width/4+7, 413)
        txt_menu_rect = txt_menu.get_rect()
        txt_menu_rect = (width/4+150, 413)
        txt_quit_rect = txt_quit.get_rect()
        txt_quit_rect = (width/4+290, 413) 
        
        # button
        btn_restart = pygame.Rect(width/4, 400, 100, 50)
        btn_menu = pygame.Rect(width/4+132, 400, 100, 50)
        btn_quit = pygame.Rect(width/4+265, 400, 100, 50 )
        
        # button conditions
        if level == level_1:
            if btn_restart.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('normal', records(), score)
                        score = 0
                        game_loop_1()
                    else:
                        db_update('normal', records(), score)
                        score = 0
                        game_loop_1()

        if level == level_2:
            if btn_restart.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('hard', records(), score)
                        score = 0
                        game_loop_2()
                    else:
                        db_update('hard', records(), score)
                        score = 0
                        game_loop_2()         
        if level == level_3:
            if btn_restart.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('extreme', records(), score)
                        score = 0
                        game_loop_3() 
                    else:
                        db_update('extreme', records(), score)
                        score = 0
                        game_loop_3() 
        if level == None:
            if btn_menu.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        game_menu()
                    else:
                        game_menu()
        if level == level_1:
            if btn_menu.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('normal', records(), score)
                        game_menu()
                    else:
                        db_update('normal', records(), score)
                        game_menu()
        if level == level_2:
            if btn_menu.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('hard',records(), score)
                        game_menu()
                    else:
                        db_update('hard',records(), score)
                        game_menu()        
        if level == level_3:
            if btn_menu.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('extreme', records(), score)
                        game_menu()   
                    else:
                        db_update('extreme', records(), score)
                        game_menu()  
        if level == None:
            if btn_quit.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        sys.exit()
                    else:
                        sys.exit()
        if level == level_1:
            if btn_quit.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('normal', records(), score)
                        sys.exit()
                    else:
                        db_update('normal', records(), score)
                        sys.exit()
        if level == level_2:
            if btn_quit.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('hard', records(), score)
                    else:
                        db_update('hard', records(), score)        
        if level == level_3:
            if btn_quit.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('extreme', records(), score)
                        sys.exit()       
                    else:
                        db_update('extreme', records(), score)
                        sys.exit()    
            
        # button color conditions
        if color_c_restart:
            pygame.draw.rect(screen, blue, btn_restart)
        else:
            pygame.draw.rect(screen, light_blue, btn_restart)
        if color_c_menu:
            pygame.draw.rect(screen, blue, btn_menu)
        else:
            pygame.draw.rect(screen, light_blue, btn_menu)
        if color_c_quit:
            pygame.draw.rect(screen, red, btn_quit)
        else:
            pygame.draw.rect(screen, light_blue,btn_quit)
        
        # screen blit(s)
        screen.blit(txt_heading, txt_heading_rect)
        screen.blit(txt, txt_rect)
        screen.blit(txt_restart, txt_restart_rect)
        screen.blit(txt_menu, txt_menu_rect)
        screen.blit(txt_quit, txt_quit_rect)
        

        # game over conditions
        for ev in pygame.event.get():
            if level == None:
                if ev.type == pygame.QUIT:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        sys.exit()
                    else:
                        sys.exit()
            if level == level_1:
                if ev.type == pygame.QUIT:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('normal', records(), score)
                        sys.exit()
                    else:
                        db_update('normal', records(), score)
                        sys.exit()
            if level == level_2:
                if ev.type == pygame.QUIT:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('hard', records(), score)
                        sys.exit()
                    else:
                        db_update('hard', records(), score)
                        sys.exit()
            if level == level_3:
                if ev.type == pygame.QUIT:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('extreme', records(), score)
                        sys.exit()
                    else:
                        db_update('extreme', records(), score)
                        sys.exit()  
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    click = True
            if width/4 < x < width/4+100 and 400 < y < 450:
                color_c_restart = True
            else:
                color_c_restart = False
            if width/4+150 < x < width/4+250 and 400 < y < 450:
                color_c_menu = True
            else:
                color_c_menu = False
            if width/4+265 < x < width/4+365 and 400 < y < 450:
                color_c_quit = True
            else:
                color_c_quit = False 
            
        pygame.display.update()

        
# game pause
def game_pause(level=None):
    click = False
    pause = True
    color_c_resume = False
    color_c_restart = False
    color_c_menu = False
    color_c_quit = False
    level = level
    global score
    score = 0
    while pause:
        screen.fill(bg)
        
        x, y = pygame.mouse.get_pos()
        
                
        font_heading = pygame.font.SysFont('times new roman', 50, bold=True, italic=False)
        txt_heading = font_heading.render(
            'PAUSED', True, black
        )
        txt_heading_rect = txt_heading.get_rect()
        txt_heading_rect = (width/2 - 100, 30)
        screen.blit(txt_heading, txt_heading_rect)
        
        font = pygame.font.SysFont('times new roman', 30)
        txt_resume = font.render(
            'RESUME', True, black
        )
        txt_restart = font.render(
            'RESTART', True, black
        )
        txt_menu = font.render(
            'MENU', True, black
        )
        txt_quit = font.render(
            'QUIT', True, black
        )
        txt_resume_rect = txt_resume.get_rect()
        txt_restart_rect = txt_restart.get_rect()
        txt_menu_rect = txt_menu.get_rect()
        txt_quit_rect = txt_quit.get_rect()
        
        # text
        txt_resume_rect = (width/4+65+50, 85+3+100)
        txt_restart_rect = (width/4+62+50, 85+40+25+3+100)
        txt_menu_rect = (width/4+80+50, 85+40+25+40+25+3+100)
        txt_quit_rect = (width/4+90+50, 85+40+25+40+25+40+25+3+100)
        
        # button
        btn_resume = pygame.Rect(width/4+50, 85+100, 250, 40)
        btn_restart = pygame.Rect(width/4+50, 85+40+25+100, 250, 40)
        btn_menu = pygame.Rect(width/4+50, 85+40+25+40+25+100, 250, 40)
        btn_quit = pygame.Rect(width/4+50, 85+40+25+40+25+40+25+100 , 250, 40)
        
        # button conditions
        if btn_resume.collidepoint(x, y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    pause = False
                else:
                    pause = False
        if level == level_1:
            if btn_restart.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('normal', records(), score)
                        score = 0
                        game_loop_1()
                    else:
                        db_update('normal', records(), score)
                        score = 0
                        game_loop_1()
        if level == level_2:
            if btn_restart.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('hard',records(), score)
                        score = 0
                        game_loop_2()
                    else:
                        db_update('hard',records(), score)
                        score = 0
                        game_loop_2()        
        if level == level_3:
            if btn_restart.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':     
                        sound_select.play()
                        db_update('extreme', records(), score)
                        score = 0
                        game_loop_3()  
                    else:
                        db_update('extreme', records(), score)
                        score = 0
                        game_loop_3() 
        if level == None:
            if btn_menu.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        game_menu()
                    else:
                        game_menu()                                          
        if level == level_1:
            if btn_menu.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('normal', records(), score)
                        game_menu()
                    else:
                        db_update('normal', records(), score)
                        game_menu()
        if level == level_2:
            if btn_menu.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('hard', records(), score)
                        game_menu()    
                    else:
                        db_update('hard', records(), score)
                        game_menu()   
        if level == level_3:
            if btn_menu.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('extreme', records(), score)
                        game_menu() 
                    else:
                        db_update('extreme', records(), score)
                        game_menu()
        if level == None:
            if btn_quit.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        sys.exit()
                    else:
                        sys.exit()
        if level == level_1:
            if btn_quit.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('normal', records(), score)
                        sys.exit()
                    else:
                        db_update('normal', records(), score)
                        sys.exit()
        if level == level_2:
            if btn_quit.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('hard', records(), score)
                        sys.exit()
                    else:
                        db_update('hard', records(), score)
                        sys.exit()         
        if level == level_3:
            if btn_quit.collidepoint(x, y):
                if click:
                    if sound_sfx == 'TRUE':
                        sound_select.play()
                        db_update('extreme', records(), score)
                        sys.exit()  
                    else:
                        db_update('extreme', records(), score)
                        sys.exit()
                        
        # button color conditions        
        if color_c_resume:
            pygame.draw.rect(screen, blue, btn_resume)
        else:
            pygame.draw.rect(screen, light_blue, btn_resume)
        if color_c_restart:
            pygame.draw.rect(screen, blue, btn_restart)
        else:
            pygame.draw.rect(screen, light_blue, btn_restart)
        if color_c_menu:
            pygame.draw.rect(screen, blue, btn_menu)
        else:
            pygame.draw.rect(screen, light_blue, btn_menu)
        if color_c_quit:
            pygame.draw.rect(screen, red, btn_quit)
        else:
            pygame.draw.rect(screen, light_blue, btn_quit)
        
        # game pause conditions
        for ev in pygame.event.get():
            if level == None:
                if ev.type == pygame.QUIT:
                    sys.exit()
            if level == level_1:
                if ev.type == pygame.QUIT:
                    db_update('normal', records(), score)
                    sys.exit()
            if level == level_2:
                if ev.type == pygame.QUIT:
                    db_update('hard', records(), score)
                    sys.exit()
            if level == level_3:
                if ev.type == pygame.QUIT:
                    db_update('extreme', records(), score)
                    sys.exit()
            if ev.type == pygame.KEYDOWN:
                if level == None:
                    if ev.key == K_ESCAPE:
                        pause = False
                if level == level_1:
                    if ev.key == K_ESCAPE:
                        pause = False
                if level == level_2:
                    if ev.key == K_ESCAPE:
                        pause = False
                if level == level_3:
                    if ev.key == K_ESCAPE:
                        pause = False
            if ev.type == MOUSEBUTTONDOWN:
                if ev.button == 1:
                    click = True
            if width/4+50< x <250+width/4+50 and 85+100< y <85+40+100 :
                color_c_resume = True
            else:
                color_c_resume = False
            if width/4+50< x <250+width/4+50 and 85+40+25+100< y < 85+40+25+40+100:
                color_c_restart = True
            else:
                color_c_restart = False
            if width/4+50< x <250+width/4+50 and 85+40+25+40+25+100< y <85+40+25+40+25+40+100:
                color_c_menu = True
            else:
                color_c_menu = False
            if width/4+50< x <250+width/4+50 and 85+40+25+40+25+40+25+100< y <85+40+25+40+25+40+25+40+100:
                color_c_quit = True
            else:
                color_c_quit = False
        
        # screen_blit(s)
        screen.blit(txt_resume, txt_resume_rect)
        screen.blit(txt_restart, txt_restart_rect)
        screen.blit(txt_menu, txt_menu_rect)
        screen.blit(txt_quit, txt_quit_rect)
        
        pygame.display.update()
        
       
def game_high_score():
    click = False
    max_list = game_db_records(records())
    high_score_game = max_list[0]
    high_score_normal = max_list[1]
    high_score_hard = max_list[2]
    high_score_extreme = max_list[3]
    while True:
        screen.fill(bg)
        x, y = pygame.mouse.get_pos()    
        # defining function heading
        font_heading = pygame.font.SysFont('times new roman', 50, bold = True)
        txt_heading = font_heading.render(
            'HIGH SCORE', True, black)
        txt_heading_rect = txt_heading.get_rect()
        txt_heading_rect = (width//3-30, 30)
        
        # defining function content
        font = pygame.font.SysFont('times new roman', 22)
        txt_1 = font.render(
            'HIGH SCORE : GAME : ' + str(high_score_game), True, black
        )
        txt_2 = font.render(
            'HIGH SCORE : LEVEL - NORMAL : ' + str(high_score_normal), True, black
        )
        txt_3 = font.render(
            'HIGH SCORE : LEVEL - HARD : ' + str(high_score_hard), True, black
        )
        txt_4 = font.render(
            'HIGH SCORE : LEVEL - EXTREME : ' + str(high_score_extreme), True, black
        )   
        txt_5 = font.render(
            'RETURN', True, black
        ) 
        txt_1_rect = txt_1.get_rect()
        txt_1_rect = (30, 200)
        txt_2_rect = txt_2.get_rect()
        txt_2_rect = (30, 300)
        txt_3_rect = txt_3.get_rect()
        txt_3_rect = (30,400)
        txt_4_rect = txt_4.get_rect()
        txt_4_rect = (30,500)
        txt_5_rect = txt_5.get_rect()
        txt_5_rect = (555,610)
        
        # btn_return 
        btn_return = pygame.Rect(600-50,600,100,50)
        
        if btn_return.collidepoint(x, y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    game_menu()
                else:
                    game_menu()
        if 600-50<x<700-50 and 600<y<650:
                pygame.draw.rect(screen, blue, btn_return)
        else:
            pygame.draw.rect(screen, light_blue, btn_return)
                           
        # screen blit(s)
        screen.blit(txt_heading, txt_heading_rect)
        screen.blit(txt_1, txt_1_rect)
        screen.blit(txt_2, txt_2_rect)
        screen.blit(txt_3, txt_3_rect)
        screen.blit(txt_4, txt_4_rect)
        screen.blit(txt_5, txt_5_rect)
        
        # function conditions
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == K_ESCAPE:
                    game_menu()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    click = True
            
        
        pygame.display.update()
        
        
# game instructions
def game_instructions(level=None):
    level = level
    click = False
    while True:
        screen.fill(black)
        
        x, y = pygame.mouse.get_pos()
        
        # defining heading
        font_heading = pygame.font.SysFont('times new roman', 50, bold = True)
        txt_heading = font_heading.render(
            'INSTRUCTIONS', True, white
        )
        txt_heading_rect = txt_heading.get_rect()
        txt_heading_rect = (width/4-17, 30)
        
        
        # defining sub_heading
        font_sub = pygame.font.SysFont('times new roman', 20)
        txt_sub = font_sub.render(
            'GAME INSTRUCTIONS ARE AS FOLLOWED :- ', True, white
        )
        txt_sub_rect = txt_sub.get_rect()
        txt_sub_rect = (10, 150)
        
        # defining content
        font = pygame.font.SysFont('times new roman', 15)
        txt_content_1 = font.render(
            '1]  DEFAULT GAME CONTROL KEYS ARE ARROW KEY(S); ', True, white
        )
        txt_content_1_1 = font.render(
            '     [ UP, DOWN, LEFT, RIGHT ] KEY(S). ', True, white,
        )
        txt_content_2 = font.render(
            '2]  YOU CAN TURN ON/OFF GAME [SOUND/SFX] FROM SETTINGS.', True, white
        )
        txt_content_3 = font.render(
            '3]  GAME WILL OVER IF YOU TOUCH SNAKE BODY OR OUTER WALLS OR ROCKS. ', True, white
        )
        txt_content_4 = font.render(
            '4]  GAME OVER SCEEN WILL AUTO-CLOSE AFTER 10 SECONDS.', True, white
        )
        txt_content_5 = font.render(
            '5]  DEFAULT NAVIGATION IS MOUSE CONTROLLED; ', True, white
        )
        txt_content_5_1 = font.render(
            '6]  USE ESCAPE KEY TO PAUSE OR RETURN TO PREVIOUS WINDOW. ', True, white,
        )
        txt_return = font.render(
            'RETURN', True, black,
        )
        txt_content_1_rect = txt_content_1.get_rect()
        txt_content_1_rect = (10,200)
        txt_content_1_1_rect = txt_content_1_1.get_rect()
        txt_content_1_1_rect = (10,250)
        txt_content_2_rect = txt_content_2.get_rect()
        txt_content_2_rect = (10,300)
        txt_content_3_rect = txt_content_3.get_rect()
        txt_content_3_rect = (10,350)
        txt_content_4_rect = txt_content_4.get_rect()
        txt_content_4_rect = (10,400)
        txt_content_5_rect = txt_content_5.get_rect()
        txt_content_5_rect = (10,450)
        txt_content_5_1_rect = txt_content_5_1.get_rect()
        txt_content_5_1_rect = (10,500)
        txt_return_rect = txt_return.get_rect()
        txt_return_rect = (567,615)
        
        # return button
        btn_return = pygame.Rect(600-50,600,100,50)
        
        if btn_return.collidepoint(x, y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    game_menu()
                else:
                    game_menu()
        if 600-50<x<700-50 and 600<y<650:
                pygame.draw.rect(screen, blue, btn_return)
        else:
            pygame.draw.rect(screen, light_blue, btn_return)
        
        # screen blit(s)
        screen.blit(txt_heading, txt_heading_rect)
        screen.blit(txt_sub, txt_sub_rect)
        screen.blit(txt_content_1, txt_content_1_rect)
        screen.blit(txt_content_1_1, txt_content_1_1_rect)
        screen.blit(txt_content_2, txt_content_2_rect)
        screen.blit(txt_content_3, txt_content_3_rect)
        screen.blit(txt_content_4, txt_content_4_rect)
        screen.blit(txt_content_5, txt_content_5_rect)
        screen.blit(txt_content_5_1, txt_content_5_1_rect)
        screen.blit(txt_return, txt_return_rect)
        
        # game instructions conditions
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if level == None:
                    if ev.key == K_ESCAPE:
                        game_menu()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    click = True
        
        pygame.display.update()


# game settings
def game_settings(level = None):
    global sound_play
    global sound_sfx
    level = level
    color_c_back = False
    click = False
    while True:
        
        screen.fill(black)
        
        x,y = pygame.mouse.get_pos()
        
        # heading
        font_heading = pygame.font.SysFont('times new roman', 50, bold = True)
        txt_heading = font_heading.render(
            'SETTINGS', True, white
        )
        txt_heading_rect = txt_heading.get_rect()
        txt_heading_rect = (width//3-10, 30)
        
        # content_header
        font = pygame.font.SysFont('times new roman', 30)
        txt_content_1 = font.render(
            '  GAME SOUND ', True, white
        )
        txt_content_2 = font.render(
            '  GAME SFX   ', True, white
        )
        txt_content_1_rect = txt_content_1.get_rect()
        txt_content_1_rect = (20, 200)
        txt_content_2_rect = txt_content_2.get_rect() 
        txt_content_2_rect = (20, 400)
        
        # content_on/off
        txt_on_1 = font.render(
            'ON', True, black
        )
        txt_off_1 = font.render(
            'OFF', True, black
        ) 
        txt_on_2 = font.render(
            'ON', True, black
        )
        txt_off_2 = font.render(
            'OFF', True, black
        ) 
        txt_back = font.render(
            'MENU', True, black
        )
        txt_on_1_rect = txt_on_1.get_rect()
        txt_off_1_rect = txt_off_1.get_rect()
        txt_on_2_rect = txt_on_2.get_rect()
        txt_off_2_rect = txt_off_2.get_rect()
        txt_back_rect = txt_back.get_rect()
        txt_on_1_rect = (205, 307)
        txt_off_1_rect = (470, 307)
        txt_on_2_rect = (205, 507)
        txt_off_2_rect = (470, 507)
        txt_back_rect = (width//3+80, 655)
        
    
    
        # on/off Rect/button
        btn_on_1 =  pygame.Rect( 180,300,   100,50)
        btn_off_1 = pygame.Rect( 450,300,   100,50)
        btn_on_2 =  pygame.Rect( 180,500,   100,50)
        btn_off_2 = pygame.Rect( 450,500,   100,50)
        btn_back = pygame.Rect(width//3+75, 650, 100, 50)
        
        
        if btn_on_1.collidepoint(x, y):
            if click:
                sound_play = 'TRUE'
                sound_select.play()
        if btn_off_1.collidepoint(x, y):
            if click:
                sound_play = 'FALSE'
                sound_bg.stop()
                sound_select.play()
                
        if btn_on_2.collidepoint(x, y):
            if click:
                sound_sfx = 'TRUE'
                sound_select.play()
        if btn_off_2.collidepoint(x, y):
            if click:
                sound_sfx = 'FALSE'
                sound_select.play()
        if btn_back.collidepoint(x, y):
            if click:
                if sound_sfx == 'TRUE':
                    sound_select.play()
                    game_menu()
                else:
                    game_menu()
        
        pygame.draw.rect(screen, light_blue, btn_on_1)
        pygame.draw.rect(screen, light_blue, btn_off_1)
        pygame.draw.rect(screen, light_blue, btn_on_2)
        pygame.draw.rect(screen, light_blue, btn_off_2)
        
        # drawing permanent button colour (on/off)
        if sound_play == 'TRUE':
            pygame.draw.rect(screen, light_green, btn_on_1)
        
        if sound_play == 'FALSE':
            pygame.draw.rect(screen, red, btn_off_1)
        if sound_sfx == 'TRUE':
            pygame.draw.rect(screen, light_green, btn_on_2)
        if sound_sfx == 'FALSE':
            pygame.draw.rect(screen, red, btn_off_2)
        
        # drawing button on hovering mouse

        if color_c_back:
            pygame.draw.rect(screen, light_blue, btn_back)
        else:
            pygame.draw.rect(screen, blue, btn_back)
             
        # settings condition
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if level == None:
                    if ev.key == K_ESCAPE:
                        game_menu()
                        
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    click = True 
            if width//3+75 < x < width//3+75+100 and  650 < y < 700:
                color_c_back = True
            else:
                color_c_back = False 

    
        # screen blit(s)
        screen.blit(txt_heading, txt_heading_rect)
        screen.blit(txt_content_1, txt_content_1_rect)
        screen.blit(txt_content_2, txt_content_2_rect)
        screen.blit(txt_on_1, txt_on_1_rect)
        screen.blit(txt_off_1, txt_off_1_rect)
        screen.blit(txt_on_2, txt_on_2_rect)
        screen.blit(txt_off_2, txt_off_2_rect)
        screen.blit(txt_back, txt_back_rect)
        
            
        pygame.display.update()
        


# game loop
def game_loop_1():
    global score
    if sound_play == 'TRUE':
        if True:
            sound_bg.play(loops = 10)
    while True:
        # fps/refress rate
        fps = pygame.time.Clock()
        
        # defining snake
        snake_speed = 13
        snake_position = [100, 50]
        snake_body = [
            [100, 50],
            [90, 50],
            [80, 50]
        ]

        # defining fruit
        fruit_position = [
            random.randrange(1, (width-20)//10)*10,
            random.randrange(1, (height-40)//10)*10
        ]
        fruit_spawn = True
        
        # defining direction
        direction = 'RIGHT'
        change_to = direction
            
        while True:
            # defining condition
            # defining movement
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    db_update('normal', records(), score)
                    sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == K_ESCAPE:
                        sound_bg.stop()
                        game_pause(level_1)
                    if ev.key == K_UP:
                        change_to = 'UP'
                    if ev.key == K_DOWN:
                        change_to = 'DOWN'
                    if ev.key == K_LEFT:
                        change_to = 'LEFT'
                    if ev.key == K_RIGHT:
                        change_to = 'RIGHT'
            # changing direction
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'
            #changing snake_position
            if direction == 'UP':
                snake_position[1] -= 10
            if direction == 'DOWN':
                snake_position[1] += 10
            if direction == 'LEFT':
                snake_position[0] -= 10
            if direction == 'RIGHT':
                snake_position[0] += 10    
            
            snake_body.insert(0, list(snake_position))
            if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                sound_item_collect.play()
                score += 10
                fruit_spawn = False 
                
            else:
                snake_body.pop()        
            
            if not fruit_spawn:
                fruit_position = [
                    random.randrange(1, (width-20)//10)*10,
                    random.randrange(1, (height-40)//10)*10
                ]
            
            screen.fill(black)
            fruit_spawn = True
            
            # drawing snake body
            for pos in snake_body:
                pygame.draw.rect(screen, light_green,
                    pygame.Rect(pos[0], pos[1], 10,10))
            pygame.draw.rect(screen, red,
                pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
            
            # game boundary/wall
            # drawing boundary
            wall_up = pygame.draw.rect(screen, light_blue, pygame.Rect(0, 0, width, 20))
            wall_down = pygame.draw.rect(screen, light_blue, pygame.Rect(0,height-20,width, 20))
            wall_left = pygame.draw.rect(screen, light_blue, pygame.Rect(0, 0, 10, height))
            wall_right = pygame.draw.rect(screen, light_blue, pygame.Rect(width-10, 0, 10, height))

            #game over conditions
            # gameover conditions-1
            for body in snake_body[1:]:
                if snake_position[0] == body[0] and snake_position[1] == body[1]:
                    sound_character_death.play()
                    sound_bg.stop()
                    db_update('normal', records(), score)
                    game_over(level_1)
            
            #game over condition-2 
            if snake_position[0] < 10 or snake_position[0] > width -20:
                sound_character_death.play()
                sound_bg.stop()
                db_update('normal', records(), score)
                game_over(level_1)
            if snake_position[1] < 20 or snake_position[1] > height - 30:
                sound_character_death.play()
                sound_bg.stop()
                db_update('normal', records(), score)
                game_over(level_1)
                
            # game score
            game_score()
            pygame.display.update()
            fps.tick(snake_speed)
            

def game_loop_2():
    global score
    if sound_play == 'TRUE':
        if True:
            sound_bg.play(loops = 10)
    while True:
        # fps/refress rate
        fps = pygame.time.Clock()
        
        # defining snake
        snake_speed = 17
        snake_position = [70, 300]
        snake_body = [
            [70, 300],
            [70, 290],
            [70, 280]
        ]

        # defining fruit
        fruit_position = [
            random.randrange(1, (width-21)//10)*10,
            random.randrange(1, (height-41)//10)*10
        ]
        fruit_spawn = True
        
        # defining direction
        direction = 'RIGHT'
        change_to = direction
            
            
        while True:
            # defining condition
            # defining movement
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    db_update('hard', records(), score)
                    sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == K_ESCAPE:
                        sound_bg.stop()
                        game_pause(level_2)
                    if ev.key == K_UP:
                        change_to = 'UP'
                    if ev.key == K_DOWN:
                        change_to = 'DOWN'
                    if ev.key == K_LEFT:
                        change_to = 'LEFT'
                    if ev.key == K_RIGHT:
                        change_to = 'RIGHT'
            # changing direction
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'
            #changing snake_position
            if direction == 'UP':
                snake_position[1] -= 10
            if direction == 'DOWN':
                snake_position[1] += 10
            if direction == 'LEFT':
                snake_position[0] -= 10
            if direction == 'RIGHT':
                snake_position[0] += 10    
            
            snake_body.insert(0, list(snake_position))
            if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                snake_speed += 0.5
                sound_item_collect.play()
                score += 10
                fruit_spawn = False 
                
            else:
                snake_body.pop()        
            
            if not fruit_spawn:
                fruit_position = [
                    random.randrange(1, (width-20)//10)*10,
                    random.randrange(1, (height-40)//10)*10
                ]
            
            screen.fill(black)
            fruit_spawn = True
            
            # drawing snake body
            for pos in snake_body:
                pygame.draw.rect(screen, light_green,
                    pygame.Rect(pos[0], pos[1], 10,10))
            pygame.draw.rect(screen, red,
                pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
            
            # game boundary/wall
            # drawing boundary
            wall_up = pygame.draw.rect(screen, light_blue, pygame.Rect(0, 0, width, 20))
            wall_down = pygame.draw.rect(screen, light_blue, pygame.Rect(0,height-20,width, 20))
            wall_left = pygame.draw.rect(screen, light_blue, pygame.Rect(0, 0, 10, height))
            wall_right = pygame.draw.rect(screen, light_blue, pygame.Rect(width-10, 0, 10, height))

            #game over conditions
            # gameover conditions-1
            for body in snake_body[1:]:
                if snake_position[0] == body[0] and snake_position[1] == body[1]:
                    sound_character_death.play()
                    sound_bg.stop()
                    db_update('hard', records(), score)
                    game_over(level_2)
            
            #game over condition-2 
            if snake_position[0] < 10 or snake_position[0] > width -20:
                sound_character_death.play()
                sound_bg.stop()
                db_update('hard', records(), score)
                game_over(level_2)
            if snake_position[1] < 20 or snake_position[1] > height - 30:
                sound_character_death.play()
                sound_bg.stop()
                db_update('hard', records(), score)
                game_over(level_2)
                
            # game score
            game_score()
            pygame.display.update()
            fps.tick(snake_speed)
      

def game_loop_3():
    global score

    if sound_play == 'TRUE':
        if True:
            sound_bg.play(loops = 10)
    rock_pos_list = []
    while True:
        # fps/refress rate
        fps = pygame.time.Clock()
        
        # defining snake
        snake_speed = 19
        snake_position = [70, 300]
        snake_body = [
            [70, 300],
            [70, 290],
            [70, 280]
        ]

        # defining fruit
        fruit_position = [
            random.randrange(1, (width-21)//10)*10,
            random.randrange(1, (height-41)//10)*10
        ]
        fruit_spawn = True
        
        # defining rock
        rock_position = [
            random.randrange(1, (width-20)//10)*10,
            random.randrange(1, (height-40)//10)*10
        ]
        rock_spawn = True

        rock_pos_list.append(rock_position)
        
        # defining direction
        direction = 'RIGHT'
        change_to = direction
            
            
        while True:
            # de    fining condition
            # defining movement
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    db_update('extreme', records(), score)
                    pygame.sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == K_ESCAPE:
                        sound_bg.stop()
                        game_pause(level_3)
                    if ev.key == K_UP:
                        change_to = 'UP'
                    if ev.key == K_DOWN:
                        change_to = 'DOWN'
                    if ev.key == K_LEFT:
                        change_to = 'LEFT'
                    if ev.key == K_RIGHT:
                        change_to = 'RIGHT'
            # changing direction
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'
            #changing snake_position
            if direction == 'UP':
                snake_position[1] -= 10
            if direction == 'DOWN':
                snake_position[1] += 10
            if direction == 'LEFT':
                snake_position[0] -= 10
            if direction == 'RIGHT':
                snake_position[0] += 10    
            
            snake_body.insert(0, list(snake_position))
            if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                snake_speed += 0.5
                sound_item_collect.play()
                score += 10
                fruit_spawn = False 
                
            else:
                snake_body.pop()        
            
            if not fruit_spawn:
                fruit_position = [
                    random.randrange(1, (width-20)//10)*10,
                    random.randrange(1, (height-40)//10)*10
                ]
                rock_position = [
                random.randrange(1, (width-20)//10)*10,
                random.randrange(1, (height-40)//10)*10
                ]
                rock_pos_list.append(rock_position)
            
            screen.fill(black)
            fruit_spawn = True
            
            # drawing snake body and fruit
            for pos in snake_body:
                pygame.draw.rect(screen, light_green,
                    pygame.Rect(pos[0], pos[1], 10,10))
            pygame.draw.rect(screen, red,
                pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
            
            # draining rock obstacles
            for rock_pos in rock_pos_list:
                pygame.draw.rect(screen, color_rock,
                    pygame.Rect(rock_pos[0], rock_pos[1], 10,10))
                
            # game boundary/wall
            # drawing boundary
            wall_up = pygame.draw.rect(screen, light_blue, pygame.Rect(0, 0, width, 20))
            wall_down = pygame.draw.rect(screen, light_blue, pygame.Rect(0,height-20,width, 20))
            wall_left = pygame.draw.rect(screen, light_blue, pygame.Rect(0, 0, 10, height))
            wall_right = pygame.draw.rect(screen, light_blue, pygame.Rect(width-10, 0, 10, height))

            # game over conditions
            # game over conditions-1
            for body in snake_body[1:]:
                if snake_position[0] == body[0] and snake_position[1] == body[1]:
                    sound_character_death.play()
                    sound_bg.stop()
                    db_update('extreme', records(), score)
                    game_over(level_3)
            
            # game over condition-2 
            if snake_position[0] < 10 or snake_position[0] > width -20:
                sound_character_death.play()
                sound_bg.stop()
                db_update('extreme', records(), score)
                game_over(level_3)
            if snake_position[1] < 20 or snake_position[1] > height - 30:
                sound_character_death.play()
                sound_bg.stop()
                db_update('extreme', records(), score)
                game_over(level_3)
                
            # game over conditions-3
            if rock_position[0] == snake_position[0] and rock_position[1] == snake_position[1]:
                sound_character_death.play()
                sound_bg.stop()
                db_update('extreme', records(), score)
                game_over(level_3)
            for rock_pos in rock_pos_list:
                if rock_pos[0] == snake_position[0] and rock_pos[1] == snake_position[1]:
                    sound_character_death.play()
                    sound_bg.stop()
                    db_update('extreme', records(), score)
                    game_over(level_3)

            # game score
            game_score()
            pygame.display.update()
            fps.tick(snake_speed)
                     

# START POINT
while running:
    if start_game == False:
        game_menu()
