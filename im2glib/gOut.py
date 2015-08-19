# Import PySerial
import serial
import serial.tools.list_ports

# Import system time
import time

def toTextFile(outfile, shapes):
    '''
    Print the coordinates to a text file formatted in G code.
    
    Arguments:
        shapes is of type list. It contains sublists of tuples that correspond
                                to (x, y) coordinates.
    '''

    file = open(outfile, "w")
    
    # Boilerplate text:
    # G17: Select X, Y plane
    # G21: Units in millimetres
    # G90: Absolute distances
    # G54: Coordinate system 1
    file.write("G17 G21 G90 G54\n")
    
    # Start at origin (0, 0)
    file.write("G00 X0. Y0.\n")

    up = True
    
    # Assume Z0 is down and cutting and Z1 is retracted up
    for shape in shapes:
        for i in range(len(shape)):
            # If coordinate is an integer, append a decimal point
            if (shape[i][0] % 1.0 == 0): xstr = str(shape[i][0]) + "."
            else: xstr = str(shape[i][0])
            
            if (shape[i][1] % 1.0 == 0): ystr = str(shape[i][1]) + "."
            else: ystr = str(shape[i][1])

            # Write coordinate to file
            file.write("X" + xstr + " Y" + ystr + "\n")

            # When arrived at point of new shape, start cutting
            if up == True:
                file.write("Z0.\n")
                up = False
        # When finished shape, retract cutter
        file.write("Z1.\n")
        up = True
    # Return to origin (0, 0) when done, then end program with M2
    file.write("X0. Y0.\nM2")

    file.close()


def toSerial(shapes):
    '''
    Send the coordinates formatted in G code through serial to Arduino.
    
    Arguments:
        shapes is of type list. It contains sublists of tuples that correspond
                                to (x, y) coordinates.
    '''

    # First, search COM ports for a connected Arduino
    found = False

    portlist = list(serial.tools.list_ports.comports())

    for tempport in portlist:
        if tempport[1].startswith("Arduino"):
            port = serial.Serial(tempport[0])
            found = True

    # If no Arduino is found, return False
    if not found:
        return False

    # Arduino restarts when serial is initialized, so wait until it's ready
    time.sleep(5)

    port.baudrate = 4800

    # Boilerplate text:
    # G17: Select X, Y plane
    # G21: Units in millimetres
    # G90: Absolute distances
    # G54: Coordinate system 1
    port.write("G17 G21 G90 G54\n".encode())

    # Start at origin (0, 0)
    port.write("G00 X0. Y0.\n".encode())

    up = True
    
    # Assume Z0 is down and cutting and Z1 is retracted up
    for shape in shapes:
        for i in range(len(shape)):
            # Since the RAM on the Arduino is limited, delay the instructions
            time.sleep(1)

            # If coordinate is an integer, append a decimal point
            if (shape[i][0] % 1.0 == 0): xstr = str(shape[i][0]) + "."
            else: xstr = str(shape[i][0])
            
            if (shape[i][1] % 1.0 == 0): ystr = str(shape[i][1]) + "."
            else: ystr = str(shape[i][1])

            # Write coordinate to serial
            port.write(("X" + xstr + " Y" + ystr + "\n").encode())

            # When arrived at point of new shape, start cutting
            if up == True:
                port.write(("Z0.\n").encode())
                up = False
        # When finished shape, retract cutter
        port.write("Z1.\n".encode())
        up = True
    # Return to origin (0, 0) when done, then end program with M2
    port.write("X0. Y0.\nM2".encode())

    port.close()

    # Once sending is completed, return True
    return True