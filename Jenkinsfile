pipeline {
    agent any
    
    parameters {
        string(name: 'NEXUS_REGISTRY', defaultValue: '159.203.56.144:8083', description: 'Nexus Docker registry URL with port')
        string(name: 'NEXUS_REPO', defaultValue: 'docker-private', description: 'Nexus repository name')
        string(name: 'DOCKER_IMAGE_NAME', defaultValue: 'calculator-app', description: 'Docker image name')
    }
    
    environment {
        VERSION_FILE = 'VERSION'
        DOCKER_IMAGE = "${params.DOCKER_IMAGE_NAME}"
        NEXUS_REGISTRY = "${params.NEXUS_REGISTRY}"
        NEXUS_REPO = "${params.NEXUS_REPO}"
    }
    
    stages {
        stage('Read Version') {
            steps {
                script {
                    echo "Reading version from ${VERSION_FILE}..."
                    def version = readFile(VERSION_FILE).trim()
                    env.APP_VERSION = version
                    echo "Building version: ${version}"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image with version ${env.APP_VERSION}..."
                    
                    sh """
                        docker build \
                            --build-arg VERSION=${env.APP_VERSION} \
                            -t ${DOCKER_IMAGE}:${env.APP_VERSION} \
                            -t ${DOCKER_IMAGE}:latest \
                            .
                    """
                    
                    echo "✅ Docker image built: ${DOCKER_IMAGE}:${env.APP_VERSION}"
                }
            }
        }
        
        stage('Tag for Nexus') {
            steps {
                script {
                    echo "Tagging images for Nexus repository..."
                    
                    sh """
                        docker tag ${DOCKER_IMAGE}:${env.APP_VERSION} \
                            ${NEXUS_REGISTRY}/${NEXUS_REPO}/${DOCKER_IMAGE}:${env.APP_VERSION}
                        
                        docker tag ${DOCKER_IMAGE}:latest \
                            ${NEXUS_REGISTRY}/${NEXUS_REPO}/${DOCKER_IMAGE}:latest
                    """
                    
                    echo "✅ Images tagged for Nexus"
                }
            }
        }
        
        stage('Push to Nexus') {
            steps {
                script {
                    echo "Pushing images to Nexus repository..."
                    
                    withCredentials([usernamePassword(
                        credentialsId: 'nexus-docker-repo-cred',
                        usernameVariable: 'NEXUS_USERNAME',
                        passwordVariable: 'NEXUS_PASSWORD'
                    )]) {
                        sh """
                            echo ${NEXUS_PASSWORD} | docker login -u ${NEXUS_USERNAME} --password-stdin ${NEXUS_REGISTRY}
                            
                            docker push ${NEXUS_REGISTRY}/${NEXUS_REPO}/${DOCKER_IMAGE}:${env.APP_VERSION}
                            docker push ${NEXUS_REGISTRY}/${NEXUS_REPO}/${DOCKER_IMAGE}:latest
                            
                            docker logout ${NEXUS_REGISTRY}
                        """
                    }
                    
                    echo "✅ Images pushed to Nexus"
                }
            }
        }
        
        stage('Cleanup Local Images') {
            steps {
                script {
                    echo "Cleaning up local Docker images..."
                    
                    sh """
                        docker rmi ${DOCKER_IMAGE}:${env.APP_VERSION} || true
                        docker rmi ${DOCKER_IMAGE}:latest || true
                        docker rmi ${NEXUS_REGISTRY}/${NEXUS_REPO}/${DOCKER_IMAGE}:${env.APP_VERSION} || true
                        docker rmi ${NEXUS_REGISTRY}/${NEXUS_REPO}/${DOCKER_IMAGE}:latest || true
                    """
                    
                    echo "✅ Cleanup completed"
                }
            }
        }
    }
    
    post {
        success {
            echo """
            ╔══════════════════════════════════════════════════════════════╗
            ║                   🎉 BUILD SUCCESSFUL 🎉                     ║
            ╠══════════════════════════════════════════════════════════════╣
            ║  Version: ${env.APP_VERSION}                                 ║
            ║  Docker Image: ${DOCKER_IMAGE}:${env.APP_VERSION}           ║
            ║  Nexus: ${NEXUS_REGISTRY}/${NEXUS_REPO}/${DOCKER_IMAGE}     ║
            ╚══════════════════════════════════════════════════════════════╝
            """
        }
        failure {
            echo """
            ╔══════════════════════════════════════════════════════════════╗
            ║                     ❌ BUILD FAILED ❌                        ║
            ╚══════════════════════════════════════════════════════════════╝
            """
        }
    }
}
