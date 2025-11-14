pipeline {
  agent any
  
  environment {
    SCANNER_IMAGE = "jenkins-scanner:${env.BUILD_NUMBER}"
    JENKINS_URL = "http://host.docker.internal:8080"
    JENKINS_USER = "Manish Behera"
    JENKINS_TOKEN = credentials('1134544e152f8ec57095ff91ffd9e2bff6')
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
            mkdir -p output
            docker run --rm \
              -v $(pwd)/output:/app/output \
              -e JENKINS_USER="$JENKINS_USER" \
              -e JENKINS_TOKEN="$JENKINS_TOKEN" \
              $SCANNER_IMAGE \
              --output /app/output/report.json \
              --render /app/output/report.html \
              --url $JENKINS_URL \
              --username "$JENKINS_USER" \
              --token "$JENKINS_TOKEN"
          '''
        }
      }
    }
    
    stage('Archive') {
      steps {
        archiveArtifacts artifacts: 'scanner/output/**', fingerprint: true
      }
    }
    
    stage('Cleanup old images') {
      steps {
        script {
          sh '''
            docker images jenkins-scanner --format "{{.Tag}}" | sort -rn | tail -n +6 | xargs -r -I {} docker rmi jenkins-scanner:{} || true
          '''
        }
      }
    }
  }
  
  post {
    always {
      echo "Build ${env.BUILD_NUMBER} completed"
    }
    success {
      echo "Scanner report generated successfully!"
    }
  }
}