from pygame import KEYDOWN
from pygame import gfxdraw
from pygame.mixer import fadeout, pause
from button import Button
import pygame
import time
import os


#TODO pause menu

class Gui:

    def __init__(self,surface,w,h):
        
        self.translate_to_center = lambda n,param: n+param/2

        self.surface = surface
        self.w = w
        self.h = h
        self.button_w = 100
        self.button_h = 50

        self.button_play = Button(self.surface,(0,0,0),(86, 78, 145),(100,100,self.button_w,self.button_h),50,pygame.font.SysFont('Verdana',15),'play',True,(86, 78, 145),(0,0,0))
        self.is_play = False


        self.button_edit = Button(self.surface,(0,0,0),(86, 78, 145),(100,200,self.button_w,self.button_h),50,pygame.font.SysFont('Verdana',15),'edit',True,(86, 78, 145),(0,0,0))          
        self.is_edit = False

        self.file_num = None
        self.is_loading_file = False
        self.file_selected = False
        self.bts = self.__get_buttons()

        self.new_file_button = Button(self.surface,(0,0,0),(86, 78, 145),(700,0,self.button_w,self.button_h),50,pygame.font.SysFont('Verdana',10),'Create new',True,(86, 78, 145),(0,0,0))
        self.is_creating_file = False

        self.save_button = Button(self.surface,(0,0,0),(86, 78, 145),(self.w/2-(self.button_w/2),self.h/2-(self.button_h/2) + 100,self.button_w,self.button_h),50,pygame.font.SysFont('Verdana',10),'Save to new',True,(86, 78, 145),(0,0,0))
        self.is_saving = False

        self.overwrite_button = Button(self.surface,(0,0,0),(86, 78, 145),(self.w/2-(self.button_w/2),self.h/2-(self.button_h/2) + 200,self.button_w,self.button_h),50,pygame.font.SysFont('Verdana',10),'Overwrite current',True,(86, 78, 145),(0,0,0))
        self.is_overwiting = False

        
        self.menu_button = Button(self.surface,(0,0,0),(86, 78, 145),(self.w/2-(self.button_w/2),self.h/2-(self.button_h/2),self.button_w,self.button_h),50,pygame.font.SysFont('Verdana',10),'Return to main',True,(86, 78, 145),(0,0,0))
        self.bact_to_play_button = Button(self.surface,(0,0,0),(86, 78, 145),(self.w/2-(self.button_w/2),self.h/2-(self.button_h/2) - 100,self.button_w,self.button_h),50,pygame.font.SysFont('Verdana',10),'Back to play',True,(86, 78, 145),(0,0,0))
        self.is_pause = False
    
    
    def gui_event_handler(self,event):

        if self.button_play.gets_clicked(event):
            self.is_play = True

        if self.button_edit.gets_clicked(event):
            self.is_edit = True

        for i,bt in enumerate(self.bts):
            if bt.gets_clicked(event) and not self.file_selected:
                self.is_loading_file = True
                #self.is_loading_file = False
                self.file_selected = True
                self.file_num = i + 1
            
        if event.type == KEYDOWN and event.key == pygame.K_ESCAPE and self.file_selected:
            self.is_pause = True


        if self.bact_to_play_button.gets_clicked(event):
            self.is_pause = False
        
        if self.menu_button.gets_clicked(event) and self.is_pause:

            self.is_edit = False
            self.is_play = False
            self.is_pause = False
            self.file_selected = False
            self.filenum = None

        if self.save_button.gets_clicked(event) and self.is_pause:
            self.is_saving = True
        #else: self.is_saving = False

        if self.overwrite_button.gets_clicked(event) and self.is_pause:
            self.is_overwiting = True
        #else: self.is_overwiting = False 
        if self.new_file_button.gets_clicked(event) and self.file_selected == False:
            self.is_creating_file = True

                
         
            

        

    def main_page_display(self):

        self.button_play.show()
        self.button_edit.show()

        #print('is_edit ->',self.is_edit,'is_play ->',self.is_play)

    def file_selector_display(self):
        
        self.new_file_button.show()

        self.bts = self.__get_buttons()
        
        for bt in self.bts:
            bt.show()

    def __get_buttons(self):

        saves = os.listdir('saves/field') # dir is your directory path
        number_files = len(saves)
        

        buttons = []
        

        for i in range(number_files):
            buttons.append(Button(self.surface,(0,0,0),(86, 78, 145),(200,100 * i,self.button_w,self.button_h),50,pygame.font.SysFont('Verdana',15),'file' + str(i + 1),True,(86, 78, 145),(0,0,0))) 
        
        return buttons
    
    # def pause_menu(self):
    #     pass

    def pause_menu_display(self):
        self.menu_button.show()
        self.bact_to_play_button.show()
        pygame.gfxdraw.box(self.surface, pygame.Rect(0,0,self.w,self.h), (0,0,0,127))
        if self.is_edit:
            self.save_button.show()
            self.overwrite_button.show()    
        #pygame.draw.circle(self.surface,(255,255,255),(self.w/2,self.h/2),20)
        
        
