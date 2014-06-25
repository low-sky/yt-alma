yt-alma
=======

YT script to make visualizations of data cubes



This is a script for making a spinning movie for a volume render of an ALMA data cube.   As written, this requires installation of http://yt-project.org and astropy from within the yt environment (http://www.astropy.org).   The script takes an input FITS file and writes out a bunch of PNGs into a directory.  

As a user, you will have to hack the script to adjust the inputs (The data files at the beginning) and outputs (in for loop at end).  I then use the linux `ffmpeg` to stitch the images together into a movie:

```
linux> ffmpeg -i ngc253_%03d.png -b:v 5000k ngc253.mp4
```

Here's a sample frame from the movie:

![Sample Image](./ngc253co_001.png?raw=True)

