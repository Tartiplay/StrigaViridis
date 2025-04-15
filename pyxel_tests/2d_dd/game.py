import pyxel



TILE_SIZE = 8
CHARACTER_SIZE = 16

SCREEN_HEIGHT = 16
SCREEN_WIDTH = 16

FLOOR = 8 * TILE_SIZE - CHARACTER_SIZE

HERO_SPACING = 10
HERO_SPEED = 2

ANIMATION_DELAY = 4



class Dungeon:
    # Dungeon dimensions
    HEIGHT = 16
    WIDTH = 16 * 2



class Hero:
    def __init__(self, u, v, order, spritesheet):
        # Sprites
        self.IMG = 1
        self.U = u
        self.V = v
        self.WIDTH = CHARACTER_SIZE
        self.HEIGHT = CHARACTER_SIZE

        # Position
        self.ORDER = order
        self.X = 4 + 3 * HERO_SPACING - self.ORDER * HERO_SPACING
        self.Y = FLOOR

        # Movement
        self.SPEED = HERO_SPEED

        # Animations
        self.SPRITES = spritesheet * CHARACTER_SIZE
        self.ANIM_TICK = 1
        self.ANIM_SPRITES = {
            "idle": [(u, v + self.SPRITES),
                     (u + CHARACTER_SIZE, v + self.SPRITES)],
            "walk": [(u, v + self.SPRITES),
                     (u + CHARACTER_SIZE * 2, v + self.SPRITES)]
        }

    def draw(self, animation = "idle"):
        pyxel.blt(
            x = self.X,
            y = self.Y,
            img = self.IMG,
            u = self.ANIM_SPRITES[animation][self.ANIM_TICK][0],
            v = self.ANIM_SPRITES[animation][self.ANIM_TICK][1],
            w = self.WIDTH,
            h = self.HEIGHT,
            colkey = 0
        )



# Create characters
Hero_01 = Hero(0, 0, 0, 0)
Hero_02 = Hero(0, 0, 1, 1)
Hero_03 = Hero(0, 0, 2, 2)
Hero_04 = Hero(0, 0, 3, 3)
Heroes = [Hero_01, Hero_02, Hero_03, Hero_04]



class Camera:
    # Camera bounds
    MIN_X = SCREEN_WIDTH * TILE_SIZE / 2
    MAX_X = (Dungeon.WIDTH * TILE_SIZE) - MIN_X

    # Camera position
    X = 0
    Y = 0

    # Move camera with the player
    def follow(hero_x):
        hero_center = hero_x + (Hero_01.WIDTH / 2)
        half_screen_px = SCREEN_WIDTH * TILE_SIZE / 2

        # Follow the hero inside camera bounds
        if hero_center < Camera.MIN_X:
            Camera.X = 0
        elif hero_center > Camera.MAX_X:
            Camera.X = Camera.MAX_X - half_screen_px
        else:
            Camera.X = hero_center - half_screen_px
        pyxel.camera(Camera.X, Camera.Y)



class App:
    def __init__(self):
        pyxel.init(
            width = SCREEN_WIDTH * TILE_SIZE,
            height = SCREEN_HEIGHT * TILE_SIZE,
            title = "Mwahahahahah"
        )

        # Import resources
        pyxel.load("resources.pyxres")

        # Init values
        self.ANIMATION_TICK = 0
        self.ANIMATION_DELAY = ANIMATION_DELAY
        self.ANIMATION_TYPE = "idle"

        # Run game
        pyxel.run(self.update, self.draw)

    def update(self):
        # Animate
        self.ANIMATION_DELAY -= 1
        if self.ANIMATION_DELAY < 0 : # +1 tick when delay is over
            
            self.ANIMATION_TICK += 1
            if self.ANIMATION_TICK > 1 : # If tick > 2, loop animation
                self.ANIMATION_TICK = 0
            self.ANIMATION_DELAY = ANIMATION_DELAY # Reset countdown

            # Animate heroes
            for hero in Heroes:
                hero.ANIM_TICK = self.ANIMATION_TICK

        # Move the characters left or right
        if pyxel.btn(pyxel.KEY_RIGHT):
            # Animate walk
            self.ANIMATION_TYPE = "walk"

            # Move only if not at the end of the map
            next_step = Hero_01.X + Hero_01.WIDTH + Hero_01.SPEED
            dungeon_end = Dungeon.WIDTH * TILE_SIZE - Hero_01.SPEED
            if next_step < dungeon_end:
                # Move heroes
                for hero in Heroes:
                    hero.X += hero.SPEED
        
        elif pyxel.btn(pyxel.KEY_LEFT):
            # Animate walk
            self.ANIMATION_TYPE = "walk"

            # Move only if not at the end of the map
            previous_step = Hero_04.X - Hero_04.SPEED
            dungeon_start = 0 + Hero_04.SPEED
            if previous_step > dungeon_start:
                # Move heroes
                for hero in Heroes:
                    hero.X -= hero.SPEED
        
        else:
            # Animate idle
            self.ANIMATION_TYPE = "idle"
    
        # Position camera
        Camera.follow(Hero_01.X)

    def draw(self):
        # Draw background
        pyxel.cls(0)

        # Draw tilemap
        pyxel.bltm(
            x = 0,
            y = 0,
            tm = 0,
            u = 0,
            v = 0,
            w = Dungeon.WIDTH * TILE_SIZE,
            h = Dungeon.HEIGHT * TILE_SIZE,
            colkey = 14
        )

        # Draw character
        for hero in Heroes:
            hero.draw(self.ANIMATION_TYPE)

        # Move the camera
        pyxel.camera()

        # ==============================================================
        # TODO:
        # Define characters and enemies battle position
        # Draw menu area (bottom of the screen)

App()