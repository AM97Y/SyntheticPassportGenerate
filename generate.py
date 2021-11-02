from argparse import ArgumentParser
from datetime import datetime

from ImageCreator import ImageCreator
from Passport import PassportContent, PassportAppearance
from utils.path_utils import Paths


def generate_path(count_examples, output):
    """
    Generate path of passport images.

    """
    passport_content = PassportContent()
    passport_appearance = PassportAppearance()

    for i in range(0, count_examples):
        passport_content.random_init()
        passport_appearance.random_init()

        img_creator = ImageCreator(passport_content.parameters, passport_appearance.parameters)
        img = img_creator.create_image()

        img_filepath = Paths.outputs(output) / f'{datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f")}.png'
        img.save(str(img_filepath))

        del img, img_creator, img_filepath


def init_argparse():
    """
    Initializes argparse
    Returns parser.

    """
    parser = ArgumentParser(description='Aug')

    parser.add_argument(
        '--output_path',
        nargs='?',
        help='Path to save files',
        default='./passports/',
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
    generate_path(args.count, args.output_path)
