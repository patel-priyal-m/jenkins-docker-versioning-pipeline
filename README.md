# Jenkins CI/CD Pipeline with Auto-Versioning

Enterprise-grade CI/CD pipeline demonstrating automated semantic versioning, branch protection, code quality gates, Docker containerization, and artifact management with Jenkins and Nexus.

## 🎯 Project Overview

This project showcases:
- **GitHub Branch Protection** - Enforce PR reviews and status checks
- **GitHub Actions** - Pre-merge quality gates (Black formatter, pytest)
- **Jenkins Pipeline** - Post-merge automation (version increment, Docker build, Nexus push)
- **Semantic Versioning** - Automated MAJOR.MINOR.PATCH version management
- **Docker Multi-stage Build** - Optimized containerization
- **Nexus Repository** - Centralized artifact storage

## 📋 Prerequisites

- **GitHub Account** with repository
- **Jenkins Server** with Docker installed
- **Nexus Repository Manager** with Docker registry configured
- **GitHub Personal Access Token** (PAT) with repo permissions
- **Nexus Credentials** for Docker registry access

## 🏗️ Architecture

```
Developer Workflow:
┌─────────────────────────────────────────────────────────────────┐
│  1. Create feature branch                                       │
│  2. Make code changes                                           │
│  3. Format code: black src/ tests/                             │
│  4. Push to GitHub                                              │
│  5. Open Pull Request to main                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  GitHub Actions (Pre-Merge Quality Gates)                       │
│  ✓ Black formatter check                                        │
│  ✓ Unit tests (pytest)                                          │
│  ✓ Code quality validation                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Code Review & Approval                                         │
│  ✓ Reviewer approval required                                   │
│  ✓ All status checks must pass                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Merge to main branch                                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Jenkins Pipeline (Post-Merge Automation)                       │
│  1. Read VERSION file (e.g., 1.0.0)                            │
│  2. Increment PATCH version (1.0.1)                            │
│  3. Commit VERSION back to main [skip ci]                      │
│  4. Create Git tag (v1.0.1)                                    │
│  5. Build Docker image (calculator-app:1.0.1)                 │
│  6. Tag image for Nexus registry                               │
│  7. Push to Nexus (versioned + latest tags)                   │
│  8. Cleanup local images                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Nexus Repository                                               │
│  calculator-app:1.0.1 ✓                                        │
│  calculator-app:latest ✓                                       │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Setup Instructions

### 1. GitHub Repository Setup

#### Push Initial Code
```bash
cd jenkins-version-auto-increment
git init
git add .
git commit -m "Initial commit: CI/CD pipeline with auto-versioning"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

#### Configure Branch Protection
1. Go to **Settings** → **Branches**
2. Click **Add rule** for `main` branch
3. Enable:
   - ✅ **Require a pull request before merging**
   - ✅ **Require approvals** (1 approval)
   - ✅ **Require status checks to pass before merging**
     - Add: `Code Quality & Tests` (from GitHub Actions)
   - ✅ **Do not allow bypassing the above settings**
   - ✅ **Restrict who can push to matching branches** (optional)

### 2. Jenkins Setup

#### Install Required Plugins
- Git Plugin
- Pipeline Plugin
- Docker Pipeline Plugin
- Credentials Plugin

#### Add Credentials

**GitHub PAT:**
1. **Manage Jenkins** → **Credentials** → **System** → **Global credentials**
2. Add **Username with password**:
   - ID: `github-pat`
   - Username: Your GitHub username
   - Password: Your Personal Access Token

**Nexus Credentials:**
1. Add **Username with password**:
   - ID: `nexus-credentials`
   - Username: Your Nexus username
   - Password: Your Nexus password

#### Create Pipeline Job
1. **New Item** → Enter name → **Pipeline**
2. **Pipeline** section:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/YOUR-USERNAME/YOUR-REPO.git`
   - Credentials: Select `github-pat`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
3. **Build Triggers**:
   - ✅ **GitHub hook trigger for GITScm polling**

#### Configure Webhook
1. **GitHub repo** → **Settings** → **Webhooks** → **Add webhook**
2. Payload URL: `http://YOUR-JENKINS-URL/github-webhook/`
3. Content type: `application/json`
4. Events: **Just the push event**
5. Active: ✅

### 3. Update Jenkinsfile

Edit `Jenkinsfile` and replace:
- Line 9: `NEXUS_REGISTRY = 'your-nexus-server.com:8082'`
- Line 69: `git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/YOUR-USERNAME/YOUR-REPO.git`
- Line 88: `git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/YOUR-USERNAME/YOUR-REPO.git`

## 👨‍💻 Developer Workflow

### Creating a Feature

```bash
# 1. Create and switch to feature branch
git checkout -b feature/add-division-enhancement

# 2. Make code changes
# Edit src/app.py

# 3. Format code with Black (REQUIRED)
black src/ tests/

# 4. Run tests locally
pytest tests/

# 5. Commit and push
git add .
git commit -m "feat: enhance division with decimal precision"
git push origin feature/add-division-enhancement
```

### Opening Pull Request

1. Go to GitHub repository
2. Click **Compare & pull request**
3. Ensure base branch is `main`
4. Add description of changes
5. Click **Create pull request**

### What Happens Next

✅ **GitHub Actions runs automatically:**
- Checks Black formatting
- Runs unit tests
- Reports status on PR

⏳ **Wait for approval:**
- Reviewer examines code
- Provides feedback
- Approves PR

✅ **Merge PR:**
- Click **Merge pull request**
- Confirm merge

🤖 **Jenkins automatically:**
- Increments version (1.0.0 → 1.0.1)
- Builds Docker image
- Pushes to Nexus
- Creates Git tag

## 🔧 Manual Commands

### Format Code
```bash
# Check formatting (what GitHub Actions does)
black --check src/ tests/

# Auto-format code
black src/ tests/
```

### Run Tests
```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_app.py::TestBasicOperations::test_add
```

### Build Docker Image Locally
```bash
# Read current version
VERSION=$(cat VERSION)

# Build image
docker build --build-arg VERSION=$VERSION -t calculator-app:$VERSION .

# Run container
docker run --rm calculator-app:$VERSION
```

### Pull from Nexus
```bash
# Login to Nexus
docker login nexus.example.com:8082

# Pull specific version
docker pull nexus.example.com:8082/docker-hosted/calculator-app:1.0.5

# Pull latest
docker pull nexus.example.com:8082/docker-hosted/calculator-app:latest
```

## 📊 Version Management

### Semantic Versioning Format
```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └── Bug fixes (backward compatible)
  │     └──────── New features (backward compatible)
  └────────────── Breaking changes
```

### Current Implementation
- **Automatic PATCH increment** on every merge to main
- Example: 1.0.0 → 1.0.1 → 1.0.2

### Future Enhancement
Parse commit messages for semantic versioning:
- `feat:` → MINOR bump (1.0.0 → 1.1.0)
- `fix:` → PATCH bump (1.0.0 → 1.0.1)
- `feat!:` or `BREAKING CHANGE:` → MAJOR bump (1.0.0 → 2.0.0)

## 🧪 Testing the Pipeline

### Test Scenario: Poorly Formatted Code

```bash
# 1. Create feature branch
git checkout -b feature/test-black-check

# 2. Add poorly formatted code (DO NOT run black)
echo "def bad_function( a,b ):return a+b" >> src/app.py

# 3. Push
git commit -am "Add bad function"
git push origin feature/test-black-check

# 4. Open PR
# Result: GitHub Actions will FAIL ❌
# Error: "Files would be reformatted"
```

### Test Scenario: Successful Merge

```bash
# 1. Create feature branch
git checkout -b feature/add-power-function

# 2. Add new function
cat >> src/app.py << 'EOF'

def power(a, b):
    """Raise a to the power of b"""
    return a ** b
EOF

# 3. Format with Black
black src/

# 4. Add test
cat >> tests/test_app.py << 'EOF'

def test_power():
    assert power(2, 3) == 8
    assert power(5, 2) == 25
EOF

# 5. Push and create PR
git add .
git commit -m "feat: add power function"
git push origin feature/add-power-function

# 6. PR checks pass ✅
# 7. Merge to main ✅
# 8. Jenkins automatically increments version and deploys 🚀
```

## 🐛 Troubleshooting

### GitHub Actions Fails: "Files would be reformatted"
**Solution:** Run `black src/ tests/` locally and push again

### Jenkins Fails: "Permission denied"
**Solution:** Ensure GitHub PAT has `repo` scope and Nexus credentials are correct

### Jenkins Fails: "docker: command not found"
**Solution:** Install Docker on Jenkins agent and add jenkins user to docker group

### Merge Conflicts on VERSION File
**Solution:** This shouldn't happen! VERSION is only modified by Jenkins on main branch. Feature branches never touch VERSION.

### Webhook Not Triggering Jenkins
**Solution:** 
- Check Jenkins URL is accessible from GitHub
- Verify webhook secret/token if configured
- Check Jenkins logs: **Manage Jenkins** → **System Log**

## 📁 Project Structure

```
jenkins-version-auto-increment/
├── .github/
│   └── workflows/
│       └── pr-checks.yml          # GitHub Actions: Black + pytest
├── src/
│   └── app.py                     # Calculator application
├── tests/
│   └── test_app.py                # Unit tests
├── .gitignore                     # Git ignore patterns
├── Dockerfile                     # Multi-stage Docker build
├── Jenkinsfile                    # Jenkins pipeline definition
├── README.md                      # This file
├── requirements.txt               # Python dependencies
└── VERSION                        # Version file (1.0.0)
```

## 🎓 Key Learning Points

1. **Branch Protection** - Enforces code review and quality checks
2. **Pre-merge vs Post-merge** - Quality gates before merge, deployment after merge
3. **Semantic Versioning** - Industry-standard version management
4. **CI/CD Separation** - GitHub Actions for validation, Jenkins for delivery
5. **Immutable Artifacts** - Each version is a unique, permanent Docker image
6. **GitOps Principles** - Version controlled, auditable, reproducible builds
7. **Multi-stage Docker** - Optimized images for production
8. **Artifact Management** - Centralized storage with Nexus

## 🌟 Skills Demonstrated

- ✅ Jenkins pipeline scripting (Groovy)
- ✅ GitHub Actions workflows (YAML)
- ✅ Docker containerization & multi-stage builds
- ✅ Git branching strategy & branch protection
- ✅ Semantic versioning automation
- ✅ Artifact repository management (Nexus)
- ✅ Code quality enforcement (Black formatter)
- ✅ Test-driven development (pytest)
- ✅ CI/CD best practices
- ✅ DevOps toolchain integration

## 📝 License

This is a learning/portfolio project. Feel free to use and modify.

## 👤 Author

[Your Name] - DevOps Engineer

---

**Note:** Remember to replace placeholders in Jenkinsfile with your actual URLs and credentials before running the pipeline!
