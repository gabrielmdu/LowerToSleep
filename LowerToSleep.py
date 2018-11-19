from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time
import os

# volume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

scalar_vol = int(volume.GetMasterVolumeLevelScalar() * 100)

# time

total_time = 0
delay_time = 0
lowering_type = ''
interval_to_lower = 0  # the time between every new lowering, determined by the lowering type
delta_main = 0  # time passed since the beginning of the program


def main():
    print('* -------------------------------------------- *')
    print('* ------------ - Lower to Sleep - ------------ *')
    print('* -Lower the speakers volume and let me sleep- *')
    print('* ------------ by Gabriel Schulte ------------ *')
    print('* -------------------------------------------- *')

    global scalar_vol
    global total_time
    global delay_time
    global lowering_type
    global interval_to_lower

    total_time_min = convert_int_value('Enter total time in minutes: ')
    total_time = total_time_min * 60

    delay_time_min = convert_int_value('Enter delay time in minutes: ')
    delay_time = delay_time_min * 60

    # time left to lower the volume
    time_left = total_time - delay_time

    lowering_type = input(
        'Choose the lowering type ([i]nterpolated/[t]ime given): ')

    interval_to_lower = {
        # the number of times the volume will have to decrease to reach zero within the time left
        'i': lambda: time_left / scalar_vol,
        't': lambda: convert_int_value(
            'Enter the interval time to lower the volume in seconds: ')
    }.get(lowering_type, lambda: time_left / scalar_vol)()

    global delta_main
    time_sec = 0
    time_interval = 0

    # sets to true if the delay time is reached
    can_lower = False

    # start counting the time here
    start_time = time.clock()

    render()

    # the main loop
    while delta_main < total_time:
        # updates the total time running
        delta_main = time.clock() - start_time

        # updates the delta for seconds counter
        deltaSec = delta_main - time_sec

        # if one second has passed, prints the current status
        if (deltaSec > 1):
            render()
            time_sec = time.clock()

        # lowering volume time

        if can_lower == False:
            if delta_main > delay_time:
                can_lower = True
                time_interval = time.clock()
        else:
            deltaInterval = delta_main - time_interval

            if deltaInterval > interval_to_lower:
                scalar_vol -= 1
                volume.SetMasterVolumeLevelScalar(scalar_vol / 100, None)
                time_interval = time.clock()

    render()


def render():
    os.system('cls')  # clear the console (Windows)

    # total, delay and interval times
    print('Total time:', int(total_time / 60), 'min')
    print('Delay time:', int(delay_time / 60), 'min')
    print('Interval to lower:', interval_to_lower, 'seconds')

    # volume
    print('Current volume:', scalar_vol)

    # current time

    time_tuple = time.gmtime(delta_main)

    print(time.strftime('%H:%M:%S', time_tuple))


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
    except KeyboardInterrupt:
        print('--- Interrupted by the user ---')
    except Exception as e:
        print('[ERROR] ' + str(e))
