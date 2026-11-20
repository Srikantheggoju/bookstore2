pipeline {
    agent any

    environment {
        IMAGE_NAME = "srikantheggoju/bookstore"
        GITOPS_REPO = "https://github.com/Srikantheggoju/bookstore-gitops.git"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Srikantheggoju/bookstore-app.git'
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh '''
                    sonar-scanner \
                    -Dsonar.projectKey=bookstore \
                    -Dsonar.sources=. \
                    -Dsonar.python.version=3
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage('Trivy Scan') {
            steps {
                sh "trivy image ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }

        stage('Push Image') {
            steps {
                sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }

        stage('Update GitOps Repo') {
            steps {
                sh '''
                git clone ${GITOPS_REPO}

                cd bookstore-gitops/helm-chart

                sed -i "s/tag:.*/tag: \\"${BUILD_NUMBER}\\"/" values.yaml

                git config user.email "jenkins@local.com"
                git config user.name "Jenkins"

                git add .
                git commit -m "Updated image tag ${BUILD_NUMBER}"

                git push
                '''
            }
        }
    }
}
