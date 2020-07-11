from .find_obj import get_bbox, get_view_image
from .create_objs import load_x_objs

# Inspiration: https://github.com/hazirbas/coco-json-converter/blob/master/generate_coco_json.py


class BulletToCOCO():
    def __init__(self, obj_folders, image_count=100, obj_repeat=5):
        self.image_count = image_count
        self.obj_repeat = obj_repeat

        self.info = {
            "year": 2020,
            "version": "1.0",
            "description": "A Dataset Created for PyBullet Robot Arm Object Detection Training.",
            "contributor": "Ian Huang",
            "url": "",
            "date_created": "2020"
        }
        self.license = {"id": 1,
                        "name": "Attribution-NonCommercial",
                        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
                        }

        self.generate()

    def generate(self):
        pass

    def bbox_to_xywh(self, aa, bb):
        (aax, aay) = aa
        (bbx, bby) = bb

        x = bbx if aax > bbx else aax
        y = bby if aay > bby else aay
        w = abs(aax - bbx)
        h = abs(aay - bby)

        return [x, y, w, h]

    def generate_annotations(self, obj_ids, image_id):

        annotations = []

        for obj_id in obj_ids:
            # compute annotations
            annotation = dict()

            aa, bb = get_bbox(obj_id)
            [x, y, w, h] = bbox_to_xywh(aa, bb)
            area = w * h

            annotation['segmentation'] = []
            annotation['bbox'] = [x, y, w, h]
            annotation['area'] = area
            annotation['iscrowd'] = 0
            annotation['image_id'] = image_id
            annotation['category_id'] = obj_id
            annotation['id'] = obj_id + "1"

            annotations.append(annotation)

        return annotations

    def generate_images(self):
        # save the image
        rgb_img = get_view_image()

        return rgb_img
