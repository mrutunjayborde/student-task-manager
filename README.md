# Student Task Manager — CCA 2 CI/CD Project

## Project Overview

The Student Task Manager is a small web application built using Python and Flask. It was developed for the Cloud Computing and DevOps CCA 2 assignment to demonstrate Continuous Integration and Continuous Deployment (CI/CD) using Jenkins, Docker, Docker Hub, Kubernetes, and Minikube.

The project demonstrates automated testing, Docker image creation, publishing images to Docker Hub, deploying the application to Kubernetes, and verifying the deployment after a code change.

## Features

- Add a task
- Mark a task as complete or incomplete
- Delete a task
- Health-check endpoint at `/health`
- Automated tests using Pytest
- Docker containerization
- Jenkins CI/CD pipeline
- Kubernetes deployment using Minikube

**Demo limitation:** Tasks are stored in memory and reset when the application process restarts. This keeps the application simple for demonstration purposes.

## Project Repositories

- **GitHub:** https://github.com/mrutunjayborde/student-task-manager
- **Docker Hub:** https://hub.docker.com/r/mrutunjayborde/student-task-manager

## Technologies Used

- Python
- Flask
- Pytest
- Git and GitHub
- Jenkins
- Docker and Docker Hub
- Kubernetes
- Minikube
- Windows PowerShell

## Project Structure

```text
student-task-manager/
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── README.md
├── .dockerignore
├── .gitignore
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── static/
│   └── style.css
├── templates/
│   └── index.html
└── tests/
    └── test_app.py
```

## CI/CD Pipeline

A Jenkins Pipeline job named `student-task-manager-pipeline` is used to automate the build, test, image publishing, and deployment process.

The pipeline contains the following stages:

1. **Checkout SCM:** Retrieves the project source code from GitHub.
2. **Build and Test:** Installs the required Python dependencies and runs automated Pytest tests.
3. **Build Docker Image:** Builds a Docker image containing the application and its dependencies.
4. **Push Image to Docker Hub:** Authenticates using Jenkins credentials and pushes the image to Docker Hub.
5. **Deploy to Minikube:** Applies the Kubernetes Deployment and Service manifests and deploys the new application image.
6. **Verify Deployment:** Checks the Kubernetes deployment, pods, service, and rollout status.

Docker Hub credentials are stored in Jenkins using the credential ID `dockerhub-creds`. The access token is not stored in this repository.

## Docker Image

The application image is published to:

`mrutunjayborde/student-task-manager`

The pipeline publishes the image with a Jenkins build-number tag and the `latest` tag. Kubernetes deploys the build-number-tagged image so that a new pipeline run can deploy the updated version.

Docker Hub repository:

https://hub.docker.com/r/mrutunjayborde/student-task-manager

## Kubernetes Deployment

The Kubernetes configuration files are stored in the `k8s/` directory:

- `k8s/deployment.yaml` defines the application deployment and container configuration.
- `k8s/service.yaml` exposes the application through a Kubernetes Service.

The application was deployed to a local Minikube cluster. The pod was verified as running, and the deployed application was opened in a web browser.

Commands used to verify the deployment include:

```bash
kubectl get pods
kubectl get deployments
kubectl get services
```

To access the application through Minikube, use:

```powershell
& "C:\Program Files\Kubernetes\Minikube\minikube.exe" service student-task-manager --url
```

Open the URL returned by the command in a web browser.

The health endpoint can also be checked at `/health` on the application URL. It returns a JSON response indicating that the application is healthy.

## Second Deployment and Code Change

To demonstrate the CI/CD process, the heading in `templates/index.html` was changed from:

`My Task Manager`

to:

`My Student Task Manager`

The change was committed and pushed to GitHub. The Jenkins pipeline was executed again and completed successfully. The updated Docker image was published, and Kubernetes deployed the new version of the application.

The updated application was verified in the browser, displaying the heading **My Student Task Manager**.

Commit:

https://github.com/mrutunjayborde/student-task-manager/commit/35bad11866f0b475c62a6b43cf362dd03358fe54

## Jenkins Environment

Jenkins was configured locally in a Docker container on Windows. Docker Desktop and Minikube were used for building the image and deploying the application to Kubernetes.

**Note:** Jenkins on AWS EC2 has not been configured as part of the setup described above. If AWS-based Jenkins is required by the assignment evaluation, that configuration must be completed separately and documented after verification.

## Conclusion

This project demonstrates a basic CI/CD workflow for a Flask application using GitHub, Jenkins, Docker, Docker Hub, Kubernetes, and Minikube. The pipeline successfully built and tested the application, published its Docker image, deployed it to Kubernetes, and verified an updated application after a source-code change.

## Submission Checklist

- [x] GitHub repository containing the project source code
- [x] Dockerfile
- [x] Jenkinsfile
- [x] Kubernetes Deployment and Service manifests
- [x] Docker Hub image repository
- [x] Successful Jenkins pipeline execution
- [x] Kubernetes deployment and pod verification
- [x] Updated application verified in the browser
- [x] Screenshots of the pipeline, image, deployment, and updated application
- [ ] AWS Jenkins setup, if required by the assignment rubric
