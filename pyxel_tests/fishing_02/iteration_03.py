import pyxel



# App level constants
TILE_SIZE = 8
SCREEN_HEIGHT = 160
SCREEN_WIDTH = 240

# Module level constants
Y = TILE_SIZE * 4



# Fishing mini-game patterns (12 slots inside the current frame)
P_01 = [
    ['slow', 1],
    ['medium', 2],
    ['fast', 6],
    ['medium', 2],
    ['slow', 1]
]



# Store fishing mini-games by difficulty
P_EASY = {
    'speeds': { 'slow': 1, 'medium': 2, 'fast': 3 },
    'patterns' : [P_01]
}



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
    def __init__(self, frame, cursor):
        
        # Frame dimensions
        self.frame = frame
        
        # Related cursor
        self.cursor = cursor
        
        # Pattern to use
        self.pattern_difficulty = P_EASY
        self.pattern = 0
        
        # Distance bar progress
        self.distance_max = 100
        self.distance_current = 0
        self.distance_speed = 1
    
    
    def pattern_color(self, type):
        if type == 'slow': 
            return 8
        elif type == 'medium':
            return 10
        elif type == 'fast':
            return 11
        else:
            return 0
    
    
    def get_distance_speed(self):
        # Get cursor center position
        cursor_center = self.cursor.x + (self.cursor.size / 2)
        
        # Get cursor speed from pattern
        pattern = self.pattern_difficulty['patterns'][self.pattern]
        
        # Find cursor position
        xmin = self.frame.xmin
        
        for p in pattern:
            width = p[1] * TILE_SIZE
            xmax = xmin + width
            
            # Is the cursor between xmin and xmax?
            if cursor_center >= xmin and cursor_center < xmax:
                speed_smf = p[0]
                speed = self.pattern_difficulty['speeds'][speed_smf]
                return speed
            
            else:
                xmin += width



    def update(self):
        # Get speed at which we close the distance to the surface
        self.distance_speed = self.get_distance_speed()
        
        # Close distance to the surface
        self.distance_current += self.distance_speed
        
        if self.distance_current >= self.distance_max:
            # Congrats, it's a win!
            print("WON")

    
    
    def draw(self):
        
        # Retrieve pattern to draw
        pattern = self.pattern_difficulty['patterns'][self.pattern]
        x = self.frame.xmin
        
        # Draw pattern sections
        for p in pattern:
            type = p[0]
            width = p[1] * TILE_SIZE
            
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
        self.pattern = Pattern(frame = self.frame, cursor = self.cursor)
    
    
    def update(self):
        
        # Animate fish
        self.cursor.move()
        
        # Pattern actions
        self.pattern.update()

    
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