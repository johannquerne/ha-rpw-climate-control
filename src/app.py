from api import ApiRequests
import network
import time
from display import Display
import config

class MainApp:

    def __init__(self, active = 0) -> None:
        self.api = ApiRequests()
        self.display = Display()
        self.__connectToWifi()
        self.entities = config.my_entities
        self.setActiveEntity(active)
        self.isAsleep = False

    def __connectToWifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(config.wifi_ssid, config.wifi_pwd)
        while wlan.isconnected() == False:
            print('Waiting for connection...')
            time.sleep(1)

    def getEntityData(self, entity_id):
        #print(self.getActiveEntity())
        climate_info = self.api.getClimateInfo(entity_id)
        return climate_info

    def setActiveEntity(self, entity_id_ref):
        self.active_entity = entity_id_ref
        return True

    def getActiveEntity(self):
        return self.entities[self.active_entity]

    def getNextEntity(self):
        ent_len = len(self.entities)
        temp_ent = None
        if self.active_entity == ent_len - 1:
            temp_ent = 0
        else:
            temp_ent = self.active_entity + 1

        self.setActiveEntity(temp_ent)
        return self.entities[temp_ent]
    
    def getPreviousEntity(self):
        ent_len = len(self.entities)
        temp_ent = None
        if self.active_entity == 0:
            temp_ent = ent_len - 1
        else:
            temp_ent = self.active_entity - 1

        self.setActiveEntity(temp_ent)
        return self.entities[temp_ent]

    def increaseTemperature(self, entity_id, targetTemperature):
        response = self.api.setTargetTemperature(entity_id, targetTemperature)
        return response
    
    def decreaseTemperature(self, entity_id, targetTemperature):
        response = self.api.setTargetTemperature(entity_id, targetTemperature)
        return response

    def displayEntityInfo(self, entity_info):
        self.display.displayInfo(entity_info)
        pass
    
    def sleep(self):
        if not self.isAsleep:
            print("sleep")
            self.display.sleep()
            self.isAsleep = True
        
    def wake(self):
        self.display.wake()
        self.isAsleep = False