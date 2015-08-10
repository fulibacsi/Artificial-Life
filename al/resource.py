# encoding: utf-8


# resources
class Resource():

    # init
    def __init__(self, id, value, rate):
        self.id = id
        self.type = 'res'
        self.value = value
        self.rate = rate

    # what happens, when consumed
    def consume(self):
        self.value -= 1.0
        # only return the leftover
        if self.value <= 0.0:
            temp = 1.0 + self.value
            self.value = 0.0
            return temp
        return 1.0

    # for one round, this happens to the resource
    def tick(self):
        self.value *= self.rate
