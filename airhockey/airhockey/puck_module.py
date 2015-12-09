import common
import vector

import cv2
import cv2.cv as cv
import numpy as np
import time


class PuckPositionBuffer:

    DEFAULT_BUFFER_SIZE = 5

    # The acceptable difference between the next predicted and detected position
    ACCEPTABLE_PUCK_POSITION_DIFF = 100

    # The time in SECONDS for which the puck path should be predicted
    TABLE_BOUNDARIES_COLLISION_FORECAST_TIME = 0.5

    # The maximum amount of successive predictions
    MAX_SUCCESSIVE_PREDICTION_AMOUNT = 4

    def __init__(self, buffer_size=None):           #aufgerufen
        self.buffer_size = (buffer_size if buffer_size is not None else self.DEFAULT_BUFFER_SIZE)

        # the point buffer
        self.buffer = []

        # the last predicted path
        self.last_path = []

        # amount of successive predictions because a puck was not found
        self.prediction_count = 0

    def _reset(self):
        """
        Resets the internal buffers.
        :return:
        """
        self.buffer = []
        self.last_path = []
        self.prediction_count = 0

    def is_empty(self):
        """
        Checks if the buffer is empty.
        :return:
        """
        return len(self.buffer) == 0

    def _predict_position(self, bag, current_time):
        """
        Guesses the puck's position.
        :param bag: The parameter bag
        :param current_time: The current time.
        :return:
        """

        # only possible if we have a path and a velocity
        if len(self.last_path) > 0:

            # find path part in which the the puck should be by now
            path_part_index = 0
            while path_part_index < len(self.last_path):
                path_part = self.last_path[path_part_index]
                if path_part[3] > current_time:

                    # collision time is in future -> take last part
                    path_part_index -= 1
                    break
                path_part_index += 1
            path_part = self.last_path[path_part_index - 1]

            # predict position
            remaining_time = current_time - path_part[3]
            direction = vector.mul_by(path_part[1], path_part[2] * remaining_time)
            bag.puck.predicted_position = vector.add(path_part[0], direction)
            

        elif 'position' in bag.puck:

            # use actual position if found
            bag.puck.predicted_position = bag.puck.position

    def _check_for_wild_shot(self, bag):
        """
        Checks if the latest puck position is a wild shot. Requires bag.puck.predicted_position.
        :param bag: The parameter bag
        :return:
        """
        predicted_position_pixel = vector.coord_to_image_space(bag.puck.predicted_position, bag.table_boundaries)
        diff = vector.length(vector.from_to(bag.puck.position_pixel, predicted_position_pixel))

        # use time_diff and velocity to play with this value
        #accepted = self.ACCEPTABLE_PUCK_POSITION_DIFF * bag.time_diff * max((1000 * self.last_path[-1][2]) if len(self.last_path) > 0 else 1.0, 1.0)

        #return diff > accepted
        return False

    def _add_point(self, bag):
        """
        Adds the current point.
        :param bag:
        :return:
        """

        # only add if we have a point
        additional = 1
        if 'position' in bag.puck:
            self.buffer.append((bag.puck.position[0], bag.puck.position[1], bag.puck.detection_time))
            additional = 0

        # remove an old entry anyways (clear buffer over time)
        if len(self.buffer) + additional > self.buffer_size:
            self.buffer.pop(0)

    def handle_new_point(self, bag):
        """
        Handles a new puck position.
        :param bag: The parameter bag.
        :param bag: The parameter bag.
        """

        # predict position and check for wild shot
        self._predict_position(bag, bag.puck.detection_time)
        if self._check_for_wild_shot(bag):
            print("Wild shot detected: expected: %s, detected: %s" % (str(bag.puck.predicted_position), str(bag.puck.position)))
            self.use_predicted_point(bag)
            return

        # reset prediction counter since we found the puck
        self.prediction_count = 0

        # check if the puck flies in a different direction
        # TODO: mirror all previous points on collision axis IF we have a collision and direction change

        # just add...
        self._add_point(bag)

    def use_predicted_point(self, bag):   #aufgerufen
        """
        Uses a predicted point instead of taking a detected one.
        :param bag: The parameter bag.
        :return:
        """

        # don't try anything is the buffer is empty
        if self.is_empty():
            return

        print('Puck not detected. Using predicted position')

        # increase prediction count
        self.prediction_count += 1
        if self.prediction_count > self.MAX_SUCCESSIVE_PREDICTION_AMOUNT:
            print("%i successive puck predictions; assuming the puck is out of the image" % self.prediction_count)
            self._reset()
            return

        current_time = time.time()
        if 'predicted_position' not in bag.puck:
            self._predict_position(bag, current_time)

        # use predicted position, but double check: can't always predict
        if 'predicted_position' in bag.puck:
            bag.puck.position = bag.puck.predicted_position
            bag.puck.position_pixel = vector.coord_to_image_space(bag.puck.position, bag.table_boundaries)
            bag.puck.is_predicted_position = True
            bag.puck.detection_time = current_time

            # save radius
            bag.next.puck.radius_unscaled = bag.puck.radius_unscaled
            print("Predicted position: (%f, %f)" % bag.puck.position)

        # add (if we couldn't predict the position, we add nothing)
        self._add_point(bag)

    def predict_puck_movement(self, bag):   #ausgefuehrt
        """
        Predicts the pucks movement.
        :param bag: The parameter bag.
        :return:
        """

        # need at least 2 points
        if len(self.buffer) < 2:
            return

        # loop over points
        direction_sum = (0, 0)
        for i in xrange(0, len(self.buffer) - 1):
            # get tuples and time diff

            current_tuple = self.buffer[i]
            next_tuple 	  = self.buffer[i+1]
            time_diff	  = next_tuple[2] - current_tuple[2]

            # get direction (length is velocity) and divide by time_diff
            direction = vector.mul_by(vector.from_to(current_tuple, next_tuple), 1.0 / time_diff)

            # sum up
            direction_sum = vector.add(direction_sum, direction)

        # averaging
        direction = vector.mul_by(direction_sum, 1.0 / self.buffer_size)

        # add puck direction (normalized) and velocity
        bag.puck.velocity = vector.length(direction)
        bag.puck.direction = vector.normalize(direction)

    def _check_collision(self, from_position, to_position, movement):    #aufgerufen
        """
        Checks if the puck path collides with the boundaries.
        :param from_position:
        :param to_position:
        :param movement:
        :return:
        """
        possibilities = []
        if to_position[0] < 0:
            collision_time = -from_position[0] / movement[0]
            collision_position = (0, from_position[1] + movement[1] * collision_time)
            new_movement = (-movement[0], movement[1])
            possibilities.append((collision_position, new_movement, collision_time))
            #print("l")
        if to_position[0] > 1:
            collision_time = (1 - from_position[0]) / movement[0]
            collision_position = (1, from_position[1] + movement[1] * collision_time)
            new_movement = (-movement[0], movement[1])
            possibilities.append((collision_position, new_movement, collision_time))
            #print("r")
        if to_position[1] < 0:
            collision_time = -from_position[1] / movement[1]
            collision_position = (from_position[0] + movement[0] * collision_time, 0)
            new_movement = (movement[0], -movement[1])
            possibilities.append((collision_position, new_movement, collision_time))
            #print("t")
        if to_position[1] > 1:
            collision_time = (1 - from_position[1]) / movement[1]
            collision_position = (from_position[0] + movement[0] * collision_time, 1)
            new_movement = (movement[0], -movement[1])
            possibilities.append((collision_position, new_movement, collision_time))
            #print("b")
        if len(possibilities) == 0:
            return None

        # find possibility with shortest time
        shortest = 0
        for i in xrange(0, len(possibilities)):
            if possibilities[i][2] < possibilities[shortest][2]:
                shortest = i
        #print("Took possibility %i: %s" % (shortest, possibilities[shortest]))
        return possibilities[shortest]

    def build_puck_path(self, bag, remaining_forecast_time=None):    #ausgefuehrt
        """
        Checks for a collision with the table boundaries.
        :param bag: The parameter bag.
        :param remaining_forecast_time:
        :return:
        """
        if 'direction' not in bag.puck:
            return

        if remaining_forecast_time is None:
            remaining_forecast_time = self.TABLE_BOUNDARIES_COLLISION_FORECAST_TIME

        if 'path' not in bag.puck:
            bag.puck.path = []
        if len(bag.puck.path) == 0:
            bag.puck.path.append((bag.puck.position, bag.puck.direction, bag.puck.velocity, bag.puck.detection_time))

        # get position and direction for the current path part
        position = bag.puck.path[-1][0]
        direction = bag.puck.path[-1][1]
        velocity = bag.puck.path[-1][2]

        # follow puck movement for remaining time
        movement = vector.mul_by(direction, velocity)
        predicted_position = vector.add(position, vector.mul_by(movement, remaining_forecast_time))

        # check if position is out of bounds
        collision = self._check_collision(position, predicted_position, movement)
        if collision is not None:

            # add to path
            bag.puck.path.append((collision[0], vector.normalize(collision[1]), velocity, bag.puck.path[-1][3] + collision[2]))

            # continue building path
            remaining_forecast_time -= collision[2]
            #print("Velocity: " + str(velocity))
            #print(remaining_forecast_time)
            #if len(bag.puck.path) > 20:
            #    exit()
            if remaining_forecast_time > 0:
                self.build_puck_path(bag, remaining_forecast_time)

        # save path
        #print("done, path: " + str(bag.puck.path))
        self.last_path = bag.puck.path


class PuckDetection(common.Component):

    listens = ['image']
    raises = ['puck']

    # Hough parameters
    # TODO: config file
    DP          = 1     # Inverse ratio of the accumulator resolution to the image resolution (keep at 1)
    MIN_DIS     = 10    # Minimum distance between the centers of the detected circles (in one frame)
    PARAM1      = 200   # Higher threshold passed to the Canny edge detector. The lower threshold is half the size of PARAM1
    PARAM2      = 30    # Accumulator threshold for the circle centers at the detection stage (the smaller it is, the more false circles)
    MIN_RADIUS  = 10    # Minimum circle radius
    MAX_RADIUS  = 20    # Maximum circle radius

    def __init__(self, event_handler, **kwargs):            #aufgerufen
        super(PuckDetection, self).__init__(event_handler)

        # initialize buffer
        self.point_buffer = PuckPositionBuffer(kwargs.get('position_buffer_size'))
        self.table_boundaries = []

    def add_table_boundary_point(self, point):
        """
        Adds a point to the table boundaries.
        :param point:
        :return:
        """
        self.table_boundaries.append(point)

    def detect_puck(self, bag):    #aufgerufen
        """
        Detects the puck inside the image.
        :param bag: The parameter bag.
        :return:
        """

        # Convert to grayscale image so HoughCircles can use it (uses Canny internally)
        gray = cv2.cvtColor(bag.image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 10)
        circles = cv2.HoughCircles(gray, cv.CV_HOUGH_GRADIENT, self.DP, minDist=self.MIN_DIS, param1=self.PARAM1, param2=self.PARAM2, minRadius=self.MIN_RADIUS, maxRadius=self.MAX_RADIUS)

        if circles is not None:

            # convert to NumPy array
            circles = np.int16(np.around(circles))

            # hard coded to only use the first detected circle (if there are more...)
            x_coord = circles[0][0][0]
            y_coord = circles[0][0][1]
            radius  = circles[0][0][2]

            # scale and save stuff
            bag.puck.position_pixel = (x_coord, y_coord)
            bag.puck.position = vector.image_to_coord_space(bag.puck.position_pixel, bag.table_boundaries)
            bag.puck.radius_unscaled = radius
            bag.puck.detection_time = time.time()

            # handle point
            self.point_buffer.handle_new_point(bag)

            # save radius in next to make it available for next iteration if we have to predict the position
            bag.next.puck.radius_unscaled = bag.puck.radius_unscaled
        else:

            # use predicted point
            self.point_buffer.use_predicted_point(bag)

        # let buffer do its business
        self.point_buffer.predict_puck_movement(bag)
        self.point_buffer.build_puck_path(bag)

    def handle_event_image(self, bag):    #aufgerufen
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        # add table boundaries
        bag.table_boundaries = self.table_boundaries

        # detect puck
        self.detect_puck(bag)

        self.event_handler.raise_event("puck", bag)


class TableSetupPuckDetection(PuckDetection):

    def is_table_setup_complete(self):   #aufgerufen
        """
        Checks if the table setup is complete.
        :return:
        """
        return len(self.table_boundaries) == 2

    def continue_table_setup(self, bag):   #aufgerufen
        """
        Continues the process for the table setup.
        :param bag: The parameter bag.
        :return:
        """

        # check for next table boundaries point
        if 'table_boundaries_point' in bag:
            self.add_table_boundary_point(bag.table_boundaries_point)
            if self.is_table_setup_complete():
                return

        # continue with table setup, save frame for next iteration
        bag.is_table_setup = True
        bag.next.image = bag.image.copy()

    def detect_puck(self, bag):
        """
        Detects the puck inside the image.
        :param bag: The parameter bag.
        :return:
        """

        # do not detect puck when table setup is on
        if not bag.is_table_setup:
            super(TableSetupPuckDetection, self).detect_puck(bag)

    def handle_event_image(self, bag):    #aufgerufen
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        # continue table setup if not ready
        if not self.is_table_setup_complete():
            self.continue_table_setup(bag)

        super(TableSetupPuckDetection, self).handle_event_image(bag)
