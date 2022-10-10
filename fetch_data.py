from minio import Minio
from convert import convert_yolo_format_data
from core.config import get_app_settings

import torch
print("check")
print(torch.cuda.is_available())

settings = get_app_settings()
minio_client = Minio(settings.minio_endpoint, access_key=settings.minio_access_key, secret_key=settings.minio_secret_key, secure=False)



def get_data_from_minio_storage(user_id, project_id, dataset_version_id):
    data_bucket_name = settings.data_bucket_name
    dataset_types = minio_client.list_objects(data_bucket_name, prefix=f"{user_id}/{project_id}/labels/{dataset_version_id}/")
    images = minio_client.list_objects(data_bucket_name, f"{user_id}/{project_id}/images/")
    image_dict = {}
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
                               f'data/{dataset_version_id}/{dataset_type}/images/{name_simple}.jpg')

            minio_client.fget_object(data_bucket_name, f'{user_id}/{project_id}/labels/{dataset_version_id}/{dataset_type}/{label_name}',
                               f'data/{dataset_version_id}/{dataset_type}/label/{label_name}')

        convert_yolo_format_data(
            labels_folder=f'data/{dataset_version_id}/{dataset_type}/label',
            new_labels_folder=f'data/{dataset_version_id}/{dataset_type}/labels',
            folder=f'data/{dataset_version_id}'
        )

if not settings.dataset_version_id:
    response = requests.post("http://10.255.187.48:8089/api/v1/pipeline/create-pipeline",
    json={
        "project_id": int(settings.project_id),
    }, headers={"token": settings.user_id}, proxies = {
        "http_proxy": "http://10.61.11.42:3128",
        "https_proxy": "http://10.61.11.42:3128"
    })
    print(response.text)
    response = json.loads(response.text).get("data")
    dataset_version_id = response.get("dataset_version_id")
    pipeline_id = response.get("pipeline_id")
    f = open("core/settings/env.txt", "w")
    f.write(f"{pipeline_id}\n")
    f.write(f"{dataset_version_id}")
    f.close()

else:
    dataset_version_id=settings.dataset_version_id


if __name__ == "__main__":
    get_data_from_minio_storage(
        user_id=settings.user_id,
        project_id=settings.project_id,
        dataset_version_id=dataset_version_id)
