import pyxel


# App level constants
TILE_SIZE = 8
SCREEN_HEIGHT = 160
SCREEN_WIDTH = 240

# Module level constants
Y = TILE_SIZE * 4



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
        
        # Run game
        pyxel.run(self.update, self.draw)
    
    
    def update(self):
        a = 1



    def draw(self):
        
        # Draw game bg
        pyxel.cls(0)
   


App()