from feline import *

logger = FuncLogger(name="Test Logger", time_tracking=True)
cl = ClassLogger(name="Test Class Logger", time_tracking=True)
me = MethodLogger(name="Test Method Logger", time_tracking=True)

@logger.info(enabled=True)
def do_smth():
    print('do smth')

@logger.error
def throw_error():
    raise ValueError('Throw error')

class Dog:
    def __init__(self, name):
        self.name = name

    @me.info(enabled=True)
    def bark(self):
        print('bark')


#do_smth()
#throw_error()
dog = Dog('Dog')
dog.bark()