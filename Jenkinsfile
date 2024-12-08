pipeline {
    agent any
    enviroment {
        SERVICE_NAME = "deskop-remoote-app"
        REPOSITORY_TAG = "${YOUR_DOCKERHUB_USERNAME}/${ORGANIZATION_NAME}-${SERVICE_NAME}:${BUILD_ID}
    }
    stages {
        stage('Preparation') {
            steps {
                cleanWs()
                git credentialsId: 'github-accunt', url: "https://github.com/${ORGANIZATION_NAME}/${SERVICE_NAME}"         
            }
        }
        stage('Build') {
            steps {
               sh 'echo No build required for Webapp'
            }
        }
        stage('Build and push image') {
            steps {
               sh 'docker image build -t ${REPOSITORY_TAG}'    
            }
        }
        stage('Deloy') {
            steps {
               sh 'envsubst < ${WORKSPACE}/deloy.yaml | kubectl apply -f -'    
            }
        }
    }
}
