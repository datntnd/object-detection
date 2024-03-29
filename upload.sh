#!/usr/bin/env bash

export GRAFANA_SERVER=10.255.187.50:8000
export GRAFANA_API_KEY=eyJrIjoiQnptYnVDNUdkZE1DMkl0aks2NER5V05JUmQzSjZkWXoiLCJuIjoibWxvcCIsImlkIjoyfQ==


function prop {
    grep "${1}" env|cut -d'=' -f2-
}

show_help_info () {
echo -e "\n\tERROR: $1"

cat <<HELPINFO
---
Usage:
Define environment variables: GRAFANA_SERVER and GRAFANA_API_KEY, e.g.
    https://grafana.com/docs/grafana/latest/http_api/auth/#create-api-token
    export GRAFANA_SERVER=grafana_server:3000
    export GRAFANA_API_KEY=asdf23vsd23
    ./upload.sh </path/to/dashboard.json>
Example:
    ./upload.sh dash.json
HELPINFO
}

function msg () { echo -e "$*"; }
function bail () { msg "\nError: ${1:-Unknown Error}\n"; exit ${2:-1}; }

# -------------------------------------------------------------------------
if [ -z "$1" ];then
    show_help_info "No dashboard parameter received"
    exit 1
fi

# GRAFANA_API_KEY=$(prop 'GRAFANA_API_KEY')
# GRAFANA_SERVER=$(prop 'GRAFANA_SERVER')

# echo $(prop 'GRAFANA_API_KEY')
# echo $(prop 'GRAFANA_SERVER')
GRAFANA_API_KEY=${GRAFANA_API_KEY:-Unset}
if [[ $GRAFANA_API_KEY == Unset ]]; then
    echo -e "\\nError: GRAFANA_API_KEY environment variable not define.\\n"
    exit 1
fi
GRAFANA_SERVER=${GRAFANA_SERVER:-Unset}
if [[ $GRAFANA_SERVER == Unset ]]; then
    echo -e "\\nError: GRAFANA_SERVER environment variable not define.\\n"
    exit 1
fi
logfile="grafana_upload.log"

# Get path/file parm
DASHBOARD=$1

# Pull through jq to validate json
payload="$(/home/anaconda3/bin/jq . ${DASHBOARD}) >> $logfile"

# Upload the JSON to Grafana
curl -X POST \
  -H "Authorization: Bearer $GRAFANA_API_KEY" \
  -H 'Content-Type: application/json' \
  -d "${payload}" \
  "http://$GRAFANA_SERVER/api/dashboards/db" -w "\n" | tee -a "$logfile"
