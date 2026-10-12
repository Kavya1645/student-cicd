pipeline {
    agent any

    environment {
        IMAGE     = 'student-app'
        CONTAINER = 'student-app'
        HOST_PORT = '5000'
    }

    triggers {
        githubPush()                 // instant trigger via GitHub webhook
        pollSCM('H/2 * * * *')       // fallback: check GitHub every ~2 minutes
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Build Docker Image') {
            steps { sh 'docker build -t ${IMAGE}:${BUILD_NUMBER} -t ${IMAGE}:latest .' }
        }

        stage('Test') {
            steps { sh 'docker run --rm ${IMAGE}:${BUILD_NUMBER} python -m pytest -q' }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f ${CONTAINER} || true
                    docker run -d --name ${CONTAINER} -p ${HOST_PORT}:5000 \
                        -v student-data:/data ${IMAGE}:${BUILD_NUMBER}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    for i in 1 2 3 4 5; do
                        docker exec ${CONTAINER} python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" && exit 0
                        sleep 3
                    done
                    exit 1
                '''
            }
        }
    }

    post {
        success { echo "Deployed build #${BUILD_NUMBER} at http://localhost:${HOST_PORT}" }
        failure { echo 'Pipeline failed. Check the stage logs above.' }
    }
}
