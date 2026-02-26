from .AAudio import AAudio

class SimpleAudio(AAudio):

    def __init__(self, object):
        AAudio.__init__(self)
        self.wave_obj = object
        self.play = None

    def playAudio(self):
        if self.play is not None:
            if self.play.is_playing():
                self.play.stop()
                
        self.play = self.wave_obj.play()
        self.play.wait_done()

    def playAudioAsync(self):
        if self.play is not None:
            if self.play.is_playing():
                self.play.stop()
                       
        self.play = self.wave_obj.play()

    def isCurrentlyPlaying(self):
        if self.play is None:
            return False
        return self.play.is_playing()

    def stop(self):
        self.play.stop()
