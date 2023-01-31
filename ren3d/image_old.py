# image.py
#   Class for manipulation of simple raster images

import array

# needed for img.show()
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
            self.size = (int(width), int(height))
            self.pixels = array.array("B", [0 for i in range(3*width*height)])
        self.viewer = None

    def _find_location(self,pos):
        """ Helper function which transforms two dimensional coordinates into
        array indexes
        Note: returns the index of the first color byte (red) of the pixel
        """
        x,y = pos
        w, h = self.size
        index = 3*((h -1 - y)*w  +x)
        assert index<len(self.pixels) , "Invalid location of pixel"
        return index

        
    def __setitem__(self, pos, rgb):
        """ Set the color of a pixel.
        pos in a pair (x, y) giving a pixel location where (0, 0) is
            the lower-left pixel
        rgb is a triple of ints in range(256) representing
            the intensity of red, green, and blue for this pixel.
        """
        index = self._find_location(pos)
        
        for item in rgb:
            self.pixels[index]= item
            index+=1

    def __getitem__(self, pos):
        """ Get the color of a pixel
        pos is a pair (x, y) giving the pixel location--origin in lower left
        returns a triple (red, green, blue) for pixel color.
        """
        index = self._find_location(pos)
        return (self.pixels[index],self.pixels[index+1],self.pixels[index+2])

    def save(self, fname):
        """ Save image as ppm in file called fname """
        with open(fname,mode = "wb") as outfile:
            outfile.write(self.getdata())
            
    def getdata(self):
        """ Get image information as bytes in ppm format
        """
        w,h = self.size
        data = "P6\n"+str(w)+" "+str(h)+"\n255\n"
        data= data.encode()
        data += self.pixels.tobytes()
        return data
        

    def load(self, fname):
        """load raw PPM file from fname.
        Note 1: The width and height of the image will be adjusted
                to match what is found in the file.

        Note 2: This is not a general method for all PPM files, but
                works for most
        """
        with open(fname,mode = "rb") as infile:
            infile.readline()
            width,height = infile.readline().decode().split()
            self.size =(int(width),int(height))
            infile.readline()
            self.pixels = array.array("B")
            self.pixels.frombytes(infile.read())           
            

    def clear(self, rgb):
        """ set every pixel in Image to rgb
        rgb is a triple: (R, G, B) where R, G, & B are 0-255.
        """
        
        w,h = self.size
        for i in range(w):
            for j in range(h):
                self[i,j] = rgb
            
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
