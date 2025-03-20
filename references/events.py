from evdev import InputDevice, categorize, ecodes
dev = InputDevice('/dev/input/event3')

with dev.grab_context():
    for event in dev.read_loop():
        # if event.type == ecodes.EV_KEY:
            # print(categorize(event))
        print(event)
