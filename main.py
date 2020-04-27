from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.properties import ListProperty, NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import WindowBase, Window
from kivy.lang import Builder
 
from libdw import sm

from time import sleep

class Velocity_sm(sm.SM):
	def __init__(self, velocity):
		super(Velocity_sm, self).__init__()
		self.velocity = velocity
		
	start_state = 1
	
	def get_next_value(self, state, inp):
		next_state = state + 1
		output = inp * (1 + 1.0 / next_state)
		return next_state, output

class MainGame(Widget):
	v = Velocity_sm(3)
	v.start()
	lvl = NumericProperty(v.state)
	
	label = ObjectProperty(None)
	ball = ObjectProperty(None)
	ball = ObjectProperty(None)
	paddle = ObjectProperty(None)
	button = ObjectProperty(None)
	box1 = ObjectProperty(None)
	box2 = ObjectProperty(None)
		
	rect1 = ObjectProperty(None)
	rect2 = ObjectProperty(None)
	rect3 = ObjectProperty(None)
	rect4 = ObjectProperty(None)
	rect5 = ObjectProperty(None)
	rect6 = ObjectProperty(None)
	rect7 = ObjectProperty(None)
	rect8 = ObjectProperty(None)
	rect9 = ObjectProperty(None)
	rect10 = ObjectProperty(None)
	rect11 = ObjectProperty(None)
	rect12 = ObjectProperty(None)
	rect13 = ObjectProperty(None)
	rect14 = ObjectProperty(None)
	rect15 = ObjectProperty(None)

	# on_click callback of the button
	def toggle(self):
		if self.ball.velocity != Vector(0, 0):
			self.ball.center = self.center[0], self.center[1] + 60
			self.stop()
		else:
			self.start()
			
	def stop(self):
		self.ball.velocity = Vector(0, 0)
		
		rectlist = [self.rect1, self.rect2, self.rect3, self.rect4, self.rect5, self.rect6, self.rect7, self.rect8, self.rect9, self.rect10, self.rect11, self.rect12, self.rect13, self.rect14, self.rect15]
		for rect in rectlist:
			rect.reset()

		self.button.text = "START"
		self.button.background_color = (0.1, 1, 0, 0.9)
		
	def start(self):
		self.paddle.center_x = self.center_x
		self.ball.velocity = Vector(0, -1 * self.v.velocity)
		self.button.text = "STOP"
		self.label.color = (1,1,1,1)
		self.label.text = "Level: " + str(self.v.state)
		self.button.background_color = (1, 0, 0, 0.6)
	
	def update(self, dt):
			if Window.size != (1000, 900):
				Window.size = (1000, 900)
			
			self.ball.move()
			self.paddle.bounce_ball(self.ball)
			
			rectlist = [self.rect1, self.rect2, self.rect3, self.rect4, self.rect5, self.rect6, self.rect7, self.rect8, self.rect9, self.rect10, self.rect11, self.rect12, self.rect13, self.rect14, self.rect15]
			counter = 0
			
			# loop to check if targets are hit, if not proceed with bounce_ball function
			for i in range(len(rectlist)):
				if rectlist[i].bounce == 0:
					rectlist[i].bounce_ball(self.ball)
				else:
					counter += 1
					
			# every targets are hit, enter the next level
			if counter == i + 1:
				self.ball.center = self.center[0], self.center[1] + 60
				self.stop()
				self.label.text = "LEVEL PASSED!"
				self.label.color = (0,1,0,1)
				
				self.v.state, self.v.velocity = self.v.get_next_value(self.v.state, self.v.velocity)
			
			# hit top, add y velocity as penalty
			if self.ball.top >= self.height - 5:
				self.ball.velocity_y *= -1 
				self.ball.velocity_y -=  0.3 * self.v.state**0.5
			
			# hit left or right
			if (self.ball.x <= 5) or (self.ball.right >= self.width - 5):
				self.ball.velocity_x *= -1
			
			# hit bottom bar, game over, reset level
			if self.ball.y <= 160:
				self.label.text = "GAME OVER"
				self.label.color = (1,0,0,0.9)
				self.v = Velocity_sm(3)
				self.v.start()
				
				self.ball.move()
				sleep(0.2)
				self.ball.center = self.center[0], self.center[1] + 60
				self.stop()
				
	def on_touch_move(self, touch):
			if touch.y < self.height / 2 + 160 and touch.y >= 130:
				self.paddle.center_x = touch.x
				
class StartButton(Button):
	pass

# blank space between the targets
class Spacing(Widget):
	pass

class Paddle(Widget):
	def bounce_ball(self, ball):
		if self.collide_widget(ball):
			vx, vy = ball.velocity
			offset = (ball.center_x - self.center_x) / (self.width / 10.0)
			
			bounced = Vector(vx, vy * -1)
			ball.velocity = (bounced.x + offset) * 1.1, bounced.y * 1.03

class Rect(Widget):
	bounce = 0
	
	def reset(self):
		self.bounce = 0
		with self.canvas:
			Color(1, 1, 0)
			Rectangle(pos=self.pos, size=self.size)

	def bounce_ball(self, ball):
		if self.collide_widget(ball):
			self.bounce += 1
			
			vx, vy = ball.velocity
			offset = (ball.center_x - self.center_x) / self.width
			bounced = Vector(vx, vy * -1)
			vel = bounced * 1.03
			ball.velocity = vel.x + offset, vel.y
			
			with self.canvas:
				Color(0, 0, 0)
				Rectangle(pos=self.pos, size=self.size)


class Ball(Widget):
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def move(self):
		self.pos = Vector(*self.velocity) + self.pos 

class MainApp(App):
	def build(self):
		
		Builder.load_string("""
<WindowBase>:
	minimum_height: 1000
	minimum_width: 900

<MainGame>:    
	canvas:
		Color:
			rgb: 1, 0, 0
		Rectangle:
			pos: 0, 155
			size: self.width, 5
		Color:
			rgb:  0, 1, 0.7
		Rectangle:
			pos: 0, 0
			size: 5, self.height
		Color:
			rgb:  0, 1, 0.7
		Rectangle:
			pos: root.width - 5, 0
			size: 5, self.height
		Color:
			rgb:  1, 0.7, 0
		Rectangle:
			pos: 0, self.height - 5
			size: self.width, 5
		Color:
			rgb: 1, 1, 1
		Rectangle:
			pos: 0, 130
			size: self.width, 25
			source: './assets/arrow.png'
		Color:
			rgb: 0.2, 0.25, 0.25
		Rectangle:
			pos: 0, 0
			size: self.width, 130
	
	ball: ball
	paddle: paddle
	button: button
	label: label
	box1: box1
	box2: box2
	rect1: rect1
	rect2: rect2
	rect3: rect3
	rect4: rect4
	rect5: rect5
	rect6: rect6
	rect7: rect7
	rect8: rect8
	rect9: rect9
	rect10: rect10
	rect11: rect11
	rect12: rect12
	rect13: rect13
	rect14: rect14
	rect15: rect15

	Paddle:
		id: paddle
		size: root.width / 8.0, root.height / 20.0
		center_x: root.center_x - 81
		y: root.y + 160
		
			
	Label:
		id: label
		font_size: root.width * 0.05  
		center_x: root.width / 4
		top: root.top - root.height + 120
		text: "Level: " + str(root.lvl)
	
	StartButton:
		id: button
		font_size: root.width * 0.05
		x: root.width *  0.6
		top: 100
		text: "START"
		size: root.width / 4.0, 130
		background_color: 0.1, 1, 0, 0.6
		on_press: root.toggle()
		
	BoxLayout:
		id: box1
		top: root.top

		Rect:
			id: rect1
		Spacing:
		Rect:
			id: rect2
		Spacing:
		Rect:
			id: rect3
		Spacing:
		Rect:
			id: rect4
		Spacing:
		Rect:
			id: rect5
		Spacing:
		Rect:
			id: rect6
		Spacing:
		Rect:
			id: rect7
		Spacing:
		Rect:
			id: rect8
		
	BoxLayout:
		id: box2
		top: root.top - 50

		Spacing:
		Rect:
			id: rect9 
		Spacing:
		Rect:
			id: rect10
		Spacing:
		Rect: 
			id: rect11
		Spacing:
		Rect: 
			id: rect12
		Spacing:
		Rect: 
			id: rect13
		Spacing:
		Rect: 
			id: rect14
		Spacing:
		Rect: 
			id: rect15
		Spacing:
		
	Ball:
		id: ball
		center: self.parent.center

<Ball>:
	size: 50, 50
	canvas:
		Color:
			rgb: 1, 0, 1
		Ellipse:
			pos: self.pos
			size: self.size
			
<Paddle>:
	canvas:
		Color:
			rgb: 1, 1, 1
		Rectangle:
			pos:self.pos
			size:self.size
			source: './assets/paddle.png'
			
<Rect>:
	top: self.parent.top - 5
	size:  self.parent.width / 8.0, 40
	canvas:
		Color:
			rgb: 1, 1, 0
		Rectangle:
			pos:self.pos
			size:self.size

<Spacing>:
	top: self.parent.top - 5
	size: self.parent.width / 8.0, 40
	size_hint_x: 0.5
	canvas:
		Color:
			rgb: 0, 0, 0
		Rectangle:
			pos:self.pos
			size:self.size
			
<BoxLayout>:
	orientation: 'horizontal'
	padding: 5
	center_x: root.center_x
	size: self.parent.width, 50
		""")
		
		game = MainGame()
		
		game.box1.width = 1400
		game.box2.width = 1400
		game.ball.center = game.center[0], game.center[1] + 180
		game.paddle.center_x = game.center_x
		Clock.schedule_interval(game.update, 1 / 64.0)
		
		return game
	
if __name__ == '__main__':

	Window.size = (1000,900)
	
	app = MainApp()
	app.run()