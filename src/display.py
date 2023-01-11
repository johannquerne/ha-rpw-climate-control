from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332
import jpegdec
import gc
from pimoroni import RGBLED

class Display:

    def __init__(self) -> None:
        gc.enable()
        self.led = RGBLED(6, 7, 8)
        self.led.set_rgb(100, 100, 100)
        self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB332, rotate=0)
        self.display.set_backlight(0.8)
        self.display.set_font("bitmap8")

        self.BLACK = self.display.create_pen(0, 0, 0)
        self.WHITE = self.display.create_pen(255, 255, 255)
        self.BG = self.display.create_pen(212, 158, 155)
        self.INACTIVE = self.display.create_pen(190, 195, 195)
        self.HEAT = self.display.create_pen(244, 135, 5)

        self.WIDTH, self.HEIGHT = self.display.get_bounds()

    def sleep(self):
        self.display.set_backlight(0)
        self.display.set_pen(self.BLACK)
        self.display.clear()
        self.display.update()
        
    def wake(self):
        self.display.set_backlight(0.8)

    def displayInfo(self, entity_info):
        #print(entity_info)
        self.__displayHeader(entity_info["name"])
        
        climate_sate = "On"
        
        if entity_info["state"] == "off":
            self.display.set_pen(self.INACTIVE)
            #self.led.set_rgb(190, 195, 195)
            climate_sate = "Off"
        elif entity_info["hvac_action"] == "idle":
            self.display.set_pen(self.WHITE)
            #self.led.set_rgb(244, 135, 5)
            climate_sate = "Idle"
        else:
            self.display.set_pen(self.HEAT)
            
        self.display.text(str(entity_info["target_temp"]) + "°C", 10, 50, self.WIDTH, scale=6)
        self.display.text("(" + climate_sate + ")", 170, 78, self.WIDTH, scale=2)
        
        self.display.text("Room " + str(entity_info["current_temp"]) + "°C", 10, 110, self.WIDTH, scale=2)
        
        self.display.update()
        
        pass

    def __displayHeader(self, name):
        
        self.display.set_pen(self.BG)
        self.display.rectangle(1, 1, self.WIDTH, self.HEIGHT)
        self.display.set_pen(self.WHITE)
        self.display.text(name, 10, 5, self.WIDTH, scale=3)
        
        return True

    def displayMsg(self, msg=None):
        self.display.set_pen(self.WHITE)
        self.display.rectangle(1, 1, self.WIDTH-1, 30)
        self.display.set_pen(self.WHITE)
        self.display.text(msg, 3, 5, 200, scale=2)
        
        # Create a new JPEG decoder for our PicoGraphics
        j = jpegdec.JPEG(self.display)

        # Open the JPEG file
        j.open_file("heat.jpg")

        # Decode the JPEG
        j.decode(0, 30, jpegdec.JPEG_SCALE_FULL)
        
        self.display.update()
        return True