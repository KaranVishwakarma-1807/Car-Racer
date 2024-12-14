#importing all the required libraries
import pygame
import time
import math
import os
# import util   -> method_1 for importing a function
from util import scale_images, rotate, blit_text_center  #->method_2 for importing a function
pygame.font.init() #to initialise the font funtion


#loading all the images
GRASS = scale_images(pygame.image.load(os.path.join("./Version 0","Resources","grass.jpg")), 1.8) #-> method_1 of scaling

ICON = pygame.image.load(os.path.join("./Version 0","Resources","icon.png"))

GREEN_CAR = pygame.image.load(os.path.join("./Version 0","Resources","green-car.png"))
GREY_CAR = pygame.image.load(os.path.join("./Version 0","Resources","grey-car.png"))
PURPLE_CAR = pygame.image.load(os.path.join("./Version 0","Resources","purple-car.png"))
WHITE_CAR = scale_images(pygame.image.load(os.path.join("./Version 0","Resources","white-car.png")), 0.4)
RED_CAR = scale_images(pygame.image.load(os.path.join("./Version 0","Resources","red-car.png")), 0.4)

TRACK_BORDER = scale_images(pygame.image.load(os.path.join("./Version 0","Resources","track-border.png")), 0.73)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)  #creating a mask
TRACK = scale_images(pygame.image.load(os.path.join("./Version 0","Resources","track.png")), 0.73)

FINISH = scale_images(pygame.image.load(os.path.join("./Version 0","Resources","finish.png")), 0.8)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (110, 190)


#making font for the main window
MAIN_FONT = pygame.font.SysFont("comicsans", 30 )


#creating the display window
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH-100, HEIGHT-100))
pygame.display.set_caption("Car Racer")
pygame.display.set_icon(ICON)



#creating a class that contians all the class info
class GameInfo:
    LEVELS = 10 #total number of levels

    #defining the initial variables
    def __init__(self, level = 1):
        self.level = level #indicates the current level
        self.started = False #indicates wether the level has started or not
        self.level_start_time = 0 #indicates the time ellapsed from the time started

    #defining 'next level' method
    def next_level(self):
        self.level += 1  #increase the level by 1
        self.started = False #we want user to start the level

    #defining 'reset' method to reset everything
    def reset(self):
        self.level = 1 #reset the level to 1
        self.started = False #reset the start_value to false for the  user to start
        self.level_start_time = 0 #resets the start_time

    #defining the 'game finished' method
    def game_finished(self):
        return self.level > self.LEVELS #when the level is greater than the no of levels then it will reset the game

    #defining the 'start level' method
    def start_level(self):
        self.started = True #indicates that the level has started
        self.level_start_time = time.time()  #to keep the track of time after the level has started

    #defining the 'get level time' method
    def get_level_time(self):
        if not self.started:
            return 0  #if not started returns false
        else:
            return round(time.time()- self.level_start_time) #returns the current time
        
 

#making an abstract class for all the cars
class AbstractCars:
    #define of the initial variables
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG #image of the car
        self.max_vel = max_vel #maximum velocity of the car
        self.vel = 0  #initial velocity of the car
        self.rotation_vel = rotation_vel  #rotational velocity of the car
        self.angle = 0 #rotational angle of the car
        self.x, self.y = self.START_POS #initial position of the car
        self.acceleration = 0.1  #acceleration of the car

    #function for rotational movement
    def  rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    #function to draw the rotation of the car
    def draw(self, win):
        rotate(win, self.img, (self.x, self.y), self.angle )

    #function to increase the acceleration
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    #function to move backwards
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()
    
    #function to move the car
    def move(self):
        radians = math.radians(self.angle) #converting the angle into radians
        vertical = math.cos(radians) * self.vel #calculating vertical velocity of the car
        horizontal = math.sin(radians) * self.vel  #calculating horizontal velocity of the car
        #moving the car
        self.y -= vertical
        self.x -= horizontal

    #function for the collision
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)  #creating a mask for the car
        offset = (int(self.x - x), int(self.y - y))  #calculating the offset
        #point of intersection
        poi = mask.overlap(car_mask, offset)  #checking for collision
        return poi
    
    #function to reset the car after finishing the track
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0 




#creating a new class for the car
class PlayerCar(AbstractCars):
    IMG = WHITE_CAR
    START_POS = (150,160)

    #function to deaccelerate the car
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()

    #function to bounce the player car back if collided  with the border
    def bounce(self):
        self.vel = -self.vel #reverse the velocity of the car
        self.move()



#creating a computer car
class ComputerCar(AbstractCars):
    IMG = RED_CAR
    START_POS = (120,160)
    #override the initialisation
    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)  #uses the parent class's initialisation
        self.path = path #path of the computer car
        self.current_point = 0  #to know the current position of the computer car
        self.vel = max_vel #computer car moves at the same velocity i.e., maximum velocity 
         
    #funtion to draw all the point on the path for the computer car     
    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255,0,0), point, 5)

    #overriding the draw function
    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    #function to calculate the angle
    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point] #get the target point
        x_diff = target_x - self.x #calculate the difference in x
        y_diff = target_y - self.y #calculate the difference in y
        #to manually calculate the angle using the arctan function
        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)
        #making claue
        if target_y > self.y:
            desired_radian_angle += math.pi
        #calculating difference in angle to determine the direction for the car
        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360
        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    #function to update the point for the computer car
    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1 

    #function for path following
    def move(self):
        if self.current_point >= len(self.path): # if the computer car has reached the end of the path
            return
        #calculate the angle and shift the car to that angle
        self.calculate_angle()
        #checks if need to move to the next point on the path
        self.update_path_point()
        super().move() #for the movement of the computer car

    #function to increase the speed of computer of the after each level
    def next_level(self, level):
        self.reset() #to reset the positon and the velocity
        self.vel = self.max_vel + (level - 1) * 0.2 #increase the speed of the comp car but max will we be always 0.2 less then player car
        self.current_point = 0




#defining a draw funtion to draw the images
def draw(win, images, player_car, computer_car, game_info):
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(f"Level: {game_info.level}", 1, (255,255,255)) #to display the level number
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 200))

    time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}s", 1, (255,255,255)) #to display the time
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 150))

    vel_text = MAIN_FONT.render(f"Speed: {round(player_car.vel, 1)}px/s", 1, (255,255,255)) #to display the velocity
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 100))

    player_car.draw(win) #draw the player car
    computer_car.draw(win) #draw the computer car
    pygame.display.update() #update the window 





#defining a funtion for the movement of the player car
def move_player(player_car):
    #movement of the player car
    key = pygame.key.get_pressed()
    moved = False
    if key[pygame.K_LEFT]:
        player_car.rotate(left=True)  #left
    if key[pygame.K_RIGHT]:
        player_car.rotate(right=True)  #right
    if key[pygame.K_UP]:
        moved = True
        player_car.move_forward()  #forwards
    if key[pygame.K_DOWN]:
        moved = True 
        player_car.move_backward()  #backwards 
    if not moved:
        player_car.reduce_speed()  #deaccelerate the car if not moving





def handle_collision(player_car, computer_car, game_info):
    #checking if the player collided with the track border
    if player_car.collide(TRACK_BORDER_MASK) != None:
        # print("Collision detected")
        player_car.bounce()

    #checking if the computer collided with the finish line
    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)  # '*' - unpacks the tuple
    if computer_finish_poi_collide != None: 
        blit_text_center(WIN, MAIN_FONT, "You lost!") #shows the text when player loses
        pygame.display.update()
        pygame.time.wait(5000) #delay the game for 5 seconds
        game_info.reset()
        computer_car.reset()
        player_car.reset()
        # print("Computer car has finished the race")
    
    #checking if the player collided with the finish line
    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)  # '*' - unpacks the tuple
    if player_finish_poi_collide != None:  
        # print(finish_poi_collide)
        if  player_finish_poi_collide[1] == 0:  #checking if the car collided backwards
            player_car.bounce()
        else:
            game_info.next_level()
            #when player wins
            blit_text_center(WIN, MAIN_FONT, "You WON!") #shows the text when player wins
            pygame.display.update()
            pygame.time.wait(2500) #delay the game for 2.5 seconds
            computer_car.reset()
            player_car.reset()
            computer_car.next_level(game_info.level)
            # print("You won!")




#defining varialbes
FPS = 60 #run the game at 60 frames per second

PATH = [(137, 109), (91, 58), (47, 108), (56, 388), (271, 597), (321, 542), (338, 428), (406, 383), (480, 448), (493, 583), (587, 578), (587, 331), (507, 292), (345, 283), (354, 215), (564, 209), (599, 94), (470, 55), (251, 63), (219, 302), (148, 303), (146, 197)]  #coordinates for the computer car path

run = True #while the game is running

clock = pygame.time.Clock() #to control the frame rate

#list of the images
images = [(GRASS,(0,0)) ,(TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]

#creating a player car
player_car = PlayerCar(4,4) #<-speed of the car
computer_car = ComputerCar(1,3, PATH) #<-speed of the computer car

#creating a varible to store the all the game info
game_info = GameInfo()


#creating an main event loop
while run:
    clock.tick(FPS) #runs the game at 60 frames per second

    #to draw the image on the screen
    draw(WIN, images, player_car, computer_car, game_info)

    #making another loop to pop up before the game starts
    while not game_info.started:
        blit_text_center(WIN, MAIN_FONT, f"Press any to Start the Level {game_info.level}...") #using f string to ambed the level number
        pygame.display.update()
        #stating level/main menu event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #if the user closes the window
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:  #if the user presses any key
                game_info.start_level()

    #loop to keep the window alive
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  #if the user closes the window
            run = False
            break

        # to get the path coordinated for the computer car
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     computer_car.path.append(pos)
    
    #calling the function to move the player car
    move_player(player_car)
    #calling the function to move the computer car
    computer_car.move() 

    handle_collision(player_car, computer_car, game_info)

# print(computer_car.path)

pygame.quit()