import pygame
from functions import *
import os

class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.loop_job=Loop_job()
        self.pic_job=Pic_job()
        self.choice_system=Choice('tree.json')
        self.running=True
        self.screen=pygame.display.set_mode((1200,800))
        self.contents=self.choice_system.read_file('menu.json')
        self.option_list=[]
        self.option_rect_list=[]
        self.option_font=pygame.font.SysFont(None,50,bold=True)
        self.title_font=pygame.font.SysFont(None,60,bold=True)
        self.white=(255,255,255)
        self.black=(0,0,0)
        self.water_blue=(0,119,190)
        self.light_blue=(0, 150, 220)
        self.hotpink=(255,105,180)
        self.bg=pygame.image.load(self.contents['bg']).convert()
        self.bg=Pic_job.ration_scale(self.bg,1200,800)
        self.music_on=False
        self.hover=False
        self.hover_list=[]
        self.click=False
        self.click_list=[]
        self.save_flag=False
        self.load_flag=False

        
        print(self.contents)
    def on_event(self,event): 
        self.mouse_pos=pygame.mouse.get_pos()
        if event.type==pygame.QUIT:
            self.running=False

        if self.option_rect_list!=[]:
            for option_rect in self.option_rect_list:
                if option_rect.collidepoint(self.mouse_pos):
                    self.hover=True
                    if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                        self.click=True
                        print(self.click)
                    else:
                        self.click=False
                        print(self.click)
                    self.click_list.append(self.click)

                else:
                    self.hover=False
                    self.click=False
                    self.click_list.append(self.click)
                self.hover_list.append(self.hover)
            self.hover_list=self.loop_job.loop_list_populate(self.hover_list,len(self.option_rect_list))
            self.click_list=self.loop_job.loop_list_populate(self.click_list,len(self.option_rect_list))
            print(self.click_list)

    def on_loop(self):
        if self.contents['music']!='' and self.music_on==False:
            pygame.mixer.music.load(self.contents['music'])
            pygame.mixer.music.play(-1)
            self.music_on=True
        else:
            pass
        self.title=self.contents['title']
        self.title=self.title_font.render(self.title,True,self.black)
        self.options=self.contents['options']
        for option in self.options.values():
            option_text=self.option_font.render(option,True,self.black)
            self.option_list.append(option_text)
        self.option_list=self.option_list[0:len(self.options)]

        
    def on_render(self):
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.title,(100,200))
        counter=0
        for option in self.option_list:
            rect=option.get_rect(topleft=(100,350+100*counter))
            self.option_rect_list.append(rect)
            self.option_rect_list=self.option_rect_list[0:len(self.option_list)]
            if len(self.hover_list)>counter:
                if self.hover_list[counter]:
                    self.pic_job.draw_alpha_rec(self.screen,(rect.x,rect.y),(rect.width,rect.height),self.hotpink,150,(20,20,20,20))
                if self.click_list[counter]:
                    if counter==0:
                        self.save_flag=True
                    if counter==1:
                        pass
                    if counter==2:
                        pass
                    if counter==3:
                        self.running=False
                    if counter==4:
                        pass
                    
            else:
                pass
            self.screen.blit(option,(100,350+100*counter))

            counter=counter+1
        pygame.display.flip()

    def on_clean(self):
        pass
    def on_execute(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.on_clean()
        














if __name__=='__main__':
    app=Menu()
    app.on_execute()

