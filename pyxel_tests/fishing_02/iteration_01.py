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
          self.Y = TILE_SIZE * 3

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
          self.cursor_speed = 2

          # Animation - pull
          self.animate_pull = -1
          self.animate_pull_speeds = [2, 4, 6, 5, 4, 3, 2, 1, 0, 0, -1]

          # Run game
          pyxel.run(self.update, self. draw)


     def update(self):

          # Pull the fish by pressing SPACE
          if self.animate_pull < 0 and pyxel.btnp(pyxel.KEY_SPACE):
               self.animate_pull = 0

          # If animate_pull >= 0, play pulling animation instead
          elif self.animate_pull >= 0:

               # Get pull animtion speed for this frame
               speed = self.animate_pull_speeds[self.animate_pull]

               # Check if the next movement = collision
               cursor_xmax = self.cursor_x + self.cursor_size
               next_position = cursor_xmax + speed

               # If next movement is inside mini-game frame, move
               if next_position < self.frame_xmax:
                    self.cursor_x += speed
               
               # Else, if we do not touch the frame border, close the gap
               elif cursor_xmax < self.frame_xmax - 1:
                    self.cursor_x = self.frame_xmax - 1 - self.cursor_size
               
               # Increment animation frame count
               if self.animate_pull < len(self.animate_pull_speeds) - 1:
                    self.animate_pull += 1
               
               # Else, the animation is over
               else:
                    self.animate_pull = -1


          # If not pulling, the fish moves to the left
          else:

               # Check if next movement = collision
               next_position = self.cursor_x - self.cursor_speed

               # If next movement is inside frame, move
               if next_position > self.frame_xmin:
                    self.cursor_x -= self.cursor_speed
               
               # Else, if we do not touch the frame border, close the gap
               elif self.cursor_x > self.frame_xmin + 1:
                    self.cursor_x = self.frame_xmin +1
     

     def draw(self):

          # Draw bg
          pyxel.cls(0)

          # # Draw frame bg
          # pyxel.rect(
          #      x = self.frame_xmin,
          #      y = self.Y,
          #      w = self.frame_size,
          #      h = TILE_SIZE,
          #      col = 10
          # )

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



App()