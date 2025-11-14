pipeline {
    agent any

    environment {
        SCANNER_IMAGE = "jenkins-scanner:${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build scanner image') {
            steps {
                dir('scanner') {
                    sh 'docker build -t $SCANNER_IMAGE .'
                }
            }
        }

        stage('Run scanner') {
            steps {
                dir('scanner') {
                    sh '''
                        mkdir -p output &&
                        docker run --rm -v $(pwd)/output:/app/output $SCANNER_IMAGE \
                            --output /app/output/report.json \
                            --render /app/output/report.html \
                            --url http://host.docker.internal:9090
                    '''
                }
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: '**/output/**', allowEmptyArchive: true
            }
        }

        stage('Cleanup old images') {
            steps {
                script {
                    sh '''
                        # Remove scanner images older than the last 5 builds
                        docker images jenkins-scanner --format "{{.Tag}}" | sort -rn | tail -n +6 | xargs -r -I {} docker rmi jenkins-scanner:{} || true
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Build ${BUILD_NUMBER} completed"
            sh 'docker images jenkins-scanner'
            echo 'Scanner report generated successfully!'
        }
    }
}