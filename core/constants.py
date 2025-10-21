# model constants
model_2WD = 2
model_4WD = 1
model = model_2WD
 
# msgserver constants
server_ipaddr = '0.0.0.0'
server_port = 8123
server_timeout = 0.1
server_backlog = 5
server_debug = False
 
# task ids
motorFlTaskID = 1
motorFrTaskID = 2
motorRlTaskID = 3
motorRrTaskID = 4
sensorTaskID = 5
timerTaskID = 6
dispTaskID = 7
keyTaskID = 8

# i2c pins
i2cSdaPin = 21
i2cSclPin = 22
i2cFreq = 400000

# lcd address
lcd_addr = 0x27
# timer task
timer_delay = 5

# motor task
if model == model_2WD:
    motor_numMotors = 2
    motor_numMotorControl = 1
    motor_encoderPins = [27, 26, 0, 0]
    motor_addr = [0x60,0]
else:
    motor_numMotors = 4
    motor_numMotorControl = 2
    motor_encoderPins = [27, 26, 0, 0]
    motor_addr = [0x60,0]

motor_flM = 0 # front left motor
motor_frM = 1 # front right motor
motor_rlM = 2 # rear left motor
motor_rrM = 3 # rear right motor
motor_pos = [2,0,3,1]
motor_waitforCon = 3
motor_max = 4000
motor_base = 500
motor_freq = 500 #1600
motor_loopDelay = 100
motor_spinupDelay = 1.5
motor_stopDelay = 500
motor_P = 100
motor_M = 2
motor_S = 2.65


# sensor task
sensor_addrPins = [10,11,12]
sensor_pcf_addr = 0x20
sensor_enablePin = 13
sensor_triggerPin = 2
sensor_echoPin = 5
sensor_numSensors = 6
sensor_readDelay = 10
sensor_waitforCon = 3
sensor_taskDelay = 1  # 0.25

# disp task
disp_fl = 5
disp_fc = 0
disp_fr = 1
disp_cl = 4
disp_cr = 2
disp_rl = 6
disp_rc = 3
disp_rr = 7
disp_taskDelay = 1

# key task
key_pcf_addr = 0x21


