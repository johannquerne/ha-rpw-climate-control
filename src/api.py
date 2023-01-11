import urequests as requests
import config
import gc

class ApiRequests:

    def __init__(self) -> None:
        self.ha_baseurl = config.ha_baseurl
        self.api_token = config.ha_token

    def getClimateInfo(self, entity_id) -> str:

        response = self.apiRequest("/api/states/" + entity_id)

        if not response.status_code == 200:
            raise Exception(f"API request failed - response code {str(response.status_code)}")
        
        climateJson = response.json()
        climateData = {
            "name": climateJson["attributes"]["friendly_name"],
            "current_temp": climateJson["attributes"]["current_temperature"],
            "target_temp": climateJson["attributes"]["temperature"],
            "current_preset": climateJson["attributes"]["preset_mode"],
            "supported_presets": climateJson["attributes"]["preset_modes"],
            "hvac_action": climateJson["attributes"]["hvac_action"],
            "state": climateJson["state"]
        }
        climateJson = None
        gc.collect()
        return climateData

    def setTargetTemperature(self, entity_id, targetTemperature):
        payload = {"entity_id": entity_id, "temperature": targetTemperature}
        response = self.apiRequest("/api/services/climate/set_temperature", payload, "POST")
        r = response.status_code
        response = None
        gc.collect()
        return r

    def switchOnOff(self, entity_id, state="OFF"):
        payload = {"entity_id": entity_id}

        action = None
        if state == "ON":
            action = "turn_on"
        elif state == "OFF":
            action = "turn_off"
        
        response = self.apiRequest("/api/services/climate/" + action, payload, "POST")
        return response.status_code

    def apiRequest(self, endpoint, payload=None, method="GET"):

        url = self.ha_baseurl + endpoint

        headers = {
            "Authorization": "Bearer " + self.api_token,
            "content-type": "application/json"
        }

        response = None

        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=payload)
        except OSError as err:
            print("OS error:", err)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise       

        return response

