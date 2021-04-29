import os
from tkinter.constants import FALSE
import pygame
from board import board
import gui





pygame.init()
pygame.font.init()
width = 800
height = 800
window = pygame.display.set_mode((width,height))
pygame.display.set_caption('cellEditor')
b = board(window,width,height)
g = gui.Gui(window,width,height)

def main():
    
    running = True
    
    
    while running:


        pygame.time.delay(20)


        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                
                
                if event.key == pygame.K_ESCAPE:
                    g.pause_menu_display()

                if event.key == pygame.K_c:
                    
                    if g.is_edit:
                        b.field = b.set_clear_field()
                        b.field[0][0] = b.player
                        b.player_x = 0
                        b.player_y = 0
            
            if g.is_edit and g.file_selected and not g.is_pause: 
                  # if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                b.place_selected(event)
                #     g.is_pause = False
                
            b.player_actions(event)
            g.gui_event_handler(event)



            

            
            
            
                
        window.fill((255, 255, 255))


        if g.file_selected and g.is_edit:
            b.player_x = b.player_x
            if g.is_loading_file:
                b.load_from_file(g.file_num)
                g.is_loading_file = False
            if not g.is_pause:
                b.show()
                b.highlight_cell()
                #print('lol')


        if g.file_selected and g.is_play:

            if g.is_loading_file:
                b.load_from_file(g.file_num)
                g.is_loading_file = False

            b.show()
        if g.is_pause:
            g.pause_menu_display()

        if g.is_saving:

            b.save_to_new_file() 

            g.is_saving = False

        if g.is_overwiting:
            
            b.save_to_current_file(g.file_num)

            g.is_overwiting = False
            

    
        if g.is_edit == False and g.is_play == False:
            g.main_page_display()

        if g.file_selected == False and g.is_edit:

            g.file_selector_display()

        if g.file_selected == False  and g.is_play:
            g.file_selector_display()


        # if g.is_edit and g.file_selected:
        #     g.show_overlay_buttons()


        

        if g.is_creating_file:
            b.create_plain_file()

            g.is_creating_file = False

        #g.pause_menu_display()
        
        pygame.display.update()

        

    pygame.quit()


if __name__ == '__main__':

    main()

