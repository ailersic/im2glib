# Import Python Image Library
from PIL import Image, ImageDraw, ImageEnhance

# Import global variables
from im2glib.config import imdim, done

# Import low-level functions
from im2glib.gTrc import nextShape, nextPixelInShape, smoothRasterCoords, scale

def initRaster(filename):
    '''
    Return the raster image represented by the file name. The file must be
    in the local folder.

    Arguments:
        filename is of type string. Contains name of image file.
    '''

    global imdim
    im = Image.open(filename)

    # Increase contrast of image
    im = ImageEnhance.Contrast(im)
    im = im.enhance(2)

    # Resize to imdim x imdim
    im = im.resize((imdim, imdim))

    return im


def initDXF(filename):
    '''
    Return the DXF text file represented by the file name. The file must be
    in the local folder.

    Arguments:
        filename is of type string. Contains name of image file.
    '''

    file = open(filename)

    # Since dxf is a fancy extension for a text file, it can be read as a string
    DXFtxt = file.readlines()

    file.close()

    return DXFtxt


def readFromRaster(filename):
    '''
    Return a list of sublists of tuples which correspond to (x, y) coordinates.
    Read the coordinates from a raster image, tracing the outline of each shape
    in the image.
    
    Arguments:
        filename is of type string. Contains name of image file.
    '''

    global done

    # Create Image object from file in local folder
    im = initRaster(filename)

    # Find first point
    point = nextShape(im)

    start = point
    nextpoint = (0, 0)
    
    i = 0
    shapeList = []

    # While there are still shapes in the image
    while point != (-1, -1):
        start = point
        
        shapeList.append([])
        shapeList[i].append(point)

        # While it has not yet fully traced around the image
        while nextpoint != start:
            nextpoint = nextPixelInShape(im, point)
            point = nextpoint

            done.append(point)
            shapeList[i].append(point)

        i += 1
        point = nextShape(im)
    
    # Smooth coordinates in image
    shapeList = smoothRasterCoords(shapeList)
    
    # Ensure that each shape starts and ends on the same coordinate
    for i in range(len(shapeList)):
        if shapeList[i][-1] != shapeList[i][0]:
            shapeList[i].append(shapeList[i][0])

    return shapeList


def readFromDXF(filename):
    '''
    Return a list of sublists of tuples which correspond to (x, y) coordinates.
    Read the coordinates from a DXF file, treating it as plaintext.
    
    Arguments:
        filename is of type string. Contains name of image file.
    '''

    # Create Image object from file in local folder
    DXFtxt = initDXF(filename)

    segment = -1

    path = []
    xold = []
    yold = []

    line = 0
    polyline = 0
    vertex = 0

    # While there is still more to read
    while line < len(DXFtxt):
        # These are just conditions how to interpret the DXF into coordinates
        if (DXFtxt[line] == "POLYLINE\n"):
            segment += 1
            polyline = 1
            path.append([])

        elif (DXFtxt[line] == "VERTEX\n"):
            vertex = 1

        elif ((DXFtxt[line].strip() == "10") & (vertex == 1) & (polyline == 1)):
            line += 1
            x = float(DXFtxt[line])

        elif ((DXFtxt[line].strip() == "20") & (vertex == 1) & (polyline == 1)):
            line += 1
            y = float(DXFtxt[line])

            if ((x != xold) | (y != yold)):
                path[segment].append([float(x),float(y)])
                xold = x
                yold = y

        elif (DXFtxt[line] == "SEQEND\n"):
            polyline = 0
            vertex = 0

        line += 1

    # Rescale the coordinates to imdim x imdim
    scale(path)

    return path
