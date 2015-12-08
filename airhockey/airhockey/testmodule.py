import common
import datetime
import time
import cv2


class TestSource(common.Component):

    listens = ['start']
    raises = ['test']

    def __init__(self, event_handler, **kwargs):
        super(TestSource, self).__init__(event_handler)

        # get random string from argument
        self.some_string = kwargs.get('test')

    def handle_event_start(self, bag):
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        print("DEBUG: TestSource handle event")

        # add some random stuff
        bag.ts = datetime.datetime.now()

        if self.some_string:
            bag.some_string = self.some_string

        self.event_handler.raise_event("test", bag)


class TestMiddle(common.Component):

    listens = ['test']
    raises = ['test2']

    def handle_event_test(self, bag):
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        print("DEBUG: TestMiddle handle event")

        # convert ts to string
        bag.ts_string = bag.ts.__str__()

        self.event_handler.raise_event("test2", bag)


class TestPrint(common.Component):

    listens = ['test2']

    def handle_event_test2(self, bag):
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        print("DEBUG: TestPrint handle event")

        # print string
        print(bag.ts_string)

        if 'some_string' in bag:
            print(bag.some_string)

        # wait some time
        time.sleep(1)
