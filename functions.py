import pygame
import json
import time

class Pic_job:
    def __init__(self):
        pass
    def ration_scale(picture,desired_width=None,desired_height=None):
        original_width, original_height=picture.get_size()
        if desired_width == None:
            scale_factor=desired_height/original_height
            scaled=pygame.transform.smoothscale(picture,(int(original_width*scale_factor),int(original_height*scale_factor)))
        elif desired_height == None:
            scale_factor=desired_width/original_width
            scaled=pygame.transform.smoothscale(picture,(int(original_width*scale_factor),int(original_height*scale_factor)))
        else:
            scaled=pygame.transform.smoothscale(picture,(desired_width,desired_height))
        return scaled
    # draw a rec with transparency
    # postion (x,y) size (x,y) transparency int
    # cornor radius (a,b,c,d)
    def draw_alpha_rec(self,screen,position,size,color,transparency,cornor_radius):
        surface=pygame.Surface(size)
        surface.set_alpha(transparency)
        surface.fill(color)
        rect=pygame.Rect(position[0],position[1],size[0],size[1])
        pygame.draw.rect(surface,color,rect,border_top_left_radius=cornor_radius[0],border_top_right_radius=cornor_radius[1],border_bottom_left_radius=cornor_radius[2],border_bottom_right_radius=cornor_radius[3])
        screen.blit(surface,position)
        return rect

class Choice:
    def __init__(self,tree_file):
        self.tree=self.read_file(tree_file)
        self.node_no='0'
        self.node=self.tree[self.node_no]
        self.choice_texts=[]
        self.loaded_script=None
        self.loop_job=Loop_job()
        self.loaded_script_name=None

    def read_file(self,address):
        with open(f'scripts/{address}','r') as f:
            file=json.load(f)
            self.loaded_script_name=f'scripts/{address}'
            return file
    
    # input the number of the choice: str
    # return a turple
    # loaded script, next node number
    # set self.loaded_script and self.choice_text
    
    # initiate choice instance in app __init__
    # in choice frame, call get_choice_text() 
    # use self.choice_text to write choices
    # get choice_no from choice_frame
    # run script choice()
    def script_choice(self,choice_no):
        script=self.node[choice_no]['script']
        self.loaded_script=self.read_file(script)
        self.node_no=self.node_no+choice_no
        self.node=self.tree[self.node_no]
        print(f'self.node is {self.node}')
        return self.loaded_script, self.node_no
    
    def get_choice_text(self):
        for choice in self.node.keys():
            self.choice_texts.append(self.node[choice]['text'])
        self.choice_texts=self.loop_job.loop_list_populate(self.choice_texts,len(self.node.keys()))
        return self.choice_texts

class Text_job:
    def __init__(self):
        pass
    # text:str, size:(x,y), font: font object of pygame.Font
    # output None
    # display the text within the rect
    def trim_text(surface,input_text,font,rect,color,w_pad, n_pad, s_pad, e_pad, space_between_line, font_height):
        size=rect.size
        def get_text_list():
            font_lenth=12
            text_box_length=size[0]/font_lenth
            text_box_height=size[1]
            text_list=[]
            text=input_text.replace('\n','')
            text_len=len(text)
            if text_len>text_box_length:
                while_breaker=0
                while text_len>text_box_length:
                    break_index=0
                    char_index=0
                    for char in text:
                        if char==' ':
                            if char_index<=text_box_length:
                                char_index=char_index+1
                            else:
                                break_index=char_index
                                break
                        else:
                            char_index=char_index+1
                    text_list.append(text[0:break_index])
                    text=text[break_index:]
                    text_len=len(text)
                    if text_len<text_box_length:
                        text_list.append(text)
                        text_list[0]=' '+text_list[0]
                    if while_breaker==10:
                        text_list[text_list.index('')]=text
                        text_list[0]=' '+text_list[0]
                        break
                    while_breaker=while_breaker+1
                return text_list
            else:
                text_list.append(text)
                text_list[0]=' '+text_list[0]
                return text_list
        def create_text_surface():
            #back_text_surface=pygame.Surface(size,flags=pygame.SRCALPHA)
            #back_text_surface.set_colorkey((0,0,0))
            #back_text_surface.fill(color)


            text_list=get_text_list()
            line_no=len(text_list)
            line_index=0
            for line in text_list:
                line=font.render(line,True,color)
                surface.blit(line, (rect.x+w_pad,n_pad+rect.y+line_index*(space_between_line+font_height)))
                line_index=line_index+1
            #return back_text_surface
        create_text_surface()

class Loop_job:
    def __init__(self):
        pass
    # when a list gets appendded in loop, refill list from the first index after certain addition
    # elements===list, number===int
    def loop_list_populate(self,elements,number):
        output_list=[None for a in range(number)]
        counter=0
        for element in elements:
            if counter<number:
                output_list[counter]=element
                counter=counter+1
            if counter>=number:
                counter=counter-number
        return output_list






    
        
if __name__=='__main__':
    loop_job=Loop_job()
    while True:
        loop_job.loop_list_populate(['a','b','c','d','e','f'],3)
        time.sleep(1)

    #pygame.init()
    #screen=pygame.display.set_mode((800,800))
    #pic_job=Pic_job()
    #while True:
        #bg=pygame.image.load('bg/Futon_Room.png').convert()
        #screen.blit(bg,(0,0))
        #font=pygame.font.SysFont(None,32)
        #text='hello'
        #text_surface=font.render(text,True,(255,255,255))
        #screen.blit(text_surface,(0,0))
        #pic_job.draw_alpha_rec(screen=screen,position=(0,0),color=(225,192,203),transparency=120,size=(200,200),cornor_radius=(0,0,0,0))
        #pygame.display.flip()
    
    #rect=pygame.Rect(0,400,800,400)
    #font=pygame.font.Font('freesansbold.ttf',32)
    #while True:
    #    text=''
    #You know the world is a bad place where thousand of people lives. I cannot bare living in such a place. It is disgusting. I have to
    #let you die. I am sorry but i have to. Sorry Sayori. SOrry. Death is unavoidable. Life can be difficult. I mean it
    #'''
    #    text1='hello how are you'
     #   text2="i can not stand myself, i want to kill myself. How are you? Life is so tiresome. Oh what can I do, I have been broken in to 3"
      #  Text_job.trim_text(surface=screen,input_text=text2,font=font,rect=rect,color=(255,255,255),w_pad=20,n_pad=20,s_pad=0,e_pad=0,space_between_line=10,font_height=20)
       # pygame.display.flip()
    


    

