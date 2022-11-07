import torch

import bentoml
from bentoml.io import Image
from bentoml.io import PandasDataFrame
from core.config import get_app_settings

settings = get_app_settings()
user_id = settings.user_id
project_id = settings.project_id

print("Serving bentoml.py")
print(f"user_id: {user_id}")
print(f"project_id: {project_id}")


class Yolov5Runnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", "cpu")
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        # self.model = torch.hub.load("ultralytics/yolov5", "yolov5s")
        self.model = torch.hub.load('./', 'custom', path='best.pt', source='local')  # custom model
        # self.model = torch.load("yolov5s.pt")

        if torch.cuda.is_available():
            self.model.cuda()
        else:
            self.model.cpu()

        # Config inference settings
        self.inference_size = 640

        # Optional configs
        # self.model.conf = 0.25  # NMS confidence threshold
        # self.model.iou = 0.45  # NMS IoU threshold
        # self.model.agnostic = False  # NMS class-agnostic
        # self.model.multi_label = False  # NMS multiple labels per box
        # self.model.classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
        # self.model.max_det = 1000  # maximum number of detections per image
        # self.model.amp = False  # Automatic Mixed Precision (AMP) inference

    @bentoml.Runnable.method(batchable=True, batch_dim=0)
    def inference(self, input_imgs):
        # Return predictions only
        results = self.model(input_imgs, size=self.inference_size)
        return results.pandas().xyxy

    @bentoml.Runnable.method(batchable=True, batch_dim=0)
    def render(self, input_imgs):
        # Return images with boxes and labels
        return self.model(input_imgs, size=self.inference_size).render()


yolo_v5_runner = bentoml.Runner(Yolov5Runnable, max_batch_size=30)

svc = bentoml.Service(f"object_detection_{user_id}_project_id_{project_id}", runners=[yolo_v5_runner])


@svc.api(input=Image(), output=PandasDataFrame())
def invocation(input_img):
    return yolo_v5_runner.inference.run([input_img])[0]


@svc.api(input=Image(), output=Image())
def render(input_img):
    return yolo_v5_runner.render.run([input_img])[0]
