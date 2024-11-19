import ir_rx
import machine
import math, time
from machine import PWM
from machine import Pin
#from machine import Pin

from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

RF_reciever_1 = Pin(6, Pin.IN)
RF_reciever_2 = Pin(7, Pin.IN)
RF_reciever_3 = Pin(8, Pin.IN)
RF_reciever_4 = Pin(9, Pin.IN)

pwm_rate = 2000
ain1_ph = Pin(12, Pin.OUT)
ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)
bin1_ph = Pin(10, Pin.OUT)
bin2_en = PWM(11, freq = pwm_rate, duty_u16 = 0)

pwm = min(max(int(2**16 * abs(1)), 0), 65535)

# 0 = Not selected, 1 = IR, 2 = RF
#mode = 0 

#RF_enable = Pin(1, Pin.IN)
#IR_enable = Pin(2, Pin.IN)

'''def ir_callback(data, addr, _):
   print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")
   if data == 0x01: #forward on joystick
       print("Motor Forward") # Print to REPL
       ain1_ph.low()
       ain2_en.duty_u16(pwm)
       bin1_ph.low()
       bin2_en.duty_u16(pwm)

   if data == 0x02: #backward on joytstick
       print("Stopped") # Print to REPL
       ain1_ph.high()
       ain2_en.duty_u16(pwm)
       bin1_ph.high()
       bin2_en.duty_u16(pwm)

   if data == 0x03: #left on joystick
       print("Motor Left") # Print to REPL
       ain1_ph.low()
       ain2_en.duty_u16(pwm)
       bin1_ph.high()
       bin2_en.duty_u16(pwm)

   if data == 0x04: #right on joystick
       print("Motor Right") # Print to REPL
       ain1_ph.high()
       ain2_en.duty_u16(pwm)
       bin1_ph.low()
       bin2_en.duty_u16(pwm)
   if data == 0x05:
       print("Motor Right") # Print to REPL
       ain1_ph.high()
       ain2_en.duty_u16(0)
       bin1_ph.low()
       bin2_en.duty_u16(0)

ir_pin = Pin(17, Pin.IN, Pin.PULL_UP)
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
ir_receiver.error_function(print_error)

while True:
    pass'''
while True:
   '''time.sleep_ms(10)
   if(RF_enable.value() == 1):
       print("RF Mode")
       mode = 1
   elif(IR_enable.value() == 1):
       print("IR Mode")
       mode = 2
 
   if(mode == 1): # RF CONTROLLED'''
   if RF_reciever_1.value() == 1: # Drive Forward
                print("Drive Forward")
                ain1_ph.low()
                ain2_en.duty_u16(pwm)
                bin1_ph.low()
                bin2_en.duty_u16(pwm)    
                time.sleep_ms(100)
   elif RF_reciever_2.value() == 1: # Drive Left
                print("Turning Left")
                ain1_ph.low()
                ain2_en.duty_u16(pwm)
                bin1_ph.high()
                bin2_en.duty_u16(pwm)
                time.sleep_ms(100)
   elif RF_reciever_3.value() == 1: # Drive Right
    print("Turning Right")
    ain1_ph.high()
    ain2_en.duty_u16(pwm)
    bin1_ph.low()
    bin2_en.duty_u16(pwm)
    time.sleep_ms(100)
   elif RF_reciever_4.value() == 1: # Drive Backward
    print("Backwards")
    ain1_ph.high()
    ain2_en.duty_u16(pwm)
    bin1_ph.high()
    bin2_en.duty_u16(pwm)
    time.sleep_ms(100)
   else:
    print("Stopped")
    ain1_ph.low()
    ain2_en.duty_u16(0)
    bin1_ph.low()
    bin2_en.duty_u16(0)
    