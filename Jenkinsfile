pipeline {
    agent any
    
    parameters {
        string(name: 'GITHUB_REPO_URL', defaultValue: 'github.com/YOUR-USERNAME/YOUR-REPO.git', description: 'GitHub repository URL (without https://)')
        string(name: 'NEXUS_REGISTRY', defaultValue: '159.203.56.144:8083', description: 'Nexus Docker registry URL with port')
        string(name: 'NEXUS_REPO', defaultValue: 'docker-private', description: 'Nexus repository name')
        string(name: 'DOCKER_IMAGE_NAME', defaultValue: 'calculator-app', description: 'Docker image name')
        choice(name: 'VERSION_INCREMENT', choices: ['PATCH', 'MINOR', 'MAJOR'], description: 'Which version number to increment')
    }
    
    environment {
        VERSION_FILE = 'VERSION'
        DOCKER_IMAGE = "${params.DOCKER_IMAGE_NAME}"
        NEXUS_REGISTRY = "${params.NEXUS_REGISTRY}"
        NEXUS_REPO = "${params.NEXUS_REPO}"
        GITHUB_REPO = "${params.GITHUB_REPO_URL}"
    }
    
    stages {
        stage('Read Current Version') {
            steps {
                script {
                    echo "Reading current version from ${VERSION_FILE}..."
                    def currentVersion = readFile(VERSION_FILE).trim()
                    echo "Current version: ${currentVersion}"
                    env.CURRENT_VERSION = currentVersion
                }
            }
        }
        
        stage('Increment Version') {
            steps {
                script {
                    echo "Incrementing version..."
                    
                    // Parse semantic version (MAJOR.MINOR.PATCH)
                    def versionParts = env.CURRENT_VERSION.tokenize('.')
                    def major = versionParts[0].toInteger()
                    def minor = versionParts[1].toInteger()
                    def patch = versionParts[2].toInteger()
                    
                    // Increment based on parameter
                    if (params.VERSION_INCREMENT == 'MAJOR') {
                        major++
                        minor = 0
                        patch = 0
                    } else if (params.VERSION_INCREMENT == 'MINOR') {
                        minor++
                        patch = 0
                    } else {
                        patch++
                    }
                    
                    def newVersion = "${major}.${minor}.${patch}"
                    env.NEW_VERSION = newVersion
                    
                    echo "New version: ${newVersion}"
                    
                    // Write new version to file
                    writeFile file: VERSION_FILE, text: newVersion
                }
            }
        }
        
        stage('Commit Version Bump') {
            steps {
                script {
                    echo "Committing version bump to main branch..."
                    
                    withCredentials([usernamePassword(
                        credentialsId: 'github-pat',
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_PASSWORD'
                    )]) {
                        sh """
                            git config user.email "jenkins@automated.build"
                            git config user.name "Jenkins CI"
                            
                            git add ${VERSION_FILE}
                            git commit -m "[skip ci] Bump version to ${env.NEW_VERSION}"
                            
                            # Push using PAT
                            git push https://${GIT_USERNAME}:${GIT_PASSWORD}@${env.GITHUB_REPO} HEAD:main
                        """
                    }
                    
                    echo "✅ Version bump committed to main"
                }
            }
        }
        
        stage('Create Git Tag') {
            steps {
                script {
                    echo "Creating Git tag v${env.NEW_VERSION}..."
                    
                    withCredentials([usernamePassword(
                        credentialsId: 'github-pat',
                        usernameVariable: 'GIT_USERNAME',
                        passwordVariable: 'GIT_PASSWORD'
                    )]) {
                        sh """
                            git tag -a v${env.NEW_VERSION} -m "Release version ${env.NEW_VERSION}"
                            git push https://${GIT_USERNAME}:${GIT_PASSWORD}@${env.GITHUB_REPO} v${env.NEW_VERSION}
                        """
                    }
                    
                    echo "✅ Git tag v${env.NEW_VERSION} created"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image with version ${env.NEW_VERSION}..."
                    
                    sh """
                        docker build \
                            --build-arg VERSION=${env.NEW_VERSION} \
                            -t ${DOCKER_IMAGE}:${env.NEW_VERSION} \
                            -t ${DOCKER_IMAGE}:latest \
                            .
                    """
                    
                    echo "✅ Docker image built: ${DOCKER_IMAGE}:${env.NEW_VERSION}"
                }
            }
        }
        
        stage('Tag for Nexus') {
            steps {
                script {
                    echo "Tagging images for Nexus repository..."
                    
                    sh """
                        docker tag ${DOCKER_IMAGE}:${env.NEW_VERSION} \
                            ${NEXUS_REGISTRY}/${NEXUS_REPO}/${DOCKER_IMAGE}:${env.NEW_VERSION}
                        
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
                        credentialsId: 'nexus-credentials',
                        usernameVariable: 'NEXUS_USERNAME',
                        passwordVariable: 'NEXUS_PASSWORD'
                    )]) {
                        sh """
                            echo ${NEXUS_PASSWORD} | docker login -u ${NEXUS_USERNAME} --password-stdin ${NEXUS_REGISTRY}
                            
                            docker push ${NEXUS_REGISTRY}/${NEXUS_REPO}/${DOCKER_IMAGE}:${env.NEW_VERSION}
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
                        docker rmi ${DOCKER_IMAGE}:${env.NEW_VERSION} || true
                        docker rmi ${DOCKER_IMAGE}:latest || true
                        docker rmi ${NEXUS_REGISTRY}/${NEXUS_REPO}/${DOCKER_IMAGE}:${env.NEW_VERSION} || true
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
            ║  Version: ${env.NEW_VERSION}                                 ║
            ║  Docker Image: ${DOCKER_IMAGE}:${env.NEW_VERSION}           ║
            ║  Nexus: ${NEXUS_REGISTRY}/${NEXUS_REPO}/${DOCKER_IMAGE}     ║
            ║  Git Tag: v${env.NEW_VERSION}                               ║
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
