from sys import flags
import pygame,random,logging,uuid,os
import pypresence

import discordsdk as dsdk
rpctg = True
client_id = "1010660355657191534"
smallimg = "blank"
pty = 1
state = ""
desc = ""

join=str(uuid.uuid4())
ptyid=str(uuid.uuid4())
#pid = os.getpid()

if rpctg:
    RPC = pypresence.Presence(client_id)
    RPC.connect()
    app = dsdk.Discord(int(client_id), dsdk.CreateFlags.default)
    activity_manager = app.get_activity_manager()
    activity_manager.register_command("C:\\Users\\Ben\\pythonprograming\\gemmr\\gemmr.bat")
    

if rpctg: RPC.update(state="loading...",details="loading")

logging.basicConfig(level=logging.DEBUG)
logging.debug("pre_init: seting up")
pygame.init()
w,h =640, 480

l = 0
d = 0
t = 0
tS = 0


def upd(state,details):
    pass



def invites(user):
    global activity_manager, pty
    activity_manager.accept_invite(user)
    activity_manager.send_request_reply(user,1)
    pty = pty +1
    RPC.update(
        state=state,
        details=desc,
        large_image="diamond",
        join=join,
        party_size=[pty,5],
        party_id=ptyid,
        spectate="000"
    )


activity_manager.on_activity_join_request = invites

def join_game(code):
    print(code)

activity_manager.on_activity_join = join_game


screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Gemmr")
clock = pygame.time.Clock()
running = True
logging.debug("pre_init: done")
logging.debug("init: loading assets")
tex = {
    "ice":pygame.image.load("assets/ice.png"),
    "pl":pygame.image.load("assets/pl.png")
    }

fonts = {
    "title":pygame.font.Font('assets/Silkscreen-Regular.ttf', 56),
    "by":pygame.font.Font('assets/Silkscreen-Regular.ttf', 25)
}
logging.debug("init: loaded assets")
logging.debug("init: rendering text")
texts = {
    "title": fonts["title"].render("gemmr", True, (80, 105, 255)),
    "by": fonts["by"].render("by badgeminer2", True, (250, 120, 0)),
}

logging.debug("init: done rendering text")
logging.debug("init: done")

selScr = 0



logging.debug("late_init: loading sprite classes")
class line:
    def __init__(self,pos1,pos2,col,size) -> None:
        self.start = pos1
        self.end = pos2
        self.col = col
        self.size =size
    def draw(self,screen:pygame.Surface):
        pygame.draw.line(screen,self.col,self.start,self.end,self.size)

beams = [line((-1,-1),(0,0),(255,0,0),0),line((-1,-1),(0,0),(255,0,0),0)]

class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, img,x,y):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = img

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.topleft = (x,y)
    def update(self, *args, **kwargs) -> None:
        return super().update(*args, **kwargs)

class entity(Block):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.hp = 0
    def update(self, *args, **kwargs) -> None:
        if self.hp <= 0:
            self.kill()
        else:
            super().update(*args, **kwargs)

class pl(entity):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.hp = 25

playr = pl(tex["pl"],w-100,h/2-(tex["pl"].get_height()/2))

class ice_wisp(entity):
    def __init__(self, img, x, y):
        super().__init__(img, x, y)
        self.hp = 50

    def update(self, *args, **kwargs) -> None:
        if tS%1 == 0:
            global beams
            beams[1].col = (50,0,255)
            beams[1].end = playr.rect.center
            beams[1].start = self.rect.center
            beams[1].size = 5 
        return super().update(*args, **kwargs)





entitys = pygame.sprite.Group()
entitys.add()


entitys.add(playr)

def spawnE(e:pygame.event.Event):
    global entitys
    if e.key == pygame.K_0:
        i=ice_wisp(tex["ice"], 50, h/2-(tex["ice"].get_height()/2))
        entitys.add(i)
        logging.info(f"dev_spawn_entity:{str(i)}")
        

logging.debug("late_init: done loading sprite classes")
logging.debug("late_init: loading screen classes")

#screens
class scr:
    def draw(screen:pygame.Surface):
        pass
    def event(event:pygame.event.Event):
        pass
    def upd():
        pass

class title(scr):
    def draw(screen:pygame.Surface):
        screen.blit(tex["ice"],(50,h/2-(tex["ice"].get_height()/2)))

        #draw title
        screen.blit(texts["title"],(w/2-(texts["title"].get_width()/2),h/2-(texts["title"].get_height()/2)))
        screen.blit(texts["by"],(w/2-(texts["by"].get_width()/2),h-50))
    def event(event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            global selScr,entitys
            selScr = 1
            logging.debug("gameplay_screenSwap: title -> main")

class main(scr):
    def draw(screen: pygame.Surface):
        for i in beams:
            i.draw(screen)
        entitys.draw(screen)
        
    def event(event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            spawnE(event)
    def upd():
        entitys.update()


logging.debug("late_init: done loading screen classes")    
logging.debug("late_init: seting up utils")


def drawScr(screen:pygame.Surface):
    if selScr == 0:
        title.draw(screen)
    elif selScr == 1:
        main.draw(screen)

def updScr():
    if selScr == 0:
        title.upd()
    elif selScr == 1:
        main.upd()

def eventScr(event:pygame.event.Event):
    if selScr == 0:
        title.event(event)
    elif selScr == 1:
        main.event(event)



logging.debug("late_init: done")
state = "idle"
desc="on Title Screen"
if rpctg: RPC.update(
    state=state,
    details=desc,
    large_image="diamond",
    join=join,
    party_size=[pty,5],
    party_id=ptyid,
    spectate="000",
    #pid=pid
    )



while running:
    screen.fill((00, 00, 00))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_F9:
                activity_manager.accept_invite()
        eventScr(event)

    updScr()


    drawScr(screen)
    pygame.display.flip()






    l += 1
    d = clock.tick()
    t += d
    tS = t/1000
    app.run_callbacks()
RPC.close()
RPC.handshake