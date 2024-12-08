pipe {
  agent any
  stage {
    stage('Build docker registry')
      step {
        withDockerRegistry(credentialsId: 'docker-hub', url: 'https://index.docker.io/v1/') {
        sh 'docker build -t whoami0709/test-jenkin-1 .'
        sh 'docker push whoami0709/test-jenkin-1'
        }
      }
  }
}
