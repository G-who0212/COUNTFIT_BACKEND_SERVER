pipeline {
    agent any

    stages {
        stage('Clone repository') {
            steps {
                // SCM(Source Control Management)을 사용하여 코드 저장소 클론
                checkout scm
            }
        }

        stage('Build image') {
            steps {
                script {
                    // Docker 이미지를 빌드하고 태그를 BUILD_NUMBER로 지정
                    app = docker.build("gwho0212/countfit-backend:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push image') {
            steps {
                script {
                    // Docker Hub에 인증하고 이미지를 푸시
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
                        app.push("${env.BUILD_NUMBER}") // 태그별로 푸시
                        app.push("latest") // latest 태그로도 푸시
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['countfit-backend-ec2-ssh-key']) { // EC2 SSH Credential ID
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@3.35.51.27 << EOF
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
