import os
import cv2
import time
import argparse
import datetime
import tkinter as tk
from tkinter import simpledialog


def argument_parsing() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, required=True,
                        help="Path where to save the output",
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             f'{str(datetime.date.today())}_output'))
    parser.add_argument("--cam_index", type=int, required=True,
                        help="Path where to save the csv",
                        default=0)
    parser.add_argument("--video_length", type=int, required=True,
                        help="Output video length in seconds",
                        default=0)

    args = parser.parse_args()
    return args


def get_output_video_name() -> str:
    """Create a pop-up window to enter the output video name"""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory_name = simpledialog.askstring("Output video name", "Enter the name for the output video:")
    return directory_name


def run_cap_video(cam_index: int, video_length: int, output: str):

    """Video capturing settings"""

    cap = cv2.VideoCapture(cam_index)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

    recording = False
    out = None
    start_time = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read the frame.")
            break

        if recording:
            out.write(frame)
            elapsed_time = time.time() - start_time
            if elapsed_time >= video_length:
                print("Recording completed. Stopping...")
                recording = False
                out.release()
                out = None

        if recording:
            cv2.circle(frame, (20, 20), 5, (255, 255, 255), -1)


        cv2.imshow("frame", frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            print("Exiting program...")
            break
        elif key & 0xFF == ord('r'):
            if not recording:
                """Setup: creating output video path"""

                file_name = get_output_video_name()
                if not file_name:
                    print("No file name entered. Exiting...")
                    return
                os.makedirs(output, exist_ok=True)
                save_path = os.path.join(output, f"{file_name}.avi")

                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(save_path, fourcc, fps, (width, height), isColor=True)

                recording = True

                start_time = time.time()  # Start the timer
                print("Started recording.")
            else:
                print("Recording is already in progress.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    args = argument_parsing()
    run_cap_video(args.cam_index, args.video_length, args.output)


