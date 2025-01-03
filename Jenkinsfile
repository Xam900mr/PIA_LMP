pipeline {
    agent any

    environment {
        VIRTUAL_ENV = "PIA_LMP"
        DOCKER_IMAGE = "sawnfozter/flask-app"
        DOCKER_COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'github-credentials', url: 'https://github.com/Xam900mr/PIA_LMP.git', branch: 'main'
            }
        }

        stage('Set up Virtual Environment') {
            steps {
                bat 'python -m venv %VIRTUAL_ENV%' 
                bat '%VIRTUAL_ENV%\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '%VIRTUAL_ENV%\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }

        stage('Push Docker Image to Registry') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        docker.image("${DOCKER_IMAGE}").push("latest")
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    bat 'docker-compose -f %DOCKER_COMPOSE_FILE% up -d'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up and finishing the pipeline.'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for more details.'
        }
    }
}
