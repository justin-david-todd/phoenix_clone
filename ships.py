# Author: Justin David Todd
# Last Modified: 02/04/2021
# Description: Imports assets for and defines Player and Enemy Ships.
import pygame
import random
from lasers import collide, Laser


class Ship:
    """
    Abstract class for objects piloting through space
    """

    def __init__(self, x, y, laser_array, health=10):
        """
        creates a ship at the x, y coordinate with
        - a ship image
        - a health total
        - a maximum health limit
        - a laser type
        - a collection of lasers fired
        - a laser cool_down_counter
        _ a movement speed
        """
        self._image = {
            # Player Images - image file should be 64x64 pixels
            "main_ship": pygame.image.load("assets/main_ship.png"),

            # Enemy Images - image file should be 32x32 pixels
            # TODO diversify enemy images
            "blue_baddy": pygame.image.load("assets/baddy_1.png"),
            "red_baddy": pygame.image.load("assets/baddy_2.png"),
            "explosion": pygame.image.load("assets/simple_explosion.png"),
            "ArrowBlue": pygame.image.load("assets/ArrowBlue.png"),
            "ArrowGold": pygame.image.load("assets/ArrowGold.png"),
            "ArrowPink": pygame.image.load("assets/ArrowPink.png"),
            "ArrowRed": pygame.image.load("assets/ArrowRed.png"),
            "ArrowStealth": pygame.image.load("assets/ArrowStealth.png"),
            "Block": pygame.image.load("assets/Block.png"),
            "BlueSquid": pygame.image.load("assets/BlueSquid.png"),
            "blueSpark": pygame.image.load("assets/blusSpark.png"),
            "CentiBlue": pygame.image.load("assets/CentiBlue.png"),
            "CentiGreen": pygame.image.load("assets/CentiGreen.png"),
            "CentiheadBlue": pygame.image.load("assets/CentiheadBlue.png"),
            "CentiheadDud": pygame.image.load("assets/CentiheadDud.png"),
            "CentiheadGreen": pygame.image.load("assets/CentiheadGreen.png"),
            "CentiheadPanda": pygame.image.load("assets/CentiheadPanda.png"),
            "CentiheadRed": pygame.image.load("assets/CentiheadRed.png"),
            "CentiheadYellow": pygame.image.load("assets/CentiheadYellow.png"),
            "CentiPurple": pygame.image.load("assets/CentiPurple.png"),
            "CentiRed": pygame.image.load("assets/CentiRed.png"),
            "FlappyBlue": pygame.image.load("assets/Flappy Blue.png"),
            "FlappyGreen": pygame.image.load("assets/FlappyGreen.png"),
            "FlappyRed": pygame.image.load("assets/FlappyRed.png"),
            "FlappyStealth": pygame.image.load("assets/FlappyStealth.png"),
            "FlappyWhite": pygame.image.load("assets/FlappyWhite.png"),
            "GreenSpark": pygame.image.load("assets/GreenSpark.png"),
            "hammer": pygame.image.load("assets/hammer.png"),
            "metal_1": pygame.image.load("assets/metal_1.png"),
            "MetalSquid": pygame.image.load("assets/MetalSquid.png"),
            "RedMetalSquid": pygame.image.load("assets/RedMetalSquid.png")
        }
        self._x = x
        self._y = y
        self._ship_img = None
        self._mask = None
        self._health = health
        self._max_health = health
        self._laser_type = None
        self._cool_down_counter = 0
        self._speed = 5
        self._lasers = laser_array

        # counter and direction indicator for timing automated movement patterns
        self._move_counter = 0
        self._direction = 0

        # dimensions of screen ships are flying on.
        self._scr_width = 800
        self._scr_height = 800

    # Get Methods
    def get_x(self):
        """returns value of ship's x coordinate"""
        return self._x

    def get_y(self):
        """returns value of ship's y coordinate"""
        return self._y

    def get_health(self):
        """returns value of ship's current health"""
        return self._health

    def get_max_health(self):
        """returns value of ship's maximum health"""
        return self._max_health

    def get_speed(self):
        """returns value of ship's speed0"""
        return self._speed

    def get_cool_down_counter(self):
        """returns current value of ship's cool_down_counter"""
        return self._cool_down_counter

    def get_laser_type(self):
        """returns ship's laser type"""
        return self._laser_type

    def get_mask(self):
        """returns the ship's image mask"""
        return self._mask

    def get_width(self):
        """returns width of ship image"""
        return self._ship_img.get_width()

    def get_height(self):
        """returns width of ship image"""
        return self._ship_img.get_height()

    # Set Methods
    def set_x(self, num):
        """takes a number and sets the x coordinate to that value"""
        self._x = num

    def set_y(self, num):
        """takes a number and sets the y coordinate to that value"""
        self._y = num

    def set_health(self, num):
        """takes a number, sets current health to that number if within max_health"""
        if num <= self._max_health:
            self._health = num

    def set_window(self, width, height):
        """Two pixel values, width and height, and informs ship of window dimensions"""
        self._scr_width = width
        self._scr_height = height

    def set_laser_type(self, laser_type):
        """
        takes a laser type
        change's ship's laser type to the specified type (string)
        """
        self._laser_type = laser_type

    # Other Methods
    def recover_health(self, num):
        """
        takes a number and adds it to health value
        if sum is greater than max health, sets it to max health
        """
        self._health += num
        if self._health > self._max_health:
            self._health = self._max_health

    def deplete_health(self, num):
        """takes a number and reduces health by that number"""
        self._health -= num
        if self._health < 0:
            self._health = 0

    def horizontal_move(self, num):
        """takes a positive or negative value and adds it to the x coordinate"""
        self._x += num

    def vertical_move(self, num):
        """takes a positive or negative value and adds it to the y coordinate"""
        self._y += num

    def draw(self, surface):
        """
        takes a surface and on that surface
        draws the ship at its current coordinates
        """
        surface.blit(self._ship_img, (self._x, self._y))

    def shoot(self):
        """if the cool_down_counter is zero, fires a laser object from the front of the ship."""
        if self._cool_down_counter <= 0:
            laser = Laser(self._x + self.get_width()/2, self._y - 10, self._laser_type)
            laser.horizontal_move(-(laser.get_width()//2))
            self._lasers.append(laser)
            self._cool_down_counter = laser.get_cool_down()

    def cool_down(self):
        if self._cool_down_counter < 0:
            self._cool_down_counter = 0
        elif self._cool_down_counter > 0:
            self._cool_down_counter -= 1

    def collision(self, obj):
        """
        takes an object
        returns True if the ship is colliding with that object, else returns False
        """
        return collide(obj, self)

    # Collection of Ship Movement Patterns
    def move_down(self):
        """movement pattern: sends the enemy down in a straight line"""
        self._y += self._speed

    def sneak_sprint(self):
        """enemy moves in a straight line, then increases speed when partway down screen."""
        # Increases speed when reaches a third down screen.
        if self._y >= self._scr_height//3:
            self._y += self._speed * 3
        else:
            self._y += self._speed

    def zig(self):
        """enemy descends while weaving left and right, directional opposite to zag"""
        # Moves ship right
        if self._move_counter <= 60:
            self._x += self._speed * 2
        # Moves ship left
        else:
            self._x -= self._speed * 2

        # Moves ship down
        self._y += self._speed

        self._move_counter += 1

        # Resets left-right movement cycle
        if self._move_counter > 120:
            self._move_counter = 0

    def zag(self):
        """enemy descends while weaving left and right, directional opposite to zig."""
        # Moves ship right
        if self._move_counter <= 60:
            self._x -= self._speed * 2
        # Moves ship left
        else:
            self._x += self._speed * 2

        # Moves ship down
        self._y += self._speed

        self._move_counter += 1

        # Resets left-right movement cycle
        if self._move_counter > 120:
            self._move_counter = 0

    def crawl_left(self):
        """Enemy descends the screen by descending at the end of each row. Starts left."""
        if self._x < 0 and self._move_counter == 0:
            self._x = 0
            self._move_counter += 70
            self._direction = 1
        if self._x > self._scr_width - 64:
            self._x = self._scr_width - 64
            self._move_counter += 70
            self._direction = 0

        # Moves the ship down while move_counter is active
        if self._move_counter > 0:
            self._y += 2
            self._move_counter -= 1
        # Moves ship left or right based on direction indicator
        elif self._direction == 0:
            self._x -= self._speed
        else:
            self._x += self._speed

    def crawl_right(self):
        """Enemy descends the screen by descending at the end of each row. Starts left."""
        if self._x < 0 and self._move_counter == 0:
            self._x = 0
            self._move_counter += 70
            self._direction = 0
        if self._x > self._scr_width - 64:
            self._x = self._scr_width - 64
            self._move_counter += 70
            self._direction = 1

        # Moves the ship down while move_counter is active
        if self._move_counter > 0:
            self._y += 2
            self._move_counter -= 1
        # Moves ship left or right based on direction indicator
        elif self._direction == 1:
            self._x -= self._speed
        else:
            self._x += self._speed

    def crawl_drop(self):
        """Enemy descends the screen by descending at the end of each row. Starts left."""
        # Randomly drops the ship after reaching halfway down the screen.
        if self._move_counter == 0 and self._y > self._scr_height//2:
            self._move_counter = random.randint(-250, -1)
        if self._move_counter < 0:
            if self._move_counter == -1:
                self._y += self._speed*3
                return
            else:
                self._move_counter += 1

        # Moves the ship through a row from left to right.
        if self._x < 0 and self._move_counter == 0:
            self._x = 0
            self._move_counter += 70
            self._direction = 0
        if self._x > self._scr_width - 64:
            self._x = self._scr_width - 64
            self._move_counter += 70
            self._direction = 1

        # Moves the ship down while move_counter is active (after hitting a wall)
        if self._move_counter > 0:
            self._y += 2
            self._move_counter -= 1
        # Moves ship left or right based on direction indicator
        elif self._direction == 1:
            self._x -= self._speed
        else:
            self._x += self._speed


class Player(Ship):
    """
    Ship controlled by the user
    """

    def __init__(self, x, y, laser_array, health):
        super().__init__(x, y, laser_array, health)
        self._ship_img = self._image["main_ship"]
        self._laser_type = "player_green"
        self._mask = pygame.mask.from_surface(self._ship_img)

    def set_image(self, ship_image):
        """Takes an image name and sets player ship to that image"""
        self._ship_img = self._image[ship_image]

    def shoot(self):
        """if the cool_down_counter is zero, fires a laser object from the front of the ship."""
        if self._cool_down_counter == 0:
            laser = Laser(self._x + self.get_width()/2-8, self._y - 10, self._laser_type)
            self._lasers.append(laser)
            self._cool_down_counter = laser.get_cool_down()

    def health_bar(self, surface):
        """
        draws two overlapping rectangles, a red one the representing size of max health
        and a green one on top the size of health relative to max health"""
        pygame.draw.rect(surface, (255, 0, 0), (self._x, self._y + self.get_height() + 10, self.get_width(), 10))
        pygame.draw.rect(surface, (0, 255, 0), (self._x, self._y + self.get_height() + 10,
                                                self.get_width() * self._health / self._max_health, 10))

    def draw(self, surface):
        super().draw(surface)
        self.health_bar(surface)

    def explode(self):
        """explodes the ship"""
        laser = Laser(self._x - 64 + self.get_width()/2, self._y - 64, "explosion_zero")
        self._lasers.append(laser)


class Enemy(Ship):
    """
    Automated ships attacking the player
    """

    def __init__(self, x, y, laser_array, enemy_type):
        super().__init__(x, y, laser_array)

        # Dictionary of Enemy Species
        self._species = {
            # "Species": (Speed, Movement Pattern, Image, Laser Type, Health, Point Value)
            "Squid": (1, self.move_down, self._image["BlueSquid"], "blueShot", 10, 10),
            "ArrowBlue": (1, self.move_down, self._image["ArrowBlue"], "blueShot", 10, 10),
            "ArrowGold": (1, self.move_down, self._image["ArrowGold"], "blueShot", 10, 10),
            "ArrowPink": (1, self.move_down, self._image["ArrowPink"], "blueShot", 10, 10),
            "ArrowRed": (1, self.move_down, self._image["ArrowRed"], "blueShot", 10, 10),
            "ArrowStealth": (2, self.move_down, self._image["ArrowStealth"], "lightning", 30, 100),
            "Block": (1, self.sneak_sprint, self._image["Block"], "blank", 20, 10),
            "BlueSquid": (1, self.move_down, self._image["BlueSquid"], "blueShot", 10, 10),
            "BlueSpark": (1, self.move_down, self._image["blueSpark"], "blueShot", 10, 10),
            "CentiBlue": (3, self.crawl_left, self._image["CentiBlue"], "blasterGreen", 60, 10),
            "CentiGreen": (3, self.crawl_left, self._image["CentiGreen"], "blank", 60, 10),
            "CentiheadBlue": (3, self.move_down, self._image["CentiheadBlue"], "blank", 60, 10),
            "CentiheadDud": (3, self.crawl_drop, self._image["CentiheadDud"], "blank", 60, 40),
            "CentiheadGreen": (3, self.move_down, self._image["CentiheadGreen"], "blank", 60, 10),
            "CentiheadPanda": (3, self.crawl_left, self._image["CentiheadPanda"], "blank", 60, 10),
            "CentiheadRed": (3, self.crawl_right, self._image["CentiheadRed"], "blasterRed", 10, 60),
            "CentiheadYellow": (3, self.move_down, self._image["CentiheadYellow"], "blank", 10, 60),
            "CentiPurple": (3, self.crawl_right, self._image["CentiPurple"], "blank", 10, 60),
            "CentiRed": (3, self.crawl_right, self._image["CentiRed"], "blank", 10, 60),
            "FlappyBlue": (1, self.move_down, self._image["FlappyBlue"], "blueShot", 10, 10),
            "FlappyGreen": (1, self.move_down, self._image["FlappyGreen"], "blueShot", 10, 10),
            "FlappyRed": (1, self.move_down, self._image["FlappyRed"], "blueShot", 10, 10),
            "FlappyStealth": (1, self.move_down, self._image["FlappyStealth"], "blueShot", 10, 10),
            "FlappyWhite": (2, self.move_down, self._image["FlappyWhite"], "blasterGreen", 20, 15),
            "FlappyWhite2": (2, self.move_down, self._image["FlappyWhite"], "blasterGreen2", 20, 15),
            "GreenSpark": (1, self.move_down, self._image["GreenSpark"], "blueShot", 10, 10),
            "Hammer": (3, self.move_down, self._image["hammer"], "explosion", 10, 10),
            "Metal1": (1, self.zig, self._image["metal_1"], "rayGreen", 10, 10),
            "MetalSquid": (1, self.move_down, self._image["MetalSquid"], "blueShot", 10, 10),
            "RedMetalSquid": (1, self.move_down, self._image["RedMetalSquid"], "blueShot", 10, 10)
        }

        # Defines Enemy Attributes based on type
        self._speed = self._species[enemy_type][0]                    # Speed
        self._movement_type = self._species[enemy_type][1]            # Movement Pattern
        self._ship_img = self._species[enemy_type][2]                 # Image
        self._laser_type = self._species[enemy_type][3]               # Laser Type
        self._health = self._species[enemy_type][4]                   # Health
        self._point_value = self._species[enemy_type][5]              # Point Value

        # Creates mask for collisions
        self._mask = pygame.mask.from_surface(self._ship_img)

    def get_value(self):
        """Returns the enemy's point value"""
        return self._point_value

    def move(self):
        """moves enemy according to movement_type"""
        self._movement_type()

    def explode(self):
        """explodes the ship"""
        laser = Laser(self._x - 64 + self.get_width()/2, self._y - 64, "explosion")
        self._lasers.append(laser)
