# Automated CI/CD Pipeline for a Student Management System

Flask + SQLite CRUD app -> GitHub -> Jenkins -> Docker -> local deployment.

## Flow
Developer pushes code -> GitHub webhook -> Jenkins job starts ->
build Docker image -> run tests inside image -> replace running container -> health check.

## 1. Run the app locally (optional check)
    pip install -r requirements.txt
    python app.py            # http://localhost:5000
    pytest                   # run tests

## 2. Push to GitHub
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/<your-username>/student-cicd.git
    git push -u origin main

## 3. Run Jenkins (with Docker access) in Docker
    docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
      -v jenkins_home:/var/jenkins_home \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -u root jenkins/jenkins:lts
    docker exec -u root jenkins sh -c "apt-get update && apt-get install -y docker.io"
Open http://localhost:8080, unlock with `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`,
install suggested plugins (Git, Pipeline, GitHub).
(If Jenkins is installed directly on Windows/Linux instead, install Docker there and add the jenkins user to the docker group.)

## 4. Create the pipeline job
New Item -> Pipeline -> Pipeline script from SCM -> Git -> your repo URL -> branch `main` -> Script Path `Jenkinsfile`.
Click Build Now once so Jenkins registers the triggers.

## 5. Automatic trigger
Option A (easiest, no setup): the Jenkinsfile already polls GitHub every ~2 minutes.
Option B (instant): expose Jenkins with ngrok (`ngrok http 8080`), then in GitHub repo ->
Settings -> Webhooks -> Payload URL `https://<ngrok-id>.ngrok-free.app/github-webhook/`,
content type `application/json`, event "Just the push event".

## 6. Demo
1. Open http://localhost:5000 and add a student.
2. Edit `templates/index.html` (e.g. change the heading), commit and push.
3. Watch Jenkins run all stages automatically.
4. Refresh http://localhost:5000 and the change is live; student data persists (Docker volume).
