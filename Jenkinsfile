// Jenkinsfile — Scanner build + run + archive
pipeline {
  agent any

  environment {
    IMAGE_NAME = "jenkins-scanner"
    IMAGE_TAG  = "5"
    SCANNER_DIR = "scanner"
    OUTPUT_DIR = "${env.WORKSPACE}/${SCANNER_DIR}/output"
    JENKINS_URL = "http://host.docker.internal:9090"
  }

  stages {
    stage('Checkout') {
      steps {
        // explicit checkout (equivalent to the logs you showed)
        checkout scm
      }
    }

    stage('Build scanner image') {
      steps {
        dir("${SCANNER_DIR}") {
          // match your log: docker build -t jenkins-scanner:5 .
          sh """
            docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
          """
        }
      }
    }

    stage('Run scanner') {
      steps {
        dir("${SCANNER_DIR}") {
          sh """
            mkdir -p ${OUTPUT_DIR}
            # run using host network and mount output
            docker run --rm --network host \\
              -v "${OUTPUT_DIR}:/app/output" \\
              ${IMAGE_NAME}:${IMAGE_TAG} \\
              --output /app/output/report.json --render /app/output/report.html --url ${JENKINS_URL}
          """
        }
      }
    }

    stage('Archive') {
      steps {
        // archive generated reports
        archiveArtifacts artifacts: "${SCANNER_DIR}/output/**", fingerprint: true
      }
    }
  }

  post {
    always {
      // optional cleanup: remove local image to avoid disk growth
      script {
        sh "docker image rm ${IMAGE_NAME}:${IMAGE_TAG} || true"
      }
    }
  }
}
