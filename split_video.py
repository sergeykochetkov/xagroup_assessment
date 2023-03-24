import os
import cv2
from argparse import ArgumentParser
from YOLO3D.inference import detect3d, ROOT


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('videos_dir', help='path to videos directory')

    parser.add_argument(
        '--score-thr', type=float, default=0.15, help='bbox score threshold')
    # yolo3d
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path(s)')

    parser.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--classes', default=[0, 2, 3, 5], nargs='+', type=int,
                        help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--reg_weights', type=str, default='weights/epoch_10.pkl', help='Regressor model weights')
    parser.add_argument('--model_select', type=str, default='resnet', help='Regressor model list: resnet, vgg, eff')
    parser.add_argument('--calib_file', type=str, default=ROOT / 'eval/camera_cal/calib_cam_to_cam.txt',
                        help='Calibration file or path')
    parser.add_argument('--show_result', action='store_true', help='Show Results with imshow')
    parser.add_argument('--save_result', action='store_true', help='Save result')
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    tmp_dir = 'tmp_5'
    show_every = 5
    os.makedirs(tmp_dir, exist_ok=True)

    for video_i, filename in enumerate(os.listdir(args.videos_dir)):
        cap = cv2.VideoCapture(os.path.join(args.videos_dir, filename))

        video_dir = os.path.join(tmp_dir, str(video_i))
        os.makedirs(video_dir, exist_ok=True)
        fps = cap.get(cv2.CAP_PROP_FPS) / show_every
        print(f' fps = {fps}')
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:

                if count % show_every == 0:
                    image_path = os.path.join(video_dir, f'tmp_{count:0>5}.png')
                    cv2.imwrite(image_path, frame)

                count += 1
            else:
                break

        cap.release()
