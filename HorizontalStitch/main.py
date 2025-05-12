import cv2
import numpy as np

def combine_images_horizontally(images):
    return np.hstack(images)
def main():
    image1_path = 'Images/1.jpg'
    image2_path = 'Images/2.jpg'
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    
    if image1 is None:
        print(f"Image could not be loaded: {image1_path}")
        return
    if image2 is None:
        print(f"Image could not be loaded: {image2_path}")
        return

    height = max(image1.shape[0], image2.shape[0])
    width = max(image1.shape[1], image2.shape[1])
    resized_image1 = cv2.resize(image1, (width, height))
    resized_image2 = cv2.resize(image2, (width, height))

    combined_horizontal = combine_images_horizontally([resized_image1, resized_image2])
    cv2.imwrite("combined_horizontal.jpg", combined_horizontal)
    cv2.imshow("Horizontal Combination", combined_horizontal)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
