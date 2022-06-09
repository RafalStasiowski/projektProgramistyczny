import cv2
from anonymize_face import anonymize_face_simple
from anonymize_face import anonymize_face_pixelate
import numpy as np


def find_face(image):
    prototxtPath = "face_detector/deploy.prototxt"
    weightsPath = "face_detector/res10_300x300_ssd_iter_140000.caffemodel"
    confidence_in = 0.2
    # prototxtPath = 'face_detector/aaa/graph.pbtxt'
    # weightsPath = 'face_detector/aaa/frozen_inference_graph.pb'

    (h, w) = image.shape[:2]

    net = cv2.dnn.readNet(prototxtPath, weightsPath)
    blob = cv2.dnn.blobFromImage(image, 1.0, (1024, 768),
                                 (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > confidence_in:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            face = image[startY:endY, startX:endX]

            face = anonymize_face_pixelate(face, blocks=4)

            image[startY:endY, startX:endX] = face

    output = image
    return output


