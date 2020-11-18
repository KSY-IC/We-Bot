
# -*- coding:utf-8 -*-

#-------------------------------------------------------------------------------------#
# We-Bot Pi Control class for Rev.2 (Ver.0.1 2020/10/31)
#-------------------------------------------------------------------------------------#

'''
## License
The MIT License (MIT)
Copyright (C) 2020  KSY Co.,Ltd.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import time
import pigpio
import smbus2


class WeBot():
    def __init__(self):
        """
        Constructor for webot class
        """
        print("Initialize WeBot Class")
        
        self.i2c = smbus2.SMBus(1)
        self.ADDR = 0x48
        self.REG_VALUE = 0x00
        self.REG_CONFIG = 0x01
        self.MAX_SPEED = 480
        
        self.max_speed = 480

        self.left_offset = 1.0
        self.right_offset = 1.0
        
        self._pigpio = pigpio.pi()
        if not self._pigpio.connected:
            print("Can't connect to pigpio")
            raise IOError("Can't connect to pigpio")
        
        print("connect pigpio.")
        self.pin_EN = 5
        self.pin_FAULT = 6
        self.pin_PWM1 = 12
        self.pin_PWM2 = 13
        self.pin_DIR1 = 24
        self.pin_DIR2 = 25
        
        print("Set FAULT pin to PULL UP.")
        self._pigpio.set_pull_up_down(self.pin_FAULT, pigpio.PUD_UP )
        print("Enable motor driver")
        self._pigpio.write(self.pin_EN, 0)
                
        pass
    
    def enableMotor(self):
        self._pigpio.write(self.pin_EN, 0)
        
    def disableMotor(self):
        self._pigpio.write(self.pin_EN, 1)
        
    def getFault(self):
        return not _pigpio.read(self.pin_FAULT)
    
    def setSpeedOffset(self, offset1, offset2):
        self.left_offset = offset1
        self.right_offset = offset2
    
    def setSpeed(self, speed1, speed2 ):
        dirvalue1 = 0
        dirvalue2 = 0
        if speed1 < 0:
            speed1 = -speed1
            dirvalue1 = 1
        
        if speed2 < 0:
            speed2 = -speed2
            dirvalue2 = 1
        
        if speed1 > self.max_speed:
            speed1 = self.max_speed
            
        if speed2 > self.max_speed:
            speed2 = self.max_speed
        
        speed1 = speed1 * self.left_offset
        speed2 = speed2 * self.right_offset
            
        self._pigpio.write(self.pin_DIR1, dirvalue1)
        self._pigpio.hardware_PWM(self.pin_PWM1, 20000, int(speed1 * 6250 / 3))

        self._pigpio.write(self.pin_DIR2, dirvalue2)
        self._pigpio.hardware_PWM(self.pin_PWM2, 20000, int(speed2 * 6250 / 3))
            

    def setMaxSpeed(self, speed):
        """
        Set maximum speed.
        
        Parameters
        ----------
        speed:int
            Maximum speed (0 - 480)
            
        Returns
        -------
        result:Boolean
            set result. If Parameter set was failed, return False.
        """
        result = False
        if speed <= self.MAX_SPEED and speed > 0:
            self.max_speed = speed
            result = True
        
        return result
    
    def getMaxSpeed(self):
        """
        Get maximum speed.
        
            
        Returns
        -------
        max_speed:float
            return current maximum speed.
        """
        return self.max_speed
            

    def stop(self):
        """
        Stop Motors.        
        """
        self.setSpeed(0,0)

    def forward(self, speed):
        """
        Go forward.
        
        Parameters
        ----------
        speed:int
            move speed (0 - 480)
            
        Returns
        -------
        result:Boolean
            excecute result. If Parameter set was failed, return False.
        """
        self.setSpeed(speed, speed)
        
        return True

    def back(self, speed):
        """
        Go back.
        
        Parameters
        ----------
        speed:int
            move speed (0 - 480)
            
        Returns
        -------
        result:Boolean
            excecute result. If Parameter set was failed, return False.
        """
        if speed > 0:
            speed = -speed
                    
        self.setSpeed(speed, speed)
        
        return True

    def left(self,speed):
        """
        Turn left.
        
        Parameters
        ----------
        speed:int
            move speed (0 - 480)
            
        Returns
        -------
        result:Boolean
            excecute result. If Parameter set was failed, return False.
        """
        self.setSpeed(speed, -speed)
        
        return True

    def right(self, speed):
        """
        Turn right.
        
        Parameters
        ----------
        speed:int
            move speed (0 - 480)
            
        Returns
        -------
        result:Boolean
            excecute result. If Parameter set was failed, return False.
        """
        self.setSpeed(-speed, speed)
        
        return True


    def readVoltage( self, port ):
        """
        Read ADC Voltage.
        
        Parameters
        ----------
        port:int
            ADC Port(0-3)
            
        Returns
        -------
        result:float
            read value(V).
        """
        data_byte = [0x00, 0x00]
    
        ratio = 1.0
    
        os = 1 << 15
        mux = 0
        if port == 0:
            mux = 4 << 12
            ratio = 3.0
        elif port == 1:
            mux = 5 << 12
            ratio = 3.0
        elif port == 2:
            mux = 6 << 12
            ratio = 11.0
        elif port == 3:
            mux = 7 << 12
            ratio = 3.0
        else:
            return -1.0
    
        pga = 2 << 9
        mode = 1 << 8
    
        dr = 4 << 5
        rsv = 3
    
        data = os | mux | pga | mode | dr | rsv
    
        data_byte[0] = (data >> 8) & 0xFF
        data_byte[1] = (data & 0xFF)
    
        self.i2c.write_i2c_block_data(self.ADDR, self.REG_CONFIG, data_byte)
        time.sleep(0.1)
        value = self.i2c.read_i2c_block_data(self.ADDR, self.REG_VALUE, 2)
    
        voltage = value[0] * 256 + value[1]
        voltage = voltage >> 4
    
        voltage = (voltage * ratio) / 1000
    
        print(voltage)
    
        return voltage




# -------------
# Test Module
# -------------
def testcase():
    webot = WeBot()
    
    print(webot.getMaxSpeed())
    webot.setMaxSpeed(300)
    print(webot.getMaxSpeed())
    webot.setMaxSpeed(480)

    print(webot.readVoltage(0))
    print(webot.readVoltage(1))
    print(webot.readVoltage(2))
    print(webot.readVoltage(3))
    
    webot.forward(480)
    time.sleep(1)
    webot.stop()
    time.sleep(1)
    webot.back(480)
    time.sleep(1)
    webot.stop()
    
    time.sleep(1)

    webot.left(480)
    time.sleep(1)
    webot.stop()
    time.sleep(1)
    webot.right(480)
    time.sleep(1)
    webot.stop()

    

if __name__ == '__main__':
    testcase()
    