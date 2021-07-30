import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window


class SnakePart(Widget):
    pass


class GameScreen(Widget):
    # Setting the how far the snake moves
    step_size = 40

    # Initializing the movement
    movement_x = 0
    movement_y = 0

    # Creating a list of snake parts to track the parts correctly
    snake_parts = []
    
    def new_game(self):
        # Removing everything except food in the game
        to_be_removed = []
        for child in self.children:
            if isinstance(child, SnakePart):
                to_be_removed.append(child)
        for child in to_be_removed:
            self.remove_widget(child)

        self.snake_parts = []
        self.movement_x = 0
        self.movement_y = 0
        head = SnakePart()
        head.pos = (0, 0)
        self.snake_parts.append(head)
        self.add_widget(head)



    def on_touch_up(self, touch):
        # Reading the change in x and the change in y and determine which direction it is going. Very interesting
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]

        # moving left or right
        if abs(dx) > abs(dy):
            self.movement_y = 0
            if dx > 0:
                self.movement_x = self.step_size
            else:
                self.movement_x = - self.step_size
        else:
            self.movement_x = 0
            if dy > 0:
                self.movement_y = self.step_size
            else:
                self.movement_y = - self.step_size

    # Rewritten the entire method of collide_widget method from collide one widget into 2 widget together
    def collides_widget(self, wid1, wid2):
        if wid1.right <= wid2.x:
            return False
        if wid1.x >= wid2.right:
            return False
        if wid1.top <= wid2.y:
            return False
        if wid1.y >= wid2.top:
            return False
        return True

    def next_frame(self, *args):
        food = self.ids.food
        head = self.snake_parts[0]

        # get the position of the previous part of the snake
        last_x = self.snake_parts[-1].x
        last_y = self.snake_parts[-1].y

        # Make the body move
        for i, part in enumerate(self.snake_parts):
            if i == 0:
                continue
            part.new_y = self.snake_parts[i-1].y
            part.new_x = self.snake_parts[i-1].x

        for part in self.snake_parts[1:]:
            part.y = part.new_y
            part.x = part.new_x

        # Make the head move
        head.x += self.movement_x
        head.y += self.movement_y


        # Checking the snake if colliding to the food
        if self.collides_widget(head, food):
            # Generating food at random location
            food.x = randint(0, Window.width - food.width)
            food.y = randint(0, Window.height - food.height)

            # Creating a new snake part that will generate the same position of the previous snake part
            new_part = SnakePart()
            new_part.x = last_x
            new_part.y = last_y
            self.snake_parts.append(new_part)
            self.add_widget(new_part)

        # Checking the snake if colliding to the wall
        for part in self.snake_parts[1:]:
            if self.collides_widget(part, head):
                self.new_game()

        # Checking the snake if colliding to its body
        if not self.collides_widget(self, head):
            self.new_game()
        pass


class SnakeApp(App):
    def on_start(self):
        # Creating a new game
        self.root.new_game()
        # Every 0.2 second, refresh the frame
        Clock.schedule_interval(self.root.next_frame, .2)


if __name__ == "__main__":
    SnakeApp().run()
