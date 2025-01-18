import os
import sys
import cv2
import time
import pickle
EXECUTABLE_NAME : str = 'term-player'

def __load_preprocessed(filepath: str) -> tuple:
  if not os.path.isfile(filepath):
    print(f'File {filepath} does not exist')
    sys.exit(1)
  with open(filepath, 'rb') as f:
    data = pickle.load(f)
  return data

def __print_frames(filepath : str) -> None:
  frames = __load_preprocessed(filepath)
  fps = frames[0]
  frames = frames[1:]
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

def __preprocess_video__(filepath : str, height : int) -> None:
  cap = cv2.VideoCapture(filepath)
  if not cap.isOpened():
    print('Error: Could not open video')
    sys.exit(1)
  _width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  _height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  fps = cap.get(cv2.CAP_PROP_FPS)
  width = round(_width * height / _height)
  output_filename = f'{filepath[:-4]}.tppm'
  frame_array = []
  frame_array.append(fps)
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break
    frame = cv2.resize(frame, (width, height))
    frame_array.append(tuple(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
  cap.release()
  frame_array = tuple(frame_array)
  with open(output_filename, 'wb') as f:
    pickle.dump(frame_array, f)

def main(filepath : str, height : int) -> None:
  if not os.path.isfile(filepath):
    print(f'File {filepath} does not exist')
    sys.exit(1)
  if filepath.endswith('.mp4'):
    __preprocess_video__(filepath, height)
  elif filepath.endswith('.tppm'):
    __print_frames(filepath)
  else:
    print('Only mp4 files are supported for now')
    sys.exit(1)

if __name__ == '__main__':
  try:
    filepath : str = sys.argv[1]
    if len(sys.argv) > 2:
      HEIGHT = int(sys.argv[2])
    else:
      HEIGHT = 32
  except IndexError:
    print(f'Usage: {EXECUTABLE_NAME} <filepath> <height : optional>')
    sys.exit(1)
  main(filepath, HEIGHT)