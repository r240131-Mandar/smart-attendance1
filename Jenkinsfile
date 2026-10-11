pipeline {
    agent any

    environment {
        IMAGE_NAME = 'smart-attendance'
        CONTAINER  = 'smart-attendance-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest -v'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Docker Deploy') {
            steps {
                sh 'docker rm -f ${CONTAINER} || true'
                sh 'docker run -d --name ${CONTAINER} -p 5000:5000 -v attendance-data:/data ${IMAGE_NAME}:latest'
            }
        }
    }

    post {
        success { echo 'Pipeline succeeded. App running on port 5000.' }
        failure { echo 'Pipeline failed. Check the stage logs.' }
    }
}
