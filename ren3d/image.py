# image.py
#   Class for manipulation of simple raster images
#   by Alexandra Wonyu 2022/5/9


import array

import ren3d.ppmview as ppmview

class Image:

    r"""Simple raster image. Allows pixel-level access and saving
    and loading as PPM image files.

    Examples:
    >>> img = Image((320, 240))    # create a 320x240 image
    >>> img.size
    (320, 240)
    >>> img[200,200]  # get color at pixel (200,200)
    (0, 0, 0)
    >>> img[200, 100] = (255, 0, 0) # set pixel to bright red
    >>> img[200, 100]   # get color of the pixel back again
    (255, 0, 0)
    >>> img.save("reddot.ppm")    # save image to a ppm file
    >>> img = Image((2, 3))
    >>> img[0,0] = 148, 103, 82
    >>> img[1,2] = 13, 127, 255
    >>> img.getdata()  # dump image data in ppm format
    b'P6\n2 3\n255\n\x00\x00\x00\r\x7f\xff\x00\x00\x00\x00\x00\x00\x94gR\x00\x00\x00'
    >>> img.load("wartburg.ppm")  # load a ppm image
    >>> img.size
    (640, 470)
    >>> img[350, 220]
    (148, 103, 82)
    >>> img.clear((255,255,255))  # make image all white
    >>> img.save("blank.ppm")     # blank.ppm is 640x470 all white
    """

    def __init__(self, fileorsize):
        """Create an Image from ppm file or create blank Image of given size.
        fileorsize is either a string giving the path to a ppm file or
        a tuple (width, height)
        """

        if type(fileorsize) == str:
            self.load(fileorsize)
        else:
            width, height = fileorsize
            self.size = (width, height)
            self.pixels = array.array("B", [0 for i in range(3*width*height)])
        self.viewer = None

    def _base_i(self, loc): # works
        """returns index of r value of pixel at location loc"""
        px, py = loc
        w, h  = self.size
        return 3 * ((h - 1 - py) * w + px)

    def __setitem__(self, pos, rgb): # works
        """ Set the color of a pixel.
        pos in a pair (x, y) giving a pixel location where (0, 0) is
            the lower-left pixel
        rgb is a triple of ints in range(256) representing
            the intensity of red, green, and blue for this pixel.
        """
        pixel_rloc = self._base_i(pos)
        self.pixels[pixel_rloc] = rgb[0]
        self.pixels[pixel_rloc+1] = rgb[1]
        self.pixels[pixel_rloc+2] = rgb[2]

    def __getitem__(self, pos): # works
        """ Get the color of a pixel
        pos is a pair (x, y) giving the pixel location--origin in lower left
        returns a triple (red, green, blue) for pixel color.
        """
        pixel_rloc = self._base_i(pos)
        red = self.pixels[pixel_rloc]
        green = self.pixels[pixel_rloc+1]
        blue = self.pixels[pixel_rloc+2]
        return (red, green, blue)

    def save(self, fname): # works?
        """ Save image as ppm in file called fname """
        outfile = open(fname, "wb")
        outfile.write(self.getdata())

    def getdata(self): # works
        """ Get image information as bytes in ppm format
        """
        data = f"P6\n{self.size[0]} {self.size[1]}\n255\n".encode() + bytes(self.pixels)
        return data

    def load(self, fname): # works
        """load raw PPM file from fname.
        Note 1: The width and height of the image will be adjusted
                to match what is found in the file.

        Note 2: This is not a general method for all PPM files, but
                works for most
        """
        infile = open(fname, "rb")
        infile.readline() # skip the line with P6
        size_array = infile.readline().strip().split()
        self.size = (int(size_array[0]), int(size_array[1]))
        infile.readline() # skip the line with 255

        self.pixels = array.array("B")
        for line in infile:
            for i in range(len(line)):
                self.pixels.append(line[i])

    def clear(self, rgb): # works
        """ set every pixel in Image to rgb
        rgb is a triple: (R, G, B) where R, G, & B are 0-255.
        """
        for i in range(0, len(self.pixels)-3, 3):
            self.pixels[i] = rgb[0]
            self.pixels[i+1] = rgb[1]
            self.pixels[i+2] = rgb[2]

    def show(self):
        """ display image using ppmview """
        if not (self.viewer and self.viewer.isalive()):
            self.viewer = ppmview.PPMViewer("PPM Image")
        self.viewer.show(self.getdata())

    def unshow(self):
        """ close viewing window """
        if self.viewer:
            self.viewer.close()
            self.viewer = None


if __name__ == '__main__':
    import doctest
    doctest.testmod()
