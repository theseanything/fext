import datetime

import cv2 as cv

class Video(cv.VideoCapture):
    def __init__(self, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)

    def __len__(self):
        return int(self.get(cv.CAP_PROP_FRAME_COUNT))

    @property
    def curr_frame(self):
        return int(self.get(cv.CAP_PROP_POS_FRAMES))

    @property
    def fps(self):
        return int(self.get(cv.CAP_PROP_FPS))

    @property
    def seconds(self):
        return len(self) // self.fps

    @property
    def time(self):
        return str(datetime.timedelta(seconds=self.seconds))

    def frames(self, time_interval):
        frame_interval = time_interval * self.fps
        while True:
            success, image = self.read()
            if not success:
                return
            yield (self.curr_frame, image)
            self.set(cv.CAP_PROP_POS_FRAMES, self.curr_frame + frame_interval)
