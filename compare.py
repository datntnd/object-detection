import os
import val
from Config import ConfigYolov5Compare
import uuid
import mlflow
import json
from minio import Minio
from minio.error import S3Error
from core.config import get_app_settings
settings = get_app_settings()


minioClient = Minio(settings.minio_endpoint,
                    access_key=settings.minio_access_key,
                    secret_key=settings.minio_secret_key,
                    secure=False)
model_bucket = "model"



def compare(opt):
    
    output = {
        "status": "Running",
        "best_model_result": None,
        "latest_model_result": None,
        "is_lastest_better": False
    }
    with open('compare.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    minioClient.fput_object("pipeline", f"{settings.user_id}/{settings.project_id}/{settings.dataset_version_id}/{settings.pipeline_id}/compare.json", "compare.json")
    mlflow.set_tracking_uri("http://10.255.187.41:5120")
    mlflow.set_experiment(f"yolov5-compare-{settings.pipeline_id}")
    weights = "./runs/train/"
    exps = os.listdir(weights)
    # if len(exps) == 1:
    #     weights = "/home/tuannm/jenkins_home/workspace/mlops-demo/runs/train/weights/best.pt"
    latest = 0
    for exp in exps:
        exp_number = int(exp[3:]) if exp != "exp" else 0
        latest = latest if latest >= exp_number else exp_number
    if latest == 0:
        weights = f"{weights}exp/weights/best.pt"
    else:
        weights = f"{weights}exp{latest}/weights/best.pt"

    result_1 = val.run(data=opt.data, weights=weights, batch_size=opt.batch_size, imgsz=opt.imgsz,
                       conf_thres=opt.conf_thres, iou_thres=opt.iou_thres, task=opt.task, device=opt.device,
                       workers=opt.workers, single_cls=opt.single_cls, augment=opt.augment, verbose=opt.verbose,
                       save_txt=opt.save_txt, save_hybrid=opt.save_hybrid, save_conf=opt.save_conf,
                       save_json=opt.save_json)
    try:
        minioClient.fget_object(model_bucket, f"{settings.user_id}/{settings.project_id}/best.pt", "./best.pt")
        result_2 = val.run(data=opt.data, weights="./best.pt", batch_size=opt.batch_size, imgsz=opt.imgsz,
                       conf_thres=opt.conf_thres, iou_thres=opt.iou_thres, task=opt.task, device=opt.device,
                       workers=opt.workers, single_cls=opt.single_cls, augment=opt.augment, verbose=opt.verbose,
                       save_txt=opt.save_txt, save_hybrid=opt.save_hybrid, save_conf=opt.save_conf,
                       save_json=opt.save_json)
        
    except S3Error:
        print(weights)
        print("object not found")
        result_2 = result_1

    if result_1[0][2] >= result_2[0][2]:
            output["is_lastest_better"] = True
            minioClient.fput_object(model_bucket, f"{settings.user_id}/{settings.project_id}/best.pt", weights)
    output["latest_model_result"] = result_1[0][2]
    output["best_model_result"] = result_2[0][2]
    output["status"] = "Done"
    with open('compare.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    mlflow.log_params(output)
    minioClient.fput_object("pipeline", f"{settings.user_id}/{settings.project_id}/{settings.dataset_version_id}/{settings.pipeline_id}/compare.json", "compare.json")

if __name__ == "__main__":
    config = {
        "data": f'data/{settings.dataset_version_id}/data.yaml',
        "task": "test"
    }
    opt = ConfigYolov5Compare(config_dict=config)
    compare(opt)
