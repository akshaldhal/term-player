import os
import sys
import cv2
import time
import pickle
EXECUTABLE_NAME: str = 'term-player'

def __load_preprocessed(filepath: str) -> tuple:
  if not os.path.isfile(filepath):
    print(f'File {filepath} does not exist')
    sys.exit(1)
  with open(filepath, 'rb') as f:
    data = pickle.load(f)
  return data

def __print_frames(filepath: str) -> None:
  data = __load_preprocessed(filepath)
  fps = data['fps']
  base_frame = data['base_frame']
  frame_diffs = data['frame_diffs']
  for y, row in enumerate(base_frame):
    for x, pixel in enumerate(row):
      print(f"\033[48;5;{pixel}m \033[0m", end="")
    print()
  print("\033[0m", end="")
  current_frame = [list(row) for row in base_frame]
  for frame_diff in frame_diffs:
    for y, x, color in frame_diff:
      print(f"\033[{y + 1};{x + 1}H\033[48;5;{color}m \033[0m", end="", flush=True)
      current_frame[y][x] = color
    time.sleep(1 / fps)

def __preprocess_video__(filepath: str, height: int) -> None:
  cap = cv2.VideoCapture(filepath)
  if not cap.isOpened():
    print('Error: Could not open video')
    sys.exit(1)
  _width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  _height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  fps = cap.get(cv2.CAP_PROP_FPS)
  width = round(_width * height / _height)
  output_filename = f'{filepath[:-4]}.tppm'
  ret, frame = cap.read()
  if not ret:
    print('Error: Could not read video')
    sys.exit(1)
  frame = cv2.resize(frame, (width, height))
  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  base_frame = []
  for row in frame:
    rows = []
    for pixel in row:
      r, g, b = pixel
      color = 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)
      rows.append(color)
    base_frame.append(tuple(rows))
  base_frame = tuple(base_frame)
  frame_diffs = []
  prev_frame = [list(row) for row in base_frame]
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break
    frame = cv2.resize(frame, (width, height))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    current_diff = []
    for y, row in enumerate(frame):
      for x, pixel in enumerate(row):
        r, g, b = pixel
        color = 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)
        if color != prev_frame[y][x]:
          current_diff.append((y, x, color))
          prev_frame[y][x] = color
    frame_diffs.append(tuple(current_diff))
  cap.release()
  data = {
    'fps': fps,
    'base_frame': base_frame,
    'frame_diffs': tuple(frame_diffs)
  }
  with open(output_filename, 'wb') as f:
    pickle.dump(data, f)

def main(filepath: str, height: int) -> None:
  if not os.path.isfile(filepath):
    print(f'File {filepath} does not exist')
    sys.exit(1)
  if filepath.endswith('.mp4'):
    __preprocess_video__(filepath, height)
  elif filepath.endswith('.tppm'):
    print("\033[2J\033[H\033[?25l", end="")
    try:
      __print_frames(filepath)
    finally:
      print("\033[?25h", end="")
  else:
    print('Only mp4 files are supported for now')
    sys.exit(1)

if __name__ == '__main__':
  try:
    filepath: str = sys.argv[1]
    if len(sys.argv) > 2:
      HEIGHT = int(sys.argv[2])
    else:
      HEIGHT = 32
  except IndexError:
    print(f'Usage: {EXECUTABLE_NAME} <filepath> <height : optional>')
    sys.exit(1)
  main(filepath, HEIGHT)