# Mini Data Quality CI/CD (Python + GitHub Actions)

A browser-only, lightweight team demo. No local Python, pip, pandas, Docker, or database is required to participate.

## The scenario

The raw data contains inconsistent capitalization/whitespace, a duplicate `order_id`, a negative amount, a zero amount, a missing customer, and a non-numeric amount. Our business rule is: **keep only unique orders with a nonempty ID and customer, and a positive integer amount**.

Expected cleaned result:

```csv
order_id,customer,amount
O001,Alice,120
O002,Bob,350
O006,Eka,80
```

## Repository files

- `data/orders_raw.csv`: dirty source data
- `wrangle.py`: CSV cleaning implementation
- `tests/test_wrangle.py`: two unit tests
- `.github/workflows/ci-cd.yml`: one GitHub-hosted job: test, transform, and (on pushes to `main`) upload artifact
- `.gitignore`: keeps generated files out of version control

## Host setup (before the meeting)

1. Create a GitHub repository with `main` as its default branch and upload these files, preserving `.github/workflows/ci-cd.yml`.
2. Confirm the `Actions` tab shows a successful run after the initial push to `main`.
3. In the run summary's **Artifacts** section, confirm `cleaned-orders` downloads correctly.
4. Check Settings > Actions > General to ensure GitHub Actions is allowed. For participants to open PRs, grant appropriate repository permissions or use the presenter account.
5. Keep a pristine branch or backup zip for a quick reset.

## Live walkthrough (around 20–25 minutes)

1. **Context (3 min)**: show raw CSV and its defects; ask which records must be excluded.
2. **CI (4 min)**: inspect the Python script, unit tests, and YAML; point out `pull_request`.
3. **Cause a failure (5 min)**: use GitHub's browser editor to create a feature branch. In `wrangle.py`, replace `amount <= 0` with `amount < 0` (zero-value orders now incorrectly pass). Open a pull request to `main`. The unit test should fail; inspect the red X and logs.
4. **Fix it (5 min)**: edit `wrangle.py` on the same feature branch and restore `amount <= 0`. Commit. The PR CI should pass.
5. **Review and deliver (5 min)**: review/merge the PR to `main`; the `push` workflow runs and uploads `cleaned-orders` as a downloadable run artifact. Compare the downloaded CSV with expected output.
6. **Wrap-up (3 min)**: CI catches defects automatically; the artifact is **continuous delivery**, not a production deployment.

> Note: GitHub Actions runner startup and queue delays vary. Individual Python operations are tiny, but total workflow time is not guaranteed. Prepare a completed failing and passing run before the session as a fallback.

## Run locally (optional, not needed for participants)

```bash
python -m unittest discover -s tests -v
python wrangle.py
```

## Security and scope

Uses only first-party GitHub Actions and the Python standard library, `contents: read` permissions, no secrets, and a single hosted runner job. This is a teaching example, not a production-ready data-quality platform. The artifact is retained for seven days.
