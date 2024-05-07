import random
import math


class Util:
    @staticmethod
    def generate_identifiers():
        digits = "0123456789"
        identifier = "EE-"
        for i in range(6):
            identifier += digits[math.floor(random.random() * 10)]
            
        print(identifier)
        return identifier