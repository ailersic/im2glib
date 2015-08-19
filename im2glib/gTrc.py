# Import global variables
from im2glib.config import imdim, done, direc, smoothError

def scale(path):
    '''
    DXF files have the coordinates prewritten into it, which means they may
    be the wrong dimension. Scale the coordinates read from the DXF to imdim.

    Arguments:
        path is of type list. Contains sublists of tuples, where each tuple is
                              an (x, y) coordinate.
    '''

    global imdim

    # Create lists of only x coordinates and only y coordinates
    x = []
    y = []

    for shape in path:
        for coord in shape:
            x.append(coord[0])
            y.append(coord[1])

    # To scale from the old size to imdim, must know the old size
    maxx = max(x)
    maxy = max(y)
    
    minx = min(x)
    miny = min(y)

    # The distance between the minimal coordinate and the edge is the margin,
    # assumed size is the maximal coordinate plus the margin
    margin = min(minx, miny)
    size = max(maxx, maxy) + margin
    scale = imdim / size

    # Once the old size is known, scale the coordinates
    for i in range(len(path)):
        for j in range(len(path[i])):
            path[i][j][0] *= scale
            path[i][j][1] *= scale


def smoothRasterCoords(coords):
    '''
    Return newCoords, a coordinate list without the excessive elements of
    the argument, coords. The coordinates read from raster images would be
    jagged, so segments can be simplified by removing intermediate coordinates.

    Basically, the function does this to the points read from raster images:

        -|                 \
         |-|      --->      \        AND     o--o--o--o   --->   o--------o
           |-                \

    Arguments:
        coords is of type list. Contains sublists of tuples, where each tuple is
                                an (x, y) coordinate.
    '''

    newCoords = []

    # For each shape in coords
    for s in range(len(coords)):
        newCoords.append([])

        # If it's a simple shape without removable elements, copy it and skip to
        # the next one
        if len(coords[s]) <= 2:
            newCoords[s] = coords[s]
            continue

        i = 0

        # For each point i in the coordinate list
        while i < len(coords[s]) - 2:
            j = len(coords[s]) - 1

            # For each point j between i and the end of the list
            while j > i + 1:
                # List of all points between i and j
                midpoints = coords[s][i + 1:j]

                # In usual case, draw line between i and j
                try:
                    m = (coords[s][j][1] - coords[s][i][1]) /\
                        (coords[s][j][0] - coords[s][i][0])
                    b = coords[s][i][1] - m * coords[s][i][0]

                    canDel = True

                    for point in midpoints:
                        if linePointDist(m, b, point) >= smoothError:
                            canDel = False
                            break

                    # If all points between i and j are within smoothError of
                    # the line, remove them
                    if canDel == True:
                        newCoords[s].append(coords[s][i])
                        newCoords[s].append(coords[s][j])
                        i = j

                # In special case where the line is vertical, m = infinity
                except ZeroDivisionError:
                    canDel = True

                    for point in midpoints:
                        if abs(coords[s][i][0] - point[0]) >= smoothError:
                            canDel = False
                            break

                    # If all points between i and j are within smoothError of
                    # the line, remove them
                    if canDel == True:
                        newCoords[s].append(coords[s][i])
                        newCoords[s].append(coords[s][j])
                        i = j
                j -= 1
            i += 1

    # If a shape did not have removable points, copy the original coordinates
    for i in range(len(newCoords)):
        if len(newCoords[i]) == 0: newCoords[i] = coords[i]

    return newCoords


def isOnEdge(im, px):
    '''
    Return a boolean value that corresponds to whether any of the adjacent
    coordinates are not in the shape, hence whether the current coordinate is on
    the edge.
    
    Arguments:
        im is of type Image. Contains the image which is being processed.
        px is of type tuple. Contains float elements (x, y) which represent the
                             coordinate being checked.
    '''
    
    hues = []
    
    # Literal edge cases
    try: hues.append(sum(im.getpixel((px[0] - 1, px[1]))))
    except IndexError: hues.append(sum((255, 255, 255)))
    
    try: hues.append(sum(im.getpixel((px[0], px[1] - 1))))
    except IndexError: hues.append(sum((255, 255, 255)))
    
    try: hues.append(sum(im.getpixel((px[0] + 1, px[1]))))
    except IndexError: hues.append(sum((255, 255, 255)))
    
    try: hues.append(sum(im.getpixel((px[0], px[1] + 1))))
    except IndexError: hues.append(sum((255, 255, 255)))    

    if (max(hues) > sum((127, 127, 127))):
        return True
    else:
        return False


def nextPixelInShape(im, px):
    '''
    Return a tuple which represents the next coordinate when proceeding
    clockwise around a shape. It is an implementation of the square tracing
    algorithm, which works as follows:
        if on a black square, turn left of previous direction and go forward
        if on a white square, turn right of previous direction and go forward

    Arguments:
        im is of type Image. Contains the image which is being processed.
        px is of type tuple. Contains float elements (x, y) which represent the
                             current coordinate.
    '''

    global direc, done
    
    pixels = im.load()

    try: pixel = pixel = sum(im.getpixel((px[0], px[1])))
    except IndexError: pixel = sum((255, 255, 255))

    # 0 = right, 1 = up, 2 = left, 3 = down
    if pixel < sum((127, 127, 127)):
        direc = (direc - 1) % 4
    else:
        direc = (direc + 1) % 4

    # Implementation of description in docstring
    if direc == 0:
        x = px[0] + 1
        y = px[1]
    elif direc == 1:
        x = px[0]
        y = px[1] + 1
    elif direc == 2:
        x = px[0] - 1
        y = px[1]
    elif direc == 3:
        x = px[0]
        y = px[1] - 1

    try: pixel = sum(im.getpixel((x, y)))
    except IndexError: pixel = sum((255, 255, 255))

    # Since this function returns the next pixel, it can't return an off-shape
    # white pixel. It recurses until it finds a black pixel, which it returns.
    if pixel < sum((127, 127, 127)):
        if (x, y) not in done:
            done.append((x, y))
        return (x, y)
    else:
        return nextPixelInShape(im, (x, y))


def nextShape(im):
    '''
    Return a tuple which represents the leftmost point of the next shape.

    Arguments:
        im is of type Image. Contains the image which is being processed.
    '''

    global imdim, done
    
    # Check the brightness of every point in the image
    for x in range(imdim):
        for y in range(imdim):

            # If a dark pixel is found that was not already read, return it
            if sum(im.getpixel((x, y))) < sum((127, 127, 127)) and\
               isOnEdge(im, (x, y)) and not (x, y) in done:
                done.append((x, y))
                return(x, y)

    # If no shape is found, return a special tuple
    return (-1, -1)


def dist(a, b):
    '''
    Return the Pythagorean distance between two points.
    
    Arguments:
        a, b are of type tuple. They represent (x, y) coordinates.
    '''

    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def linePointDist(m, b, p):
    '''
    Return the distance between a point and a line.
    
    Arguments:
        m, b are of type float. Represent slope and y-intercept of line.
        p is of type tuple. Represents (x, y) coordinates.
    '''

    n = (m * p[0] - p[1] + b)
    d = (m ** 2 + 1) ** 0.5
    return abs(n / d)