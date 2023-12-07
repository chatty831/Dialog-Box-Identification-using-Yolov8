from shapely.geometry import Polygon
from shapely.ops import unary_union
import cv2
import numpy as np
import os

def img_details(img_path):
    return os.path.splitext(os.path.basename(img_path))

    
def generate(img_path,model,model_name):
    
    img = cv2.imread(img_path)
    img_h,img_w,_ = img.shape
    imgs = []
    num_img = 1
    
    if img_h > 640*2:
        num_img = img_h//(int(1.8*640))
        for i in range(num_img):
            temp = img[i*img_h // (num_img):(i+1)*img_h // (num_img), :]
            imgs.append(temp)

        results = model.predict(
        source=imgs,
        # save=True,
        stream = False,
        conf=0.4,
        half=True,
        retina_masks = True,
        show_conf = False,
        show_labels = False
        )
        
    else:
        results = model.predict(
        source=img,
        # save=True,
        stream = False,
        conf=0.4,
        half=True,
        retina_masks = True,
        show_conf = False,
        show_labels = False
        )
        
    bboxes = []
    for i,result in enumerate(results):
        for j in range(result.boxes.shape[0]):
            xc,yc,w,h = np.round(result.boxes.xywh[j].cpu().numpy())
            bbox = cv2.boxPoints(((xc,yc),(w,h),0))
            for coord in bbox:
                coord[1] = coord[1] + (img_h/num_img)*(i)
            bboxes.append(bbox)
    
    intersections = {}
    for bbox in bboxes:
        poly1 = Polygon(bbox)
        intersections[poly1] = []
        for bbox2 in bboxes:
            poly2 = Polygon(bbox2)
            if poly1.intersection(poly2).area>0:
                intersections[poly1].append(poly2)
    
    combined_polygons = set() 
    for poly in intersections:
        combined_polygon = unary_union(intersections[poly])
        combined_polygons.add(combined_polygon)
                
    
    
    for combined_polygon in combined_polygons:
        points = list(combined_polygon.exterior.coords)
        points = np.array([[(x),(y)] for x,y in points[:-1]],np.int32)
        points = points.reshape(-1,1,2)
        
        img = cv2.polylines(img, [points], isClosed=True, color=(255,0,0), thickness=4)
    
    img_det = img_details(img_path)
    path = f'./static/transforms/{model_name}_{img_det[0]}_changed{img_det[1]}'
    cv2.imwrite(path,img)
    return os.path.normpath(path)