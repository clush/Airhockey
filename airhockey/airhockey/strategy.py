from common import Component
import vector
import time
import math


class SimpleStrategy(Component):

    listens = ['puck']
    raises = ['move_stick']

    # The radius of the stick
    STICK_RADIUS = 0.05  # in coordinate space, needs to be computed

    # The stick's max movement speed
    STICK_MAX_SPEED = 2.3

    # The stick's acceleration
    STICK_ACCELERATION = 1

    HOME_POSITION = (0.9, 0.5)
    AWAY_FROM_HOME = (-1, 0)

    def __init__(self, event_handler):
        super(SimpleStrategy, self).__init__(event_handler)

        # keep the results of the last computation
        self.last_stick_data = None

    def can_go_home(self, bag):
        """
        Checks if the stick can go home.
        :param bag: The parameter bag.
        :return:
        """

        # no detected puck movement: go home
        if 'direction' not in bag.puck:
            return True

        # nothing to do if the puck is not here
        if bag.puck.position[0] < 0.2:
            return True

        # check if the puck is flying away from home
        return vector.dot(self.AWAY_FROM_HOME, bag.puck.direction) > 0.25

    def go_home(self, bag):
        """
        Starts to move the stick to its home position.
        :param bag: The parameter bag.
        :return:
        """

        # can only go home if we actually have a stick
        if 'position' in bag.stick:

            dist_home = vector.length(vector.from_to(bag.stick.position, self.HOME_POSITION))

            bag.stick.dest_position = self.HOME_POSITION
            bag.stick.dest_direction = (0, 0)
            bag.stick.dest_velocity = 0
            bag.stick.dest_time = time.time() + dist_home / self.STICK_MAX_SPEED

    def _calculate_collision_point(self, bag):
        """
        Calculates the collision point between the puck and the stick.
        :param bag: The parameter bag.
        :return:
        """

        # NOTE: First attempt, ignoring stick and puck acceleration, puck radius and stick radius here

        # OK, math first:
        #
        # S = stick position
        # C = point of collision
        # v = max speed of the stick
        # P = puck position
        # p = puck direction * velocity
        #
        # Points which the stick can reach in time t build a circle around him:
        # 1. (Cx - Sx)^2 + (Cy - Sy)^2 = r = v * t
        #
        # Points which the puck reaches in time t are on the line:
        # 2. Px + px * t = Cx
        # 3. Py + py * t = Cy
        #
        # Approach:
        # - replace Cx and Cy in 1. with 2. and 3.
        # - bracket the square terms (Px + px * t - Sx)^2 and (Py + py * t - Sy)^2
        # - outline t^2 and t to get a formula like t^2*(...) + t*(...) + (...)
        # - name (...) a, b and c
        # - use the quadratic formula to get t
        # - use puck movement and t to get collision point
        # - use stick position and collision point
        # - gg

        Sx = bag.stick.position[0]
        Sy = bag.stick.position[1]
        Px = bag.puck.position[0]
        Py = bag.puck.position[1]
        px = bag.puck.direction[0] * bag.puck.velocity
        py = bag.puck.direction[1] * bag.puck.velocity
        v = self.STICK_MAX_SPEED

        # calculate a, b and c
        a = px*px + py*py - v*v
        b = 2*Px*px - 2*Sx*px + 2*Py*py - 2*Sy*py
        c = Px*Px - 2*Px*Sx + Sx*Sx + Py*Py - 2*Py*Sy + Sy*Sy

        # calculate t
        inner_sqrt = b*b - 4*a*c
        if inner_sqrt < 0:
            print("Going home, inner sqrt: " + str(inner_sqrt))

            # no chance to get that thing, go home
            self.go_home(bag)
            return

        # use + first, since a is negative (Vpuck - Vstick)
        # (... / 2 * a) -> shortest time needed
        sqrt_b2_4ac = math.sqrt(inner_sqrt)
        t = (-b + sqrt_b2_4ac) / 2*a
        print("Vp: "+str(bag.puck.velocity))
        print("t:  "+str(t))
        if t < 0:

            # too late for that chance, use other result
            t = (-b - sqrt_b2_4ac) / 2*a
            print("t2: "+str(t))

        # get collision point
        C = vector.add((Px, Py), vector.mul_by((px, py), t))
        s = vector.from_to((Sx, Sy), C)

        # save
        bag.stick.dest_position = C
        bag.stick.dest_direction = vector.normalize(s)
        bag.stick.dest_velocity = self.STICK_MAX_SPEED
        bag.stick.dest_time = time.time() + t

    def attack(self, bag):
        """
        Attacks the puck.
        :param bag: The parameter bag.
        :return:
        """

        # only if we have the stick position
        if 'position' in bag.stick:

            # compute collision point
            self._calculate_collision_point(bag)

            # TODO: compare with self.last_stick_data and send data only if we have something new?

    def handle_event_puck(self, bag):
        """
        Handles an event.
        :param bag: The parameter bag.
        :return:
        """

        # either go home or attack the puck
        self.go_home(bag) if self.can_go_home(bag) else self.attack(bag)

        # save result
        self.last_stick_data = bag.stick

        self.event_handler.raise_event("move_stick", bag)
