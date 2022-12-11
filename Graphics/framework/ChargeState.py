import pysdl2.sdl2 as sdl2
import pysdl2.sdl2.keycode as keycode
import enum
import Globals as globs
class ChargeStater(enum.Enum):
    Idle = 1
    Charge = 2
    Fired = 3
    cooldown = 4

class ChargeStateMachine:

    def __init__(self):

        self.currentState = ChargeStater.Idle
        self.chargeTime = 0
        self.cooldown = False
        self.cooldownTime = 0.5
    def update(self,keysBefore,keysAfter,elapsed):

        if self.currentState == ChargeStater.Idle:
            if (keycode.SDLK_SPACE in keysAfter and keycode.SDLK_SPACE not in keysBefore):
                self.currentState = ChargeStater.Charge

        if self.currentState == ChargeStater.Charge:
            self.chargeTime += elapsed * 3.0
            
            if self.chargeTime > 1:
                self.chargeTime - 1
        
        if self.currentState == ChargeStater.Charge:
            if (keycode.SDLK_SPACE not in keysAfter and keycode.SDLK_SPACE in keysBefore):
                cur_charrge = self.chargeTime
                self.chargeTime = 0
                self.currentState = ChargeStater.cooldown
                self.cooldown = True
                self.cooldownTime = 0.5
                # Create a bullet
                return cur_charrge
        
        if self.currentState == ChargeStater.cooldown:
            
            self.cooldownTime -= elapsed / 2

        if self.cooldownTime <= 0:
            self.cooldown = False
            self.currentState = ChargeStater.Idle
            self.cooldownTime = 0.5
