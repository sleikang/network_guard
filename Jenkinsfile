pipeline {
    agent any

    stages {
        stage('构建') {
            steps {
                script {
                    sh 'docker build -t sleikang/network_guard:latest .'
                }
            }
        }

        stage('推送到Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_HUB_USERNAME', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                        sh "docker login -u $DOCKER_HUB_USERNAME -p $DOCKER_HUB_PASSWORD"
                        sh 'docker push sleikang/network_guard:latest'
                    }
                }
            }
        }
    }
}
