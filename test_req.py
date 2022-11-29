import requests
from core.config import get_app_settings

settings = get_app_settings()
model_name = "test"

res = requests.post("http://10.255.187.50:8089/api/v1/model/create",
    json={
        "model_name": model_name,
        "model_url": f"{settings.user_id}/{settings.project_id}/{settings.dataset_version_id}/{settings.pipeline_id}/best.pt",
        "model_result": {},
        "pipeline_id": settings.pipeline_id,
        "project_id": settings.project_id,
        "description": ""
    },  headers={"user_id": settings.user_id})

print("res: ", res)


# proxies = {
#         "http_proxy": "http://10.61.11.42:3128",
#         "https_proxy": "http://10.61.11.42:3128"
#     },
