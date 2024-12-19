node {
  stage('Clone repository') {
    // SCM(Source Control Management)을 사용하여 코드 저장소 클론
    checkout scm
  }
  
  stage('Build image') {
    // Docker 이미지를 빌드하고 태그를 BUILD_NUMBER로 지정
    app = docker.build("gwho0212/countfit-backend:$BUILD_NUMBER")
  }
  
  stage('Push image') {
    // Docker Hub에 인증하고 이미지를 푸시
    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
      app.push("${env.BUILD_NUMBER}") // 태그별로 푸시
      app.push("latest") // latest 태그로도 푸시
    }
  }
}
