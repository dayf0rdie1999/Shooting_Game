import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Ellipse
from threading import Timer
from random import randint
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView
from MyPlayerDB import MyPlayerDB


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        mydb = MyPlayerDB()
        playerList = mydb.listPlayer()
        self.data = [{'text': x} for x in playerList]

class PlayerName_LB(Label):
    pass


class TI(TextInput):
    pass


class Start(Button):
    pass


class LB(Label):
    pass


class Tank(Widget):
    pass


class Monster(Widget):
    pass


class Bullet(Widget):
    pass

class Restart(Button):
    pass

class GameScreen(Widget):
    mydb = MyPlayerDB()
    movement_x_tank = 0
    movement_y_tank = 0
    tanks = []
    monsters = []
    bullets = []
    score = 0
    count = 0
    run = 0

    def new_game(self):
        to_be_removed = []
        for child in self.children:
            if isinstance(child, Tank):
                to_be_removed.append(child)
            if isinstance(child, Monster):
                to_be_removed.append(child)
            if isinstance(child, Bullet):
                to_be_removed.append(child)
        for child in to_be_removed:
            self.remove_widget(child)

        self.run = 0
        self.label = LB()
        self.add_widget(self.label)
        self.textinput = TI()
        self.add_widget(self.textinput)
        self.button = Start()
        self.add_widget(self.button)

        self.button.bind(on_press=self.Start_Game)
        self.score = 0
        self.tanks = []
        self.monsters = []
        self.bullets = []
        self.movement_x_tank = 0
        self.movement_y_tank = 0

        bullet = Bullet()
        self.bullets.append(bullet)
        self.add_widget(bullet)

        tank = Tank()
        self.tanks.append(tank)
        self.add_widget(tank)

        monster = Monster()
        self.monsters.append(monster)
        self.add_widget(monster)

    def on_touch_move(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]

        # moving left or right
        if abs(dx) > abs(dy):
            self.movement_y_tank = 0
            if dx > 0:
                self.movement_x_tank = self.step_size_tank
            else:
                self.movement_x_tank = - self.step_size_tank
        # Moving Up And Down
        else:
            pass

    def Start_Game(self, instance):
        self.score = 0
        self.score_widget.text = "Score: " + str(self.score)
        self.mydb.insertPlayer(playername=self.textinput.text)
        self.new_game()
        self.delete_Input_Widget()

    def delete_Input_Widget(self):
        to_be_removed = []
        for child in self.children:
            if isinstance(child, TI):
                to_be_removed.append(child)
            if isinstance(child, LB):
                to_be_removed.append(child)
            if isinstance(child, Start):
                to_be_removed.append(child)
            if isinstance(child,Restart):
                to_be_removed.append(child)
            if isinstance(child, RV):
                to_be_removed.append(child)
            if isinstance(child, PlayerName_LB):
                to_be_removed.append(child)

        for child in to_be_removed:
            self.remove_widget(child)

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

    def collides_Window(self, window, wid2):

        if window.right - wid2.width + 1 <= wid2.x:
            return False
        if window.x + wid2.width - 1 >= wid2.right:
            return False
        if window.top <= wid2.y:
            return False
        if window.y >= wid2.top:
            return False
        return True

    def Bullet_collides_Window(self, window, wid2):

        '''if window.right - 100 <= wid2.x:
            return False'''
        '''if window.x + 100 >= wid2.right:
            return False'''
        if window.top - 200 <= wid2.y:
            return False
        '''if window.y + 100 >= wid2.top:
            return False'''
        return True

    def create_Bullet(self):
        self.bullet = Bullet()
        self.bullet.x = self.current_x + 50
        self.bullet.y = self.current_y + 110

    def next_frame(self, dt):
        # Move the tank
        self.score_widget = self.ids.score_widget
        tank = self.tanks[0]

        self.current_x = tank.pos[0]
        self.current_y = tank.pos[1]
        self.step_size_tank = 500 * dt

        self.step_size_bullet_x = 400 * dt

        self.step_size_monster = 100 * dt
        # Response multiple monsters and move monsters
        for i, monster in enumerate(self.monsters):
            if i == 0:
                pass
            # current_x = monster.pos[0]
            # current_y = monster.pos[1]
            monster.y += - self.step_size_monster

        # move the bullet
        for i, bullet in enumerate(self.bullets):
            if i == 0:
                pass
            bullet.y += self.step_size_bullet_x

        # Colliding the monster
        for monster_widget in self.monsters:
            if self.collides_widget(monster_widget, tank):
                self.mydb.updateScore(self.score, 0)
                self.run += 1
                self.leaderBoard_Widget(self.run)
                self.remove_widget(tank)


        # Tank Colliding with the frame
        if self.collides_Window(self, tank):
            tank.x += self.movement_x_tank
            tank.y += self.movement_y_tank

        if not self.collides_Window(self, tank):
            tank.x -= self.movement_x_tank

        # Recreate Bullets
        if not self.Bullet_collides_Window(self, bullet):
            bullet = Bullet()
            bullet.x = self.current_x + 50
            bullet.y = self.current_y + 110
            self.bullets.append(bullet)
            self.add_widget(bullet)

        for monster_widget in self.monsters:
            if self.collides_widget(bullet, monster_widget):
                self.score += 1
                self.count += 1
                self.score_widget.text = "Score: " + str(self.score)
                self.monsters.remove(monster_widget)
                self.remove_widget(monster_widget)
                newMonster = Monster()
                newMonster.y = randint(Window.top - 10, Window.top)
                newMonster.x = randint(newMonster.width, Window.width - newMonster.width)
                self.monsters.append(newMonster)
                self.add_widget(newMonster)

        if self.count == 5:
            self.count = 0
            newMonster = Monster()
            newMonster.y = randint(Window.top - 10, Window.top)
            newMonster.x = randint(newMonster.width, Window.width - newMonster.width)
            self.monsters.append(newMonster)
            self.add_widget(newMonster)

        # Monster Colliding with the frame
        for monster_widget in self.monsters:
            if not self.collides_widget(self, monster_widget):
                self.score -= 1
                self.count -= 1
                self.score_widget.text = "Score: " + str(self.score)
                self.monsters.remove(monster_widget)
                self.remove_widget(monster_widget)
                newMonster = Monster()
                newMonster.y = randint(Window.top - 10, Window.top)
                newMonster.x = randint(newMonster.width, Window.width - newMonster.width)
                self.monsters.append(newMonster)
                self.add_widget(newMonster)

    def restart_Game(self, instance):
        self.delete_Input_Widget()
        self.new_game()

    def leaderBoard_Widget(self, run):
        if run == 1:
            self.count = 0
            self.score = 0
            self.score_widget.text = "Score: " + str(self.score)
            PlayerBoard = PlayerName_LB()
            RVplayer = RV()
            Button_Restart = Restart()
            self.add_widget(Button_Restart)
            self.add_widget(PlayerBoard)
            self.add_widget(RVplayer)
            Button_Restart.bind (on_press= self.restart_Game)


class mainApp(App):
    def on_start(self):
        self.root.new_game()
        Clock.schedule_interval(self.root.next_frame, 0)

    pass


if __name__ == "__main__":
    mainApp().run()
