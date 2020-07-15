import os
import png
import json
import random
import pybullet as p

from PIL import Image

from .find_obj import get_bbox, get_view_image
from .create_objs import load_x_objs

# Inspiration: https://github.com/hazirbas/coco-json-converter/blob/master/generate_coco_json.py
PIXEL_WIDTH = 1920
PIXEL_HEIGHT = 1080


class BulletToCOCO():
    def __init__(self, obj_folders, save_path, image_count=100, obj_repeat=2, obj_per_view=5):
        self.obj_folders = obj_folders
        self.save_path = save_path
        self.image_count = image_count
        self.obj_repeat = obj_repeat
        self.obj_per_view = obj_per_view

        self.images = []
        self.annotations = []

        self.info = {
            "year": 2020,
            "version": "1.0",
            "description": "A Dataset Created for PyBullet Robot Arm Object Detection Training.",
            "contributor": "Ian Huang",
            "url": "",
            "date_created": "2020"
        }
        self.licenses = {
            "id": 1,
            "name": "",
            "url": ""
        }
        self.categories = dict()
        self.type = 'instances'

        self.generate()

    def generate(self):
        for i in range(self.image_count):
            self.run_iteration()

        print('Done with Image generation. ')

        json_data = {
            'info': self.info,
            'images': self.images,
            'licenses': self.licenses,
            'type': self.type,
            'annotations': self.annotations,
            'categories': [a[1] for a in self.categories.items()]
        }

        with open(os.path.join(self.save_path, "annotations", "all.json"), 'w') as jsonfile:
            json.dump(json_data, jsonfile)

        print('Done with JSON generation. ')

    def run_iteration(self):
        # randomply pick and create objects
        obj_data = load_x_objs(self.obj_folders, 4, count=self.obj_per_view,
                               offset=random.randrange(0, self.image_count))
        for obj in obj_data:
            category = obj['file']
            if not category in self.categories:
                self.categories[category] = ({
                    'id': obj['id']+10,
                    'name': category,
                    'supercategory': category
                })

        for _ in range(1000):
            # somewhat stabilize simulation
            p.stepSimulation()

        # randomly set camera position and distance
        view_matrix = p.computeViewMatrixFromYawPitchRoll(
            cameraTargetPosition=[0, 0, 0],
            distance=10,
            yaw=180,
            pitch=-90.0,
            roll=0,
            upAxisIndex=2
        )
        projection_matrix = p.computeProjectionMatrixFOV(
            fov=60.0,
            aspect=PIXEL_WIDTH/PIXEL_HEIGHT,
            nearVal=0.01,
            farVal=100
        )

        # take a picture
        rgb_img = get_view_image(
            PIXEL_WIDTH, PIXEL_HEIGHT, view_matrix, projection_matrix)
        im = Image.fromarray(rgb_img)
        img_id = len(self.images)

        img_filename = str(img_id)+'.png'
        img_path = os.path.join(self.save_path, 'images', img_filename)
        self.images.append({
            "data_captured": "2020",
            "file_name": img_filename,
            "id": img_id,
            "license": 1,
            "url": "",
            "height": PIXEL_HEIGHT,
            "width": PIXEL_WIDTH
        })
        im.save(img_path)

        # get annotations
        img_annots = self.generate_annotations(obj_data, img_id)
        self.annotations.append(img_annots)

        # clean up
        for obj in obj_data:
            p.removeBody(obj["id"])

        # return img, annotations
        return rgb_img, img_annots

    def bbox_to_xywh(self, aa, bb):
        (aax, aay) = aa
        (bbx, bby) = bb

        x = bbx if aax > bbx else aax
        y = bby if aay > bby else aay
        w = abs(aax - bbx)
        h = abs(aay - bby)

        return [x, y, w, h]

    def generate_annotations(self, obj_data, image_id):
        annotations = []

        for obj in obj_data:
            # compute annotations
            annotation = dict()

            obj_id = obj['id']
            obj_file = obj['file']

            aa, bb = get_bbox(obj_id)
            [x, y, w, h] = self.bbox_to_xywh(aa, bb)
            area = w * h

            annotation['segmentation'] = []
            annotation['bbox'] = [x, y, w, h]
            annotation['area'] = area
            annotation['iscrowd'] = 0
            annotation['image_id'] = image_id
            annotation['category_id'] = obj_file
            annotation['id'] = obj_file + "abc"

            annotations.append(annotation)

        return annotations

    def generate_images(self):
        # save the image
        rgb_img = get_view_image()

        return rgb_img
