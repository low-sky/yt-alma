import numpy as np
import yt
from astropy.io import fits
import os
import numpy as np
def ytrender(filename, vmin = None, vmax = None,
             useLog = False, nLayer = 10, cmap = 'gist_rainbow',
             colorwidth = 0.005, phi = 0.5, theta = 1.570796,
             outfile = None, usedomain = (0.25, 0.6, 0.6),
             Xrays = 768, Yrays = 512):
    cube = fits.getdata(filename)
    if not vmin:
        vmin = np.percentile(cube,50)
    if not vmax:
        vmax = np.percentile(cube,99.5)
    if len(cube.shape)>3:
        cube = cube.squeeze()
    if not outfile:
        outfile = filename.replace('fits','png')
    cube[np.isnan(cube)] = np.nanmin(cube)
    data = dict(density = cube)
    pf = yt.load_uniform_grid(data, cube.shape, 9e16)
    tf = yt.ColorTransferFunction((vmin, vmax))
    c = (pf.domain_right_edge + pf.domain_left_edge)/2.0
    tf.add_layers(nLayer, w=colorwidth,colormap=cmap,
                  alpha = np.logspace(-1.0,0,nLayer))
    c = [0.51, 0.51, 0.51] # centre of the image
    L = [np.cos(theta),
         np.sin(theta)*np.cos(phi),
         np.sin(theta)*np.sin(phi)] # normal vector
    W = usedomain

    cam = pf.camera(c,L,W,(Xrays,Yrays),tf,no_ghost=False,
                    north_vector=[1.0,0,0],
                    fields=['density'],log_fields=[useLog])
    image = cam.snapshot(outfile, 8.0)

