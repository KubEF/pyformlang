pipeline {
  agent {
    docker {
      image 'python:3.6'
    }

  }
  stages {
    stage('Build') {
      steps {
        sh 'pip3 install --user -r requirements.txt'
      }
    }
    stage('Test') {
      steps {
        sh 'make test-code'
      }
    }
  }
}