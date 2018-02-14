pipeline {
  agent any
  stages {
    stage('Tests') {
      steps {
        bat 'py -3 -m unittest tests.py'
        junit 'TEST-*'
      }
    }
  }
}