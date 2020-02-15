import random
import roll
import team
import pickle
import season
import match
import field
import view
import draw
import sdl2
import sdl2.ext
import time


min=1
max=6

def main():

#    print ("The values are....", roll.roll(min, max), roll.roll(min, max))
#    print ("The values are....", roll.sum_rolls(3))
#    print ("Compared to 4 ....", roll.compare_rolls(2, 4))
#    group = [[1,2],[3,4],[5,6]] 
#    val = roll.sum_rolls(1)
#    print ("Roll",val,"Matches group",roll.find_group(val, group));
#    t = team.team(1)
#    print (t)
#    t2 = team.team(1)
#    print (t2)
    
#    with open('data.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
#        pickle.dump(t2, f, pickle.HIGHEST_PROTOCOL)
#        f.close()


#    with open('data.pickle', 'rb') as g:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
#        data = pickle.load(g)
#        g.close()

#    print (data)
    ssn = season.season(2020)


    with open('data.2020', 'wb') as f:
        pickle.dump(ssn, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    with open('data.2020', 'rb') as g:
        data = pickle.load(g)
        g.close()
    
    print (data)
    f = field.field(int((1800/2)-(1598/2)),int((900/2)-(821/2)))
    m = match.match(f)
#    v = view.view(1598,821)
    v = view.view(1800,900)
    playing = True

    last = time.time()*1000
    while (playing == True):
        new = time.time()*1000
        elapsed = new-last
        if (elapsed >= 20): 
            last = new
            v.view_refresh(v.window, f)
            if (m.do_tick() == 0):
               # playing = False
               playing = True 

            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
                if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    print ("Mouse Button Down", event.button.button, event.button.x, event.button.y, event.button.state, event.button.clicks);
                    f.add_ball(event.button.x, event.button.y);
                # draw_rect(windowsurface, event.button.x, event.button.y, 10, 10)
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

#    v.view_cleanup()      

if __name__ == "__main__":
        main()


