# Global constants
IMDIM = 305         # Pixels in each dimension of image, 305 mm in 12 inches
SMOOTHERR = 1		# Rounding error when approx. raster with straight lines

# Global variables
done = []           # Record of all coordinates that were read from the image
direc = 0           # Current direction for tracing algorithm
                    # (0 = right, 1 = up, 2 = left, 3 = down)