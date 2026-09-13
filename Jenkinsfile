pipeline {
    agent any
    environment {
        DOCKERHUB_CREDS = credentials('dockerhub-cred')
        IMAGE_NAME = "jarvis/simple-app:${env.BUILD_ID}"
    }
    stages {
        stage('Build & Test') {
            steps {
                sh 'python3 -m unittest discover || python test_app.py'
            }
      stage('SonarQube Analysis') {
        environment {
            // The name here must match the tool name you set in the previous step
            SCANNER_HOME = tool 'sonar-scanner'
        }
        steps {
            withSonarQubeEnv('sonarqube-server') {
                sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=jarvis-repo -Dsonar.sources=."
            }
        }
    }
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        stage('Docker Build & Push') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
                sh "echo \$DOCKERHUB_CREDS_PSW | docker login -u \$DOCKERHUB_CREDS_USR --password-stdin"
                sh "docker push ${IMAGE_NAME}"
            }
        }
        stage('Deploy to EC2') {
            steps {
                sh "docker run -d --name app-${env.BUILD_ID} -p 5000:5000 ${IMAGE_NAME}"
            }
        }
    }
    post {
        always {
            sh "docker logout"
        }
    }
}
