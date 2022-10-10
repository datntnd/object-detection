export GRAFANA_SERVER=10.61.185.119:3000
export GRAFANA_API_KEY=eyJrIjoiQ3BvSnVaamYydEF0UkpFV3dLQkgxRmdUZ24xWUtMREMiLCJuIjoia2luZ2tvbmciLCJpZCI6MX0=


bash upload.sh  data.json

#kong_address
kong_address=${kong_address:-10.255.187.48:8001}
serving_host=${serving_host:-10.61.185.119}
serving_port=${serving_port:-6000}

# export user_id=linhnt153 
# export serving_host=10.255.187.46
# export serving_port=6000 
# export kong_address=10.255.187.48:8001
unset HTTPS_PROXY HTTP_PROXY http_proxy https_proxy

python upload_kong.py
