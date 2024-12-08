pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub')
        IMAGE_NAME = 'whoami0709/deskop-remote-app-image'
        CONTAINER_NAME = 'deskop-remote-app-container'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Pulling code from repository'
                    checkout scm
                }
            }
        }
        stage('Build') {
            steps {
                script {
                    echo 'Building the app'
                    sh 'docker build -t ${IMAGE_NAME} .'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    echo 'Testing the app'
                    sh 'pytest tests/'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying the app'
                }
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}
                        docker push ${IMAGE_NAME}
                    '''
                }
            }
        }
        stage('Run Container') {
            steps {
                script {
                    echo 'Running the Docker container'
                    sh '''
                        docker pull ${IMAGE_NAME}
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                        docker run -d --name ${CONTAINER_NAME} -p 8081:8080 ${IMAGE_NAME}
                    '''
                }
            }
        }
    }
}