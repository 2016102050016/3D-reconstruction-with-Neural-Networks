import os
import re
import json
import sys
import math
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import exposure
from PIL import Image


def grep_epoch_name(epoch_dir):
    return re.search(".*(epoch_.*).*", epoch_dir).group(1)


def vis_montage(im, axis, f_name=None):
    ret_im = exposure.rescale_intensity(montage(im, axis))
    return vis_im(ret_im, f_name)


def vis_im(im, f_name=None):
    fig = plt.figure()
    if f_name is None:
        return plt.imshow(im)
    plt.imsave(f_name, im)
    plt.clf()
    plt.close()


def vis_multichannel(im, f_name=None):
    mulitchannel_montage = montage(im, -1)
    return vis_im(mulitchannel_montage, f_name)


def vis_sequence(im, f_name=None):
    sequence_montage = montage(im, 0)
    return vis_im(sequence_montage, f_name)


def vis_voxel(vox, f_name=None):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(vox, edgecolor='k')
    ax.view_init(30, 30)
    if f_name is None:
        return plt.show()

    plt.savefig(f_name, bbox_inches='tight')
    plt.clf()
    plt.close()


def hstack(a, b):
    return np.hstack((a, b))


def vstack(a, b):
    return np.vstack((a, b))


def montage(packed_ims, axis):
    """display as an Image the contents of packed_ims in a square gird along an aribitray axis"""
    if packed_ims.ndim == 2:
        return packed_ims

    # bring axis to the front
    packed_ims = np.rollaxis(packed_ims, axis)

    N = len(packed_ims)
    n_tile = math.ceil(math.sqrt(N))
    rows = []
    for i in range(n_tile):
        im = packed_ims[i * n_tile]
        for j in range(1, n_tile):
            ind = i * n_tile + j
            if ind < N:
                im = hstack(im, packed_ims[ind])
            else:
                im = hstack(im, np.zeros_like(packed_ims[0]))
        rows.append(im)

    matrix = rows[0]
    for i in range(1, len(rows)):
        matrix = vstack(matrix, rows[i])
    return matrix


def check_dir():
    TRAIN_DIRS = ["out", "data", "aws"]
    for d in TRAIN_DIRS:
        make_dir(d)


def read_params(json_dir="params.json"):
    return json.loads(open(json_dir).read())


def grep_params(param_line):
    regex = "^.*=(.*)$"
    return re.findall(regex, param_line)[0]


def make_dir(file_dir):
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
