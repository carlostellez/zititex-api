# Git Setup and GitHub Actions Configuration

This guide explains how to set up the Git repository and configure GitHub Actions for CI/CD.

## 📋 Prerequisites

- Git installed
- GitHub account
- Repository created on GitHub (or will create one)

---

## 🚀 Initial Git Setup

### 1. Initialize Git Repository

```bash
# Navigate to project directory
cd /Users/ctellez/developer/back/zititex-api/zititex-api

# Initialize git
git init

# Check status
git status
```

### 2. Add All Files

```bash
# Add all files to staging
git add .

# Verify files are staged
git status
```

### 3. Create Initial Commit

```bash
# Create initial commit
git commit -m "feat: initial project setup with Clean Architecture

- Implement Clean Architecture structure (domain, application, infrastructure, presentation)
- Configure FastAPI with async support
- Set up PostgreSQL and Redis integration
- Add comprehensive test suite with pytest
- Configure pre-commit hooks (black, isort, flake8, mypy)
- Create GitHub Actions workflows (CI, CD, PR checks)
- Add Docker and Docker Compose configuration
- Create comprehensive documentation (README, run.md, prompts.md)
- Set up development tools (Makefile, setup script)
- Implement SOLID principles throughout codebase
- Configure type hints and coverage requirements (>99%)
- Add health check endpoints
- Create contribution guidelines and issue templates"
```

### 4. Create Main Branch

```bash
# Rename master to main (if needed)
git branch -M main
```

---

## 🔗 Connect to GitHub

### Option A: Create New Repository on GitHub

1. Go to https://github.com/new
2. Create repository named `zititex-api`
3. Do NOT initialize with README, .gitignore, or license
4. Copy the repository URL

### Option B: Use Existing Repository

If you already have a repository, get its URL.

### Connect Local to Remote

```bash
# Add remote origin (replace with your repository URL)
git remote add origin https://github.com/yourusername/zititex-api.git

# Verify remote
git remote -v
```

### Push to GitHub

```bash
# Push to main branch
git push -u origin main
```

---

## ⚙️ Configure GitHub Secrets

For GitHub Actions to work properly, configure these secrets:

### 1. Go to Repository Settings

Navigate to: `Settings` → `Secrets and variables` → `Actions`

### 2. Add Required Secrets

Click **"New repository secret"** and add:

#### Docker Hub (for CD pipeline)

| Secret Name | Description | Example |
|------------|-------------|---------|
| `DOCKER_USERNAME` | Docker Hub username | `yourusername` |
| `DOCKER_PASSWORD` | Docker Hub password or token | `dckr_pat_...` |

#### Codecov (optional, for coverage reporting)

| Secret Name | Description |
|------------|-------------|
| `CODECOV_TOKEN` | Codecov upload token |

### 3. Configure Environment Variables (optional)

For deployment, you may need:

| Variable | Description |
|----------|-------------|
| `STAGING_SERVER` | Staging server URL |
| `PRODUCTION_SERVER` | Production server URL |
| `SSH_PRIVATE_KEY` | SSH key for deployment |

---

## 🔧 Enable GitHub Actions

### 1. Enable Actions

- Go to repository `Settings` → `Actions` → `General`
- Under "Actions permissions", select **"Allow all actions"**
- Save changes

### 2. Verify Workflows

- Go to `Actions` tab
- You should see three workflows:
  - ✅ CI (Continuous Integration)
  - ✅ CD (Continuous Deployment)
  - ✅ Pull Request

### 3. Trigger First CI Run

```bash
# Make a small change to trigger CI
echo "# Zititex API" > test.txt
git add test.txt
git commit -m "test: trigger CI workflow"
git push origin main

# Remove test file
git rm test.txt
git commit -m "chore: remove test file"
git push origin main
```

Check the `Actions` tab to see the workflow run.

---

## 🌿 Branch Protection Rules

Protect your main branch:

### 1. Configure Branch Protection

Go to: `Settings` → `Branches` → `Add rule`

### 2. Recommended Settings

- **Branch name pattern**: `main`
- ✅ Require a pull request before merging
  - ✅ Require approvals (1)
- ✅ Require status checks to pass before merging
  - ✅ Require branches to be up to date before merging
  - Select checks: `lint`, `test`, `security`
- ✅ Require conversation resolution before merging
- ✅ Do not allow bypassing the above settings

### 3. Save Changes

---

## 🔄 Workflow Examples

### Create Feature Branch

```bash
# Create and switch to feature branch
git checkout -b feature/add-user-authentication

# Make changes...
# Add files
git add .

# Commit with conventional commit message
git commit -m "feat(auth): add JWT authentication

- Implement JWT token generation
- Add user login endpoint
- Create authentication middleware
- Add tests for authentication flow"

# Push branch
git push origin feature/add-user-authentication
```

### Create Pull Request

1. Go to GitHub repository
2. Click **"Compare & pull request"**
3. Fill in PR template:
   - Description of changes
   - Type of change
   - Testing performed
   - Checklist items
4. Click **"Create pull request"**
5. Wait for CI checks to pass
6. Request review
7. Merge after approval

### Update from Main

```bash
# Switch to main
git checkout main

# Pull latest changes
git pull origin main

# Switch back to feature branch
git checkout feature/your-feature

# Rebase or merge
git rebase main
# or
git merge main

# Push updates
git push origin feature/your-feature
```

---

## 📦 Release Process

### Create a Release

```bash
# Create and checkout release branch
git checkout -b release/v1.0.0

# Update version in files
# - pyproject.toml
# - src/__init__.py
# - CHANGELOG.md

# Commit version bump
git add .
git commit -m "chore: bump version to 1.0.0"

# Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0

Features:
- User authentication
- User management
- Health check endpoints

Breaking Changes:
- None

Bug Fixes:
- None"

# Push tag
git push origin v1.0.0

# Push branch
git push origin release/v1.0.0
```

### Create GitHub Release

1. Go to `Releases` → `Draft a new release`
2. Choose tag: `v1.0.0`
3. Release title: `Version 1.0.0`
4. Description: Copy from CHANGELOG.md
5. Click **"Publish release"**

This will trigger the CD workflow to deploy to production!

---

## 🔍 Verify GitHub Actions

### Check CI Workflow

```bash
# Push changes and check Actions tab
git push origin main
```

Expected CI steps:
1. ✅ Checkout code
2. ✅ Set up Python 3.12
3. ✅ Install dependencies
4. ✅ Run Black
5. ✅ Run isort
6. ✅ Run Flake8
7. ✅ Run MyPy
8. ✅ Run tests with coverage
9. ✅ Security checks

### Check CD Workflow

```bash
# Push tag to trigger deployment
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0
```

Expected CD steps:
1. ✅ Build Docker image
2. ✅ Push to Docker Hub
3. ✅ Deploy to staging/production

---

## 🐛 Troubleshooting

### Workflow Not Triggering

**Problem**: GitHub Actions not running

**Solution**:
```bash
# Ensure workflows are in correct location
ls -la .github/workflows/

# Check file permissions
chmod 644 .github/workflows/*.yml

# Verify yaml syntax
yamllint .github/workflows/ci.yml
```

### Secret Not Found

**Problem**: `Error: Secret DOCKER_USERNAME not found`

**Solution**:
- Go to repository Settings → Secrets
- Add the missing secret
- Re-run workflow

### Permission Denied

**Problem**: `Permission denied (publickey)`

**Solution**:
```bash
# Check SSH key
ssh -T git@github.com

# Or use HTTPS
git remote set-url origin https://github.com/yourusername/zititex-api.git
```

### Merge Conflicts

**Problem**: Conflicts when merging/rebasing

**Solution**:
```bash
# View conflicts
git status

# Edit conflicted files
# Then:
git add .
git rebase --continue
# or
git merge --continue
```

---

## 📚 Git Best Practices

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

### Branch Naming

```
feature/short-description
fix/bug-description
docs/documentation-update
refactor/code-improvement
```

### Keep Commits Small

- One logical change per commit
- Write clear commit messages
- Reference issues when applicable

---

## ✅ Checklist

After completing this guide:

- [ ] Git repository initialized
- [ ] Connected to GitHub remote
- [ ] Initial commit pushed
- [ ] GitHub secrets configured
- [ ] GitHub Actions enabled
- [ ] Branch protection rules set
- [ ] First CI workflow ran successfully
- [ ] Docker Hub credentials configured
- [ ] Release process understood

---

## 🎉 You're All Set!

Your repository is now configured with:
- ✅ Automated CI/CD pipelines
- ✅ Code quality checks
- ✅ Branch protection
- ✅ Deployment automation

**Next Steps**:
1. Start developing features
2. Create pull requests
3. Let CI/CD handle testing and deployment

---

For more information, see:
- [README.md](README.md) - Project overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guide
- [GitHub Actions Docs](https://docs.github.com/en/actions)

