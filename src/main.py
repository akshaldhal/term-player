import os
import sys
EXECUTABLE_NAME = 'term-player'

def __preprocess_video__(filepath : str) -> None:
  # convert video to frames and save array of downscaled pixel values from each frame to a file
  raise NotImplementedError("Not implemented yet")

def main(filepath : str) -> None:
  if filepath.endswith('.mp4'):
    if not os.path.isfile(filepath):
      print(f'File {filepath} does not exist')
      sys.exit(1)
    __preprocess_video__(filepath)
  else:
    print('Only mp4 files are supported for now')
    sys.exit(1)

if __name__ == '__main__':
  try:
    filepath = sys.argv[1]
  except IndexError:
    print(f'Usage: {EXECUTABLE_NAME} <filepath>')
    sys.exit(1)
  main(filepath)


#for color in {0..255}; do
#    echo -e "\e[48;5;${color}m  \e[0m"
#done