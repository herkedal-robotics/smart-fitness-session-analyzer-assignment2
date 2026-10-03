"""
store one smartwatch measurement
"""
class Observation():
    def __init__(self,
                 timestamp,
                 heart_rate,
                 skin_response,
                 temperature,
                 activity_level,
                 signal_quality):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality

    def is_valid(self):
        """
        we want a structure that:
        checks heart rate:
            if not ... return False
            if < 0 return False
        checks activity level:
            if < 0 return False
            ...
        checks signal quality:
            if bad return False
            ...
        return True
        """
        #if self.heart_rate == None:
        if not isinstance(self.heart_rate, (int, float)):
            return False
        if self.heart_rate < 35 or self.heart_rate > 205:
            return False
        #checks acitivity level:
        if not isinstance(self.activity_level,(int,float)):
            return False
        if self.activity_level < 0 or self.activity_level > 1:
            return False
        #checks temperature:
        if not isinstance(self.temperature, (int,float)):
            return False
        if self.temperature < 25 or self.temperature > 42:
            return False
        #checks skin response:
        if not isinstance(self.skin_response, (int,float)):
            return False
        if self.skin_response < 0:
            return False
        #checks signal quality:
        if not isinstance(self.signal_quality,(int,float)):
            return False
        if self.signal_quality < 0.7 or self.signal_quality > 1:
            return False
        # Check timestamp
        if not isinstance(self.timestamp, int):
            return False
        if self.timestamp < 0:
            return False
        return True


if __name__ == "__main__":

    observation1 = Observation(0, 78, 1.5, 32.5, 0.5, 0.9)
    observation2 = Observation(1, 265, 1.5, 32.5, 0.5, 0.9)
    observation3 = Observation(2, None, 1.5, 32.5, 0.5, 0.9)
    observation4 = Observation(3, -35, 1.5, 32.5, 0.5, 0.9)

    print(observation1.is_valid())
    print(observation2.is_valid())
    print(observation3.is_valid())
    print(observation4.is_valid())