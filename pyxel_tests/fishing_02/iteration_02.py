# ======================================================================
# SOURCES
# ======================================================================
# Inspiration for Stardew-like physics:
# https://www.youtube.com/watch?v=iikL3iWUGRk

import pyxel



TILE_SIZE = 8
SCREEN_HEIGHT = 160
SCREEN_WIDTH = 240



class App:
    def __init__(self):

        # Init
        pyxel.init(
            width = SCREEN_WIDTH,
            height = SCREEN_HEIGHT,
            title = "Fishing 02"
        )

        # Load resources
        pyxel.load("resources.pyxres")

        # Global Y positioning
        self.Y = TILE_SIZE * 4

        # Frame
        self.frame_size = TILE_SIZE * 12
        self.frame_xmin = SCREEN_WIDTH / 2 - self.frame_size / 2
        self.frame_xmax = self.frame_xmin + self.frame_size

        # Target area
        self.target_size = TILE_SIZE * 3
        self.target_xmin = self.frame_xmin + 32

        # Cursor (fish)
        self.cursor_size = TILE_SIZE
        self.cursor_x = SCREEN_WIDTH / 2 - self.cursor_size / 2
        
        self.cursor_velocity = 0
        self.cursor_acceleration = 0.1
        self.cursor_deceleration = 0.2
        self.cursor_max_velocity = 6.0
        self.cursor_bounce = 0.6
        
        # Reel
        self.reel_value = 0
        self.reel_velocity = 0.1
        self.reel_distance = 10
        
        self.tmp = "…"

        # Run game
        pyxel.run(self.update, self.draw)



    def update(self):
        
        # Accelerate towards right when key is pressed
        if pyxel.btn(pyxel.KEY_SPACE):
            
            # If the fish speed is not at max to the right, increase acceleration
            if self.cursor_velocity < self.cursor_max_velocity:
                self.cursor_velocity += self.cursor_deceleration
        
        # Accelerate towards left when key is pressed
        else:
            
            # If the fish speed is not at max to the left, increase acceleration
            if self.cursor_velocity > -self.cursor_max_velocity:
                self.cursor_velocity -= self.cursor_acceleration
        
        # Move the fish
        target_position = self.cursor_x + self.cursor_velocity
        
        # If we hit the sides, bounce
        if target_position >= self.frame_xmax - self.cursor_size - 1:
            self.cursor_velocity *= -self.cursor_bounce
        elif target_position <= self.frame_xmin + 1:
            self.cursor_velocity *= -self.cursor_bounce
        else:
            self.cursor_x = target_position
        
        # Check if the cursor si in red, orange or green
        cursor_center = self.cursor_x + (self.cursor_size / 2)
        
        if cursor_center >= self.target_xmin and cursor_center <= (self.target_xmin + self.target_size):
            if self.reel_value < self.frame_size:
                self.reel_value += 1
        
        # Increment reel value
        # self.reel_value += 1
     


    def draw(self):

        # Draw bg
        pyxel.cls(0)

        # Draw frame
        pyxel.rectb(
            x = self.frame_xmin,
            y = self.Y,
            w = self.frame_size,
            h = TILE_SIZE,
            col = 9
        )

        # Draw target area inside of frame
        pyxel.rect(
            x = self.target_xmin,
            y = self.Y + 1,
            w = self.target_size,
            h = TILE_SIZE - 2,
            col = 3
        )

        # Draw cursor (fish)
        pyxel.blt(
            x = self.cursor_x,
            y = self.Y,
            img = 0,
            u = TILE_SIZE,
            v = 0,
            w = self.cursor_size,
            h = TILE_SIZE,
            colkey = 0
        )
        
        # Draw reel bar
        pyxel.rectb(
            x = self.frame_xmin,
            y = self.Y - TILE_SIZE,
            w = self.frame_size,
            h = 4,
            col = 3
        )
        
        # Fill reel bar
        pyxel.rect(
            x = self.frame_xmin,
            y = self.Y - TILE_SIZE,
            w = int(self.reel_value),
            h = 4,
            col = 3
        )
        
        # Show values
        pyxel.text(
            x = TILE_SIZE,
            y = TILE_SIZE,
            s = f"G: {self.tmp}",
            col = 7
        )



App()