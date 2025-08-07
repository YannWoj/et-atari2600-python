# audio_manager.py
import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        
        # load all sounds once
        self.sounds = {
            # E.T. sounds
            "et_walk": pygame.mixer.Sound("assets/sounds/E.T/walk.wav"),
            "et_run": pygame.mixer.Sound("assets/sounds/E.T/run.wav"),
            "et_head_raise": pygame.mixer.Sound("assets/sounds/E.T/head_raise.wav"),
            "et_fall": pygame.mixer.Sound("assets/sounds/E.T/fall.wav"),
            "et_head_raise_levitating": pygame.mixer.Sound("assets/sounds/E.T/head_raise_levitating.wav"),
            
            # spaceship sounds
            "spaceship": pygame.mixer.Sound("assets/sounds/spaceship/spaceship.wav")
        }
        
        # set volumes
        self.sounds["et_head_raise"].set_volume(0.75)
        
        # music tracking
        self.current_music = None
        self.music_playing = False
        
        # music files
        self.music_files = {
            "title": "assets/music/title_music.wav"
        }
    
    def play_sound(self, sound_name, loops=0):
        """plays a specific sound"""
        if sound_name in self.sounds:
            return self.sounds[sound_name].play(loops)
        return None
    
    def stop_sound(self, sound_name):
        """stops a specific sound"""
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
    
    def play_music(self, music_name, loops=-1):
        """play some music"""
        if music_name in self.music_files and self.current_music != music_name:
            pygame.mixer.music.load(self.music_files[music_name])
            pygame.mixer.music.play(loops)
            self.current_music = music_name
            self.music_playing = True
    
    def stop_music(self):
        """stop music"""
        pygame.mixer.music.stop()
        self.current_music = None
        self.music_playing = False
    
    def is_music_playing(self):
        return self.music_playing
    
    def get_sound(self, sound_name):
        """returns a sound object for external use"""
        return self.sounds.get(sound_name)