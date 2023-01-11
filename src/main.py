import utime as time
from api import ApiRequests
from app import MainApp
from pimoroni import Button

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

entity_info = None

try:
    app = MainApp()
    entity_info = app.getEntityData(app.getActiveEntity())
    app.displayEntityInfo(entity_info)

    #entity_info = app.getEntityData(app.getPreviousEntity())
    #toggle_on = test.switchOnOff(my_entities[0], "ON")
    #toggle_off = test.switchOnOff(my_entities[0], "OFF")
    #setTemp = test.setTargetTemperature(my_entities[0], 19)

    start = time.ticks_ms()

    while True:
        
        if time.ticks_diff(time.ticks_ms(), start) >= 30000:
            app.sleep()
            if button_a.read() or button_b.read() or button_x.read() or button_y.read():
                start = time.ticks_ms()
                app.wake()
                entity_info = app.getEntityData(app.getActiveEntity())
                app.displayEntityInfo(entity_info)
        else:
            if button_a.read():
    #             print("button A pressed")
                start = time.ticks_ms()
                entity_info = app.getEntityData(app.getPreviousEntity())
                app.displayEntityInfo(entity_info)
            elif button_b.read():
    #             print("button B pressed")
                start = time.ticks_ms()
                entity_info = app.getEntityData(app.getNextEntity())
                app.displayEntityInfo(entity_info)
            elif button_x.read():
    #             print("button X pressed")
                start = time.ticks_ms()
                app.increaseTemperature(app.getActiveEntity(), float(entity_info["target_temp"])+0.5)
                entity_info = app.getEntityData(app.getActiveEntity())
                app.displayEntityInfo(entity_info)
            elif button_y.read():
    #             print("button Y pressed")
                start = time.ticks_ms()
                app.decreaseTemperature(app.getActiveEntity(), float(entity_info["target_temp"])-0.5)
                entity_info = app.getEntityData(app.getActiveEntity())
                app.displayEntityInfo(entity_info)
            
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Goodbye")
except AssertionError as error:
    print(error)
