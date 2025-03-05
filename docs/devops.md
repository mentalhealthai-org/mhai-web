# DevOps Guide

This guide provides instructions on how to set up and deploy `mhai-web` for **local development**, how to follow the **Git workflow**, and how to contribute using **semantic release**.

## Local Deployment for Development

To deploy `mhai-web` locally for development, follow these steps:

### 1. Clone the Repository

```bash
git clone git@github.com:your_username/mhai-web.git
cd mhai-web
```

### 2. Set Up the Environment

Use `mamba` to create a **Conda environment** and install dependencies using **Poetry**:

```bash
mamba env create --file conda/dev.yaml --yes
conda activate mhai-web
poetry config virtualenvs.create false
poetry install
```

### 3. Run the Database and Services

`mhai-web` requires **PostgreSQL, Redis, and Celery** to function properly. Start the necessary services using **Docker Compose**:

```bash
sugar compose-ext start --options -d
```

To stop the services:

```bash
sugar compose down
```

### 4. Apply Migrations and Start the Server

```bash
makim django.migrate
makim django.runserver
```

### 5. Access the Application

Once the development server is running, visit:

```
http://127.0.0.1:8000
```

---

## Git Workflow: Forking and Creating a Working Branch

### 1. Fork the Repository

Go to the [`mhai-web`](https://github.com/mentalhealthai-org/mhai-web) repository and **fork** it to your own GitHub account.

### 2. Clone Your Fork

```bash
git clone git@github.com:your_username/mhai-web.git
cd mhai-web
```

### 3. Add the Original Repository as Upstream

```bash
git remote add upstream git@github.com:mentalhealthai-org/mhai-web.git
```

To verify:

```bash
git remote -v
```

### 4. Create a New Branch

Always create a new branch when working on a feature or fix:

```bash
git checkout -b feat/your-new-feature
```

---

## Making Changes and Committing with Semantic Release

### 1. Make Your Changes

Edit or add new files as needed.

### 2. Run Pre-Commit Hooks

Ensure your code is formatted and follows best practices:

```bash
pre-commit run --all-files
```

### 3. Stage the Changes

```bash
git add .
```

### 4. Commit Using **Semantic Release Format**

```bash
git commit -m "feat: Add new feature description"
```

#### Semantic Commit Types:
- `feat`: Introduces a new feature.
- `fix`: Fixes a bug.
- `refactor`: Refactors code without changing functionality.
- `perf`: Improves performance.
- `docs`: Updates documentation.
- `style`: Formatting, whitespace, and linting changes.
- `test`: Adds or updates tests.
- `ci`: Changes to CI/CD configuration.
- `chore`: Miscellaneous tasks (e.g., dependencies update).

---

## Pushing Changes and Opening a PR

### 1. Push the Changes

```bash
git push --set-upstream origin feat/your-new-feature
```

### 2. Open a Pull Request

Go to the [mhai-web repository](https://github.com/mentalhealthai-org/mhai-web) and create a **Pull Request (PR)**.

---

## Special DevOps Section: Database Migrations and Updates

If you are working on **database migrations**, follow these steps:

### **Reset and Apply Migrations Locally**
```bash
makim django.bash
python manage.py migrate my_diary zero  # Revert migrations for my_diary (previously mhai_chat)
git pull upstream main  # Update your branch with latest changes
makim django.migrate  # Reapply migrations
```
