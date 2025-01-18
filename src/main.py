import os
import sys
import cv2
import time
EXECUTABLE_NAME : str = 'term-player'
HEIGHT = 64

def __print_frames(frames : list, fps : float) -> None:
  for frame in frames:
    for row in frame:
      for pixel in row:
        r, g, b = pixel
        color = 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)
        print(f"\033[48;5;{color}m \033[0m", end="")
      print()
    print("\033[0m", end="")
    time.sleep(1 / fps)
    print("\033[H", end="")

def __preprocess_video__(filepath : str) -> None:
  cap = cv2.VideoCapture(filepath)
  if not cap.isOpened():
    print('Error: Could not open video')
    sys.exit(1)
  _width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  _height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  fps = cap.get(cv2.CAP_PROP_FPS)
  height = HEIGHT
  width = int(_width * height / _height)
  # frame_count = 0
  # output_dir = 'frames.temp'
  # os.makedirs(output_dir, exist_ok=True)
  frame_array = []
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break
    frame = cv2.resize(frame, (width, height))
    frame_array.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    # frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
    # cv2.imwrite(frame_filename, frame)
    # frame_count += 1
  cap.release()
  __print_frames(frame_array, fps)  

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