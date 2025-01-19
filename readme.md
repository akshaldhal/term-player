# Term Player

Term Player is a terminal-based video player that converts video files into a series of colored ASCII frames and displays them in the terminal.

## Features

- Convert MP4 videos to a custom format.
- Play preprocessed video files in the terminal.
- Adjustable video height for different terminal sizes.

## Requirements

- Python 3.6+
- numpy>=2.2.1
- opencv-python>=4.11.0.86
- nuitka>=2.5.9

## Installation

1. Clone the repository:
  ```sh
  git clone https://github.com/akshaldhal/term-player.git
  cd term-player
  ```

2. Install the required packages:
  ```sh
  pip install -r requirements.txt
  ```

## Usage

To preprocess a video file:
```sh
python main.py <filepath> <height>
```
- `<filepath>`: Path to the MP4 video file.
- `<height>`: (Optional) Height of the video in terminal characters. Default is 32.

To play a preprocessed video file:
```sh
python main.py <filepath>
```
- `<filepath>`: Path to the preprocessed `.tppm` file.

## Example

Preprocess and play a video:
```sh
python main.py example.mp4 32
python main.py example.tppm
```

## Improvements

- **Sound Support**: Currently, Term Player does not support audio playback. Adding sound support would significantly enhance the viewing experience.
- **File Format Efficiency**: The custom file format used for preprocessed videos is not very efficient. Exploring more efficient encoding and compression techniques could improve performance and reduce file sizes.