import cv2
import json

class BoundingBoxDrawer:
    def __init__(self, image_files):
        self.image_files = image_files
        self.current_image_index = 0
        self.image_file = self.image_files[self.current_image_index]
        self.image = cv2.imread(self.image_file)
        self.clone = self.image.copy()
        self.refPt = []
        self.cropping = False
        self.box_count = 0
        self.bounding_boxes = {}

    def click_and_crop(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            self.cropping = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.cropping == True:
                image_copy = self.image.copy()
                cv2.rectangle(image_copy, self.refPt[0], (x, y), (0, 255, 0), 2)
                cv2.imshow("image", image_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            self.refPt.append((x, y))
            self.cropping = False
            cv2.rectangle(self.image, self.refPt[0], self.refPt[1], (0, 255, 0), 2)
            cv2.imshow("image", self.image)
            self.box_count += 1
            if self.image_file not in self.bounding_boxes:
                self.bounding_boxes[self.image_file] = []
            self.bounding_boxes[self.image_file].append({
                'x1': min(self.refPt[0][0], self.refPt[1][0]),
                'y1': min(self.refPt[0][1], self.refPt[1][1]),
                'x2': max(self.refPt[0][0], self.refPt[1][0]),
                'y2': max(self.refPt[0][1], self.refPt[1][1])
            })
            if self.box_count == 3:
                filename, file_extension = self.image_file.rsplit('.', 1)
                cv2.imwrite(f"{filename}_bbox.{file_extension}", self.image)
                self.move_to_next_image()

    def move_to_next_image(self):
        self.current_image_index += 1
        if self.current_image_index < len(self.image_files):
            self.image_file = self.image_files[self.current_image_index]
            self.image = cv2.imread(self.image_file)
            self.clone = self.image.copy()
            self.refPt = []
            self.cropping = False
            self.box_count = 0
        else:
            cv2.destroyAllWindows()
            import json
            with open('bounding_boxes.json', 'w') as f:
                json.dump(self.bounding_boxes, f)

    def draw_boxes(self):
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_and_crop)
        while True:
            cv2.imshow("image", self.image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                cv2.destroyAllWindows()
                import json
                with open('bounding_boxes.json', 'w') as f:
                    json.dump(self.bounding_boxes, f)
                break

image_files = ["thyrocare_0_1374.jpg", "thyrocare_0_1861.jpg", "thyrocare_0_2300.jpg", "thyrocare_0_3813.jpg", "thyrocare_0_5816.jpg", "thyrocare_0_5858.jpg", "thyrocare_0_7635.jpg", "thyrocare_0_7791.jpg", "thyrocare_0_8251.jpg", "thyrocare_0_8302.jpg"]
drawer = BoundingBoxDrawer(image_files)
drawer.draw_boxes()