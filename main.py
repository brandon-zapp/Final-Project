import ir_rx
import machine
import math, time
from machine import PWM
from machine import Pin
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging

pwm_rate = 2000
ain1_ph = Pin(12, Pin.OUT)
ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)
bin1_ph = Pin(10, Pin.OUT)
bin2_en = PWM(11, freq = pwm_rate, duty_u16 = 0)

RF_reciever_1 = Pin(6, Pin.IN)
RF_reciever_2 = Pin(7, Pin.IN)
RF_reciever_3 = Pin(8, Pin.IN)
RF_reciever_4 = Pin(9, Pin.IN)

RF_enable = Pin(0, Pin.IN)
IR_enable = Pin(1, Pin.IN)

pwm_rate = 2000
ain1_ph = Pin(12, Pin.OUT)
ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)
bin1_ph = Pin(10, Pin.OUT)
bin2_en = PWM(11, freq = pwm_rate, duty_u16 = 0)

pwm = min(max(int(2**16 * abs(1)), 0), 65535)

def ir_callback(data, addr, _):
   if(IR_enable.value == 0):
       return
   
   print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")
   if data == 0x01: #forward on joystick
       print("Motor Forward") # Print to REPL
       ain1_ph.low()
       ain2_en.duty_u16(pwm)
       bin1_ph.low()
       bin2_en.duty_u16(pwm)

   if data == 0x02: #backward on joytstick
       print("Stopped") # Print to REPL
       ain1_ph.low()
       ain2_en.duty_u16(0)
       bin1_ph.low()
       bin2_en.duty_u16(0)

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

ir_pin = Pin(17, Pin.IN, Pin.PULL_UP)
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
ir_receiver.error_function(print_error)

## Speed can be from 0 to 1
speed = 1
pwm = min(max(int(2**16 * speed), 0), 65535)
instruction = 0b0000

while True:
   if(RF_enable.value() == 0):
       print("IR Enabled")
       continue

   print("RF Enabled")
   
   ## Calculate Instruction
   ## A = 0001
   ## B = 0010
   ## C = 0100
   ## D = 1000
   instruction = RF_reciever_1.value() | RF_reciever_2.value() << 1 | RF_reciever_3.value() << 2 | RF_reciever_4.value() << 3

   if instruction == 0b0001: # Drive Forward
       print("Driving Forward")
       ain1_ph.low()
       ain2_en.duty_u16(pwm)
       bin1_ph.high()
       bin2_en.duty_u16(pwm)
       time.sleep_ms(1000)
   elif instruction == 0b0010: # Drive Left
       print("Turning Left")
       ain1_ph.low()
       ain2_en.duty_u16(pwm)
       bin1_ph.high()
       bin2_en.duty_u16(pwm)
       time.sleep_ms(1000)
   elif instruction == 0b0100: # Drive Right
       print("Turning Right")
       ain1_ph.high()
       ain2_en.duty_u16(pwm)
       bin1_ph.low()
       bin2_en.duty_u16(pwm)
       time.sleep_ms(1000)
   elif instruction == 0b1000: # Drive Backward
       print("Backwards")
       ain1_ph.high()
       ain2_en.duty_u16(pwm)
       bin1_ph.high()
       bin2_en.duty_u16(pwm)
       time.sleep_ms(1000)
   elif instruction == 0b0000:
       print("Stopped")
       ain1_ph.low()
       ain2_en.duty_u16(0)
       bin1_ph.low()
       bin2_en.duty_u16(0)
       time.sleep_ms(100)
