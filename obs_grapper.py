import cv2


def get():
    cam = cv2.VideoCapture(3)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    ret, frame = cam.read()
    frame = cv2.resize(frame, None, None, 0.3, 0.3)
    cv2.imwrite("test_screenshot.png", frame)
