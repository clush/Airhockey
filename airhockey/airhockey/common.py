import copy
import re


class AirhockeyException(Exception):
    pass


class Bag(dict):
    """
    An extended dictionary containing additional functionality:
    - Access items as attributes, like "bag.item1".
      The return value converts to False (__nonzero__) if the item does not exist.
    - Set items as attributes, like "bag.item1 = value1".
      Nested assignments are value even if the parent key does not exist yet:
      "bag.item1.item2 = value" although "bag.item1" did not exist.
    """

    def __init__(self, creator=None, item=None):

        # use super to avoid infinite recursion
        super(Bag, self).__setattr__('_creator', creator) 
        super(Bag, self).__setattr__('_item', item)
        super(Bag, self).__setattr__('_children', [])

    def delete(self):

        # remove creator reference from children
        for child in super(Bag, self).__getattribute__('_children'):
            child._grow_up()

    def _grow_up(self):
        """
        Sets the creator and item variable to None
        :return:
        """
        super(Bag, self).__setattr__('_creator', None)
        super(Bag, self).__setattr__('_item', None)

    def __getattr__(self, item):
        """
        Returns an attribute from the bag or an empty bag (which converts to False) if the item does not exist.
        :param item:
        :return:
        """

        i = self.get(item)
        if i is None:
            # create child
            i = Bag(self, item)
            super(Bag, self).__getattribute__('_children').append(i)
        return i

    def __setattr__(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """

        self[key] = value

        # attach to creator to allow nested item assignment
        # use super to avoid infinite recursion
        creator = super(Bag, self).__getattribute__('_creator')
        if creator is not None:
            creator.__setattr__(super(Bag, self).__getattribute__('_item'), self)
            self._grow_up()


class EventHandler:
    def __init__(self):     #aufgerufen

        # mapping of event name to array with objects which listen to the event
        self.receivers = {}

        # list of event names that may occur
        self.events = ['start']

    def add_component(self, component):     #aufgerufen
        """
        Registers a component in the event bus system.
        :param component: The component
        :return:
        """

        component_class = component.__class__

        # add component to receivers for each event it listens to
        for event in component_class.listens:
            self.receivers.setdefault(event, []).append(component)

        # register events that may occur
        for event in component_class.raises:
            if event not in self.events:
                self.events.append(event)

    def raise_event(self, name, bag):   #aufgerufen
        """
        Raises an event.
        :param name: The event name.
        :param bag: The bag of parameters.
        :return:
        """

        if name in self.receivers:
            for receiver in self.receivers[name]:
                receiver.handle_event(name, bag)

    def check_event_structure(self):   #aufgerufen
        """
        Checks if the current event configuration is valid. Raises an exception if the configuration is invalid.
        :return:
        """

        # check if all events that are required can occur
        for (event, receivers) in self.receivers.items():
            if event not in self.events:
                msg = "Event '%s' is expected by the following component(s), but no component can raise this event: %s"
                classes = ", ".join(receiver.__class__.__name__ for receiver in receivers)
                raise AirhockeyException(msg % (event, classes))


class Component(object):

    listens = []
    raises = []

    def __init__(self, event_handler):   #aufgerufen
        self.event_handler = event_handler

    def handle_event(self, name, bag):    #aufgerufen
        """
        Handles an event. This method calls the handle_event_{name} method.
        :param name: The event name
        :param bag: The parameter bag
        :return:
        """
        method = getattr(self, "handle_event_" + name)
        if method is not None:
            method(bag)


class ComponentManager:
    def __init__(self, event_handler):   #aufgerufen
        self.event_handler = event_handler
        self.components = []

    def _get_class(self, module_name, class_name):   #aufgerufen
        """
        Gets the python class.
        :param class_name: The class name.
        :return:
        """
        try:
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            return class_
        except:
            raise AirhockeyException("Class '%s' not found" % (module_name + "." + class_name))

    def _create_instance(self, config):   #aufgerufen
        """
        Creates an instance of a class.
        :param config: The class name and additional keyword arguments.
        :return: The object
        """

        # split definition into its components
        m = re.search('^((\w+\.)*\w+)\.(\w+)(:((\w+=.*?,)*\w+=.*?))?$', config)
        if not m:
            raise Exception("Configuration '%s' not valid" % config)
        module_name = m.group(1)
        class_name = m.group(3)
        arguments_string = m.group(5)
        arguments = {}
        if arguments_string:
            for argument in arguments_string.split(","):
                argument_parts = argument.split("=")
                arguments[argument_parts[0]] = argument_parts[1]

        # get class and build instance
        class_ = self._get_class(module_name, class_name)
        return class_(self.event_handler, **arguments)

    def create_component(self, name):   #aufgerufen
        """
        Creates a new component and registers this component in the system.
        :param name: The class name of the component.
        :return:
        """
        instance = self._create_instance(name)
        self.event_handler.add_component(instance)
        self.components.append(instance)
        return instance

    def create_from_names(self, names):  #aufgerufen
        """
        Creates components from a names array.
        :param names: An array with component names
        :return:
        """
        for name in names:
            self.create_component(name)

    def check_components(self):    #aufgerufen
        """
        Checks if the current component configuration is valid. Raises an exception if the configuration is invalid.
        :return:
        """

        # at least one component given
        if not len(self.components):
            raise AirhockeyException("At least one component has to be set")

        # first component given should listen to the start event
        first = self.components[0]
        if 'start' not in first.__class__.listens:
            raise AirhockeyException("The first component given must listen to the 'start' event")
