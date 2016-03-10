import sys
from common import EventHandler, ComponentManager, Bag, AirhockeyException


try:
    protokoll=open("protokoll.txt","w")
    protokoll.close()
    # create objects
    event_handler = EventHandler()
    component_manager = ComponentManager(event_handler)

    # add components specified in argv
    component_manager.create_from_names(sys.argv[1:])

    # check if the component configuration is valid
    component_manager.check_components()
    event_handler.check_event_structure()

    bag = Bag()
    while True:

        # invoke start event
        event_handler.raise_event('start', bag)

        # use 'next' property from bag to define new bag
        # cool thing: if next is not set, bag.next returns a new bag
        old_bag = bag
        bag = bag.next
        old_bag.delete()

except KeyboardInterrupt:
    pass
except AirhockeyException as e:
    print("ERROR:")
    print(e)
except RuntimeError:
    pass