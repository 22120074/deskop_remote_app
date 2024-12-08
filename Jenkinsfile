pipe {
  agent any
  tool {
    jdk 'OpenJDK8'
    maven 'Maven3'
  }
  stage {
    stage('SCM') {
      step {
        git branch: 'main', changelog: false, credentialsId: 'github-account', poll: false, url: 'https://github.com/22120074/deskop_remote_app.git'
      }
    }
    stage('Maven build'){
      step {
        sh 'mvn clean install'
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
