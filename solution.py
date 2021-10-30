import os
from imaging_interview import preprocess_image, compare_frames
import cv2
import glob
import time
from tqdm import tqdm



def is_similar(prev_frame, next_frame):
    """

    :param prev_frame:
    :param next_frame:
    :return:
    """
    img1 = cv2.imread(prev_frame)
    img2 = cv2.imread(next_frame)
    processed_img1 = preprocess_image(img1, [21])
    processed_img2 = preprocess_image(img2, [21])
    score, _, _ = compare_frames(processed_img1, processed_img2, 7000.0)
    if score == 0:
        return True
    else:
        return False


def remove_similar_images():
    """

    :return:
    """
    removed_image_list = []
    # remove similar consecutive image frames
    image_frame_list = [img for img in glob.glob("c23/*.png")]
    frame_pbar = tqdm(len(image_frame_list)-1)
    frame_pbar.set_description("Deleting consecutive similar image frames: ")

    for i in range(len(image_frame_list) - 1):
        frame_pbar.update()
        if is_similar(image_frame_list[i], image_frame_list[i + 1]):
            removed_image_list.append(image_frame_list[i])
            os.remove(image_frame_list[i])
    frame_pbar.close()

    # remove the remaining similar images
    image_list = [img for img in glob.glob("c23/*.png")]
    i = 0
    img_pbar = tqdm(len(image_list))
    img_pbar.set_description("Deleting similar images: ")

    while i < len(image_list):
        img_pbar.update()
        j = i + 1
        while j < len(image_list):
            if is_similar(image_list[i], image_list[j]):
                os.remove(image_list[j])
                removed_image_list.append(image_list[j])
                del image_list[j]
            else:
                j += 1
        i += 1
    img_pbar.close()

    return len(removed_image_list)


if __name__ == "__main__":
    print(f"Total deleted images: {remove_similar_images()}")
