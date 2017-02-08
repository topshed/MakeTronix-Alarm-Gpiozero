from gpiozero import Button, PWMLED, MotionSensor, Buzzer
from time import sleep

# Setup all the GPIO pins and their devices
led = PWMLED(18)
buzzer = Buzzer(15)
pir = MotionSensor(14)
button1 = Button(3)
button2 = Button(27)
button3 = Button(7)
button4 = Button(4)
button5 = Button(22)
button6 = Button(8)
button7 = Button(17)
button8 = Button(10)
button9 = Button(25)
button0 = Button(9)
button_del = Button(11)

# create a dictionary of all the numerical buttons
# and their values
buttons = {button1 : '1',
           button2 : '2',
           button3 : '3',
           button4 : '4',
           button5 : '5',
           button6 : '6',
           button7 : '7',
           button8 : '8',
           button9 : '9',
           button0 : '0'}

setPIN = ['1','2','3','4'] # Default unlock code for the alarm

# Read 4 button presses. DEL button act as as 'backspace':
#  but if you get the last number wrong you can't undo!
def get_4_digits():
    entered=[] # list to store entered numbers
    button_del.when_pressed = lambda : entered.pop() if len(entered) > 0 else False
    for b in buttons: # set a function for every button in buttons list
        b.when_pressed = lambda b: entered.append(buttons[b])
    pressed_keys = 0 # keeps track of how many numbers have been entered
    while len(entered) < 4: # keep waiting until 4 numbers entered
        if len(entered) != pressed_keys:
             buzzer.beep(on_time=0.2, off_time=0.2,n=1) # beep every time button is pressed
             pressed_keys = len(entered)
    buzzer.beep(on_time=0.2, off_time=0.2,n=1)
    return(entered)

# Givesa 10 second window to eneter the correct code
# LED flashes faster and faster as countdown goes on
def countdown():
    counter = 10 # start at 10
    led.off()
    while (not disabled) and (counter > 0):
        counter -=1
        sleep(1)
        print(counter)
        led.blink(on_time=0.4,off_time=0.4,n=1)
    # whne time is up, start beeping!
    if not disabled:
        buzzer.beep(on_time=0.5,off_time=0.5)
        led.on()

print('ready')
disabled = False
led.pulse(fade_in_time=1, fade_out_time=1) # LED glows to show alarm is active
pir.when_motion = countdown # start countdown when motion detected
pir.wait_for_motion()
print('alarm')
PIN = get_4_digits() # wait for buttons presees
if PIN == setPIN: # if the code was correct....
    print('pin ok')
    led.off()
    disabled = True  # ... disable the alarm
