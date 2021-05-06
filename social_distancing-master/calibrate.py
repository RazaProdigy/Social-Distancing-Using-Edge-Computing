import sys
import argparse
import cv2
import pickle
from config.config import Configuration as config
from calibration.transform_camera_view import TransformCameraView
from calibration.scale_factor_estimation import ScaleFactorEstimator

def gstreamer_pipeline(
    capture_width=3280,
    capture_height=2464,
    display_width=820,
    display_height=616,
    framerate=21,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def transform_camera_view(image, no_points):
    transformer = TransformCameraView(image)
    transformer.mark_points_on_camera_view_image(no_points)
    transformer.mark_points_on_top_view(no_points)
    transformer.calculate_transformation()
    transformer.generate_transformed_image()
    transformer.display_camera_image_on_top_view()
    cv2.destroyAllWindows()

    return transformer


def calculate_scale_factor(image, transformation_matrix, no_points, iterations):
    scale_factor_estimator = ScaleFactorEstimator(image, transformation_matrix)
    for i in range(iterations):
        scale_factor_estimator.mark_points(no_points)

    return scale_factor_estimator.estimate_scale_factor()


def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video_path", required=True, help="Path to video file.")
    ap.add_argument("-n", "--num_points", required=False, type=int, default=4, help="Number of calibration points.")
    ap.add_argument("-iter", "--num_iterations", required=False, type=int, default=4,
                    help="Number of iterations for finding the scale factor.")

    return vars(ap.parse_args())


if __name__ == "__main__":
    # Read program config
    config.load_config("./config.yml")
    # Parse the command line arguments
    args = parse_arguments()
    video_path = args["video_path"]
    num_points = args["num_points"]
    num_iterations = args["num_iterations"]
    # Read video and get the first frame
    video = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if video.isOpened():
         ret, frame = video.read()
         if not ret:
             print(f"Error reading the video file. Existing")
             sys.exit(1)
    else:
         print(f"Invalid video path. Existing")
         sys.exit(1)
    video.release()
    #img = cv2.imread(video_path)
    #scale_percent = 20 # percent of original size
    #width = int(img.shape[1] * scale_percent / 100)
    #height = int(img.shape[0] * scale_percent / 100)
    #dim = (width, height)
    # resize image
    #frame = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    # Estimate the camera view to bird eye view transformation and scale factor
    cal_obj = transform_camera_view(frame, num_points)
    scale_factor = calculate_scale_factor(frame, cal_obj.transformation_matrix, 2, num_iterations)
    # Save the transformation matrix and scale factor as pkl file
    pkl_file_path = config.cfg["calibration"]["pkl_file_path"]
    with open(pkl_file_path, 'wb') as f:
        pickle.dump([cal_obj.transformation_matrix, scale_factor], f)

    print(f"Calibration completed and written to '{pkl_file_path}'.")
