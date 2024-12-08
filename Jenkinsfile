pipe {
  agent any
  
  stage {
    stage('Pull Code') {
      steps {
        script {
          sh 'git pull origin main' // Pull branch "main"
        }
      }
    }
    stage('Build docker registry and push') {
      step {
        withDockerRegistry(credentialsId: 'docker-hub', url: 'https://index.docker.io/v1/') {
        sh 'docker build -t whoami0709/test-jenkin-1 .'
        sh 'docker push'
        }
      }
    }
  }
}
