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
        KUBECONFIG = '/var/jenkins_home/minikube-config'
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

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    sed "s|DOCKERHUB_IMAGE_PLACEHOLDER|$DOCKERHUB_USERNAME/$APP_IMAGE:$BUILD_NUMBER|g" \
                      k8s/deployment.yaml > k8s/deployment.generated.yaml

                    kubectl --kubeconfig="$KUBECONFIG" apply -f k8s/deployment.generated.yaml
                    kubectl --kubeconfig="$KUBECONFIG" apply -f k8s/service.yaml

                    kubectl --kubeconfig="$KUBECONFIG" rollout status deployment/student-task-manager --timeout=180s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl --kubeconfig="$KUBECONFIG" get pods -l app=student-task-manager
                    kubectl --kubeconfig="$KUBECONFIG" get deployment student-task-manager
                    kubectl --kubeconfig="$KUBECONFIG" get service student-task-manager
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
            echo 'Pipeline failed. Check the failed stage in Console Output.'
        }
    }
}
