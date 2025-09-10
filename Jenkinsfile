pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/salmaahmed22mohamed-oss/devops-project.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Start All Services') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Verify Services') {
            steps {
                sh 'docker ps'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
    }
}
