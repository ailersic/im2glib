im2glib: Image to G Code Interpreter
====================================

This Python package includes one main function, imToPaths(string filename), which converts a raster image into a list of sublists of (x, y) tuple coordinates, representing the outline of the shapes in the image. Each sublist represents a path for a CNC cutter.

To output proper G code, there are two functions: toTextFile(string outfile, list shapes) and toSerial(list shapes). They format the coordinates as proper G code instructions, then either print it to a text file or send the instructions sequentially to a serial port. For the sake of my own projects, the toSerial function automatically looks for an Arduino. toSerial returns True or False depending on if it succeeded.

Author::

    Andrew Ilersich <andrew.ilersich@mail.utoronto.ca>

License::

    MIT

Example Usage::

    import im2glib

    paths = im2glib.imToPaths("square.jpg")
    outfile = "square.gcode"
    
    im2glib.toTextFile(outfile, paths)

    if im2glib.toSerial(coords): print("Done!")
    else: print("No serial device connected!")

Supported File Extensions::

	jpg/jpeg
	png
	bmp
	dxf