from im2glib.gInit import readFromRaster, readFromDXF

def imToPaths(filename):
    '''
    Return a list of paths, where each path is a sublist of tuples which contain
    (x, y) coordinates. Read the coordinates from any file type supported by the
    package.
    
    Arguments:
        filename is of type string. Contains name of image file.
    '''

    # Read the image as raster or as DXF depending on file extension
    if filename.endswith((".jpg", ".jpeg", ".png", ".bmp")):
        coords = readFromRaster(filename)
    elif filename.endswith(".dxf"):
        coords = readFromDXF(filename)
    else:
        coords = [[(0, 0)]]

    return coords
