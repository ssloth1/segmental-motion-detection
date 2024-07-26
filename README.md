# Segmental Motion Detection

A Python-based segmental motion detection system that uses OpenCV to identify and highlight movement within a video feed. The program divides the video frame into segments and detects movement based on statistical changes in pixel values.

## Features

- **Segmental Analysis**: The video frame is divided into segments for detailed motion analysis.
- **Motion Detection**: Detects and highlights movement in the video feed based on changes in pixel values.
- **Configurable Settings**: Adjust the number of segments, detection threshold, and recording delay time using trackbars.
- **Recording Status**: Displays 'RECORDING' or 'IDLE' status based on detected movement.

## Code Overview

### `SegmentalMotionDetection` Class

- **`__init__(self, segments=20, threshold=10, delay_seconds=3)`**: Initializes the class with the number of segments, threshold, and delay time.
- **`segment_calculation(self, frame)`**: Calculates the average and standard deviation of pixel values in each segment.
- **`detect_movement(self, previous_stats, current_stats)`**: Compares the average and standard deviation of pixel values in each segment to detect movement.
- **`run(self)`**: Runs the motion detection demonstration.
- **`update_threshold(self, threshold_value)`**: Updates the threshold value.
- **`update_segments(self, segments_value)`**: Updates the number of segments.
- **`update_delay(self, delay_value)`**: Updates the delay time.

### `main()`

- Initializes and runs the `SegmentalMotionDetection` demonstration.

## License

This project is licensed under the MIT License.

## Author

James Bebarski
