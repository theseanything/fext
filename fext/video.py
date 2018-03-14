import datetime

import cv2 as cv

class VideoProperty(object):
    """docstring for VideoProperty."""
    def __init__(self, property_code, type_cast=None):
        self.property_code = property_code
        self.type_cast = type_cast

    def __get__(self, instance, owner):
        value = instance.get(self.property_code)
        return self.type_cast(value) if self.type_cast else value

    def __set__(self, instance, value):
        instance.set(self.property_code, value)

class Video(cv.VideoCapture):
    curr_frame = VideoProperty(cv.CAP_PROP_POS_FRAMES, int)
    frame_count = VideoProperty(cv.CAP_PROP_FRAME_COUNT, int)
    fps = VideoProperty(cv.CAP_PROP_FPS)
    height = VideoProperty(cv.CAP_PROP_FRAME_HEIGHT, int)
    width = VideoProperty(cv.CAP_PROP_FRAME_WIDTH, int)

    def __init__(self, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)

    def __len__(self):
        return int(self.frame_count)

    @property
    def seconds(self):
        return self.frame_count // self.fps

    @property
    def time(self):
        return str(datetime.timedelta(seconds=self.seconds))

    def frames(self, frame_interval):
        while True:
            success, image = self.read()
            if not success:
                return
            yield (self.curr_frame, image)
            self.curr_frame += frame_interval - 1
