from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time
import os

# volume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

scalarVol = int(volume.GetMasterVolumeLevelScalar() * 100)

# time

totalTime = 0
delayTime = 0
loweringType = ''
intervalToLower = 0  # the time between every new lowering, determined by the lowering type
deltaMain = 0  # time passed since the beginning of the program


def main():
    print('* -------------------------------------------- *')
    print('* ------------ - Lower to Sleep - ------------ *')
    print('* -Lower the speakers volume and let me sleep- *')
    print('* ------------ by Gabriel Schulte ------------ *')
    print('* -------------------------------------------- *')

    global scalarVol
    global totalTime
    global delayTime
    global loweringType
    global intervalToLower

    totalTimeMin = convert_int_value('Enter total time in minutes: ')
    totalTime = totalTimeMin * 60

    delayTimeMin = convert_int_value('Enter delay time in minutes: ')
    delayTime = delayTimeMin * 60

    # time left to lower the volume
    timeLeft = totalTime - delayTime

    loweringType = input(
        'Choose the lowering type ([i]nterpolated/[t]ime given): ')

    intervalToLower = {
        # the number of times the volume will have to decrease to reach zero within the time left
        'i': lambda: timeLeft / scalarVol,
        't': lambda: convert_int_value(
            'Enter the interval time to lower the volume in seconds: ')
    }.get(loweringType, lambda: timeLeft / scalarVol)()

    global deltaMain
    timeSec = 0
    timeInterval = 0

    # sets to true if the delay time is reached
    canLower = False

    # start counting the time here
    startTime = time.clock()

    render()

    # the main loop
    while deltaMain < totalTime:
        # updates the total time running
        deltaMain = time.clock() - startTime

        # updates the delta for seconds counter
        deltaSec = deltaMain - timeSec

        # if one second has passed, prints the current status
        if (deltaSec > 1):
            render()
            timeSec = time.clock()

        # lowering volume time

        if canLower == False:
            if deltaMain > delayTime:
                canLower = True
                timeInterval = time.clock()
        else:
            deltaInterval = deltaMain - timeInterval

            if deltaInterval > intervalToLower:
                scalarVol -= 1
                volume.SetMasterVolumeLevelScalar(scalarVol / 100, None)
                timeInterval = time.clock()

    render()


def render():
    os.system('cls')  # clear the console (Windows)

    # total, delay and interval times
    print('Total time:', int(totalTime / 60), 'min')
    print('Delay time:', int(delayTime / 60), 'min')
    print('Interval to lower:', intervalToLower, 'seconds')

    # volume
    print('Current volume:', scalarVol)

    # current time

    timeTuple = time.gmtime(deltaMain)

    print(time.strftime('%H:%M:%S', timeTuple))


def convert_int_value(msg):
    converted_val = None

    while converted_val is None:
        try:
            converted_val = int(input(msg))
        except ValueError:
            print("[ERROR] Entered an invalid integer")

    return converted_val


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('[ERROR] ' + str(e))
