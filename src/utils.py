'''
utils.py
source: https://github.com/yjn870/SRCNN-pytorch/blob/master/utils.py
modification: 
    - wrote comments for each function

GunGyeom James Kim
September 28th, 2023
CS 7180: Advnaced Perception

code for utility functions
'''
import torch
import numpy as np

def convert_rgb_to_y(img):
    '''
    convert RGB to brightness

    Parameters:
        img - input
    
    Return:
        brightness 

    Raise:
        if the type of input is not expected
    '''
    if type(img) == np.ndarray:
        return 16. + (64.738 * img[:, :, 0] + 129.057 * img[:, :, 1] + 25.064 * img[:, :, 2]) / 256.
    elif type(img) == torch.Tensor:
        if len(img.shape) == 4:
            img = img.squeeze(0)
        return 16. + (64.738 * img[0, :, :] + 129.057 * img[1, :, :] + 25.064 * img[2, :, :]) / 256.
    else:
        raise Exception('Unknown Type', type(img))


def convert_rgb_to_ycbcr(img):
    '''
    convert RGB to YCbCr color space

    Parameters:
        img - input
    
    Return:
        YCbCr color img

    Raise:
        if the type of input is not expected
    '''
    if type(img) == np.ndarray:
        y = 16. + (64.738 * img[:, :, 0] + 129.057 * img[:, :, 1] + 25.064 * img[:, :, 2]) / 256.
        cb = 128. + (-37.945 * img[:, :, 0] - 74.494 * img[:, :, 1] + 112.439 * img[:, :, 2]) / 256.
        cr = 128. + (112.439 * img[:, :, 0] - 94.154 * img[:, :, 1] - 18.285 * img[:, :, 2]) / 256.
        return np.array([y, cb, cr]).transpose([1, 2, 0])
    elif type(img) == torch.Tensor:
        if len(img.shape) == 4:
            img = img.squeeze(0)
        y = 16. + (64.738 * img[0, :, :] + 129.057 * img[1, :, :] + 25.064 * img[2, :, :]) / 256.
        cb = 128. + (-37.945 * img[0, :, :] - 74.494 * img[1, :, :] + 112.439 * img[2, :, :]) / 256.
        cr = 128. + (112.439 * img[0, :, :] - 94.154 * img[1, :, :] - 18.285 * img[2, :, :]) / 256.
        return torch.cat([y, cb, cr], 0).permute(1, 2, 0)
    else:
        raise Exception('Unknown Type', type(img))


def convert_ycbcr_to_rgb(img):
    '''
    convert YCbCr to RGB color space

    Parameters:
        img - input
    
    Return:
        RGB color img

    Raise:
        if the type of input is not expected
    '''
    if type(img) == np.ndarray:
        r = 298.082 * img[:, :, 0] / 256. + 408.583 * img[:, :, 2] / 256. - 222.921
        g = 298.082 * img[:, :, 0] / 256. - 100.291 * img[:, :, 1] / 256. - 208.120 * img[:, :, 2] / 256. + 135.576
        b = 298.082 * img[:, :, 0] / 256. + 516.412 * img[:, :, 1] / 256. - 276.836
        return np.array([r, g, b]).transpose([1, 2, 0])
    elif type(img) == torch.Tensor:
        if len(img.shape) == 4:
            img = img.squeeze(0)
        r = 298.082 * img[0, :, :] / 256. + 408.583 * img[2, :, :] / 256. - 222.921
        g = 298.082 * img[0, :, :] / 256. - 100.291 * img[1, :, :] / 256. - 208.120 * img[2, :, :] / 256. + 135.576
        b = 298.082 * img[0, :, :] / 256. + 516.412 * img[1, :, :] / 256. - 276.836
        return torch.cat([r, g, b], 0).permute(1, 2, 0)
    else:
        raise Exception('Unknown Type', type(img))
    
def psnr(img1, img2):
    '''
    calculate PSNR(dB) of img1 and img2

    Parameters:
        img1 - input
        img2 - input
    
    Return:
        PSNR(dB)
    '''
    return 10. * torch.log10(1. / torch.mean((img1-img2)**2))



class AverageMeter(object):
    '''
    To keep the track of statistic
    '''
    def __init__(self):
        '''
        constructor
        '''
        self.reset()

    def reset(self):
        '''
        reset the statistics
        '''
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0
    
    def update(self, val, n=1):
        '''
        update the statistics according to given value(s) and number of value(s)

        Parameters:
            val: value to calculate
            n:   number of value
        '''
        self.val = val
        self.sum += val*n
        self.count += n 
        self.avg = self.sum / self.count