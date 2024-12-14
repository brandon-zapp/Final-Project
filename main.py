import ir_rx
import machine
import math, time
from machine import PWM
from machine import Pin
from ir_rx.nec import NEC_8  # Use the NEC 8-bit class
from ir_rx.print_error import print_error  # for debugging

pwm_rate = 2000
ain1_ph = Pin(12, Pin.OUT)
ain2_en = PWM(13, freq=pwm_rate, duty_u16=0)
bin1_ph = Pin(14, Pin.OUT)
bin2_en = PWM(15, freq=pwm_rate, duty_u16=0)
nick_ph = Pin(16, Pin.OUT)
nick_en = PWM(17, freq=pwm_rate, duty_u16=0)

RF_reciever_1 = Pin(7, Pin.IN)
RF_reciever_2 = Pin(6, Pin.IN)
RF_reciever_3 = Pin(5, Pin.IN)
RF_reciever_4 = Pin(4, Pin.IN)

pwm = min(max(int(2**16 * abs(1)), 0), 65535)

pwm2 = 50000
pwm3 = 26200
# Flag to track the active control source
active_control = None

def ir_callback(data, addr, _):
    global active_control
    active_control = 'IR'  # Set active control to IR

    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")
    if data == 0x05:  # forward on joystick
        print("Motor Forward")  # Print to REPL
        ain1_ph.low()
        ain2_en.duty_u16(pwm3)
        bin1_ph.low()
        bin2_en.duty_u16(pwm3)
    elif data == 0x06:  # backward on joystick
        print("Motor Backward")  # Print to REPL
        ain1_ph.high()
        ain2_en.duty_u16(pwm3)
        bin1_ph.high()
        bin2_en.duty_u16(pwm3)
    elif data == 0x07:  # left on joystick
        print("Motor Left")  # Print to REPL
        ain1_ph.low()
        ain2_en.duty_u16(pwm3)
        bin1_ph.high()
        bin2_en.duty_u16(pwm3)
    elif data == 0x08:  # right on joystick
        print("Motor Right")  # Print to REPL
        ain1_ph.high()
        ain2_en.duty_u16(pwm3)
        bin1_ph.low()
        bin2_en.duty_u16(pwm3)
    elif data == 0x10:
        print ("Fire")
        nick_ph.high()
        nick_en.duty_u16(pwm)
    elif data == 0x09:  # stop
        print("Motor Stopped")  # Print to REPL
        ain1_ph.high()
        ain2_en.duty_u16(0)
        bin1_ph.low()
        bin2_en.duty_u16(0)
        nick_ph.high()
        nick_en.duty_u16(0)

# Setup IR receiver
ir_pin = Pin(18, Pin.IN, Pin.PULL_UP)
ir_receiver = NEC_8(ir_pin, callback=ir_callback)
ir_receiver.error_function(print_error)

while True:
    time.sleep_ms(10)

    # Check RF signals
    if active_control != 'IR':  # Only check RF if IR is not active
        if RF_reciever_1.value() == 1:  # Drive Forward
            print("Drive Forward")
            ain1_ph.high()
            ain2_en.duty_u16(pwm3)
            bin1_ph.low()
            bin2_en.duty_u16(pwm3)
            active_control = 'RF'  # Set active control to RF
            time.sleep(0.5)
        elif RF_reciever_2.value() == 1:  # Drive Left
            print("Turning Left")
            ain1_ph.low()
            ain2_en.duty_u16(pwm3)
            bin1_ph.low()
            bin2_en.duty_u16(pwm3)
            active_control = 'RF'  # Set active control to RF
            time.sleep(0.5)
        elif RF_reciever_3.value() == 1:  # Drive Right
            print("Turning Right")
            ain1_ph.high()
            ain2_en.duty_u16(pwm3)
            bin1_ph.high()
            bin2_en.duty_u16(pwm3)
            active_control = 'RF'  # Set active control to RF
            time.sleep(0.5)
        elif RF_reciever_4.value() == 1:  # Drive Backward
            print("Backwards")
            ain1_ph.low()
            ain2_en.duty_u16(pwm3)
            bin1_ph.high()
            bin2_en.duty_u16(pwm3)
            active_control = 'RF'  # Set active control to RF
            time.sleep(0.5)
        else:
            if active_control == 'RF':  # If last control was RF and no signal is received
                print("Stopped")
                ain1_ph.low()
                ain2_en.duty_u16(0)
                bin1_ph.low()
                bin2_en.duty_u16(0)
                active_control = None  # Reset control

    # Allow switching back to RF control if the IR is inactive
    if active_control == 'IR':
        # You can implement a timeout here if you want IR to have a limited duration
        pass  # IR control will handle its own stopping and motor control



#semi working
# import ir_rx
# import machine
# import math, time
# from machine import PWM
# from machine import Pin
# from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
# from ir_rx.print_error import print_error # for debugging

# pwm_rate = 2000
# ain1_ph = Pin(12, Pin.OUT)
# ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)
# bin1_ph = Pin(14, Pin.OUT)
# bin2_en = PWM(15, freq = pwm_rate, duty_u16 = 0)

# RF_reciever_1 = Pin(7, Pin.IN)
# RF_reciever_2 = Pin(6, Pin.IN)
# RF_reciever_3 = Pin(5, Pin.IN)
# RF_reciever_4 = Pin(4, Pin.IN)

# # RF_enable = Pin(0, Pin.IN)
# # IR_enable = Pin(1, Pin.IN)


# pwm = min(max(int(2**16 * abs(1)), 0), 65535)

# def ir_callback(data, addr, _):
# #    if(IR_enable.value == 0):
# #        return
   
#    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")
#    if data == 0x01: #forward on joystick
#        print("Motor Forward") # Print to REPL
#        ain1_ph.low()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.low()
#        bin2_en.duty_u16(pwm)

#    if data == 0x02: #backward on joytstick
#        print("Stopped") # Print to REPL
#        ain1_ph.high()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.high()
#        bin2_en.duty_u16(pwm)

#    if data == 0x03: #left on joystick
#        print("Motor Left") # Print to REPL
#        ain1_ph.low()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.high()
#        bin2_en.duty_u16(pwm)

#    if data == 0x04: #right on joystick
#        print("Motor Right") # Print to REPL
#        ain1_ph.high()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.low()
#        bin2_en.duty_u16(pwm)
#    if data == 0x05: #right on joystick
#        print("Motor Right") # Print to REPL
#        ain1_ph.high()
#        ain2_en.duty_u16(0)
#        bin1_ph.low()
#        bin2_en.duty_u16(0)

# ir_pin = Pin(18, Pin.IN, Pin.PULL_UP)
# ir_receiver = NEC_8(ir_pin, callback=ir_callback)
# ir_receiver.error_function(print_error)

# while True:
#    pass
# ## Speed can be from 0 to 1
# speed = 1
# pwm = min(max(int(2**16 * speed), 0), 65535)
# instruction = 0b0000


# while True:
   
#    if RF_reciever_1.value() == 1: # Drive Forward
#        print("Drive Forward")
#        ain1_ph.low()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.low()
#        bin2_en.duty_u16(pwm)
#        time.sleep(1)
#    elif RF_reciever_2.value() == 1: # Drive Left
#        print("Turning Left")
#        ain1_ph.low()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.high()
#        bin2_en.duty_u16(pwm)
#        time.sleep(1)
#    elif RF_reciever_3.value() == 1: # Drive Right
#        print("Turning Right")
#        ain1_ph.high()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.low()
#        bin2_en.duty_u16(pwm)
#        time.sleep(1)
#    elif RF_reciever_4.value() == 1: # Drive Backward
#        print("Backwards")
#        ain1_ph.high()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.high()
#        bin2_en.duty_u16(pwm)
#        time.sleep(1)
#    else:
#        print("Stopped")
#        ain1_ph.low()
#        ain2_en.duty_u16(0)
#        bin1_ph.low()
#        bin2_en.duty_u16(0)
# while True:
#     # if(RF_enable.value() == 0):
#     #    print("IR Enabled")
#     #    continue

#     # print("RF Enabled")
   
#    ## Calculate Instruction
#    ## A = 0001
#    ## B = 0010
#    ## C = 0100
#    ## D = 1000
#     instruction = RF_reciever_1.value() | RF_reciever_2.value() << 1 | RF_reciever_3.value() << 2 | RF_reciever_4.value() << 3

#     if instruction == 0b0001: # Drive Forward
#        print("Driving Forward")
#        ain1_ph.low()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.low()
#        bin2_en.duty_u16(pwm)
#       # time.sleep_ms(1000)
#     elif instruction == 0b0010: # Drive Left
#        print("Turning Left")
#        ain1_ph.low()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.low()
#        bin2_en.duty_u16(pwm)
#        #time.sleep_ms(1000)
#     elif instruction == 0b0100: # Drive Right
#        print("Turning Right")
#        ain1_ph.high()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.low()
#        bin2_en.duty_u16(pwm)
#        #time.sleep_ms(1000)
#     elif instruction == 0b1000: # Drive Backward
#        print("Backwards")
#        ain1_ph.high()
#        ain2_en.duty_u16(pwm)
#        bin1_ph.high()
#        bin2_en.duty_u16(pwm)
#        #time.sleep_ms(1000)
#     elif instruction == 0b0000:
#        print("Stopped")
#        ain1_ph.low()
#        ain2_en.duty_u16(0)
#        bin1_ph.low()
#        bin2_en.duty_u16(0)
#        #time.sleep_ms(100)
