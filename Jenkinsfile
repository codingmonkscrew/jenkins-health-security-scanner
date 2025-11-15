pipeline {
  agent any
  
  environment {
    SCANNER_IMAGE = "jenkins-scanner:${env.BUILD_NUMBER}"
    JENKINS_URL = "http://host.docker.internal:9090"
    JENKINS_USER = "Manish Behera"
    JENKINS_TOKEN = credentials('scanner-token')
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
            # Try to run with host network (Linux or when Docker socket works).
            docker run --rm --network host -v $(pwd)/output:/app/output -e JENKINS_USER="$JENKINS_USER" -e JENKINS_TOKEN="$JENKINS_TOKEN" $SCANNER_IMAGE --output /app/output/report.json --render /app/output/report.html --url $JENKINS_URL --username "$JENKINS_USER" --token "$JENKINS_TOKEN" || \
            # Fallback: run without --network host (works on many systems)
            docker run --rm -v $(pwd)/output:/app/output -e JENKINS_USER="$JENKINS_USER" -e JENKINS_TOKEN="$JENKINS_TOKEN" $SCANNER_IMAGE --output /app/output/report.json --render /app/output/report.html --url $JENKINS_URL --username "$JENKINS_USER" --token "$JENKINS_TOKEN"
          '''
        }
      }
    }
    
    stage('Archive') {
      steps {
        archiveArtifacts artifacts: 'scanner/output/**', fingerprint: true
      }
    }
  }
}
