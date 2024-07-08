import cv2
import numpy as np
import time

class SegmentalMotionDetection:
    
    # initialize the class with the number of segments, threshold, and delay time before it stops recording
    # I found 20 segments is a good balance between detecting movement and not detecting too much noise, 
    # plus increasing the number of segments increases the processing time, and will really bog down the program
    def __init__(self, segments=20, threshold=10, delay_seconds=3):
        self.segments = segments
        self.threshold = threshold
        self.delay_seconds = delay_seconds
        self.last_motion_time = time.time()

    # calculate the average and standard deviation of pixel values in each segment
    def segment_calculation(self, frame):

        # get the height and width of the frame and calculate the segment height and width
        frame_height, frame_width = frame.shape
        segment_height = frame_height // self.segments
        segment_width = frame_width // self.segments
        stats = []

        # loop through the segments and calculate the average and standard deviation of pixel values
        for i in range(self.segments):
            row_stats = []
            for j in range(self.segments):
                start_y = i * segment_height
                end_y = (i + 1) * segment_height if (i + 1) * segment_height < frame_height else frame_height
                start_x = j * segment_width
                end_x = (j + 1) * segment_width if (j + 1) * segment_width < frame_width else frame_width
                segment = frame[start_y:end_y, start_x:end_x]
                segment_average = np.mean(segment)
                segment_standard_deviation = np.std(segment)
                row_stats.append((segment_average, segment_standard_deviation))
            stats.append(row_stats)

        return stats

    # this method will compare the average and standard deviation of pixel values in each segment
    # essentially, it will compare the stats of the current frame with the previous frame
    # if the difference is greater than the threshold, then movement is detected
    def detect_movement(self, previous_stats, current_stats):
        movement_detected = False
        movement_segments = []

        # loop through the segments and compare the average and standard deviation of pixel values
        for i in range(min(len(previous_stats), len(current_stats))):
            for j in range(min(len(previous_stats[i]), len(current_stats[i]))):
                avg_diff = abs(previous_stats[i][j][0] - current_stats[i][j][0])
                std_diff = abs(previous_stats[i][j][1] - current_stats[i][j][1])

                # if the difference is greater than the threshold, then movement is detected
                if avg_diff > self.threshold or std_diff > self.threshold:
                    movement_detected = True
                    movement_segments.append((i, j))

        # return whether movement was detected and the segments where movement was detected
        return movement_detected, movement_segments

    # this method will run the motion detection demonstration
    def run(self):

        print("Press any key to exit.")
        capture = cv2.VideoCapture(0)
        if not capture.isOpened():
            print("Error: Could not open video device.")
            return

        cv2.namedWindow('Motion Detection Demonstration', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Recording Status', cv2.WINDOW_NORMAL)
        cv2.createTrackbar('Threshold', 'Motion Detection Demonstration', self.threshold, 255, self.update_threshold)
        cv2.createTrackbar('Segments', 'Motion Detection Demonstration', self.segments, 100, self.update_segments)
        cv2.createTrackbar('Delay (s)', 'Motion Detection Demonstration', self.delay_seconds, 60, self.update_delay)

        value, prev_frame = capture.read()
        if not value:
            print("Error: Could not read frame from video device.")
            capture.release()
            cv2.destroyAllWindows()
            return

        prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        prev_stats = self.segment_calculation(prev_frame_gray)

        while True:
            value, frame = capture.read()
            if not value:
                print("Error: Could not read frame from video device.")
                break
            
            current_stats = self.segment_calculation(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

            # ensure the stats are the same length before detecting movement
            if len(prev_stats) == len(current_stats) and all(len(row) == len(current_stats[i]) for i, row in enumerate(prev_stats)):
                movement_detected, movement_segments = self.detect_movement(prev_stats, current_stats)
                
                # if movement is detected, update the last motion time
                if movement_detected:
                    self.last_motion_time = time.time()
                    cv2.putText(frame, 'Motion', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(frame, '...', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                
                # draw rectangles around segments where movement was detected   
                frame_height, width = frame.shape[:2]
                segment_height = frame_height // self.segments
                segment_width = width // self.segments
                for (i, j) in movement_segments:
                    top_left = (j * segment_width, i * segment_height)
                    bottom_right = ((j + 1) * segment_width, (i + 1) * segment_height)
                    cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)

            # update previous stats
            prev_stats = current_stats

            # update recording status window
            time_since_last_motion = time.time() - self.last_motion_time
            if time_since_last_motion < self.delay_seconds:
                status_frame = frame.copy()
                cv2.putText(status_frame, 'RECORDING', (50, frame_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4, cv2.LINE_AA)
            else:
                status_frame = np.zeros_like(frame)
                cv2.putText(status_frame, 'IDLE', (50, frame_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4, cv2.LINE_AA)

            cv2.imshow('Motion Detection Demonstration', frame)
            cv2.imshow('Recording Status', status_frame)

            if cv2.waitKey(1) != -1:
                print("Exiting...")
                break

        capture.release()
        cv2.destroyAllWindows()

    # these methods will update the threshold, number of segments, and delay time
    def update_threshold(self, threshold_value): self.threshold = threshold_value
    def update_segments(self, segments_value): self.segments = max(segments_value, 1)
    def update_delay(self, delay_value): self.delay_seconds = delay_value

def main():

    print("Initializing Segmental Motion Detection Demonstration...")
    detector = SegmentalMotionDetection()
    detector.run()

if __name__ == "__main__":
    main()
