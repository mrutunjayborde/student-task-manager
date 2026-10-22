
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_IMAGE = 'student-task-manager'
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        DOCKERHUB_USERNAME = 'mrutunjayborde'
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
                      -v "$WORKSPACE:$WORKSPACE" \
                      -w "$WORKSPACE" \
                      -e PYTHONPATH="$WORKSPACE" \
                      python:3.12-slim sh -c \
                      "pip install --no-cache-dir -r requirements.txt && python -m pytest -q"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t "$DOCKERHUB_USERNAME/$APP_IMAGE:$BUILD_NUMBER" \
                      -t "$DOCKERHUB_USERNAME/$APP_IMAGE:latest" .
                '''
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKERHUB_CREDENTIALS}",
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_TOKEN'
                )]) {
                    sh '''
                        echo "$DH_TOKEN" | docker login \
                          -u "$DH_USER" --password-stdin

                        docker push "$DOCKERHUB_USERNAME/$APP_IMAGE:$BUILD_NUMBER"
                        docker push "$DOCKERHUB_USERNAME/$APP_IMAGE:latest"

                        docker logout
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker image prune -f || true'
        }
        success {
            echo 'Pipeline succeeded: tested, built and pushed Student Task Manager.'
        }
        failure {
            echo 'Pipeline failed. Check the failed stage in Console Output.'
        }
    }
}
