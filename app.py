import pygame
from pygame.locals import *
from functions import *
from menu import Menu
import time
import datetime
import os
# things need to do
# tomrrow finish comments
# newline finished
# choice system finished
# menu screen----now, how to change between 2 screens and 2 files?
# current solution is not a good one. Find another solution
# start screen
# save and load----make load and save page to control save and load flag

# parse

class App:
    def __init__(self):
        self.running=True
        pygame.init()
        pygame.mixer.init()
        # initiate choice system, read in tree
        self.choice_system=Choice('tree.json')
        self.choice_system_run_count=0
        # initiate picture process system
        self.pic_job=Pic_job()
        # initiate loop control
        self.loop_job=Loop_job()
        self.music_on=False
        self.screen=pygame.display
        # set main surface
        self.surface=self.screen.set_mode((1200,800))
        self.surface.set_colorkey((0,0,0))
        # set usable color
        self.white=(255,255,255)
        self.water_blue=(0,119,190)
        self.light_blue=(0, 150, 220)
        self.hotpink=(255,105,180)
        # set usable fonts
        self.text_font=pygame.font.Font('freesansbold.ttf',20)
        self.choice_font=pygame.font.SysFont(None,50)
        # set starting frame
        self.frame='0'
        # set music frame to None at first
        self.music=None
        # initiate 2 lists to preload pics
        self.bg_history={}
        self.sp_history={}
        # initial read from json file to get data
        self.text=self.get_text()
        # get choice rectangles to use check colision
        self.choice_rectangles=[]
        self.choice_flag=False
        self.choice_flags=[]
        # flag to see if a choice has been clicked
        self.choice_clicked_flag=False
        self.choice_clicked_flags=[]
        # flag to control the timing of cleaning choice rectangles
        self.clean_choice_rectangles=False
        # flag to disable usual frame progression
        self.no_progression=False
        # flag to see if menu is going to be shown
        self.show_menu=False
        # save point info
        self.save_flag=False
        self.save_info=(self.choice_system.loaded_script_name,self.frame)
        self.load_flag=False
  
    def get_text(self):
        # read in script
        self.text=self.choice_system.read_file('script1.json')
        # pre-convert the pics to get quicker loading time
        # set a convert history for bg and sp to reduce loading time

        for value in self.text.values():
            if 'bg' in value.keys():
                bg=value['bg']
                if bg not in self.bg_history:
                    bg_loaded=pygame.image.load(bg).convert()
                    bg_converted=pygame.transform.scale(bg_loaded,(1200,800))
                    value['bg']=bg_converted
                    self.bg_history[bg]=bg_converted
                else:
                    value['bg']=self.bg_history[bg]
            else:
                pass
            if 'sp' in value.keys():
                for key,sp in value['sp'].items():
                    if sp!='' and sp not in self.sp_history:
                        sp_loaded=pygame.image.load(sp).convert_alpha()
                        sp_converted=Pic_job.ration_scale(sp_loaded,None,900)
                        value['sp'][key]=sp_converted
                        self.sp_history[sp]=sp_converted
                    elif sp!='' and sp in self.sp_history:
                        value['sp'][key]=self.sp_history[sp]
                    else:
                        pass
            else:
                pass
        return self.text
    
    # convert picture in self.text into converted picture file ready to be used
    def convert_pic(self):
        for value in self.text.values():
            if 'bg' in value.keys():
                bg=value['bg']
                if bg not in self.bg_history:
                    print(bg)
                    bg_loaded=pygame.image.load(bg).convert()
                    bg_converted=pygame.transform.scale(bg_loaded,(1200,800))
                    value['bg']=bg_converted
                    self.bg_history[bg]=bg_converted
                else:
                    value['bg']=self.bg_history[bg]
            else:
                pass
            if 'sp' in value.keys():
                for key,sp in value['sp'].items():
                    if sp!='' and sp not in self.sp_history:
                        sp_loaded=pygame.image.load(sp).convert_alpha()
                        sp_converted=Pic_job.ration_scale(sp_loaded,None,900)
                        value['sp'][key]=sp_converted
                        self.sp_history[sp]=sp_converted
                    elif sp!='' and sp in self.sp_history:
                        value['sp'][key]=self.sp_history[sp]
                    else:
                        pass
            else:
                pass
        return self.text



    def on_event(self,event):
        # add quit button
        if event.type==pygame.QUIT:
            self.running=False
        # when click, add 1 frame
        if event.type==pygame.MOUSEBUTTONDOWN and self.no_progression==False:
            if event.button==1 and int(self.frame)<len(self.text)-1:
                self.frame=str(int(self.frame)+1)
        # right click to switch to menu

        # detect collision between mouse and choice
        # get mouse position
        self.mouse_pos=pygame.mouse.get_pos()
        for rect in self.choice_rectangles:
            # check if the mouse is hovering on the choice
            if rect.collidepoint(self.mouse_pos):
                self.choice_flag=True
                # check if choise has been clicked
                if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    self.choice_clicked_flag=True
                    self.clean_choice_rectangles=True
                else:
                    self.choice_clickedflag=False
            else:
                self.choice_flag=False
                self.choice_clicked_flag=False

            
            self.choice_flags.append(self.choice_flag)
            self.choice_clicked_flags.append(self.choice_clicked_flag)
        # list containing the flags of all choices
        self.choice_flags=self.loop_job.loop_list_populate(self.choice_flags,len(self.choice_rectangles))
        self.choice_clicked_flags=self.loop_job.loop_list_populate(self.choice_clicked_flags,len(self.choice_rectangles))
        print(self.choice_clicked_flags)
        # calculate which choice has been selected
        counter=0
        for flag in self.choice_clicked_flags:
            if not flag:
                counter=counter+1
            else:
                # load the selected script
                result=self.choice_system.script_choice(str(counter))
                self.text=result[0]
                print(self.text)
                self.text=self.convert_pic()
                print(result)
        if event.type==pygame.KEYDOWN and event.key==K_m:
            self.show_menu=True
        else: pass
        # create save when save_flag is true
        if self.save_flag==True:
            current_time=datetime.datetime.now()
            time_string=current_time.strftime("%Y%m%d%H%M%S")
            with open(f'saves/{time_string}.save','w') as f:
                f.write(f'{self.save_info[0]} {self.save_info[1]}')
                self.save_flag=False
        else:pass
        # load save_file if load_flag is true
        if self.load_flag:
            with open('saves/20240428233259.save') as f:
                save_data=f.readline()
                self.choice_system.read_file(save_data[8:save_data.find(' ')])
                self.frame=save_data[save_data.find(' ')+1:]
                


                   
    def on_loop(self):
        # create rectangle containing name
        self.name_box=pygame.Rect(120,550,150,50)
        # create rectangle containing message
        self.m_box=pygame.Rect(100,600,900,200)
        # prevent frame number exceeding data length
        if int(self.frame)<len(self.text):
            if self.text[self.frame]['menu']:
                pass
            # program choice system
            elif self.text[self.frame]['choice']:
                # disable click to progress
                self.no_progression=True
                # read choice texts, set choice_system.choice_texts as a list, return the list
                self.choice_system.get_choice_text()
                choices=self.choice_system.choice_texts
                #create a surface to contain all the choices
                self.choice_text_surface=pygame.Surface((1200,800))
                self.choice_text_surface.set_colorkey((0,0,0))
                choice_counter=0
                number_of_choices=len(choices)
                # lay out the choices on the screen
                for choice in choices:
                    choice_text_rect=pygame.Rect(400,150+choice_counter*(650/number_of_choices),400,80)
                    if choice_text_rect not in self.choice_rectangles:
                        self.choice_rectangles.append(choice_text_rect)

                    else: pass
                    # draw the choices rectangles
                    choice_text=self.choice_font.render(choice,True,self.white)
                    pygame.draw.rect(self.choice_text_surface,self.hotpink,choice_text_rect,0,25,25,25,25)
                    if len(self.choice_flags)>choice_counter:
                        # change color if the rectangle is not hovered on
                        if not self.choice_flags[choice_counter]:
                            pygame.draw.rect(self.choice_text_surface,self.hotpink,choice_text_rect,0,25,25,25,25)
                        else:
                            pygame.draw.rect(self.choice_text_surface,self.light_blue,choice_text_rect,0,25,25,25,25)
                    # blit choices onto choice text surface
                    self.choice_text_surface.blit(choice_text,(choice_text_rect.x+0.5*(choice_text_rect.width-choice_text.get_width()),choice_text_rect.y+0.5*(choice_text_rect.height-choice_text.get_height())))
                    choice_counter=choice_counter+1
                # load bg
                self.bg=self.text[self.frame]['bg']
                # load music
                if self.text[self.frame]['music']:
                    music=self.text[self.frame]['music']
                    # change music if encounter new music setting
                    if music!=self.music:
                        self.music_on=False
                        self.music=music
                    else:
                        pass
                    if self.music_on==False:
                        # set music on when music is not on
                        pygame.mixer.music.load(music)
                        pygame.mixer.music.play(-1)
                        self.music_on=True
                    else:
                        pass
                else:
                    pass
            # if the frame is a cg frame
            elif self.text[self.frame]['cg']:
                pass
            # if the frame is a normal frame
            else:
                self.no_progression=True
                music=self.text[self.frame]['music']
                # change music if encounter new music setting
                if music!=self.music:
                    self.music_on=False
                    self.music=music
                else:
                    pass
                if self.music_on==False:
                    # set music on when music is not on
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play(-1)
                    self.music_on=True
                else:
                    pass
                message=self.text[self.frame]['message']
                self.message=message
                name=self.text[self.frame]['name']
                self.name=self.text_font.render(name,True,self.white)
                self.bg=self.text[self.frame]['bg']
                sps=self.text[self.frame]['sp']
                self.sps=sps
                self.sps_len=len([sp_v for sp_v in sps.values() if sp_v!=''])
                if self.sps_len==0:
                    pass
                elif self.sps_len==1:
                    width,height=sps['0'].get_size()
                    self.sp_p0=(600-width/2,100)
                elif self.sps_len==2:
                    width,height=sps['0'].get_size()
                    self.sp_p0=(300-width/2,100)
                    width,height=sps['1'].get_size()
                    self.sp_p1=(900-width/2,100)
                elif self.sps_len==3:
                    width,height=sps['0'].get_size()
                    self.sp_p0=(200-width/2,100)
                    width,height=sps['1'].get_size()
                    self.sp_p1=(600-width/2,100)
                    width,height=sps['2'].get_size()
                    self.sp_p2=(1000-width/2,100)
                else:
                    pass

    def on_render(self):
        if self.text[self.frame]['menu']:
            pass
        elif self.text[self.frame]['choice']:
            self.surface.blit(self.bg,(0,0))
            self.surface.blit(self.choice_text_surface,(0,0))
        elif self.text[self.frame]['cg']:
            pass
        else:
            self.surface.blit(self.bg,(0,0))
            try:
                self.surface.blit(self.sps['0'],self.sp_p0)
                self.surface.blit(self.sps['1'],self.sp_p1)
                self.surface.blit(self.sps['2'],self.sp_p2)
            except Exception as e:
                pass
            self.pic_job.draw_alpha_rec(screen=self.surface,position=(self.m_box.x,self.m_box.y),size=(self.m_box.width,self.m_box.height),color=self.water_blue,transparency=160,cornor_radius=(0,0,0,0))
            Text_job.trim_text(surface=self.surface,input_text=self.message,font=self.text_font,rect=self.m_box,color=self.white,w_pad=20,n_pad=20,s_pad=0,e_pad=0,space_between_line=10,font_height=20)
            self.pic_job.draw_alpha_rec(screen=self.surface,position=(self.name_box.x,self.name_box.y),size=(self.name_box.width,self.name_box.height),color=self.light_blue,transparency=160,cornor_radius=(0,0,0,0))
            x1=self.name_box.x+(1/2)*(self.name_box.width-self.name.get_width())
            y1=self.name_box.y+(1/2)*(self.name_box.height-self.name.get_height())
            self.surface.blit(self.name,(x1,y1))
        self.screen.flip()

    def on_clean(self):
        # clean unnecessary data
        if int(self.frame)<len(self.text)-1:
            self.sp_p0=None
            self.sp_p1=None
            self.sp_p2=None
            if self.clean_choice_rectangles:
                self.choice_rectangles=[]
                self.clean_choice_rectangles=False
            else:pass
         

  


    def on_execute(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            if self.show_menu==True:
                break
            self.on_loop()
            self.on_render()
            self.on_clean()
                
class Save:
    def __init__(self):
        # initiate
        pygame.init()
        pygame.mixer.init()
        self.running=True
        self.pic_job=Pic_job()
        self.loop_job=Loop_job()
        # set display screen
        self.screen=pygame.display.set_mode((1200,800))
        # define usable color
        self.white=(255,255,255)
        self.black=(0,0,0)
        self.water_blue=(0,119,190)
        self.light_blue=(0, 150, 220)
        self.hotpink=(255,105,180)
        # define usable font
        self.title_font=pygame.font.SysFont(None,70)
        self.description_font=pygame.font.SysFont(None,50)
        # define the list for all save files
        self.save_list=os.listdir('saves')
        self.save_rects=[]
        self.rover=False
        self.rover_list=[]
        
    def on_event(self,event):
        self.mouse_pos=pygame.mouse.get_pos()
        if event.type==pygame.QUIT:
            self.running=False
        for rect in self.save_rects:
            if rect.collidepoint(self.mouse_pos):
                self.rover=True
                if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    App.save_flag=True
            else:
                self.rover=False
            self.rover_list.append(self.rover)
        self.rover_list=self.loop_job.loop_list_populate(self.rover_list,len(self.save_rects))
        print(self.rover_list)
        
    def on_loop(self):
        for a in range(3):
            save_rect=self.pic_job.draw_alpha_rec(self.screen,(100+a*350,200),(300,200),self.hotpink,160,(0,0,0,0))
            self.save_rects.append(save_rect)
            save_rect=self.pic_job.draw_alpha_rec(self.screen,(100+a*350,500),(300,200),self.hotpink,160,(0,0,0,0))
            self.save_rects.append(save_rect)
        self.save_rects=self.save_rects[0:6]
        self.title=self.title_font.render('Save',True,self.white)

    def on_render(self):
        self.screen.blit(self.title,(100,50))
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
    app=App()
    app.on_execute()
    if app.show_menu:
        app=Menu()
        app.on_execute()
    
