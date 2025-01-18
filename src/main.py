import os
import sys
import cv2
EXECUTABLE_NAME : str = 'term-player'
HEIGHT = 32

def __preprocess_video__(filepath : str) -> None:
  # convert video to frames and save array of downscaled pixel values from each frame to a file
  cap = cv2.VideoCapture(filepath)
  if not cap.isOpened():
    print('Error: Could not open video')
    sys.exit(1)
  _width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  _height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  fps = cap.get(cv2.CAP_PROP_FPS)
  height = HEIGHT
  width = int(_width * height / _height)
  frame_count = 0
  output_dir = 'frames.temp'
  os.makedirs(output_dir, exist_ok=True)
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break
    frame = cv2.resize(frame, (width, height))
    frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
    cv2.imwrite(frame_filename, frame)
    frame_count += 1
    

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
    filepath : str = sys.argv[1]
  except IndexError:
    print(f'Usage: {EXECUTABLE_NAME} <filepath>')
    sys.exit(1)
  main(filepath)


#for color in {0..255}; do
#    echo -e "\e[48;5;${color}m  \e[0m"
#done