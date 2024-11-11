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
                git 'PIA_LMP/requirements.txt at main · Xam900mr/PIA_LMP'
            }
        }

        stage('Set up Virtual Environment') {             
            steps {
                        
                sh 'python -m venv $VIRTUAL_ENV' 
                sh '$VIRTUAL_ENV/bin/pip install --upgrade pip'  
                sh '$VIRTUAL_ENV/bin/pip install -r requirements.txt'  
            }         
        }         

        stage('Run Unit Tests') {             
            steps {                 
                sh '$VIRTUAL_ENV/bin/python -m unittest discover tests/ -s tests -p "test.py"'  
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
                    sh 'docker-compose -f ${DOCKER_COMPOSE_FILE} up -d'
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
