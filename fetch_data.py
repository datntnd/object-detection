import json

import requests
from minio import Minio
from core.config import get_app_settings
import yaml
import glob
import os


settings = get_app_settings()
minio_client = Minio(settings.minio_endpoint, access_key=settings.minio_access_key,
                     secret_key=settings.minio_secret_key, secure=False)

classes = []


def get_data_from_minio_storage(user_id, project_id, dataset_version_id):
    data_bucket_name = settings.data_bucket_name
    dataset_types = minio_client.list_objects(data_bucket_name, prefix=f"{user_id}/{project_id}/labels/{dataset_version_id}/")
    images = minio_client.list_objects(data_bucket_name, f"{user_id}/{project_id}/images/")
    image_dict = {}

    folder = f'data/{dataset_version_id}'

    for image in images:
        object_name = str(image.object_name)
        image_dict[object_name.split("/")[-1].split(".")[0]] = object_name

    for dataset_type in dataset_types:
        dataset_type = str(dataset_type.object_name)
        dataset_type = (dataset_type.split('/'))[-2]
        path_dataset_type = f'{user_id}/{project_id}/labels/{dataset_version_id}/{dataset_type}/'
        labels_object = minio_client.list_objects(data_bucket_name, prefix=path_dataset_type)
        for label_object in labels_object:
            object_name = str(label_object.object_name)
            label_name = (object_name.split('/'))[-1]
            name_simple = label_name.split(".")[0]
            minio_client.fget_object(data_bucket_name, image_dict[name_simple],
                                     f'{folder}/{dataset_type}/images/{name_simple}.jpg')

            minio_client.fget_object(data_bucket_name, f'{user_id}/{project_id}/labels/{dataset_version_id}/{dataset_type}/{label_name}',
                                     f'{folder}/{dataset_type}/label/{label_name}')

        convert_yolo_format_data(
            labels_folder=f'{folder}/{dataset_type}/label',
            new_labels_folder=f'{folder}/{dataset_type}/labels',
        )

    data = dict(
        train=folder + '/training/images',
        val=folder + '/validation/images',
        test=folder + "/testing/images",
        nc=len(classes),
        names=classes
    )
    with open(f'{folder}/data.yaml', 'w') as outfile:
        yaml.safe_dump(data, outfile, default_flow_style=False)


def convert_yolo_format_data(labels_folder="label", new_labels_folder="new_label"):
    if not os.path.exists(new_labels_folder):
        os.mkdir(new_labels_folder)

    for file in glob.glob(labels_folder + "/*.txt"):
        label_file = open(file, "r")
        new_label_file = open(new_labels_folder + file[len(labels_folder):], "w")
        labels = label_file.readlines()
        for label in labels:
            obj = label.strip().split(" ")
            label_class = " ".join(obj[:-4])
            if label_class not in classes:
                classes.append(label_class)
            index = classes.index(label_class)
            try:

                new_label_file.write(
                    f'{index} {float(obj[1-5])+float(obj[3-5])/2} {float(obj[2-5])+float(obj[4-5])/2} {float(obj[3-5])} {float(obj[4-5])}')
            except ValueError:
                print("value error")
            except IndexError:
                print("index error")


if __name__ == "__main__":
    if not settings.dataset_version_id:
        response = requests.post("http://10.255.187.48:8089/api/v1/pipeline/create-pipeline",
                                 json={
                                     "project_id": int(settings.project_id),
                                 }, headers={"token": settings.user_id})
        print(response.text)
        response = json.loads(response.text).get("data")
        dataset_version_id = response.get("dataset_version_id")
        pipeline_id = response.get("pipeline_id")
        f = open("core/settings/env.txt", "w")
        f.write(f"{pipeline_id}\n")
        f.write(f"{dataset_version_id}")
        f.close()

    else:
        dataset_version_id = settings.dataset_version_id

    get_data_from_minio_storage(
        user_id=settings.user_id,
        project_id=settings.project_id,
        dataset_version_id=dataset_version_id)
