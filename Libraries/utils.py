import pygame

def y_correction(y):
    return -y

def get_mouse_ui_pos(camera):
    mx, my = pygame.mouse.get_pos()
    win_w, win_h = pygame.display.get_window_size()  # current window size

    # Map screen pixels → camera logical coordinates
    mx = mx * (camera.width / win_w)
    my = my * (camera.height / win_h)

    # Undo zoom (centered zoom)
    cx = camera.width * 0.5
    cy = camera.height * 0.5
    mx = cx + (mx - cx) / camera.zoom
    my = cy + (my - cy) / camera.zoom

    return mx, my
