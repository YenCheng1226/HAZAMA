# Team Git Workflow Guide

Establishing a clear and consistent Git workflow is one of the most critical steps for a successful team project. This guide outlines our team's workflow, based on best practices used by many development teams.

We use a **Trunk-Based Development** approach, which is simple, effective, and focuses on keeping our main branch clean and deployable at all times.

### 1. The Branching Model

The core idea is to have one main, stable branch and use short-lived branches for all development work.

*   **`main` Branch (The Trunk):**
    *   This is your single source of truth.
    *   It must **always** be in a stable, working, and potentially releasable state.
    *   **Rule:** No one ever commits directly to `main`. All changes must come through Pull Requests.

*   **Feature Branches (`feature/`, `bugfix/`, `docs/`):**
    *   All new work—features, bug fixes, documentation, etc.—is done on a separate branch.
    *   These branches are created from the `main` branch.
    *   **Naming Convention:** Use a clear and descriptive naming convention. A good practice is to prefix the branch name with a type, like `feature/add-user-login` or `bugfix/fix-map-rendering-issue`.
    *   These branches should be **short-lived**. Aim to have them merged within a day or two to avoid diverging too far from `main`.

*   **Release Branches (`release/v1.1`, `release/v1.2`): (Optional, but good for formal releases)**
    *   When you are ready to prepare a new release, create a `release` branch from `main`.
    *   This branch is used for final testing, minor bug fixes, and preparing release notes. No new features are added here.
    *   This allows the `main` branch to continue accepting new features for the *next* release while the current one is being finalized.

### 2. The Core Workflow in 6 Steps

Here is the day-to-day workflow for every developer on the team:

1.  **Create a Branch:** Before starting any work, pull the latest from `main` and create a new feature branch.
    ```bash
    git checkout main
    git pull origin main
    git checkout -b feature/my-new-feature
    ```

2.  **Develop and Commit:** Work on your feature. Make small, atomic commits with clear messages.
    *   **Commit Message Best Practice:** A good commit message has a short subject line (e.g., `feat: Add user authentication endpoint`) and an optional body explaining the "why" of the change. Following a convention like [Conventional Commits](https://www.conventionalcommits.org/) is highly recommended.

3.  **Push and Open a Pull Request (PR):** Once your work is ready for review (or even if it's a work-in-progress you want feedback on), push your branch and open a Pull Request against the `main` branch.
    ```bash
    git push -u origin feature/my-new-feature
    ```
    Your PR description should be clear, explaining what the change does and how to test it. Using a PR template can help enforce this.

4.  **Code Review & Automated Checks (CI):**
    *   **Code Review:** Team members review the PR. The goal is to catch bugs, improve code quality, and share knowledge. At least **one approval** from another developer should be required.
    *   **Continuous Integration (CI):** Automated checks (like linting with `ruff`, formatting with `black`, and running your `pytest` suite) should automatically run on every PR. A PR should not be mergeable if these checks fail.

5.  **Merge the PR:** Once the PR is approved and all checks pass, merge it into `main`.
    *   **Recommendation:** Use **Squash and Merge**. This combines all the commits from your feature branch into a single, clean commit on the `main` branch. It keeps the history of `main` easy to read and understand.

6.  **Clean Up:** After merging, delete the feature branch. This keeps your repository tidy.
    ```bash
    git branch -d feature/my-new-feature
    ```

### 3. How to Enforce This Workflow

You can—and should—enforce this workflow using your Git provider's features (e.g., GitHub, GitLab):

*   **Protect Your `main` Branch:**
    *   Go to your repository settings and set up branch protection rules for `main`.
    *   Require Pull Requests before merging.
    *   Require status checks (your CI pipeline) to pass before merging.
    *   Require at least one code review approval.
    *   Disable "force push" on `main`.

### Summary of Recommendations:

1.  **Adopt a trunk-based model:** `main` is always stable; work happens in feature branches.
2.  **Enforce Pull Requests:** All changes to `main` go through a PR.
3.  **Require Code Reviews:** Mandate at least one approval.
4.  **Automate Everything:** Use CI for linting, testing, and formatting checks.
5.  **Use Squash and Merge:** Keep your `main` history clean.
6.  **Protect `main`:** Use your Git provider's branch protection rules.
