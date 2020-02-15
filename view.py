"""2D drawing examples."""
import sys
from random import randint
import sdl2
import sdl2.ext
#import vec3
import glm
import field
import match
import draw


class view:
    def __init__(self, _xWinSize, _yWinSize):
        # Initialize the video subsystem, create a window and make it visible.
        sdl2.ext.init()
        self.window = sdl2.ext.Window("2D drawing primitives", size=(_xWinSize, _yWinSize))
        self.window.show()
        self.xsize = _xWinSize 
        self.ysize = _yWinSize

        # explicitly acquire the window's surface to draw on.
        windowsurface = self.window.get_surface()

        sdl2.ext.fill(windowsurface, 0)

    def view_input(self):
        # The event loop is nearly the same as we used in colorpalettes.py. If you
        # do not know, what happens here, take a look at colorpalettes.py for a
        # detailled description.
        running = True
        while running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
                if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    print ("Mouse Button Down", event.button.button, event.button.x, event.button.y, event.button.state, event.button.clicks);
                    draw_rect(windowsurface, event.button.x, event.button.y, 10, 10)
#                   curindex += 1
#                   if curindex >= len(functions):
#                       curindex = 0
                    # In contrast to colorpalettes.py, our mapping table consists
                    # of functions and their arguments. Thus, we get the currently
                    # requested function and argument tuple and execute the
                    # function with the arguments.
                    break
                if event.type == sdl2.SDL_MOUSEBUTTONUP:
                    print ("Mouse Button Up", event.button.button, event.button.x, event.button.y, event.button.state, event.button.clicks);
                    break;
                if event.type == sdl2.SDL_MOUSEMOTION:
                    print ("Mouse Motion", event.motion.which, event.motion.state, event.motion.x, event.motion.y, event.motion.xrel, event.motion.yrel);
                    break
                if event.type == sdl2.SDL_MOUSEWHEEL:
                    print ("Mouse Wheel", event.wheel.x, event.wheel.y, event.wheel.direction)
                    break
                if event.type == sdl2.SDL_KEYDOWN:
                    print ("Key Down: ", event.key.state);
                    if (event.key.keysym.sym == sdl2.SDLK_UP):
                        print("Up Arrow");
                    if (event.key.keysym.sym == sdl2.SDLK_DOWN):
                        print("DOWN Arrow");
                    if (event.key.keysym.sym == sdl2.SDLK_a):
                        print("a");

                    break

    def view_refresh(self, window, playfield):
        # Fill the whole surface with a black color.
        windowsurface = window.get_surface()
        sdl2.ext.fill(windowsurface, 0)
        playfield.draw(windowsurface)

        # load the background TODO

        # load the balls
        for i in playfield.power_cells:
            i.pos.tick_update()
            i.draw(windowsurface)
            #self.draw_ball(windowsurface, i.pos.center_pos, 18, 18)

        # load the robots TODO
        for r in playfield.robots:
            r.plan_move(playfield)
            r.pos.tick_update()
            r.draw(windowsurface)

        # re-blit the window
        window.refresh()

    def view_cleanup(self):
        sdl2.ext.quit()
        return 0

