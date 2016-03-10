import common
import vector
import strategy
import cv2
import const


class SimpleImageDisplay(common.Component):

    listens = ['image']    #wird in PuckimageDisplay ueberschrieben


    def __init__(self, event_handler):
        super(SimpleImageDisplay, self).__init__(event_handler)

        cv2.namedWindow(const.CONST.WINDOW_TITLE)

    def __del__(self):

        # destroy windows
        cv2.destroyAllWindows()

    def handle_event_image(self, bag):
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        cv2.imshow(const.CONST.WINDOW_TITLE, bag.image)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            raise common.AirhockeyException("Operation cancelled by user")


class PuckImageDisplay(SimpleImageDisplay):

    listens = ['puck']
    raises = ["strategy"]

    def draw_table_boundaries(self, bag):
        """
        Draws the table boundaries into the image.
        :param bag: The parameter bag.
        :return:
        """
        if 'table_boundaries' in bag:
            cv2.rectangle(bag.image, bag.table_boundaries[0], bag.table_boundaries[1], (0, 0, 255), 1)

    def draw_puck(self, bag):
        """
        Draws the puck into the image.
        :param bag:
        :return:
        """

        if 'position' in bag.puck:

            # draw puck itself
            color = ((255, 0, 0) if bag.puck.is_predicted_position else (0, 255, 0))
            cv2.circle(bag.image, bag.puck.position_pixel, bag.puck.radius_unscaled, color, 2)
            cv2.circle(bag.image, bag.puck.position_pixel, 2, (0, 0, 255), 3)

            if 'path' in bag.puck:

                # draw puck movement
                #direction_velocity = vector.mul_by(bag.puck.direction, bag.puck.velocity)
                #destination = vector.add(bag.puck.position, direction_velocity)
                #destination_pixel = vector.coord_to_image_space(destination, bag.table_boundaries)
                #cv2.line(bag.image, bag.puck.position_pixel, destination_pixel, (255, 0, 0))

                # draw path
                for i in xrange(0, len(bag.puck.path) - 1):
                    position = vector.coord_to_image_space(bag.puck.path[i][0], bag.table_boundaries)
                    destination = vector.coord_to_image_space(bag.puck.path[i + 1][0], bag.table_boundaries)
                    cv2.line(bag.image, position, destination, (255, 0, 0))
                    cv2.circle(bag.image, position, 1, (0, 0, 255), 2)
                position_pixel = vector.coord_to_image_space(bag.puck.path[-1][0], bag.table_boundaries)
                direction_velocity = vector.mul_by(bag.puck.path[-1][1], bag.puck.path[-1][2])
                destination = vector.add(bag.puck.path[-1][0], direction_velocity)
                destination_pixel = vector.coord_to_image_space(destination, bag.table_boundaries)
                cv2.line(bag.image, position_pixel, destination_pixel, (255, 0, 0))

    def draw_puck_information(self, bag):
        """
        Draws puck information like position, direction and velocity.
        :param bag: The parameter bag.
        :return:
        """
        if 'position' in bag.puck:

            # draw position information
            cv2.putText(bag.image, "Position", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
            cv2.putText(bag.image,
                        "({:1.3f}, {:1.3f})".format(bag.puck.position[0], bag.puck.position[1]),
                        (75, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

            if 'direction' in bag.puck:

                # draw direction and velocity
                cv2.putText(bag.image, "Direction", (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
                cv2.putText(bag.image,
                            "({:1.3f}, {:1.3f})".format(bag.puck.direction[0], bag.puck.direction[1]),
                            (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
                cv2.putText(bag.image, "Velocity", (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
                cv2.putText(bag.image,
                            "{:2.3f}".format(bag.puck.velocity),
                            (75, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

    def handle_event_puck(self, bag):
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        # draw stuff
        self.draw_table_boundaries(bag)
        self.draw_puck(bag)
        self.draw_puck_information(bag)

        super(PuckImageDisplay, self).handle_event_image(bag)


class SimulationImageDisplay(PuckImageDisplay):

    listens = ['move_stick']

    def move_stick(self, bag):
        """
        Moves the stick.
        :param bag: The parameter bag.
        :return:
        """
        if 'position' not in bag.stick:
            bag.next.stick.position = strategy.SimpleStrategy.HOME_POSITION
            return
        if 'dest_position' not in bag.stick:
            position = bag.stick.position
        else:

            # move stick towards destination
            # ignore dest_direction and dest_velocity
            dist_moved = strategy.SimpleStrategy.STICK_MAX_SPEED * bag.time_diff
            direction = vector.from_to(bag.stick.position, bag.stick.dest_position)
            if dist_moved > vector.length(direction):
                position = bag.stick.dest_position
            else:
                direction = vector.mul_by(vector.normalize(direction), dist_moved * strategy.SimpleStrategy.STICK_MAX_SPEED)
                position = vector.add(bag.stick.position, direction)

        # set new position
        bag.next.stick.position = position

    def draw_stick(self, bag):
        """
        Draws the stick and it's destination.
        :param bag: The parameter bag.
        :return:
        """

        if 'stick' in bag and 'table_boundaries' in bag:

            # draw stick itself
            position_unscaled = vector.coord_to_image_space(bag.stick.position, bag.table_boundaries)
            cv2.circle(bag.image, position_unscaled, 10, (0, 255, 0), 2)
            cv2.circle(bag.image, position_unscaled, 2, (50, 50, 50), 3)

            if 'dest_position' in bag.stick:

                # draw desired stick movement
                dest_position_unscaled = vector.coord_to_image_space(bag.stick.dest_position, bag.table_boundaries)
                cv2.line(bag.image, position_unscaled, dest_position_unscaled, (0, 0, 0))

    def handle_event_move_stick(self, bag):
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        # move and draw stick
        self.move_stick(bag)
        self.draw_stick(bag)

        super(SimulationImageDisplay, self).handle_event_puck(bag)


class TableSetupImageDisplay(PuckImageDisplay):

    def __init__(self, event_handler):              #aufgerufen
        super(TableSetupImageDisplay, self).__init__(event_handler)

        cv2.setMouseCallback(const.CONST.WINDOW_TITLE, self.mouse_click_handler)
        self.last_is_table_setup = False
        self.next_table_boundaries = None

    def mouse_click_handler(self, event, x, y, flags, param):
        """
        Handles a mouse click.
        :return:
        """
        if self.last_is_table_setup and event == cv2.EVENT_LBUTTONDBLCLK:
            self.next_table_boundaries = (x, y)

    def draw_table_boundaries(self, bag):
        """
        Draws the table boundaries into the image.
        :param bag: The parameter bag.
        :return:
        """
        if bag.is_table_setup:

            # give instructions
            cv2.putText(bag.image, "Double click on image to set table boundaries",
                        (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
            for point in bag.table_boundaries:
                cv2.circle(bag.image, point, 2, (0, 0, 255), -1)

        elif 'table_boundaries' in bag:
            super(TableSetupImageDisplay, self).draw_table_boundaries(bag)

    def draw_puck(self, bag):
        """
        Draws the puck into the image.
        :param bag:
        :return:
        """

        # only if table setup is over
        if not bag.is_table_setup:
            super(TableSetupImageDisplay, self).draw_puck(bag)

    def update_self_and_bag(self, bag):    #aufgerufen
        """
        Updates the local attributes and the bag.
        :param bag: The parameter bag.
        :return:
        """
        self.last_is_table_setup = bag.is_table_setup
        if self.next_table_boundaries is not None:

            # scale boundaries point
            bag.next.table_boundaries_point = self.next_table_boundaries
            self.next_table_boundaries = None

    def handle_event_puck(self, bag):  #aufgerufen
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        # exchange information
        self.update_self_and_bag(bag)

        super(TableSetupImageDisplay, self).handle_event_puck(bag)
        self.event_handler.raise_event("strategy", bag)


class TableSetupSimulationImageDisplay(SimulationImageDisplay, TableSetupImageDisplay):

    listens = ['move_stick']

    def __init__(self, event_handler):
        super(TableSetupSimulationImageDisplay, self).__init__(event_handler)

    def move_stick(self, bag):
        """
        Moves the stick.
        :param bag: The parameter bag.
        :return:
        """

        # only if table setup is over
        if not bag.is_table_setup:
            super(TableSetupSimulationImageDisplay, self).move_stick(bag)

    def draw_stick(self, bag):
        """
        Draws the stick and it's destination.
        :param bag: The parameter bag.
        :return:
        """

        # only if table setup is over
        if not bag.is_table_setup:
            super(TableSetupSimulationImageDisplay, self).draw_stick(bag)

    def handle_event_move_stick(self, bag):
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        # exchange information
        self.update_self_and_bag(bag)

        # move and draw stick
        self.move_stick(bag)
        self.draw_stick(bag)

        # call handle event of PuckImageDisplay, the next common base class
        PuckImageDisplay.handle_event_puck(self, bag)
