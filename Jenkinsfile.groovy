pipeline {
    agent any

    stages {
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }

        stage('Build image') {
            steps {
                script {
                    app = docker.build("gwho0212/countfit-backend:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
                        app.push("${env.BUILD_NUMBER}")
                        app.push("latest")
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['countfit-backend-ec2-ssh-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@3.35.51.27 <<EOF
                    docker pull gwho0212/countfit-backend:latest
                    docker stop countfit-backend || true
                    docker rm countfit-backend || true
                    docker run -d --name countfit-backend -p 80:80 gwho0212/countfit-backend:latest
                    EOF
                    '''
                }
            }
        }

    }
}
