import pyxel
from enum import Enum



# App level constants
TILE_SIZE = 8
SCREEN_HEIGHT = 160
SCREEN_WIDTH = 240

# Module level constants
Y = TILE_SIZE * 4



# Fishing status
class FishingStatus(Enum):
    ONGOING = 'ongoing'
    SUCCESS = 'success'
    FAILURE = 'failure'
    ABORT = 'abort'



# Fishing mini-game patterns (12 slots inside the current frame)
P_01 = [
    ['slow', 1],
    ['medium', 2],
    ['fast', 6],
    ['medium', 2],
    ['slow', 1]
]



# Store fishing mini-game patterns and speeds by difficulty
PATTERNS = {
    'easy': {
        'speeds': { 'slow': 0.5, 'medium': 1, 'fast': 3 },
        'patterns': [P_01]
    }
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
    def __init__(self, frame, cursor, difficulty):
        
        # Frame dimensions
        self.frame = frame
        
        # Related cursor
        self.cursor = cursor
        
        # Pattern to use
        self.pattern_difficulty = difficulty
        self.pattern = 0
        
        # Speed
        self.speed = 1
    
    
    def pattern_color(self, type):
        if type == 'slow': 
            return 8
        elif type == 'medium':
            return 10
        elif type == 'fast':
            return 11
        else:
            return 0


    def update(self):
        # ===== Get speed at which we close the distance to the surface: =====
        # Get cursor center position
        cursor_center = self.cursor.x + (self.cursor.size / 2)
        
        # Get cursor speed from pattern
        pattern = PATTERNS[self.pattern_difficulty]['patterns'][self.pattern]
        
        # Find cursor position
        xmin = self.frame.xmin
        
        # Speed found?
        speed_found = False
        
        for p in pattern:
            if not speed_found:
                width = p[1] * TILE_SIZE
                xmax = xmin + width
                
                # Is the cursor between xmin and xmax?
                if cursor_center >= xmin and cursor_center < xmax:
                    speed_smf = p[0]
                    speed = PATTERNS[self.pattern_difficulty]['speeds'][speed_smf]
                    self.speed = speed
                    speed_found = True
                
                else:
                    xmin += width
    
    
    def draw(self):
        
        # Retrieve pattern to draw
        pattern = PATTERNS[self.pattern_difficulty]['patterns'][self.pattern]
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
    def __init__(self, distance, difficulty):
                
        # Related objects
        self.frame = Frame()
        self.cursor = FishCursor(frame = self.frame)
        self.pattern = Pattern(
            frame = self.frame,
            cursor = self.cursor,
            difficulty = difficulty
            )
        
        # Dimensions
        self.width = self.frame.size
        
        # Distance bar progress
        self.distance_max = distance
        self.distance_current = 0
        self.distance_speed = 1
        
        # Fishing mini-game events
        self.status = FishingStatus.ONGOING
    
    
    def update(self):
        
        # If fishing is ongoing, animate cursor
        self.cursor.move()
        
        # Get speed from pattern
        self.pattern.update()
        
        # Get current distance cursor speed
        self.distance_speed = self.pattern.speed
        # print(f"Speed: {self.pattern.speed} || Speed px: {self.distance_speed}")
        
        # Close distance to the surface
        self.distance_current += self.distance_speed
        
        # Handle success and failure
        if self.status == FishingStatus.ONGOING:
            if self.distance_current >= self.distance_max: # SUCCESS
                self.status = FishingStatus.SUCCESS
                
            elif self.distance_current < 0: # FAILURE
                self.status = FishingStatus.FAILURE
            
            elif pyxel.btnp(pyxel.KEY_BACKSPACE): # ABORT
                self.status = FishingStatus.ABORT

    
    def draw(self):
               
        # Draw pattern
        self.pattern.draw()
        
        # Draw frame
        self.frame.draw()
        
        # If fishing is ongoing, animate cursor
        self.cursor.draw()
        
        # Draw distance bar - frame
        pyxel.rectb(
            x = self.frame.xmin,
            y = self.frame.y - 7,
            w = self.frame.size,
            h = 4,
            col = 3
        )
        
        # Draw distance bar - fill
        current_width = int(self.distance_current * self.width / self.distance_max)
        if current_width <= self.width:
            width = current_width
        else:
            width = self.width
        
        pyxel.rect(
            x = self.frame.xmin,
            y = self.frame.y - 7,
            w = width,
            h = 4,
            col = 3
        )



class Fish:
    def __init__(self, difficulty):
        self.difficulty = difficulty



class App:
    def __init__(self):
        
        # Init pyxel app
        pyxel.init(
            width = SCREEN_WIDTH,
            height = SCREEN_HEIGHT,
            title = "Fishing 03"
        )
        
        # Load resources
        pyxel.load("resources.pyxres")
        
        # --------- FISHING GAME -----------
        # Hook depth
        self.depth = 300
        
        # Add fish to the game
        self.fish = Fish('easy')
        
        # Init fishing mini-game prop
        self.fishing = False
        
        # Show mini-game related message
        self.message = False
        # ----------------------------------
        
        # Run game
        pyxel.run(self.update, self.draw)
    
    
    def update(self):
        
        # Press SPACE to start fishing
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.fishing:
            
            # Create fishing minigame
            self.fishing = FishingMiniGame(self.depth, self.fish.difficulty)
        
        # If we are fishing, run the mini_game until it returns success or failure
        if self.fishing:
            
            # Run minigame
            self.fishing.update()
            
            # Do something on success
            if self.fishing.status == FishingStatus.SUCCESS:
                self.message = "Well done, you caught the fish"
                self.fishing = False
                print(self.message)
            
            # Do something on failure
            elif self.fishing.status == FishingStatus.FAILURE:
                self.message = "The fish is gone with your bait"
                self.fishing = False
                print(self.message)
            
            # Do something on abort fishing
            elif self.fishing.status == FishingStatus.ABORT:
                self.message = "You let the fish go with your bait"
                self.fishing = False
                print(self.message)
            


    def draw(self):
        
        # Draw game bg
        pyxel.cls(0)
        
        # Draw depending on if we are fishing or not
        if self.fishing:
            self.fishing.draw()
            pyxel.text(
                x = TILE_SIZE * 8,
                y = TILE_SIZE * 16,
                s = "Press BACKSPACE to abort fishing",
                col = 7
            )
        
        elif self.message:
            pyxel.text(
                x = TILE_SIZE * 8,
                y = TILE_SIZE * 15,
                s = self.message,
                col = 7
            )
            
            pyxel.text(
                x = TILE_SIZE * 8,
                y = TILE_SIZE * 16,
                s = "Press SPACE to fish again",
                col = 7
            )
        
        else:
            pyxel.text(
                x = TILE_SIZE * 8,
                y = TILE_SIZE * 16,
                s = "Press SPACE to start fishing",
                col = 7
            )
        


App()