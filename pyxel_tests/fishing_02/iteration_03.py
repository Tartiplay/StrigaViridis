import pyxel



# App level constants
TILE_SIZE = 8
SCREEN_HEIGHT = 160
SCREEN_WIDTH = 240

# Module level constants
Y = TILE_SIZE * 4



# Fishing mini-game patterns (width = TILESIZE * 12)
P_01 = [
    ['slow', TILE_SIZE],
    ['medium', TILE_SIZE * 2],
    ['fast', TILE_SIZE * 6],
    ['medium', TILE_SIZE * 2],
    ['slow', TILE_SIZE]
]



# Store fishing mini-games by difficulty
P_EASY = [P_01]



class Frame:
    def __init__(self):
        
        # Frame dimensions
        self.size = TILE_SIZE * 12
        self.xmin = SCREEN_WIDTH / 2 - self.size / 2
        self.xmax = self.xmin + self.size
        self.y = Y
    
    
    def draw(self):
        pyxel.rectb(
            x = self.xmin,
            y = Y,
            w = self.size,
            h = TILE_SIZE,
            col = 9
        )



class FishCursor:
    def __init__(self, frame):
        
        # Related objects
        self.frame = frame
        
        # Cursor dimensions
        self.size = TILE_SIZE
        self.x = SCREEN_WIDTH / 2 - self.size / 2
        self.y = Y
        
        # Cursor movement
        self.velocity = 0
        self.acceleration = 0.1
        self.deceleration = 0.2
        self.max_velocity = 6.0
        self.bounce = 0.6
    
    
    def move(self):
        # Accelerate to right when SPACE is pressed
        if pyxel.btn(pyxel.KEY_SPACE):
            
            # If speed < max, accelerate
            if self.velocity < self.max_velocity:
                self.velocity += self.deceleration
            
        # Accelerate to left when key is released
        else:
            
            # If speed < max, accelerate
            if self.velocity > -self.max_velocity:
                self.velocity -= self.acceleration
        
        # Calculate next position
        target_position = self.x + self.velocity
        
        # If we hit the sides, bounce
        if target_position >= self.frame.xmax - self.size - 1:
            self.velocity *= -self.bounce
        elif target_position <= self.frame.xmin + 1:
            self.velocity *= -self.bounce
        else:
            self.x = target_position
        
    
    
    def draw(self):
        pyxel.blt(
            x = self.x,
            y = self.y,
            img = 0,
            u = TILE_SIZE,
            v = 0,
            w = self.size,
            h = TILE_SIZE,
            colkey = 0
        )



class Pattern:
    def __init__(self, frame):
        
        # Frame dimensions
        self.frame = frame
        
        # Pattern to use
        self.pattern_difficulty = P_EASY
        self.pattern = 0
    
    
    def pattern_color(self, type):
        if type == 'slow': 
            return 8
        elif type == 'medium':
            return 10
        elif type == 'fast':
            return 11
        else:
            return 0
    
    
    def draw(self):
        
        # Retrieve pattern to draw
        pattern = self.pattern_difficulty[self.pattern]
        x = self.frame.xmin
        
        # Draw pattern sections
        for p in pattern:
            type = p[0]
            width = p[1]
            
            pyxel.rect(
                x = x,
                y = self.frame.y,
                w = width,
                h = TILE_SIZE,
                col = self.pattern_color(type)
            )
            
            x += width

        
        
class FishingMiniGame:
    def __init__(self):
        
        # Related objects
        self.frame = Frame()
        self.cursor = FishCursor(frame = self.frame)
        self.pattern = Pattern(frame = self.frame)
    
    
    def update(self):
        
        # Animate fish
        self.cursor.move()
        
        # Pattern actions
        # …

    
    def draw(self):
               
        # Draw frame pattern
        self.pattern.draw()
        
        # Draw frame
        self.frame.draw()
        
        # Draw fish cursor
        self.cursor.draw()



class App:
    def __init__(self):
        
        # Init pyxel app
        pyxel.init(
            width = SCREEN_WIDTH,
            height = SCREEN_HEIGHT,
            title = "Fishing 03"
        )
        
        # Create fishing mini game
        self.minigame = FishingMiniGame()
        
        # Load resources
        pyxel.load("resources.pyxres")
        
        # Run game
        pyxel.run(self.update, self.draw)
    
    
    def update(self):
        
        # Run minigame
        self.minigame.update()


    def draw(self):
        
        # Draw game bg
        pyxel.cls(0)
        
        # Draw minigame
        self.minigame.draw()
   


App()