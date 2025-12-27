# Jenkins CI/CD Pipeline with Auto-Versioning

Production-grade CI/CD pipeline demonstrating automated semantic versioning, branch protection with GitHub Actions pre-merge quality gates, and Jenkins post-merge Docker build automation with Nexus artifact management.

## 🎯 Project Overview

This project showcases:
- **GitHub Branch Protection Rulesets** - Enforce PR workflow with status checks
- **GitHub Actions Pre-Merge Gates** - Black formatter validation and pytest execution
- **GitHub Actions Post-Merge Versioning** - Automated version increment with manual override support
- **Version Validation** - Prevents version downgrades and ensures semantic versioning compliance
- **Jenkins Docker Build Pipeline** - Containerization and Nexus push automation
- **Semantic Versioning** - Automated MAJOR.MINOR.PATCH version management with Git tagging
- **Docker Multi-stage Build** - Optimized production images
- **Nexus Repository** - Centralized Docker artifact storage

## 📋 Prerequisites

- **GitHub Account** with repository
- **GitHub Personal Access Token (PAT)** with `repo` and `workflow` scopes
- **Jenkins Server** with Docker installed and accessible to Jenkins user
- **Nexus Repository Manager** with Docker hosted repository configured
- **Nexus Credentials** for Docker registry authentication

## 🏗️ Architecture

```
Developer Workflow:
┌─────────────────────────────────────────────────────────────────┐
│  1. Create feature branch from main                             │
│  2. Make code changes                                           │
│  3. Format code: black src/ tests/                             │
│  4. Push to GitHub                                              │
│  5. Open Pull Request to main                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  GitHub Actions: PR Quality Checks (Pre-Merge)                  │
│  ✓ Black formatter check (must pass)                            │
│  ✓ Unit tests with pytest (must pass)                           │
│  ✓ Status reported on PR                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Branch Protection Enforcement                                  │
│  ✓ All status checks must pass                                  │
│  ✓ PR required (no direct commits to main)                      │
│  ✓ Bypass enabled for Repository Admins (for automation)        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Merge to main branch                                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  GitHub Actions: Version Bump (Post-Merge)                      │
│  1. Check if commit author is bot → Skip if yes                 │
│  2. Check if VERSION manually changed in PR                     │
│     - If YES: Validate version is forward-only                  │
│       (prevents 1.0.6 → 1.0.5 downgrades)                       │
│     - If NO: Auto-increment PATCH (1.0.11 → 1.0.12)            │
│  3. Commit VERSION to main as github-actions[bot]               │
│  4. Create Git tag (v1.0.12)                                    │
│  5. Push triggers Jenkins webhook                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Jenkins Pipeline: Docker Build & Deploy                        │
│  1. Read VERSION file (1.0.12)                                  │
│  2. Build Docker image with version tag                         │
│  3. Tag for Nexus registry                                      │
│  4. Push to Nexus (versioned + latest tags)                    │
│  5. Cleanup local images                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Nexus Repository                                               │
│  calculator-app:1.0.12 ✓                                       │
│  calculator-app:latest ✓                                       │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Setup Instructions

### 1. GitHub Repository Setup

#### Create GitHub Personal Access Token (PAT)
1. Go to: https://github.com/settings/tokens/new
2. Token name: `Jenkins CI/CD Pipeline`
3. Expiration: 90 days (or your preference)
4. Select scopes:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **workflow** (Update GitHub Action workflows)
5. Click **Generate token**
6. **COPY THE TOKEN** - You'll only see it once!

#### Add PAT as Repository Secret
1. Go to your repo: **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `PAT_TOKEN`
4. Secret: Paste your PAT token
5. Click **Add secret**

#### Push Initial Code
```bash
cd jenkins-docker-versioning-pipeline
git init
git add .
git commit -m "Initial commit: CI/CD pipeline with auto-versioning"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

#### Configure Branch Protection Ruleset
1. Go to **Settings** → **Rules** → **Rulesets**
2. Click **New ruleset** → **New branch ruleset**
3. Ruleset name: `main-branch-protection`
4. Enforcement status: **Active**
5. **Target branches**: Add target → Include by pattern → Pattern: `main`
6. **Bypass list**: Add bypass → **Repository roles** → Select **Repository admin**
7. Enable these rules:
   - ✅ **Restrict deletions**
   - ✅ **Require a pull request before merging** (Required approvals: 0 for solo, 1+ for team)
   - ✅ **Require status checks to pass**
     - ✅ **Require branches to be up to date before merging**
     - Add required check: `Code Quality & Tests`
   - ✅ **Block force pushes**
8. Click **Create**

### 2. Jenkins Setup

#### Install Required Plugins
- Git Plugin
- Pipeline Plugin
- Docker Pipeline Plugin
- Credentials Plugin

#### Configure Docker Access
Jenkins needs permission to use Docker. On your Jenkins server:
```bash
# Add jenkins user to docker group
sudo usermod -aG docker jenkins

# Restart Jenkins
sudo systemctl restart jenkins

# Verify docker access
sudo -u jenkins docker ps
```

#### Add Credentials

**GitHub Credentials (for git checkout):**
1. **Manage Jenkins** → **Credentials** → **System** → **Global credentials**
2. Add **Username with password**:
   - ID: `github-creds`
   - Username: Your GitHub username
   - Password: Your GitHub Personal Access Token

**Nexus Docker Repository Credentials:**
1. Add **Username with password**:
   - ID: `nexus-docker-repo-cred`
   - Username: Your Nexus username
   - Password: Your Nexus password

#### Create Pipeline Job
1. **New Item** → Enter name: `jenkins-docker-versioning-pipeline` → **Pipeline**
2. **Build Triggers**:
   - ✅ **GitHub hook trigger for GITScm polling**
3. **Pipeline** section:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/YOUR-USERNAME/YOUR-REPO.git`
   - Credentials: Select `github-creds`
   - Branch Specifier: `*/main`
   - Script Path: `Jenkinsfile`
4. **Save**

#### Configure GitHub Webhook
1. **GitHub repo** → **Settings** → **Webhooks** → **Add webhook**
2. Payload URL: `http://YOUR-JENKINS-URL:PORT/github-webhook/`
3. Content type: `application/json`
4. SSL verification: Disable (if using HTTP) or Enable (if using HTTPS)
5. Which events: **Just the push event**
6. Active: ✅
7. **Add webhook**

### 3. Configure Project Parameters

The Jenkinsfile uses parameters that can be set on first run or updated later:
- **NEXUS_REGISTRY**: Your Nexus server URL with port (e.g., `159.203.56.144:8083`)
- **NEXUS_REPO**: Nexus repository name (e.g., `docker-private`)
- **DOCKER_IMAGE_NAME**: Docker image name (e.g., `calculator-app`)

Parameters are automatically prompted on first pipeline run.

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

🤖 **GitHub Actions automatically:**
- Detects merge to main
- Checks if VERSION was manually changed
  - If YES: Validates version is forward-only (no downgrades)
  - If NO: Auto-increments PATCH (1.0.11 → 1.0.12)
- Commits VERSION file back to main
- Creates Git tag (v1.0.12)
- Triggers Jenkins via webhook

🐳 **Jenkins automatically:**
- Reads VERSION file (1.0.12)
- Builds Docker image with version tag
- Pushes to Nexus registry
- Cleans up local images

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

### Automatic Version Increment
- **Default behavior**: PATCH increment on every merge (1.0.0 → 1.0.1 → 1.0.2)
- **Triggered by**: GitHub Actions after merge to main
- **Committed as**: `github-actions[bot]` with message `[skip ci] Bump version to X.Y.Z`
- **Tagged**: Creates Git tag `vX.Y.Z` automatically

### Manual Version Control
Developers can manually bump version by modifying the VERSION file in their PR:

**Valid manual bumps:**
```bash
# Current version: 1.2.5

# MAJOR version bump (breaking changes)
echo "2.0.0" > VERSION

# MINOR version bump (new features)
echo "1.3.0" > VERSION

# PATCH version bump (bug fix)
echo "1.2.6" > VERSION
```

**Version Validation:**
- ✅ Workflow validates manual version changes
- ❌ Prevents downgrades (1.2.5 → 1.2.4 will FAIL)
- ❌ Prevents same version (1.2.5 → 1.2.5 will FAIL)
- ✅ Only forward versions allowed

**Error Example:**
```
❌ ERROR: Invalid version bump!
   Current version: 1.2.5
   Your version: 1.2.4

Version must be GREATER than current version.
Examples of valid bumps from 1.2.5:
  - Patch: 1.2.6
  - Minor: 1.3.0
  - Major: 2.0.0
```

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
**Cause:** Code not formatted with Black  
**Solution:** Run `black src/ tests/` locally and push again

### GitHub Actions Fails: "Permission denied" when pushing version
**Cause:** PAT token missing or incorrect, or bypass list not configured  
**Solution:**
1. Verify `PAT_TOKEN` secret exists with correct value
2. PAT must have `repo` and `workflow` scopes
3. Add "Repository admin" to bypass list in branch protection ruleset

### Jenkins Fails: "docker: command not found" or "permission denied"
**Cause:** Jenkins user lacks Docker permissions  
**Solution:**
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Jenkins Not Triggering After Merge
**Cause:** Webhook not configured or Jenkins URL unreachable  
**Solution:**
1. Verify webhook exists: Repo → Settings → Webhooks
2. Check webhook delivery history for errors
3. Test Jenkins URL accessibility from external network
4. Verify build trigger enabled in Jenkins job config

### Version Stays at 1.0.11 After Multiple Merges
**Cause:** GitHub Actions version bump workflow is failing  
**Solution:**
1. Check Actions tab for failed workflows
2. Review error messages in workflow logs
3. Common issues: PAT token, bypass permissions, git conflicts

### Merge Conflicts on VERSION File
**Cause:** Multiple PRs modifying VERSION simultaneously  
**Solution:**
1. Feature branches should NEVER modify VERSION (unless intentional manual bump)
2. Pull latest main before creating new feature branch
3. If conflict occurs, accept main's version and resolve

### Docker Build Fails: "No space left on device"
**Cause:** Docker image cleanup not working, disk full  
**Solution:**
```bash
# On Jenkins server
docker system prune -a -f
docker volume prune -f
```

## 📁 Project Structure

```
jenkins-docker-versioning-pipeline/
├── .github/
│   └── workflows/
│       ├── pr-checks.yml         # Pre-merge: Black + pytest
│       └── version-bump.yml      # Post-merge: Version increment + validation
├── src/
│   └── app.py                    # Calculator application (with power function)
├── tests/
│   └── test_app.py               # Unit tests with pytest
├── .gitignore                    # Git ignore patterns
├── Dockerfile                    # Multi-stage Docker build
├── Jenkinsfile                   # Jenkins Docker build pipeline
├── README.md                     # This documentation
├── requirements.txt              # Python dependencies (black, pytest)
└── VERSION                       # Current version (e.g., 1.0.12)
```

## 🎓 Key Learning Points

1. **Separation of Concerns** - GitHub Actions for quality gates & versioning, Jenkins for Docker build & deployment
2. **Branch Protection Rulesets** - Modern GitHub branch protection with bypass lists for automation
3. **Pre-merge vs Post-merge** - Quality validation before merge, versioning & deployment after merge
4. **Semantic Versioning** - Industry-standard version management with manual override capability
5. **Version Validation** - Prevents version downgrades and maintains version integrity
6. **Immutable Artifacts** - Each version is a unique, permanent Docker image with Git tag reference
7. **GitOps Principles** - Version controlled, auditable, reproducible builds
8. **Multi-stage Docker** - Optimized production images with separate build and runtime stages
9. **Artifact Management** - Centralized Docker image storage with Nexus Repository
10. **Webhook Integration** - Event-driven pipeline triggers for automated workflows
11. **Credential Management** - Secure handling of PATs and service credentials
12. **CI/CD Best Practices** - No manual intervention, automated testing, deployment automation

## 🌟 Skills Demonstrated

**DevOps & CI/CD:**
- ✅ CI/CD pipeline design and implementation
- ✅ GitHub Actions workflows (YAML)
- ✅ Jenkins pipeline scripting (Groovy)
- ✅ Webhook-based automation
- ✅ Multi-tool integration (GitHub + Jenkins + Nexus)

**Version Control & Git:**
- ✅ Git branching strategies (feature branches, main branch protection)
- ✅ Branch protection rules and enforcement
- ✅ Git tagging for releases
- ✅ Automated version management

**Containerization:**
- ✅ Docker containerization
- ✅ Multi-stage Docker builds
- ✅ Image tagging strategies
- ✅ Container registry management (Nexus)

**Code Quality:**
- ✅ Automated code formatting (Black)
- ✅ Test-driven development (pytest)
- ✅ Pre-merge quality gates
- ✅ Status check enforcement

**Security & Best Practices:**
- ✅ PAT token management
- ✅ Credential storage (GitHub Secrets, Jenkins Credentials)
- ✅ Least privilege access
- ✅ Branch protection bypass for automation

**Problem Solving:**
- ✅ Infinite loop prevention (bot commit detection)
- ✅ Version conflict resolution
- ✅ Permission management for automation
- ✅ Docker permission issues

## 🔮 Future Enhancements

1. **Conventional Commits**: Parse commit messages to determine MAJOR/MINOR/PATCH increment automatically
   - `feat:` → MINOR bump
   - `fix:` → PATCH bump  
   - `feat!:` or `BREAKING CHANGE:` → MAJOR bump

2. **Multi-environment Deployment**: Extend Jenkins pipeline for dev/staging/prod deployments

3. **Release Notes Generation**: Auto-generate CHANGELOG.md from commit messages

4. **Slack/Discord Notifications**: Alert team on successful deployments or failures

5. **Rollback Capability**: Automated rollback to previous version on deployment failure

6. **Pre-release Versions**: Support alpha/beta/rc versions (1.0.0-alpha.1)

7. **Parallel Testing**: Run tests in parallel for faster feedback

8. **Code Coverage Reporting**: Integrate coverage reports in PR checks

9. **Security Scanning**: Add Trivy or Snyk for vulnerability scanning

10. **Performance Testing**: Load testing before production deployment

## 📝 License

This is a learning/portfolio project. Feel free to use and modify.

## 👤 Author

Priyal Patel

---

**Note:** Remember to replace placeholders in Jenkinsfile with your actual URLs and credentials before running the pipeline!
