import numpy as np
from yt.mods import *
from yt.frontends.stream.api import load_uniform_grid
from astropy.io import fits
#from aplpy.image_util import percentile_function

# Loading fits data
dir = '/srv/astro/erosolo/n253/cubes/newrelease/lines/robust/non_pbcor/'
tracer = 'hcn'    
cube= fits.getdata(dir+'ngc253_'+tracer+'_clean_RO.fits')

#ALMA data has a polarization axis.  Collapse along it.
cube = cube.sum(axis=0)

#Log transform the data in order to get on a viewable scale
cube = np.log(cube)
# Masking out nan elements
cube[np.isnan(cube)] = np.nanmin(cube)

# Loading data into yt structure
data = dict(Density = cube)
pf = load_uniform_grid(data, cube.shape, 9e16)

# Set the min/max to the data set (in units of log(I))
mi,ma = -5.7,-1.76


# Define a colour transfer function.
tf = ColorTransferFunction((mi, ma))
nLayer = 10
tf.add_layers(nLayer, w=0.005,colormap='gist_rainbow',
              alpha = np.logspace(-1.0,0,nLayer))

nStep = 60 # Number of frames in the movie
phiarray = np.linspace(0,2*np.pi,nStep)
count = 0
for phi in phiarray:
    count += 1 #Because iterators are hard
    ctstring = str(count)
    c = [0.51, 0.51, 0.51] # centre of the image
    L = [0.00,np.cos(phi),np.sin(phi)] # normal vector
    W = (0.25,0.6,0.6)
    Nvec = 512
    cam = pf.h.camera(c, L, W, (768,Nvec), tf,no_ghost=False,north_vector=[1.0,0,0])
#Define a custom file output here.
    image = cam.snapshot("hcnmovie/ngc253_"+ctstring.zfill(3)+".png" % pf, 8.0)

