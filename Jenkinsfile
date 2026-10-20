pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_IMAGE = 'student-task-manager'
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        // Set this in Jenkins > Manage Jenkins > System > Global properties,
        // or replace it with your Docker Hub username in this file.
        DOCKERHUB_USERNAME = 'REPLACE_WITH_DOCKERHUB_USERNAME'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$WORKSPACE:/app" -w /app \
                      python:3.12-slim sh -c \
                      "pip install --no-cache-dir -r requirements.txt && pytest -q"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKERHUB_USERNAME}/${APP_IMAGE}:${BUILD_NUMBER} -t ${DOCKERHUB_USERNAME}/${APP_IMAGE}:latest .'
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DH_USER', passwordVariable: 'DH_TOKEN')]) {
                    sh '''
                        echo "$DH_TOKEN" | docker login -u "$DH_USER" --password-stdin
                        docker push "$DOCKERHUB_USERNAME/$APP_IMAGE:$BUILD_NUMBER"
                        docker push "$DOCKERHUB_USERNAME/$APP_IMAGE:latest"
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    sed "s|DOCKERHUB_IMAGE_PLACEHOLDER|$DOCKERHUB_USERNAME/$APP_IMAGE:$BUILD_NUMBER|g" k8s/deployment.yaml > k8s/deployment.generated.yaml
                    kubectl apply -f k8s/deployment.generated.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout status deployment/student-task-manager --timeout=180s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl get pods -l app=student-task-manager
                    kubectl get deployment student-task-manager
                    kubectl get service student-task-manager
                '''
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
        }
        success {
            echo 'Pipeline succeeded: tested, built, pushed and deployed Student Task Manager.'
        }
        failure {
            echo 'Pipeline failed. Open the failed stage logs and fix that stage before retrying.'
        }
    }
}
