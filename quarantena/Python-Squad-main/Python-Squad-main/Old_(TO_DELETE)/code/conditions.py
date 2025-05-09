import util
import numpy as np
import pandas as pd
import math

_excel2bikeinfo_attributes = {"Vehicle": "bike", "Driver": "driver", "Wheels": "wheels", "GearBox": "gear_box"}   #conversion from Excel name (in conditions file) to BikeInfo attribute name

class Vehicle:
    '''Contains information of a vehicle (bike)'''
    def __init__(self,name=None,chassis_weight=None,hull_weight=None,frontal_area=None,inertia=None,leg_traction=None,crank=None):
        '''name: String'''
        self.name = name
        self.chassis_weight = chassis_weight   #peso telaio
        self.hull_weight = hull_weight   #peso carena
        self.frontal_area = frontal_area
        self.inertia = inertia
        self.leg_traction = leg_traction
        self.crank = crank   #pedivella
        self._string_attributes = ["name"]

    def setInfo(self,name=None,chassis_weight=None,hull_weight=None,frontal_area=None,inertia=None,leg_traction=None,crank=None):
        '''
        chassis_weight: Float
        hull_weight: Float
        frontal_area: Float
        inertia: Float
        leg_traction: Bool
        crank: Float (length)'''
        if name is not None:
            self.name = name
        if chassis_weight is not None:
            self.chassis_weight = chassis_weight   #peso telaio
        if hull_weight is not None:
            self.hull_weight = hull_weight   #peso carena
        if frontal_area is not None:
            self.frontal_area = frontal_area
        if inertia is not None:
            self.inertia = inertia
        if leg_traction is not None:
            self.leg_traction = leg_traction
        if crank is not None:
            self.crank = crank

    def getInfoFromMatrix(self, matrix, delimiter=','):
        '''
        matrix: 2D Array-like (attribute, value)
        '''
        for attribute, value in matrix:
            if value != '':
                if attribute not in self._string_attributes:
                    value = float(value)
            try:
                setattr(self, attribute, value)
            except AttributeError:
                print(f"Object has no attribute {attribute}")
                
    def getInfoFromDict(self, dictionary={}):
        '''
        dict: Dict Object
        '''
        if not dictionary=={}:
            for key in dictionary.keys():
                try:
                    setattr(self, key, dictionary.get(key))
                except AttributeError:
                    print(f"Object has no attribute {key}")

class GearBox:
    def __init__(self, gear_box=None, chainring=None, sec_ratio=None):
        '''
        gear_box: List of gear
        chainring: Integer
        sec_ratio: pair of Integers
        '''
        self.gear_box = gear_box
        self.chainring = chainring   #moltiplica
        self.sec_ratio = sec_ratio   #secondary ratio / rimando finale
        self._string_attributes = []
        self._list_attributes = ["gear_box", "sec_ratio"]

    def setInfo(self, gear_box=None, chainring=None, sec_ratio=None):
        '''
        chainring: Int (number of theet)
        sec_ratio: 2D Iterable (number of theet, es. [greatest, lowest])
        '''
        if gear_box is not None:
            self.gear_box = gear_box
        if chainring is not None:
            self.chainring = chainring
        if sec_ratio is not None:
            self.sec_ratio = sec_ratio
        
    def getInfoFromMatrix(self, matrix, delimiter=','):
        '''
        matrix: 2D Array-like (attribute, value)
        '''
        for attribute, value in matrix:
            if value != '':
                if attribute not in self._string_attributes:
                    if attribute in self._list_attributes:
                        value = [int(num) for num in value.split(delimiter)]
                    else:
                        value = int(value)
            try:
                setattr(self, attribute, value)
            except AttributeError:
                print(f"Object has no attribute {attribute}")
                
    def getInfoFromDict(self, dictionary={}):
        '''
        dict: Dict Object
        '''
        if not dictionary=={}:
            for key in dictionary.keys():
                try:
                    setattr(self, key, dictionary.get(key))
                except AttributeError:
                    print(f"Object has no attribute {key}")

class Wheels:
    '''Contains information of a wheel (of a bike)'''
    def __init__(self,tyre=None,pressure=None,radius=None,rolling_circum=None,inertia=None):
        self.tyre = tyre
        self.pressure = pressure
        self.radius = radius
        self.rolling_circum = rolling_circum   #circonferenza di rotolamento
        self.inertia = inertia
        self._string_attributes = ["tyre"]


    def setInfo(self,tyre=None,pressure=None,radius=None,rolling_circum=None,inertia=None):
        '''
        pressure: Float
        radius: Float
        rolling_circum: Float
        inertia: Float
        '''
        if tyre is not None:
            self.tyre = tyre
        if pressure is not None:
            self.pressure = pressure
        if radius is not None:
            self.radius = radius
        if rolling_circum is not None:
            self.rolling_circum = rolling_circum
        if inertia is not None:
            self.inertia = inertia

    def getInfoFromMatrix(self, matrix, delimiter=','):
        '''
        matrix: 2D Array-like (attribute, value)
        '''
        for attribute, value in matrix:
            if value != '':
                if attribute not in self._string_attributes:
                    value = float(value)
            try:
                setattr(self, attribute, value)
            except AttributeError:
                print(f"Object has no attribute {attribute}")
                
    def getInfoFromDict(self, dictionary={}):
        '''
        dict: Dict Object
        '''
        if not dictionary=={}:
            for key in dictionary.keys():
                try:
                    setattr(self, key, dictionary.get(key))
                except AttributeError:
                    print(f"Object has no attribute {key}")

class Driver:
    '''Contains information of a driver (of a bike)'''
    def __init__(self,name=None,weight=None):
        self.name = name
        self.weight = weight
        self._string_attributes = ["name"]   #List of attributes that are String, not numbers

    def setInfo(self,name=None,weight=None):
        '''weight: Float'''
        if name is not None:
            self.name = name
        if weight is not None:
            self.weight = weight

    def getInfoFromMatrix(self, matrix, delimiter=','):
        '''
        matrix: 2D Array-like (attribute, value)
        '''
        for attribute, value in matrix:
            if value != '':
                if attribute not in self._string_attributes:
                    value = float(value)
            try:
                setattr(self, attribute, value)
            except AttributeError:
                print(f"Object has no attribute {attribute}")
                
    def getInfoFromDict(self, dictionary={}):
        '''
        dict: Dict Object
        '''
        if not dictionary=={}:
            for key in dictionary.keys():
                try:
                    setattr(self, key, dictionary.get(key))
                except AttributeError:
                    print(f"Object has no attribute {key}")

class AtmConditions:
    '''Contains information of atmospheric conditions'''
    def __init__(self,temperature=None,pressure=None,humidity=None,wind=None,angle=None):
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.wind = wind
        self.angle = angle   #clockwise?

    def setInfo(self,temperature=None,pressure=None,humidity=None,wind=None,angle=None):
        '''
        temperature: Iterable of Float
        pressure: Iterable of Float
        humidity,: Iterable of Float
        wind: Iterable of Float
        angle: Iterable of Float
        '''
        if temperature is not None:
            self.temperature = temperature
        if pressure is not None:
            self.pressure = pressure
        if humidity is not None:
            self.humidity = humidity
        if wind is not None:
            self.wind = wind
        if angle is not None:
            self.angle = angle

    def getInfoFromCsv(self):
        pass

    def getInfoFromDict(self, dictionary={}):
        '''
        dict: Dict Object
        '''
        if not dictionary=={}:
            for key in dictionary.keys():
                try:
                    setattr(self, key, dictionary.get(key))
                except AttributeError:
                    print(f"Object has no attribute {key}")

class BikeInfo:
    '''Contains all information of Bike and Driver'''
    def __init__(self, vehicle_obj=Vehicle(), driver_obj=Driver(), wheels_obj=Wheels(), gear_box_obj=GearBox()):
        self.bike = vehicle_obj
        self.driver = driver_obj
        self.wheels = wheels_obj
        self.gear_box = gear_box_obj   #sprocket pack / pacco pignoni

    def setInfo(self, vehicle_obj=None, driver_obj=None, wheels_obj=None, gear_box_obj=None):
        if vehicle_obj is not None:
            self.bike = vehicle_obj
        if driver_obj is not None:
            self.driver = driver_obj
        if wheels_obj is not None:
            self.wheels = wheels_obj
        if gear_box_obj is not None:
            self.gear_box = gear_box_obj

    def getInfoFromExcel(self, file_name):
        column_names = ["attribute", "value"]
        df = pd.read_excel(file_name, header=None, names=column_names)
        # Delete void rows (NaN)
        df = df.dropna(axis=0, how='all')
        for attribute, value in df.values:
            if attribute in _excel2bikeinfo_attributes.keys():
                obj_name = _excel2bikeinfo_attributes[attribute]
                obj = getattr(self,obj_name)
            else:
                # if pd.isna(value):   #comment these 2 lines if
                #     value=""   #you want nan instead of "" (change "getInfoFromCsv" too)
                obj.getInfoFromMatrix([[attribute,value]],delimiter=';')

    def getInfoFromCsv(self, csv_file):
        '''
        csv_file: String (path)
        '''
        data, dummy = util.readCsvFile(csv_file, delimiter=';')
        
        for row in data:
            attribute = row[0]
            value = row[1]
            if str(attribute).strip()=="":
                pass
            elif attribute in _excel2bikeinfo_attributes.keys():
                obj_name = _excel2bikeinfo_attributes[attribute]
                obj = getattr(self,obj_name)
            else:
                if value=="":   #comment these 2 lines if
                    value = math.nan   #you wnat "" instead of nan (change "getInfoFromExcel" too)
                obj.getInfoFromMatrix([[attribute,value]])
        

