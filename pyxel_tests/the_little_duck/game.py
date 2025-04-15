import pyxel


TILE_SIZE = 8



class World():
    HEIGHT = 16
    WIDTH = 16

    # World items
    GROUND = (0, 0)
    TREE = (1, 0)



class Player():
    DUCK_SPRITE = (16, 0)
    DUCK_STATIC = [(16, 0)]
    DUCK_WALK = [(24, 0), (16, 0), (32, 0), (16, 0)]

    X = 80
    Y = 32
    SPEED = 4
    ANIMATION_TICK = 0



class App():
    def __init__(self):
        pyxel.init(
            width = World.WIDTH * TILE_SIZE,
            height = World.HEIGHT * TILE_SIZE,
            title = "The little duck"
        )
        pyxel.load("resources.pyxres")

        # Run game
        pyxel.run(self.update, self.draw)
    
    def update(self):

        # Animate the little duck
        Player.ANIMATION_TICK = int(pyxel.frame_count / 4 % 4)

        # Move the little duck
        if pyxel.btn(pyxel.KEY_UP):
            # What are the top tiles?
            tile_left_x = int(Player.X / TILE_SIZE)
            tile_right_x = int((Player.X + TILE_SIZE - 1) / TILE_SIZE)
            tile_y = int((Player.Y - Player.SPEED) / TILE_SIZE)

            tile_left = pyxel.tilemaps[0].pget(tile_left_x, tile_y)
            tile_right = pyxel.tilemaps[0].pget(tile_right_x, tile_y)

            if tile_left == World.GROUND and tile_right == World.GROUND:
                # Move the duck
                Player.Y -= Player.SPEED

        elif pyxel.btn(pyxel.KEY_DOWN):
            # What are the bottom tiles?
            tile_left_x = int(Player.X / TILE_SIZE)
            tile_right_x = int((Player.X + TILE_SIZE - 1) / TILE_SIZE)
            tile_y = int((Player.Y + TILE_SIZE - 1 + Player.SPEED) / TILE_SIZE)

            tile_left = pyxel.tilemaps[0].pget(tile_left_x, tile_y)
            tile_right = pyxel.tilemaps[0].pget(tile_right_x, tile_y)

            if tile_left == World.GROUND and tile_right == World.GROUND:
                # Move the duck
                Player.Y += Player.SPEED

        elif pyxel.btn(pyxel.KEY_LEFT):
            # What are the left tiles?
            tile_x = int((Player.X - Player.SPEED) / TILE_SIZE)
            tile_top_y = int(Player.Y / TILE_SIZE)
            tile_bot_y = int((Player.Y + TILE_SIZE - 1) / TILE_SIZE)

            tile_top = pyxel.tilemaps[0].pget(tile_x, tile_top_y)
            tile_bot = pyxel.tilemaps[0].pget(tile_x, tile_bot_y)

            if tile_top == World.GROUND and tile_bot == World.GROUND:
                # Move the duck
                Player.X -= Player.SPEED

        elif pyxel.btn(pyxel.KEY_RIGHT):
            # What are the left tiles?
            tile_x = int((Player.X + TILE_SIZE - 1 + Player.SPEED) / TILE_SIZE)
            tile_top_y = int(Player.Y / TILE_SIZE)
            tile_bot_y = int((Player.Y + TILE_SIZE - 1) / TILE_SIZE)

            tile_top = pyxel.tilemaps[0].pget(tile_x, tile_top_y)
            tile_bot = pyxel.tilemaps[0].pget(tile_x, tile_bot_y)

            if tile_top == World.GROUND and tile_bot == World.GROUND:
                # Move the duck
                Player.X += Player.SPEED

        # Quit game if "Q" is pressed
        if pyxel.btn(key = pyxel.KEY_Q):
            pyxel.quit()
    
    def draw(self):
        # Black background
        pyxel.cls(0)
        
        # Draw tilemap
        pyxel.bltm(
            x = 0,
            y = 0,
            tm = 0,
            u = 0,
            v = 0,
            w = 16 * TILE_SIZE,
            h = 16 * TILE_SIZE
        )

        # Draw the little duck
        pyxel.blt(
            x = Player.X,
            y = Player.Y,
            img = 0,
            u = Player.DUCK_WALK[Player.ANIMATION_TICK][0],
            v = Player.DUCK_WALK[Player.ANIMATION_TICK][1],
            w = TILE_SIZE,
            h = TILE_SIZE,
            colkey = 0
        )


App()