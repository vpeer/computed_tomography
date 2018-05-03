import numpy as np
import os
import glob
import skimage.io
import matplotlib.pyplot as plt
import re
import astra


def load_images(directory):
    images = glob.glob(directory + '/scan*.tif')
    # Make sure we process the files in the same order they where scanned.
    images.sort(key=lambda f: int(re.search(r'scan_([0-9]+).tif', f).group(1)))

    first_image = skimage.io.imread(images[0])
    x, y = first_image.shape
    sinogram = np.zeros((len(images), y))
    
    for i, imagefile in enumerate(images):
        image = skimage.io.imread(imagefile)
        sinogram[i] = image[x // 2]

    return sinogram, images


if __name__ == '__main__':

    scans_directory = '/mnt/datasets1/fgustafsson/cwi_ct_scan/wooden_block/'
    sinogram, images = load_images(scans_directory)

    plt.imshow(sinogram, cmap='gray')
    plt.show()
    
    # As a sanity check look at first scan at angle 0
    first_image = skimage.io.imread(images[0])
    plt.imshow(first_image, cmap='gray')
    plt.show()

    # Last scan angle == first scan angle, so we drop the last.
    scanned_angles = first_image.shape[0] - 1
    scan_width = first_image.shape[1]


    proj_angles = np.linspace(0, (scanned_angles -1.0)*2.0*np.pi / scanned_angles, scanned_angles)
    