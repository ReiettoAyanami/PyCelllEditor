import pygame
from pygame import gfxdraw
from pygame import mouse
from pygame import math
from pygame import fastevent
from pygame.constants import KEYDOWN, K_DOWN, K_LEFT, K_RIGHT, K_UP, MOUSEBUTTONDOWN
import utils
import json
import os
import math



class board:

    

    def __init__(self,surf,w,h):
        
        self.width = w
        self.height = h
        self.surface = surf
        self.free = ' '
        self.bomb = 'o'
        self.player = '@'
        self.wall = '#'
        self.dim = 11
        self.scale_W = self.width / self.dim
        self.scale_H = self.height / self.dim
        self.field = self.set_clear_field()
        self.player_x = int() 
        self.player_y = int()
        self.field[0][0] = self.player
        self.mouse_wheel_value = 0
        self.bomb_x = int()
        self.bomb_y = int()
        self.bomb_range = 2
        self.player_direction_x = 1
        self.player_direction_y = 0
        self.solid_tiles = (self.wall,self.bomb)
        self.items = (self.wall,self.bomb)
        self.selected_item = 0

        self.scale = lambda pos, scl: int(pos*scl)
        self.cell_state = lambda x,y: self.field[x][y] 
        self.distance = lambda x1,y1,x2,y2: abs(math.sqrt((x2-x1)**2+(y2-y1)**2))



    def set_clear_field(self) -> list:

        b = []
        

        for i in range(self.dim):
               
            b.append([self.free]*self.dim)
        
        return b
    
    def __check_collision(self,collider_tile):
       return self.field[self.player_x +self.player_direction_x][self.player_y+self.player_direction_y] != collider_tile
    

    def __show_item_on_grid(self,i,j,item,color):
        if self.field[i][j] == item:

            ix = self.scale(i,self.scale_W)
            iy = self.scale(j,self.scale_H)
            pygame.draw.rect(self.surface,color,(ix,iy,self.scale_W,self.scale_H))
            


    def trigger_bomb(self,x,y,activator,event) -> None:
        
     #TODO fai esplodere la bomba se il player la attiva -> FATTO
     #TODO fixa bug esplosione -> Non Fatto
        
    
        if self.cell_state(x,y) == self.bomb:
            self.bomb_x = x
            self.bomb_y = y
            
        try:
            if event.type == KEYDOWN and event.key == pygame.K_SPACE and self.field[self.player_x+self.player_direction_x][self.player_y+self.player_direction_y]:
                if self.field[x][y] == self.bomb:
                    for i in range(-1,self.bomb_range,1):
                        for j in range(-1,self.bomb_range,1):
                            if self.field[x+i][y+j] != activator:
                                self.field[x+i][y+j] = self.free
        except IndexError:
            pass



    def show(self) -> None:
    

        for i in range(len(self.field)):

            for j in range(len(self.field)):
                
                
                scaled_x = self.scale(i,self.scale_W)
                scaled_y = self.scale(j,self.scale_H)

                pygame.gfxdraw.pixel(self.surface,scaled_x,scaled_y,(0,0,0))
                

                self.__show_item_on_grid(self.player_x,self.player_y,self.player,(50,50,50))

                self.__show_item_on_grid(i,j,self.wall,(0,0,0))

                self.__show_item_on_grid(i,j,self.bomb,(255,50,50))
                


    def __move_player(self,event):
            
        if event.type == KEYDOWN:

            if event.key == pygame.K_RIGHT:
                self.player_direction_x = 1
                self.player_direction_y = 0

            elif event.key == pygame.K_LEFT:
                self.player_direction_x = -1
                self.player_direction_y = 0
            elif event.key == pygame.K_DOWN:
                self.player_direction_x = 0
                self.player_direction_y = 1
            elif event.key == pygame.K_UP:
                self.player_direction_x = 0
                self.player_direction_y = -1

            try:
                if self.__check_collision(self.solid_tiles[0]) and self.__check_collision(self.solid_tiles[1]) and (event.key == K_RIGHT or event.key == K_LEFT or event.key == K_DOWN or event.key == K_UP):
                    self.player_x += self.player_direction_x
                    self.player_y += self.player_direction_y
                    self.field[self.player_x][self.player_y] = self.player
                    self.field[self.player_x - self.player_direction_x][self.player_y - self.player_direction_y] = self.free
            except IndexError:
                pass
                
        if self.player_x < 0:
            
            self.player_x = 0
            self.field[self.player_x][self.player_y] = self.player
            self.field[len(self.field)-1][self.player_y] = self.free

        if self.player_y < 0:

            self.player_y = 0
            self.field[self.player_x][self.player_y] = self.player
            self.field[self.player_x][len(self.field)-1] = self.free


    

    def player_actions(self,event) -> None:

        #TODO movimenti più efficienti -> Fatto  

        

        self.trigger_bomb(self.player_x + self.player_direction_x,self.player_y + self.player_direction_y,self.player,event)

        self.__move_player(event)


    
    def highlight_cell(self):
        for i in range(len(self.field)):
            for j in range(len(self.field)):

                x = self.scale(i,self.scale_W)
                y = self.scale(j,self.scale_H)
                if utils.mouse_overlaps(x,y,self.scale_W,self.scale_H):

                    pygame.gfxdraw.box(self.surface, pygame.Rect(x,y,self.scale_W,self.scale_H), (255,0,0,127))
                    #pygame.gfxdraw.circle(self.surface,pygame.Circle)



    def place_selected(self,event):
        

        wheel_divisor = 121

        for i in range(len(self.field)):
            for j in range(len(self.field)):



                x = self.scale(i,self.scale_W)
                y = self.scale(j,self.scale_H)
                
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 4 and self.selected_item < len(self.items)-1:
                        
                        self.mouse_wheel_value += 1
                        self.selected_item = int(self.mouse_wheel_value/wheel_divisor)
                        print(self.selected_item,self.mouse_wheel_value)

                    if event.button == 5 and self.selected_item > 0:

                        self.mouse_wheel_value -= 1
                        self.selected_item = int(self.mouse_wheel_value/wheel_divisor)
                        print(self.selected_item,self.mouse_wheel_value)
                        
                        
                if utils.mouse_overlaps(x,y,self.scale_W,self.scale_H) and pygame.mouse.get_pressed()[0]:
                    
                    
                    self.field[i][j] = self.items[self.selected_item]
                    

                elif utils.mouse_overlaps(x,y,self.scale_W,self.scale_H) and pygame.mouse.get_pressed()[2]:
                    self.field[i][j] = self.free




    def save_to_new_file(self) -> None:
        
        list = os.listdir('saves/field') # dir is your directory path
        
        file_num = len(list)

        player_data = (self.player_x,self.player_y)


        with open('saves/player/player_data'+ str(file_num + 1) +'.json', 'w') as player_json:
            json.dump(player_data, player_json, indent= 4,ensure_ascii=True)

        with open('saves/field/saves'+str(file_num + 1) +'.json','w')as field_json:
            json.dump(self.field, field_json, indent= 4,ensure_ascii=True)

    def create_plain_file(self) -> None:
        
        player_data = (0,0)


        list = os.listdir('saves/field') # dir is your directory path
        
        file_num = len(list)

        empt = self.set_clear_field()

        with open('saves/player/player_data'+ str(file_num + 1) +'.json', 'w') as player_json:
            json.dump(player_data, player_json, indent= 4,ensure_ascii=True)

        with open('saves/field/saves'+str(file_num + 1) +'.json','w')as field_json:
            json.dump(empt, field_json, indent= 4,ensure_ascii=True)


                

    def save_to_current_file(self,file_num) -> None:
        player_data = (self.player_x,self.player_y)

        with open('saves/player/player_data'+ str(file_num) +'.json', 'w') as player_json:
            json.dump(player_data, player_json, indent= 4,ensure_ascii=True)
        
        with open('saves/field/saves'+str(file_num)+'.json', 'w') as field_json:
            json.dump(self.field, field_json,indent=4, ensure_ascii=True)
        

    def load_from_file(self,save_index) -> None:
        
        with open('saves/player/player_data'+ str(save_index) +'.json', 'r') as player_json:    
            player_data = json.load(player_json)
            self.player_x = player_data[0]
            self.player_y = player_data[1]
            

        with open('saves/field/saves'+str(save_index)+'.json', 'r') as field_json:
            self.field = json.load(field_json)

    

