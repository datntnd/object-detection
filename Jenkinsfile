pipeline {
    agent none
    stages {
        stage('Clone Stage') {
            agent {label 'master'}
            steps {
                git credentialsId: 'object-detection-gitlab', url: 'https://gitlab.com/21031998a/simple-demo.git' 
            }
        }
        stage('Process Data Stage')
        {
            agent {label 'master'}
            steps {
                sh 'pip3 --proxy http://10.61.11.42:3128 install -r requirements.txt'
                sh 'python3 fetch_data.py'
        }
        }
        stage('Training Stage'){
            agent {label 'master'}
            steps {
                sh 'python3 train.py'
            }
        }
        stage ('Evaluating Stage'){
            agent {label 'master'}
            steps {
                sh 'python3 compare.py'
            }
        }
        stage ('Serving Model Stage'){
            agent{label 'quangtv'}
            steps {
                git credentialsId: 'serving-gitlab', url: 'https://gitlab.com/21031998a/bentoml-serving-service.git'
                sh 'pip3 --proxy http://10.61.11.42:3128 install -r requirements.txt'
                sh 'python3.6 app/models/get_best_model.py'
                sh 'docker build --build-arg http_proxy=http://10.61.11.42:3128 --build-arg https_proxy=http://10.61.11.42:3128 -t bentoml_serving_service .'
                sh 'docker-compose up -d'
            }
        }
    }  
}
