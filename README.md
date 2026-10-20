# Student Task Manager — CCA 2 CI/CD Project

A small Flask web application for managing student tasks. This repository is designed for a Cloud Computing and DevOps CCA demonstrating Jenkins, Docker Hub, and Kubernetes on Minikube.

## Features
- Add a task
- Mark a task complete or incomplete
- Delete a task
- `/health` endpoint for Kubernetes health checks
- Pytest automated tests

**Demo limitation:** tasks are held in memory. They reset when the application process restarts. This is intentional to keep the CCA application small; it is not intended as a production task manager.

## 1. Run locally (optional)

Requires Python 3.12 or newer.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python app.py
```

Open `http://127.0.0.1:5000`.

## 2. Create GitHub repository

1. Create a new **public** GitHub repository named `student-task-manager` (or use a private repo and configure credentials in Jenkins).
2. In this project folder, run:

```bash
git init
git add .
git commit -m "Initial Student Task Manager project"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/student-task-manager.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with your own GitHub username. Do not commit passwords or access tokens.

## 3. Prepare Docker Hub

1. Create/sign in to Docker Hub and create a repository named `student-task-manager`.
2. In Jenkins, add a credential of type **Username with password** (or a Docker Hub access token as the password).
3. Set its ID to `dockerhub-creds`. Use your Docker Hub username as the username and an access token as the password.
4. In the `Jenkinsfile`, replace `REPLACE_WITH_DOCKERHUB_USERNAME` with your Docker Hub username.

## 4. Jenkins and required tools

The Jenkins agent that runs this pipeline must have `git`, `docker`, `kubectl`, access to the Docker daemon, and a working kubeconfig for the target Minikube cluster. Jenkins also needs Pipeline and Git plugins. Docker must be usable by the Jenkins agent account.

The assignment guide expects Jenkins on an AWS server and deployment to Minikube. Configure Minikube on the environment where `kubectl` in the Jenkins agent can reach it. A Minikube cluster on a separate laptop is not automatically reachable from an AWS Jenkins server. If your college setup uses a different arrangement, adapt the deployment connection accordingly.

Create a Jenkins **Pipeline** job:
1. Choose **Pipeline script from SCM**.
2. SCM: **Git**.
3. Repository URL: `https://github.com/YOUR_GITHUB_USERNAME/student-task-manager.git`.
4. Branch: `*/main`.
5. Script path: `Jenkinsfile`.
6. Save and click **Build Now**.

For automatic builds on every GitHub push, configure a GitHub webhook to your reachable Jenkins URL and enable the GitHub hook trigger in the job. For a classroom demo, Build Now is acceptable if automatic webhook triggering is not required by your evaluator; the guide itself asks for the pipeline and a second run after a code change.

## 5. Verify the deployment

After a successful Jenkins run, on the machine/context configured for Minikube run:

```bash
kubectl get pods -l app=student-task-manager
kubectl get deployment student-task-manager
kubectl get service student-task-manager
kubectl port-forward service/student-task-manager 8080:5000
```

Then open `http://127.0.0.1:8080`. Keep port-forward running while testing. You can also check `http://127.0.0.1:8080/health` and should see `{"status":"ok"}`.

## 6. Demonstrate the second deployment

1. Edit a visible heading in `templates/index.html`, for example change `My Task Manager` to `My Student Task Manager`.
2. Commit and push the change:

```bash
git add templates/index.html
git commit -m "Update task manager heading"
git push
```
3. Run the Jenkins job again (or let the configured webhook trigger it).
4. Show the new successful build number, image tag in Docker Hub, and updated page.

The pipeline tags each image with the Jenkins build number as well as `latest`. Kubernetes uses the build-number tag, so the second run deploys the new image version.

## Pipeline stages (viva summary)

1. **Checkout:** Jenkins downloads the latest repository code.
2. **Build and Test:** runs the pytest tests inside a temporary Python container.
3. **Build Docker Image:** packages the app and its runtime dependencies into an image.
4. **Push Image:** logs in with a Jenkins-stored credential and uploads the image to Docker Hub.
5. **Deploy to Minikube:** applies Kubernetes Deployment and Service manifests.
6. **Verify Deployment:** checks the pod, Deployment, Service and rollout status.

## Submission checklist

- [ ] GitHub repository URL
- [ ] `Jenkinsfile`
- [ ] `Dockerfile`
- [ ] `k8s/deployment.yaml` and `k8s/service.yaml`
- [ ] Screenshot of Jenkins pipeline success
- [ ] Screenshot of Docker Hub image tags
- [ ] Screenshot of `kubectl get pods`, Deployment and Service
- [ ] Screenshot of the application in a browser
- [ ] Screenshot showing the second code change deployed
- [ ] Brief report explaining setup and pipeline stages

## Troubleshooting notes

- **`docker: permission denied`:** ensure the Jenkins agent can access the Docker daemon; restart the agent after changing group permissions.
- **Docker Hub push denied:** verify the repo exists, credential ID is `dockerhub-creds`, and the Jenkinsfile username matches the Docker Hub account.
- **`kubectl` connection refused:** verify Minikube is running and the Jenkins agent's kubeconfig points to a cluster it can actually reach.
- **ImagePullBackOff:** verify the image repository/tag exists and is public, or configure Kubernetes image-pull credentials for a private repository.
- **Port-forward doesn't start:** run the command on a machine with access to the correct cluster context and check `kubectl get pods` first.
