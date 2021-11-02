import os
from argparse import ArgumentParser

import albumentations as A
import cv2
from os import listdir


def init_argparse():
    """
    Initializes argparse
    Returns parser.
    """
    parser = ArgumentParser(description='Aug')

    parser.add_argument(
        '--input_path',
        nargs='?',
        help='Path to load files',
        default='imgs/',
        type=str)
    parser.add_argument(
        '--output_path',
        nargs='?',
        help='Path to save files',
        default='aug/',
        type=str)
    parser.add_argument(
        '--count',
        nargs='?',
        help='Count imgs',
        default=2,
        type=int)

    return parser


if __name__ == "__main__":
    args = init_argparse().parse_args()

    transform = A.Compose([
        # A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2),
        A.RGBShift(r_shift_limit=10, g_shift_limit=10, b_shift_limit=10),
        A.RandomBrightnessContrast(brightness_limit=0.1, contrast_limit=0.15),
        A.OneOf([A.GaussianBlur(p=1), A.MedianBlur(p=1), A.Blur(p=1)], p=0.25),
        A.RandomSunFlare(flare_roi=(0, 0, 1, 1), num_flare_circles_lower=1, num_flare_circles_upper=5, src_radius=100),
        A.OneOf([
            A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.05, rotate_limit=10, p=0.2),
            A.RandomScale(scale_limit=0.05),
            A.RandomScale(scale_limit=0.05),
            A.SafeRotate(limit=10)], p=0.2),

    ])
    path = args.input_path
    count = args.count

    for index, file_img in enumerate(listdir(path)):
        image = cv2.imread(f'{path}/{file_img}')
        if image is not None:
            print(file_img)
            for i in range(count):

                # Augment an image
                transformed = transform(image=image)
                transformed_image = transformed["image"]
                print(f'{path}/{args.output_path}/{index}_{count}_{file_img}')
                cv2.imwrite(f'{path}/{args.output_path}/{index}_{i}_{file_img}', transformed_image)
