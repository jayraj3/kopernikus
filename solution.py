import os
from imaging_interview import preprocess_image_change_detection, compare_frames_change_detection
import cv2
import glob
from tqdm import tqdm
import argparse


def is_similar(prev_frame, next_frame):
    """Check similarity between two images

    :param  prev_frame: Previous frame path
    :type prev_frame: str
    :param next_frame: Next frame path
    :type next_frame: str
    :return: True for similar images
    :rtype: bool
    """
    img1 = cv2.imread(prev_frame)
    img2 = cv2.imread(next_frame)
    processed_img1 = preprocess_image_change_detection(img1, [21])
    processed_img2 = preprocess_image_change_detection(img2, [21])
    min_contour_area = 7000
    score, _, _ = compare_frames_change_detection(processed_img1, processed_img2, min_contour_area)
    if score == 0:
        return True
    else:
        return False


def delete_similar_images(path):
    """ Delete similar images from directory

    :param path: Image directory path
    :type path: str
    :return: total deleted images
    :rtype: int
    """
    deleted_image_list = []
    # remove similar consecutive image frames
    image_frame_list = [img for img in glob.glob(path + "/*.png")]
    frame_pbar = tqdm(len(image_frame_list) - 1)
    frame_pbar.set_description("Deleting consecutive similar image frames: ")

    for i in range(len(image_frame_list) - 1):
        frame_pbar.update()
        if is_similar(image_frame_list[i], image_frame_list[i + 1]):
            deleted_image_list.append(image_frame_list[i])
            os.remove(image_frame_list[i])
    frame_pbar.close()

    # remove the remaining similar images
    image_list = [img for img in glob.glob(path + "/*.png")]
    i = 0
    img_pbar = tqdm(len(image_list))
    img_pbar.set_description("Deleting similar images: ")

    while i < len(image_list):
        img_pbar.update()
        j = i + 1
        while j < len(image_list):
            if is_similar(image_list[i], image_list[j]):
                os.remove(image_list[j])
                deleted_image_list.append(image_list[j])
                del image_list[j]
            else:
                j += 1
        i += 1
    img_pbar.close()

    return len(deleted_image_list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="image directory path to delete similar images")
    args = parser.parse_args()
    path = args.path
    print(f"Total deleted images: {delete_similar_images(path)}")


if __name__ == "__main__":
    main()
