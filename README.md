# LowerToSleep

LowerToSleep is a very simple Python script that decreases the speakers volume based on time.

### Usage

Starting the script, the user has to input: 
  - The total time (in minutes) the script will run
  - The delay time (in minutes) for the script to start lowering the volume
  - The type of interval to lower the volume, being:
    - **interpolated**: automatically calculates the interval of each new decreasing based on the time left. This interval is fixed and will lower the volume by one scalar unity until it reaches zero by the end of the execution
    - **given time**: the interval (in seconds) must be given, so the volume will decrease every time the interval is reached.

### Requirements

There is only one requirement, and it is [pycaw](https://github.com/AndreMiras/pycaw), a library to handle Windows audio volume. 

### Why the name "LowerToSleep"?

I really like to lay down and put some music to relax, but sometimes I like to hear it loud. The problem is: at some point I'll be very sleepy and I won't be able to sleep because of the high volume. I think you get the idea now :)