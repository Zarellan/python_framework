from SceneManager.Scene import Scene
from Libraries.spriteGL import SpriteGL
from OpenGL.GL import *
from Libraries.camera import Camera
import pygame
from Libraries.Windows import Windows
from Libraries.Deltatime import Deltatime
from Libraries.MainCamera import MainCamera
from Libraries.KeyPress import KeyPress
from Libraries.GameObject import GameObject

class CharacterController:

    TagsCollide = ["wall", "floor"]

    dx = 0
    dy = 0
    jump_power = 7
    speed_x = 100
    gravity = 30
    def __init__(self, image_path, x, y):
        self.player = GameObject("player")
        self.player.add_component(SpriteGL,image_path,MainCamera.camera)
        self.player.transform.x = x
        self.player.transform.y = y
        pass

    
    def check_ground(self, player, walls, margin=2):
    # Check a slightly taller rectangle under feet
        feet_rect = pygame.Rect(player.rect.left, player.rect.bottom, player.rect.width, margin)
        for wall in walls:
            if feet_rect.colliderect(wall.rect):
                return True
        return False

    def check_ceil(self, player, walls, margin=1):
        # Small rectangle just above the player's head
        head_rect = pygame.Rect(player.rect.left, player.rect.top - margin, player.rect.width, margin)
        for wall in walls:
            if head_rect.colliderect(wall.rect):
                return True
        return False

    def collision(self, sprite1, sprite2):
        return sprite1.rect.colliderect(sprite2.rect)


    def sync_sprite_to_transform(self):
        """Sync sprite position from transform for collision detection"""
        self.player.sprite.x = self.player.transform.x - self.player.sprite.width / 2
        self.player.sprite.y = self.player.transform.y - self.player.sprite.height / 2

    def move_player(self, walls):
        self.player.transform.x += self.dx
        self.sync_sprite_to_transform()
        for wall in walls:
            if self.player.sprite.rect.colliderect(wall.rect):
                if self.dx > 0:
                    self.player.transform.x = wall.rect.left - self.player.sprite.rect.width + self.player.sprite.width / 2
                elif self.dx < 0:
                    self.player.transform.x = wall.rect.right + self.player.sprite.width / 2
                self.sync_sprite_to_transform()

        self.player.transform.y += self.dy
        self.sync_sprite_to_transform()
        for wall in walls:
            if self.player.sprite.rect.colliderect(wall.rect):
                if self.dy > 0:
                    self.player.transform.y = wall.rect.top - self.player.sprite.rect.height + self.player.sprite.height / 2
                elif self.dy < 0:
                    self.player.transform.y = wall.rect.bottom + self.player.sprite.height / 2
                self.sync_sprite_to_transform()

    def resolve_collisions(self, walls):
        # X-axis
        for wall in walls:
            if self.player.sprite.rect.colliderect(wall.rect):
                if self.player.sprite.rect.centerx < wall.rect.centerx:
                    # player is left of wall -> push left
                    self.player.transform.x = wall.rect.left - self.player.sprite.rect.width + self.player.sprite.width / 2
                else:
                    # player is right of wall -> push right
                    self.player.transform.x = wall.rect.right + self.player.sprite.width / 2
                self.sync_sprite_to_transform()

        # Y-axis
        for wall in walls:
            if self.player.sprite.rect.colliderect(wall.rect):
                if self.player.sprite.rect.bottom <= wall.rect.centery:
                    # player above wall -> stand on top
                    self.player.transform.y = wall.rect.top - self.player.sprite.rect.height + self.player.sprite.height / 2
                else:
                    # player below wall -> hit ceiling
                    self.player.transform.y = wall.rect.bottom + self.player.sprite.height / 2
                self.sync_sprite_to_transform()

    def player_movement(self):
        self.dx = 0
        if KeyPress.left:
            self.dx = -2 * self.speed_x * Deltatime.dt
        elif KeyPress.right:
            self.dx = 2 * self.speed_x * Deltatime.dt

        collidables = self.get_collidables()

        if self.check_ground(self.player.sprite, collidables):
            self.dy = 0
        elif self.check_ceil(self.player.sprite, collidables):
            self.dy = max(self.dy, 0.4)
        else:
            self.dy += self.gravity * Deltatime.dt

        if KeyPress.up and self.check_ground(self.player.sprite, collidables):
            self.dy = -self.jump_power

        self.move_player(collidables)
        self.resolve_collisions(collidables)

    def get_collidables(self):
        collidables = []
        for tag in self.TagsCollide:
            collidables.extend([obj.sprite for obj in GameObject.get_all_by_tag(tag)])
        return collidables
    
    def change_size(self, widtho, heighto):
        # Compute current visual width/height (floats) and center/bottom without using pygame.Rect
        cur_w = self.player.sprite.width * getattr(self.player.sprite, 'scale_x', 1.0)
        cur_h = self.player.sprite.height * getattr(self.player.sprite, 'scale_y', 1.0)
        if getattr(self.player.sprite, 'origin_centered', False):
            old_centerx = float(self.player.sprite.x)
            old_bottom = float(self.player.sprite.y + cur_h / 2)
        else:
            old_centerx = float(self.player.sprite.x + cur_w / 2)
            old_bottom = float(self.player.sprite.y + cur_h)

        # Apply size change to base dimensions
        self.player.sprite.width = widtho
        self.player.sprite.height = heighto

        # Treat this as changing the base/original size so scale stays consistent
        self.player.sprite.original_width = self.player.sprite.width
        self.player.sprite.original_height = self.player.sprite.height
        self.player.sprite.scale_x = 1.0
        self.player.sprite.scale_y = 1.0

        # New visual size
        new_w = self.player.sprite.width * self.player.sprite.scale_x
        new_h = self.player.sprite.height * self.player.sprite.scale_y

        # Reposition so center-x and bottom remain unchanged (use floats)
        if getattr(self.player.sprite, 'origin_centered', False):
            self.player.sprite.x = old_centerx
            self.player.sprite.y = old_bottom - new_h / 2
        else:
            self.player.sprite.x = old_centerx - new_w / 2
            self.player.sprite.y = old_bottom - new_h

    def change_scale(self, x, y):
        # Compute current visual width/height (floats) and center/bottom without using pygame.Rect
        cur_w = self.player.sprite.width * getattr(self.player, 'scale_x', 1.0)
        cur_h = self.player.sprite.height * getattr(self.player, 'scale_y', 1.0)
        if getattr(self.player.sprite, 'origin_centered', False):
            old_centerx = float(self.player.sprite.x)
            old_bottom = float(self.player.sprite.y + cur_h / 2)
        else:
            old_centerx = float(self.player.sprite.x + cur_w / 2)
            old_bottom = float(self.player.sprite.y + cur_h)

        self.player.sprite.scale_x = x
        self.player.sprite.scale_y = y

        # Use floats internally
        new_width = self.player.sprite.original_width * self.player.scale_x
        new_height = self.player.sprite.original_height * self.player.scale_y

        # Reposition so center-x and bottom remain unchanged
        if getattr(self.player, 'origin_centered', False):
            self.player.sprite.x = old_centerx
            self.player.sprite.y = old_bottom - new_height / 2
        else:
            self.player.sprite.x = old_centerx - new_width / 2
            self.player.sprite.y = old_bottom - new_height

