import requests
import json
from core.config import get_app_settings
import os

settings = get_app_settings()

user_id = settings.user_id
project_id = settings.project_id
serving_host = os.environ.get("serving_host")
serving_port = os.environ.get("serving_port")
kong_address = os.environ.get("kong_address")

print(f"user_id: {user_id}")
print(f"project_id: {project_id}")
print(f"kong address: {kong_address}")
print(f"serving_port: {serving_port}")
print(f"serving_host: {serving_host}")


# Create services

url_service = f"http://{kong_address}/services/"
print(f"url service: {url_service}")

headers = {
  'Content-Type': 'application/json'
}

name_service = "yolo_v5_demo" + "_" + user_id

payload_services=json.dumps({
  "name": name_service,
  "host": serving_host,
  "port": int(serving_port),
  "path": "/invocation",
  "protocol": "http"
})

print(f"payload_services:{payload_services}")

response = requests.request("POST", url_service, headers=headers, data=payload_services)

print(response.text)

#Create routes

url = f"http://{kong_address}/services/{name_service}/routes"
name_route = f"/{project_id}/iva-model"

payload_routes = json.dumps({
  "name": name_service,
  "paths": [ name_route ]
})


response = requests.request("POST", url, headers=headers, data=payload_routes)

print(response.text)
