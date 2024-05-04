import json
text={
            0:{
                'menu':False,
                'choice':False,
                'cg':False,
                'name':'Sayori',
                'message':'Hello',
                'bg':'bg/Futon_Room.png',
                'sp':{
                    0:'sp/Miho_WinterUni_Smile.png',
                    1:'sp/Miho_WinterUni_Smile.png',
                    2:'sp/Miho_WinterUni_Smile.png'
                },
                'music':'music/track1.mp3'

            },
            1:{
                'menu':False,
                'choice':False,
                'cg':False,
                'name':'Wu',
                'message':'i can not stand myself',
                'bg':'bg/Futon_Room.png',
                'sp':{
                    0:'sp/Miho_WinterUni_Smile.png',
                    1:'sp/Miho_WinterUni_Smile.png',
                    2:''
                },
                'music':'music/track2.mp3'
            },
            2:{
                'menu':False,
                'choice':False,
                'cg':False,
                'name':'Sayori',
                'message':'i really want to hang myself',
                'bg':'bg/Futon_Room.png',
                'sp':{
                    0:'sp/Miho_WinterUni_Smile.png',
                    1:'sp/Miho_WinterUni_Open_Blush.png',
                    2:'sp/Miho_WinterUni_Smile.png'
                },
                'music':'music/track1.mp3'
            }           
        }


tree={
    '0':{
        0:{
            'text':'first choice',
            'script':'script1.json'
        },
        1:{
            'text':'second choice',
            'script':'script2.json'
        }
    },
    '00':{
       0:{
            'text':'first choice',
            'script':'script3.json'
        },
        1:{
            'text':'second choice',
            'script':'script4.json'
        }
    },
    '01':{
       0:{
            'text':'first choice',
            'script':'script5.json'
        },
        1:{
            'text':'second choice',
            'script':'script6.json'
        }
    }
}
with open('tree.json','w') as f:
    json.dump(tree,f,indent=6)