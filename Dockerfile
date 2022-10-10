FROM nvcr.io/nvidia/pytorch:20.08-py3

RUN apt update && apt install -y zip htop screen libgl1-mesa-glx

# Install python dependencies

RUN python -m pip install --upgrade pip
RUN pip uninstall -y nvidia-tensorboard nvidia-tensorboard-plugin-dlprof
COPY requirements.txt .
RUN pip install --proxy http_proxy=http://10.61.11.42:3128 -r requirements.txt

# Create working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy contents
COPY . /usr/src/app


