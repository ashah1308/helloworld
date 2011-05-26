#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 004_alphademo.py
    colorkey and alpha-value
    url: http://thepythongamebook.com/en:part2:pygame:step004
    author: horst.jens@spielend-programmieren.at
    per-pixel-alpha code by Claudio Canepa <ccanepacc@gmail.com>
    licence: gpl, see http://www.gnu.org/licenses/gpl.html
"""
import pygame
import os

 
def get_alphaed( surf, alpha=128, red=128, green=128, blue=128, mode=pygame.BLEND_RGBA_MULT):
    """returns a copy of a surface object with user-defined 
       values for red, green, blue and alpha. 
       Values from 0-255. 
       thanks to Claudio Canepa <ccanepacc@gmail.com>
       for this function."""
  
    tmp = pygame.Surface( surf.get_size(), pygame.SRCALPHA, 32)
    tmp.fill( (red,green,blue,alpha) )
    tmp.blit(surf, (0,0), surf.get_rect(), mode)
    return tmp
 
def bounce(value, direction, bouncing=True, valuemin=0, valuemax=255):
    """bouncing a value (like alpha or color) between 
       baluemin and valuemax. 
       When bouncing is True,
       direction (usually -1 or 1)  is inverted when reaching valuemin or valuemax"""
       
    value += direction # increase or decrase value by direction
    if value <= valuemin:
        value = valuemin
        if bouncing:
            direction *= -1
    elif value >= valuemax:
        value = valuemax
        if bouncing: 
            direction *= -1
    return value, direction  
    
def write(msg="pygame is cool", size=24, color=(255,255,255)):
    myfont = pygame.font.SysFont("None", size)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext
 
def alphademo(width=800, height=600):
    pygame.init()
    screen=pygame.display.set_mode((width, height))
    background = pygame.Surface(screen.get_size()).convert()
    #background.fill((255, 255, 255))     #fill the background white
    venus = pygame.image.load(os.path.join("data","800px-La_naissance_de_Venus.jpg")).convert()
    # transform venus and blit on background in one go
    pygame.transform.scale(venus, (width, height), background) 
    # --------- png image with convert.alpha() ------------------
    # .png and .gif graphics can have transparency. use convert_alpha()
    pngMonster = pygame.image.load(os.path.join("data", "colormonster.png")).convert_alpha()
    pngMonster0 = pngMonster.copy() # a copy 
    pngMonster3 = pngMonster.copy() # copy for per-pixel alpha
    
    # ---------- jpg image  ------------
    # using .convert() at an .png image is the same as using a .jpg  
    # => no transparency !
    jpgMonster = pygame.image.load(os.path.join("data","colormonster.jpg")).convert()
    jpgMonster0 = jpgMonster.copy() # copy of jpgMonster 
    jpgMonster1 = jpgMonster.copy() # another copy to demonstrate colorkey
    jpgMonster1.set_colorkey((255,255,255)) # make white color transparent
    jpgMonster1.convert_alpha() 
    jpgMonster2 = jpgMonster.copy() # another copy for surface alpha
    jpgMonster3 = jpgMonster.copy() # anoter copy for per-pixel alpha
    # ------- text surfaces ----------
    png0text = write("png (has alpha)")
    png3text = write("png with pixel-alpha")
    jpg0text = write("jpg (no alpha)")
    jpg1text = write("jpg with colorkey")
    jpg2text = write("jpg with surface alpha")
    jpg3text = write("jpg with pixel-alpha")
    # ------- for bitmap-alpha --------
    alpha = 128   # between 0 and 255. 
    direction = 1 # change of alpha
    # ------- for per-pixel-alpha -----
    r = 255 # red
    g = 255 # green
    b = 255 # blue
    a = 255 # pixel-alpha
    modenr = 7 # --> 8 --> RGB_MULT 
    
    #mode = pygame.BLEND_ADD #1 #pygame 1.8.0
    #mode = pygame.BLEND_SUB #2
    #mode = pygame.BLEND_MULT #3
    #mode = pygame.BLEND_MIN #4
    #mode = pygame.BLEND_MAX #5
    #mode = pygame.BLEND_RGBA_ADD #6 # pygame 1.8.1
    #mode = pygame.BLEND_RGBA_SUB #7
    #mode = pygame.BLEND_RGBA_MULT #8 #the best !!!!
    #mode = pygame.BLEND_RGBA_MIN #9
    #mode = pygame.BLEND_RGBA_MAX #10
    
    modeStrings = { 1: "pygame.BLEND_ADD",
                    2: "pygame.BLEND_SUB",
                    3: "pygame.BLEND_MULT",
                    4: "pygame.BLEND_MIN",
                    5: "pygame.BLEND_MAX",
                    6: "pygame.BLEND_RGBA_ADD",
                    7: "pygame.BLEND_RGBA_SUB",
                    8: "pygame.BLEND_RGBA_MULT",
                    9: "pygame.BLEND_RGBA_MIN",
                    16: "pygame.BLEND_RGBA_MAX" }
    modekeys = modeStrings.keys()
    modekeys.sort() # [1,2,3,4,5,6,7,8,9,16]
    
    
    # -------  mainloop ----------
    clock = pygame.time.Clock()
    mainloop = True
    effects = False
    while mainloop:
        clock.tick(30)
        screen.blit(background, (0,0)) # draw background every frame
        pygame.display.set_caption("insert/del=red:%i, home/end=green:%i, pgup/pgdwn=blue:%i, +/-=pixalpha:%i press ESC" % ( r, g, b, a))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN: # press and release key
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                if event.key == pygame.K_RETURN:
                    print "alt", modenr
                    modenr += 1
                    if modenr > 9: 
                        modenr = 0 # cycle throug number 0 to 9
                    print "neu", modenr
                    print modekeys[modenr]
        # ------ keyb is pressed ? -------
        dr, dg, db, da = 0,0,0,0 # set changing to 0 for red, green, blue, pixel-alpha
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_PAGEUP]: 
            db = 1 # blue up
        if pressed_keys[pygame.K_PAGEDOWN]: 
            db = -1 # blue down
        if pressed_keys[pygame.K_HOME]:
            dg = 1 # green up
        if pressed_keys[pygame.K_END]:
            dg = -1 # green down
        if pressed_keys[pygame.K_INSERT]:
            dr = 1 # red up
        if pressed_keys[pygame.K_DELETE]:
            dr = -1 # red down
        if pressed_keys[pygame.K_KP_PLUS]:
            da = 1 # alpha up
        if pressed_keys[pygame.K_KP_MINUS]:
            da = -1 # alpha down
        # ------- change color and alpha values -------- 
        alpha, direction = bounce(alpha, direction) # change alpha
        r, dr = bounce(r,dr, False)  # red for per-pixel
        g, dg = bounce(g,dg, False)  # green for per-pixel
        b, db = bounce(b, db, False) # blue for per-pixel
        a, da = bounce(a, da, False) # alpha for per-pixel
        
        # ----- blit jpgMonster0 as ist is, no alpha at all ------
        screen.blit(jpgMonster0, (0, 300))
        screen.blit(jpg0text,(0,550))
        # ------blit jpgMonster1 with the colorkey set to white ------
        screen.blit(jpgMonster1, (200,300))
        screen.blit(jpg1text, (200,550))
        # ----- blit jpgmonster2 with alpha for whole  surface  --------
        jpgMonster2.set_alpha(alpha) # alpha for whole surface
        screen.blit(jpgMonster2, (400,300))  # blit on screen
        screen.blit(jpg2text,(400,550))
        screen.blit(write("surface-alpha: %i" % alpha),(400,570))
        # ----- blit jpgmonster3 with per-pixel alpha-------
        tmp = get_alphaed(jpgMonster3, a, r, g, b, modekeys[modenr]) # get current alpha
        screen.blit(tmp, (600,300))
        screen.blit(jpg3text, (600, 550))
        # ----- blit pngMonster0 as it is, with transparency from image ---
        screen.blit(pngMonster0, (0, 10))
        screen.blit(png0text, (0, 200))
        # ----- blit pngMonster1 with colorkey set to black ----
        #  ***  png already has alpha, does not need colorkey **
        # ----- blit pngMonster2 with alpha for whole surface -----
        #  *** surface-alpha does not work if surface (png) already has alpha ***
        # ----- blit pngmonster3 with per-pixel alpha-------
        tmp = get_alphaed(pngMonster3, a, r, g, b, modekeys[modenr]) # get current alpha
        screen.blit(tmp, (600,10))
        screen.blit(png3text, (600,200))
        # ---- instructions ----
        screen.blit(write("press [INS] / [DEL] to change red value: %i" % r,24, (255,255,255)),(190,150))
        screen.blit(write("press [HOME] / [END] to change green value: %i" % g),(190,170))
        screen.blit(write("press [PgUp] / [PgDwn] to chgange blue value: %i"% b), (190, 190))
        screen.blit(write("press [Enter] to change blit mode: %i (%s)" % (modekeys[modenr], modeStrings[modekeys[modenr]])), (190,230))
        screen.blit(write("press [Num+] / [Num-] to chgange alpha value: %i"% a), (190, 210))
        
        
 
 
        pygame.display.flip()       # flip the screen 30 times a second
if __name__ == "__main__":
    alphademo()
