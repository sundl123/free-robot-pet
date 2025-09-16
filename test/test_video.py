import unittest


class TestVideo(unittest.TestCase):
    def test_video(self):
        import cv2

        # Step 1: Create a VideoCapture object to capture video from the first camera
        cap = cv2.VideoCapture(0)
        # cap.set(3, 320)
        # cap.set(4, 240)

        # Step 2: Check if the camera opened successfully
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        # Step 3: Capture a single frame
        for i in range(100):
            ret, frame = cap.read()

            # Check if frame is read correctly
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                exit()

        # Step 4: Encode the frame as a JPEG image
        ret, jpeg = cv2.imencode('.jpg', frame)

        # Step 5: You can now use the JPEG image (stored in 'jpeg' variable)
        # For example, to save it to a file:
        with open('frame.jpg', 'wb') as f:
            f.write(jpeg)

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def test_video_2(self):
        import cv2

        # Try different indices if 0 doesn't work
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            cv2.imshow('Camera Test', frame)

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    unittest.main()
