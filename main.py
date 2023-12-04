import machine, neopixel, time, random

# Config: Pin Assignment
vcc_pin = 0                 # VCC pin
din_pin = 1                 # DIN pin, data input for the NeoPixel strip
up_button_pin = 6           # Button (momentary push button)
down_button_pin = 7         # Button (momentary push button)
left_button_pin = 8         # Button (momentary push button)
right_button_pin = 9        # Button (momentary push button)

# Config: Game Settings
speed = 0.5                 # Snake speed (seconds per move)
snake_color = (0, 20, 0)    # Snake color (RGB), green by default
fruit_color = (20, 0, 0)    # Fruit color (RGB), red by default

# Config: Canvas Settings
canvas_width = 5            # Canvas height
canvas_height = 5           # Canvas width


# Matrix class by gandro
class Matrix:
    def __init__(self, pin, width, height):
        self.np = neopixel.NeoPixel(pin, width * height)
        self.w = width
        self.h = height

    def width(self):
        return self.w

    def height(self):
        return self.h

    def pixel(self, x, y, c):
        self.np[(self.w * self.h - 1) - (x + y * self.h)] = c

    def draw(self):
        self.np.write()

# Some simple snake game
class snake:
    def __init__(self, matrix):
        self.matrix = matrix
        self.snake = [(0, 2)]  # Snake starting position
        self.food = None
        self.direction = (1, 0)  # Initial direction: right

    def draw_snake(self):
        for x, y in self.snake:
            self.matrix.pixel(x, y, snake_color)

    def draw_food(self):
        # prevent the food from spawning on the snake
        while not self.food or self.food in self.snake:
            self.food = (random.randint(0, self.matrix.width() - 1), random.randint(0, self.matrix.height() - 1))
        x, y = self.food
        self.matrix.pixel(x, y, fruit_color)

    def move_snake(self):
        head_x, head_y = self.snake[-1]
        dx, dy = self.direction
        new_head = ((head_x + dx) % self.matrix.width(), (head_y + dy) % self.matrix.height())
        self.snake.append(new_head)

        # Check if the snake eats the food
        if self.food and new_head == self.food:
            self.food = None
        else:
            # Remove the tail of the snake if it doesn't eat the food
            self.snake.pop(0)

    def update_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):  # Prevent the snake from reversing its direction
            self.direction = (dx, dy)

    def check_collision(self):
        head_x, head_y = self.snake[-1]
        # Check if the snake hits the boundaries or collides with itself
        # Boundaries disabled for the small canvas
        if head_x < 0 or head_x >= self.matrix.width() or head_y < 0 or head_y >= self.matrix.height() or len(set(self.snake)) != len(self.snake):
            self.game_over_animation()
            return True
        return False

    def game_over_animation(self):
        # EPIC Game Over Animation
        for _ in range(3):  # Repeat the animation 3 x 4 times
            for _ in range(4):
                self.clear_canvas()
                canvas.draw()
                time.sleep(0.05)

                for x in range(self.matrix.width()):
                    for y in range(self.matrix.height()):
                        if (x, y) not in self.snake:  # Fill the rest of the canvas with flashy flashes
                            self.matrix.pixel(x, y, (random.randint(0, 30), 0, 0))
                self.draw_snake()
                canvas.draw()
                time.sleep(0.05)

            time.sleep(0.1)

    def clear_canvas(self):
        for x in range(self.matrix.width()):
            for y in range(self.matrix.height()):
                self.matrix.pixel(x, y, (0, 0, 0))

# Prepare pins, pixels and canvas
vcc = machine.Pin(vcc_pin, machine.Pin.OUT)
din = machine.Pin(din_pin, machine.Pin.OUT)
np = neopixel.NeoPixel(din, canvas_width*canvas_height)
vcc.on()
canvas = Matrix(din, canvas_width, canvas_height)

# Create an instance of the snake game
game = snake(canvas)

def up_button_pressed(pin):
    game.update_direction(0, -1) # Move up

def down_button_pressed(pin):
    game.update_direction(0, 1)  # Move down

def left_button_pressed(pin):
    game.update_direction(-1, 0) # Move left

def right_button_pressed(pin):
    game.update_direction(1, 0)  # Move right

# GPIO pins as inputs w/ pull-up
up_button = machine.Pin(up_button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
down_button = machine.Pin(down_button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
left_button = machine.Pin(left_button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
right_button = machine.Pin(right_button_pin, machine.Pin.IN, machine.Pin.PULL_UP)

# Interrupts for button presses
up_button.irq(up_button_pressed, machine.Pin.IRQ_FALLING)
down_button.irq(down_button_pressed, machine.Pin.IRQ_FALLING)
left_button.irq(left_button_pressed, machine.Pin.IRQ_FALLING)
right_button.irq(right_button_pressed, machine.Pin.IRQ_FALLING)

# Game loop
while True:
    # Clear the canvas and draw the snake and food
    for x in range(canvas.width()):
        for y in range(canvas.height()):
            canvas.pixel(x, y, (0, 0, 0))

    game.draw_snake()
    game.draw_food()
    canvas.draw()

    # Move the snake
    game.move_snake()

    # Check for collisions
    if game.check_collision():
        time.sleep(1)

        # Game state reset
        game.snake = [(0, 2)]
        game.food = None
        game.direction = (1, 0)

    # Snake speed
    time.sleep(speed)