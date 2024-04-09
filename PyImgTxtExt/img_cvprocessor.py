import cv2
import numpy as np


def show_img(title='CV Image', img=None):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def create_window():
    cv2.namedWindow('Trackbar', cv2.WINDOW_NORMAL)
    cv2.resizeWindow(winname='Trackbar', width=450, height=450)


def create_trackbars():
    cv2.createTrackbar('Resize', 'Trackbar', 9, 10, do_nothing)
    cv2.createTrackbar('Threshold', 'Trackbar', 125, 255, do_nothing)
    cv2.createTrackbar('Thresh Inverse', 'Trackbar', 125, 255, do_nothing)
    cv2.createTrackbar('Blur', 'Trackbar', 5, 10, do_nothing)
    cv2.createTrackbar('Canny Edge', 'Trackbar', 300, 500, do_nothing)
    cv2.createTrackbar('ED Kernel', 'Trackbar', 5, 10, do_nothing)
    cv2.createTrackbar('ED Iterations', 'Trackbar', 1, 5, do_nothing)
    cv2.createTrackbar('Contour Size', 'Trackbar', 50, 1000, do_nothing)
    cv2.createTrackbar('Contour Color', 'Trackbar', 1, 2, do_nothing)
    cv2.createTrackbar('Contour Thickness', 'Trackbar', 2, 10, do_nothing)


def do_nothing(x):
    pass


def get_resize_trackbar():
    value = cv2.getTrackbarPos('Resize', 'Trackbar')
    return value


def get_thresh_trackbar():
    value = cv2.getTrackbarPos('Threshold', 'Trackbar')
    return value


def get_thresh_inv_trackbar():
    value = cv2.getTrackbarPos('Threshold Inverse', 'Trackbar')
    return value


def get_blur_trackbar():
    value = cv2.getTrackbarPos('Blur', 'Trackbar')
    return value


def get_canny_trackbar():
    value = cv2.getTrackbarPos('Canny Edge', 'Trackbar')
    return value


def get_erode_dilate_trackbar():
    kernel_val = cv2.getTrackbarPos('ED Kernel', 'Trackbar')
    iterations_val = cv2.getTrackbarPos('ED Iterations', 'Trackbar')
    return kernel_val, iterations_val


def get_contours_trackbar():
    size_val = cv2.getTrackbarPos('Contour Size', 'Trackbar')
    color_val = cv2.getTrackbarPos('Contour Color', 'Trackbar')
    thickness_val = cv2.getTrackbarPos('Contour Thickness', 'Trackbar')
    return size_val, color_val, thickness_val


def bgr_to_rgb_spectrum(img=None):
    if img is not None:
        img_copy = img.copy()
        img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
        return img_copy


class CVProcessor:

    def __init__(self, img=None):
        self.bgr_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.original_img = None
        self.copy_img = None
        self.gray_img = None
        self.thresh_img = None
        self.thresh_inv_img = None
        self.blur_img = None
        self.canny_img = None
        self.erode_img = None
        self.dilate_img = None
        if img:
            self.original_img = cv2.imread(img)
            self.copy_img = self.original_img.copy()
            create_window()
            create_trackbars()

    def resize_image(self, x_scale=1, y_scale=1):
        if self.copy_img is not None:
            self.copy_img = cv2.resize(self.copy_img, (0, 0), fx=x_scale, fy=y_scale)
            inter_img = bgr_to_rgb_spectrum(img=self.copy_img)
            return inter_img

    def gray_image(self):
        if self.copy_img is not None:
            self.gray_img = cv2.cvtColor(self.copy_img, cv2.COLOR_BGR2GRAY)
            inter_img = bgr_to_rgb_spectrum(img=self.gray_img)
            return inter_img

    def thresh_image(self, thresh_val=125):
        if self.gray_img is not None:
            self.thresh_img = cv2.threshold(self.gray_img, thresh_val, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            inter_img = bgr_to_rgb_spectrum(self.thresh_img)
            return inter_img

    def thresh_inv_image(self, thresh_val=125):
        if self.gray_img is not None:
            self.thresh_inv_img = cv2.threshold(self.gray_img, thresh_val, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            inter_img = bgr_to_rgb_spectrum(self.thresh_inv_img)
            return inter_img

    def blur_image(self, blur_val=5):
        kernel = (blur_val, blur_val)
        if self.thresh_img is not None:
            self.blur_img = cv2.GaussianBlur(self.thresh_img, kernel, 0)
        elif self.thresh_inv_img is not None:
            self.blur_img = cv2.GaussianBlur(self.thresh_inv_img, kernel, 0)
        else:
            self.blur_img = None
        if self.blur_img is not None:
            inter_img = bgr_to_rgb_spectrum(self.blur_img)
            return inter_img

    def canny_image(self, lower_thresh=100, upper_thresh=300):
        if self.blur_img is not None:
            self.canny_img = cv2.Canny(self.blur_img, lower_thresh, upper_thresh)
            inter_img = bgr_to_rgb_spectrum(self.canny_img)
            return inter_img

    def erode_image(self, kernel_val=5, iteration_val=1):
        if self.blur_img is not None:
            kernel = np.ones((kernel_val, kernel_val), np.uint8)
            self.erode_img = cv2.erode(self.blur_img, kernel=kernel, iterations=iteration_val)
            inter_img = bgr_to_rgb_spectrum(self.erode_img)
            return inter_img

    def dilate_image(self, kernel_val=5, iteration_val=1):
        if self.erode_img is not None:
            kernel = np.ones((kernel_val, kernel_val), np.uint8)
            self.dilate_img = cv2.dilate(self.erode_img, kernel=kernel, iterations=iteration_val)
            inter_img = bgr_to_rgb_spectrum(self.dilate_img)
            return inter_img

    def draw_contours(self, area_size=50, rectangle_color=1, thickness=2):
        if self.dilate_img is not None:
            bbox_color = self.bgr_colors[rectangle_color]
            contours, hierarchy = cv2.findContours(self.dilate_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area >= area_size:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(self.copy_img, (x, y), (x + w, y + h), color=bbox_color, thickness=thickness)
        if self.copy_img is not None:
            inter_img = bgr_to_rgb_spectrum(self.copy_img)
            return inter_img

    def restore_original(self):
        self.copy_img = None
        self.gray_img = None
        self.thresh_img = None
        self.thresh_inv_img = None
        self.blur_img = None
        self.canny_img = None
        self.erode_img = None
        self.dilate_img = None
        self.copy_img = self.original_img.copy()
        return self.copy_img
