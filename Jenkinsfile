pipeline {
    agent any
    stages {
        stage('Pull Code') {
            steps {
                script {
                    sh 'git pull origin main' // Pull branch "main"
                }
            }
        }
        stage('Build Docker Image and Push') {
            steps {
                withDockerRegistry(credentialsId: 'docker-hub', url: 'https://index.docker.io/v1/') {
                    sh 'docker build -t whoami0709/test-jenkin-1 .'
                    sh 'docker push whoami0709/test-jenkin-1'
                }
            }
        }
    }
}
