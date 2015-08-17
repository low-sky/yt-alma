import numpy as np
import yt
from astropy.io import fits
import os
# Loading fits data
dir = '/srv/astro/erosolo/n253/cubes/newrelease/lines/robust/non_pbcor/'
tracer = 'hcn'    
cube= fits.getdata(dir+'ngc253_'+tracer+'_clean_RO.fits')

#ALMA data has a polarization axis.  Collapse along it.
cube = cube.squeeze()

#Log transform the data in order to get on a viewable scale
# color transfer function no longer correct.
#cube = np.log(cube)
# Masking out nan elements
cube[np.isnan(cube)] = np.nanmin(cube)

# Loading data into yt structure
data = dict(density = cube)
pf = yt.load_uniform_grid(data, cube.shape, 9e16)

# Set the min/max to the data set (in units of log10(I))
# These values are specific to the example cube
mi,ma = -2.47,-0.764

# Define a colour transfer function.
tf = yt.ColorTransferFunction((mi, ma))
c = (pf.domain_right_edge + pf.domain_left_edge)/2.0
nLayer = 10
tf.add_layers(nLayer, w=0.005,colormap='gist_rainbow',
              alpha = np.logspace(-1.0,0,nLayer))

nStep = 6 # Number of frames in the movie
phiarray = np.linspace(0,2*np.pi,nStep)
count = 0

if not os.path.isdir("movie/"):
    os.mkdir("movie")

for phi in phiarray:
    count += 1 #Because iterators are hard
    ctstring = str(count)
    c = [0.51, 0.51, 0.51] # centre of the image
    L = [0.00,np.cos(phi),np.sin(phi)] # normal vector
    W = (0.25,0.6,0.6)
    Nvec = 512

    cam = pf.camera(c,L,W,(768,Nvec),tf,no_ghost=False,
                    north_vector=[1.0,0,0],fields=['density'],log_fields=[True])
    #Define your custom file output here.
    image = cam.snapshot("movie/ngc253_"+ctstring.zfill(3)+".png" % pf, 8.0)

