import pyxel
from enum import Enum



TILE_SIZE = 8

SCREEN_HEIGHT = 160
SCREEN_WIDTH = 240



# Enums
class FishingModes(Enum):
    DREDGE = "Dredge"
    STARDEW = "Stardew"



class FishingFrame:

    def __init__(self, x, y):

        # Frame
        self.x = x
        self.y = y
        self.w = TILE_SIZE
        self.h = 7 * TILE_SIZE

        # Target area
        self.target_y = 8
        self.target_h = 16


    def draw(self):
        # Draw frame
        pyxel.blt(
            x = self.x,
            y = self.y,
            img = 0,
            u = 1 * TILE_SIZE,
            v = 0,
            w = self.w,
            h = self.h,
            colkey = 0
        )
        # Draw target area
        pyxel.rect(
            x = self.x + 1,
            y = self.y + self.target_y,
            w = self.w - 2,
            h = self.target_h,
            col = 3
        )
    
    def new_target_area(self):
        # Define random target area limitations
        hmax = 16
        # TODO: Generate a random new target area



class Hook:

    def __init__(self, fishing_frame):

        self.frame = fishing_frame
        self.y = self.frame.y + (self.frame.h / 2)

        # Dredge fishing mode
        self.d_speed = 1

        # Stardew fishing mode
        self.s_speed = 1

        self.flap_cooldown = 0
        self.flap_cooldown_value = 5 # Can flap every x frames

        self.flap_frame = -1 # Flap animation frame count
        self.flap_animate = [3, 2, 1, 0, 0, 0, -0.5]

        # Sprite
        self.u = 0
        self.v = 1 * TILE_SIZE + 2
        self.w = 8
        self.h = 4

        # Bbox
        self.xmin = 1
        self.xmax = 7
        self.ymin = 1
        self.ymax = 10

        # Fishing mode
        self.fishing_mode = FishingModes.STARDEW

        # Animations
        self.bouncing = False


    def draw(self):
        # Draw little fish
        pyxel.blt(
            x = self.frame.x,
            y = self.y,
            img = 0,
            u = 0,
            v = 1 * TILE_SIZE + 2,
            w = 8,
            h = 4,
            colkey = 0
        )


    def move(self):
        # ==============================================================
        # DREDGE FISHING
        # ==============================================================
        if self.fishing_mode == FishingModes.DREDGE:
            # Move the hook between top and bottom
            self.y += self.d_speed
            if self.hits_frame_top() or self.hits_frame_bottom():
                self.d_speed = -self.d_speed
        
        # ==============================================================
        # STARDEW FISHING
        # ==============================================================
        elif self.fishing_mode == FishingModes.STARDEW:
            # Reduce "Flap" cooldown
            if self.flap_cooldown > 0:
                self.flap_cooldown -= 1
            
            # Start "flap" animation when SPACE is pressed
            if pyxel.btnp(pyxel.KEY_SPACE) and self.flap_cooldown == 0:
                self.flap_frame = 0 # Start flapping
                self.flap_cooldown = self.flap_cooldown_value
            
            # Either flap (if anim is triggered) or fall
            if self.flap_frame >= 0:
                # Calculate next movement speed
                movement = self.flap()

                # If next movement goes further than top, limit it
                frame_top = self.frame.y + 1
                next_y = self.y - movement
                if next_y <= frame_top:
                    movement = self.y - frame_top

                self.y -= movement

                # If we reached the last frame, reset animation
                if self.flap_frame == (len(self.flap_animate) - 1):
                    self.flap_frame = -1
                else:
                    self.flap_frame += 1
            
            # If not flapping, then falling
            elif not self.hits_frame_bottom():
                self.y += self.s_speed
    

    def flap(self):
        if self.flap_frame >= 0:
            return self.flap_animate[self.flap_frame]
        else: # Just a security, this shouldn't happen
            return self.s_speed
    

    def hits_frame_top(self):
        if self.y <= (self.frame.y + 1):
            return True
        

    def hits_frame_bottom(self):
        if self.y >= (self.frame.y + self.frame.h - self.h - 1):
            return True
    

    def center_hook(self):
        self.y = self.frame.y + (self.frame.h / 2)
    

    def is_inside(self):
        # Target min and max y (with 1 pixel allowance)
        ymin = self.frame.y + self.frame.target_y
        ymax = ymin + self.frame.target_h

        # Define fish hitbox (with 1 pixel allowance)
        fishmin = self.y + 1
        fishmax = self.y + self.h - 1

        # If fish hitbox is contained by target, return true
        if fishmin >= ymin and fishmax <= ymax:
            return True
        else:
            return False
    
    
    def fish(self):
        if self.fishing_mode == FishingModes.DREDGE:
            if self.is_inside():
                print("OK")
            else:
                print("…")



# Create objects
fishing_frame = FishingFrame(0, 0)
hook = Hook(fishing_frame)


class App:
    
    def __init__(self):
        pyxel.init(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            title="Peche 01"
        )

        pyxel.load("resources.pyxres")

        pyxel.run(self.update, self.draw)
    


    def update(self):
        # Fishing modes swap
        if pyxel.btnp(pyxel.KEY_1):
            if hook.fishing_mode != FishingModes.DREDGE:
                hook.fishing_mode = FishingModes.DREDGE
                hook.center_hook()
                print("Fishing mode changed: Dredge")
        elif pyxel.btnp(pyxel.KEY_2):
            if hook.fishing_mode != FishingModes.STARDEW:
                hook.fishing_mode = FishingModes.STARDEW
                hook.center_hook()
                print("Fishing mode changed: Stardew")

        # Move the hook
        hook.move()

        # Press SPACE to fish
        if pyxel.btnp(pyxel.KEY_SPACE):
            hook.fish()
        


    def draw(self):
        # Draw background
        pyxel.cls(0)

        # Draw fishing frame
        fishing_frame.draw()

        # Draw hook
        hook.draw()

        # Write tutorial text
        pyxel.text(
            x = 8 * 8,
            y = 8,
            s = "Press 1: Dredge mode",
            col = 7
        )
        pyxel.text(
            x = 8 * 8,
            y = 8 * 2,
            s = "Press 2: Stardew mode",
            col = 7
        )

        # Show current fishing mode
        pyxel.text(
            x = 8 * 8,
            y = 8 * 4,
            s = f"Current mode: {hook.fishing_mode.value}",
            col = 7
        )

        # Tutorial
        if hook.fishing_mode == FishingModes.DREDGE:
            pyxel.text(
                x = 8 * 8,
                y = 8 * 6,
                s = "Press SPACE when the fish is in the\ngreen area.",
                col = 7
            )

        elif hook.fishing_mode == FishingModes.STARDEW:
            pyxel.text(
                x = 8 * 8,
                y = 8 * 6,
                s = "Press SPACE to go up.\nKeep the fish inside the green area.",
                col = 7
            )



App()