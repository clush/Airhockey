from common import Component, AirhockeyException
import os.path
import cv2
import time

from time import sleep


class OpenCvCapture(Component):

    listens = ['start']
    raises = ['image']

    def __init__(self, event_handler, **kwargs):    #aufgerufen
        super(OpenCvCapture, self).__init__(event_handler)

        # get source
        if 'source' not in kwargs:
            raise AirhockeyException("Component '%s' requires the 'source' parameter" % self.__class__.__name__)
        self._create_capture(kwargs['source'])

        # get fps
        self.fps = 0
        self.last_capture = None
        if 'fps' in kwargs:
            try:
                self.fps = int(kwargs['fps'])
            except ValueError:
                raise AirhockeyException("FPS has to be integer, '%s' given" % kwargs['fps'])

    def _create_capture(self, source):
        """
        Creates the capture.
        :param source:
        :return:
        """
        try:

            # try to convert to integer (to use as camera index)
            source = int(source)
            print("Using camera with index '%i' as source for video capture" % source)

        except ValueError:

            # use as file name
            if not os.path.isfile(source):
                raise AirhockeyException("Source file '%s' does not exist" % source)
            print("Using file '%s' as source for video capture" % source)

        # create capture
        self.capture = cv2.VideoCapture(source)

    def __del__(self):

        # release capture
        if hasattr(self, 'capture'):
            self.capture.release()

    def get_next_frame(self, bag):  #aufgerufen
        """
        Gets the next frame.
        :param bag: The parameter bag.
        :return:
        """

        # check if capture is still open
        if not self.capture.isOpened():
            raise AirhockeyException("VideoCapture closed")

        # sleep if we are allowed to
        # sleep bis naechster Frame vorhanden ist
        current_time = time.time()
        if self.fps and self.last_capture is not None:
            spf = 1.0 / self.fps
            if current_time < self.last_capture + spf:
                time.sleep(self.last_capture + spf - current_time)
                current_time = time.time()

        # get image
        ret, frame = self.capture.read()
        if not ret:
            raise AirhockeyException("VideoCapture closed (at capture.read())")

        # safe image
        bag.image = frame
        bag.time_diff = current_time - (self.last_capture if self.last_capture is not None else current_time)
        self.last_capture = current_time

    def handle_event_start(self, bag):   #aufgerufen
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        self.get_next_frame(bag)
        self.event_handler.raise_event("image", bag)


class TableSetupCapture(OpenCvCapture):

    def get_next_frame(self, bag):   #aufgerufen
        """
        Gets the next frame.
        :param bag: The parameter bag.
        :return: True if the next event can be raised, otherwise False
        """

        # if a frame is already in the bag, just go on without capturing a new one
        if 'image' not in bag:
            return super(TableSetupCapture, self).get_next_frame(bag)
