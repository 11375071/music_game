import pygame
import matplotlib.image as mpimg

def make_tuple(path):
    surface = pygame.image.load(path)
    ndarray = mpimg.imread(path)
    return (surface, ndarray)

homepage_path = "src/image/home_page.png"
homepage_surface = pygame.image.load(homepage_path)

play_path = "src/image/play_background.png"
play_surface = pygame.image.load(play_path)

note_path = "src/image/note_green.png"
note_surface = pygame.image.load(note_path)
note_surface_scaled = pygame.transform.scale(note_surface, (50, 10))

homepage_play_button_path_1 = "src/image/play_origin.png"
homepage_play_button_tuple_1 = make_tuple(homepage_play_button_path_1)

homepage_play_button_path_2 = "src/image/play_selected.png"
homepage_play_button_tuple_2 = make_tuple(homepage_play_button_path_2)

homepage_settings_button_path_1 = "src/image/setting_origin.png"
homepage_settings_button_tuple_1 = make_tuple(homepage_settings_button_path_1)

homepage_settings_button_path_2 = "src/image/setting_selected.png"
homepage_settings_button_tuple_2 = make_tuple(homepage_settings_button_path_2)
