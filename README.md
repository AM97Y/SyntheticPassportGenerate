# PyQt5_PassportsRF
## Installation

    1) Create virtual environment:
        conda create -n <your_virtual_environment_name> python=3.7 -y
        conda activate <your_virtual_environment_name>
        
    2) Build virtual environment:
        pip install -r requirements.txt
        
## Prerequisites

* Installed [Python](https://www.python.org/downloads/) >= 3.6 or [Anaconda](https://www.anaconda.com/products/individual) >= 4.10.1



# Augmentation
Augmentation with parameters selected for passports.

1) Run Augmentation:
    python main.py --input_path <folder with generated images> --output_path <output path> --count <number of augmented images>
For more information launch `python main.py -h`. Please also look at `configs/README.md` to get to know about config parameters.
