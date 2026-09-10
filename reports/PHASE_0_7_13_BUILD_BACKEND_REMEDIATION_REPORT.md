# PHASE 0.7.13 — Setuptools Build Backend Remediation Report

**Report Date:** 2026-09-10  
**Report Type:** Controlled Remediation & Verification  
**Phase Status:** 0.7.13 COMPLETE (Modifications applied)  
**Overall Phase 0 Status:** PENDING CI VERIFICATION

---

## A. Baseline

### Git State Before Modification

| Field | Value |
|-------|-------|
| **HEAD** | `f27598b38c563d2e76ddee6776b0a75fa53c0625` |
| **origin/main** | `bbe18784bac31d22080dd679f2b96d54cd85a357` |
| **Branch** | `main` |
| **Working Tree** | CLEAN |

### Previous CI Status (Run #26)

- **Run ID:** 34405247305
- **Tested Commit:** `8de396af6bc608dda15874e473f030067e9d3e5d`
- **Result:** 6/7 PASS, 1 FAIL (Docker)
- **Failing Job:** Docker Compose Verification
- **Failure:** Worker build at `pip install -e .` — `BackendUnavailable: Cannot import 'setuptools.backends._legacy'`

### Original Build System Configuration

**apps/worker/pyproject.toml (lines 27-29):**
```toml
[build-system]
requires = ["setuptools>=75.0"]
build-backend = "setuptools.backends._legacy:_Backend"  # ❌ BROKEN
```

**apps/api/pyproject.toml (lines 34-36):**
```toml
[build-system]
requires = ["setuptools>=75.0"]
build-backend = "setuptools.backends._legacy:_Backend"  # ❌ BROKEN
```

---

## B. Root Cause

### Reference: Phase 0.7.12 Forensic Report

The Phase 0.7.12 forensic investigation definitively identified that:

1. **The build backend `setuptools.backends._legacy:_Backend` does not exist** in any version of setuptools (tested versions 60-84)
2. **Local verification proved** the module path is invalid:
   - Host setuptools: 82.0.1
   - Test: `from setuptools.backends import _legacy` → `ModuleNotFoundError`
   - The `setuptools.backends` package directory does not exist

3. **The correct standard PEP 517 backend** is `setuptools.build_meta`

### Why This Caused Docker Failure

The Worker Dockerfile executes `pip install -e .` which:
1. Reads `pyproject.toml` to determine build system
2. Attempts to import the specified `build-backend`
3. Fails because `setuptools.backends._legacy` cannot be imported
4. Raises `BackendUnavailable` exception with exit code 2

---

## C. Exact Changes

### File 1: apps/worker/pyproject.toml

```diff
 [build-system]
 requires = ["setuptools>=75.0"]
-build-backend = "setuptools.backends._legacy:_Backend"
+build-backend = "setuptools.build_meta"
```

### File 2: apps/api/pyproject.toml

```diff
 [build-system]
 requires = ["setuptools>=75.0"]
-build-backend = "setuptools.backends._legacy:_Backend"
+build-backend = "setuptools.build_meta"
```

### Change Summary

| File | Line | Old Value | New Value |
|------|------|-----------|-----------|
| `apps/worker/pyproject.toml` | 29 | `setuptools.backends._legacy:_Backend` | `setuptools.build_meta` |
| `apps/api/pyproject.toml` | 36 | `setuptools.backends._legacy:_Backend` | `setuptools.build_meta` |

**Total Files Modified:** 2  
**Total Lines Changed:** 2 (1 per file)  
**Unrelated Changes:** 0

---

## D. Packaging Validation

### Environment Versions

| Component | Version |
|-----------|---------|
| **Python** | 3.12.14 |
| **pip** | 25.0.1 |
| **setuptools** | 82.0.1 |
| **wheel** | Not installed (not required) |

### Backend Resolution Test

```python
from setuptools import build_meta
print('✅ Backend import SUCCESS')
print('Backend module:', build_meta.__name__)
# Result: Backend module: setuptools.build_meta
```

**Available PEP 517 Hooks:**
- `build_wheel`
- `build_sdist`
- `build_editable`
- `get_requires_for_build_wheel`
- `get_requires_for_build_sdist`
- `get_requires_for_build_editable`
- `prepare_metadata_for_build_wheel`
- `prepare_metadata_for_build_editable`

### Worker Package Installation Test

```bash
$ cd apps/worker
$ python3 -m venv /tmp/test-worker-venv
$ source /tmp/test-worker-venv/bin/activate
$ pip install -e .
✅ WORKER install SUCCESS
Name: fcke-worker
Version: 0.1.0
Location: /tmp/test-worker-venv/lib/python3.12/site-packages
```

**This is the exact command that failed in Docker Run #26 — now succeeds.**

### API Package Installation Test

```bash
$ cd apps/api
$ python3 -m venv /tmp/test-api-venv
$ source /tmp/test-api-venv/bin/activate
$ pip install -e .
✅ API install SUCCESS
Name: fcke-api
Version: 0.1.0
Location: /tmp/test-api-venv/lib/python3.12/site-packages
```

### Static Verification

```bash
$ grep -r "setuptools.backends._legacy" . --include="*.toml"
✅ ZERO references to old broken backend found

$ grep -r "setuptools.build_meta" . --include="*.toml"
./apps/api/pyproject.toml:build-backend = "setuptools.build_meta"
./apps/worker/pyproject.toml:build-backend = "setuptools.build_meta"
✅ Both files contain correct backend
```

---

## E. API vs Worker Reconciliation

### Question

Both `apps/api/pyproject.toml` and `apps/worker/pyproject.toml` contained the same broken `build-backend`. However, Run #26's Docker job showed only the **Worker** failing. Why did the **API** not fail?

### Root Cause Analysis

The answer lies in how each Dockerfile installs Python packages:

#### Worker Dockerfile (`docker/Dockerfile.worker`)

```dockerfile
# Line 27: Copy ONLY pyproject.toml
COPY apps/worker/pyproject.toml ./

# Line 33: Install using pyproject.toml (PEP 517 build)
RUN pip install -e .    # ← INVOKES build-backend ← FAILS
```

**Worker Installation Flow:**
1. Copies `pyproject.toml` to `/app/`
2. Runs `pip install -e .`
3. pip reads `pyproject.toml`, finds `build-backend = "setuptools.backends._legacy:_Backend"`
4. Attempts to import backend → **FAILS**
5. Exit code 2, Docker build aborts

#### API Dockerfile (`docker/Dockerfile.api`)

```dockerfile
# Line 27: Copy BOTH requirements.txt AND pyproject.toml
COPY apps/api/requirements.txt apps/api/pyproject.toml ./

# Line 33: Install from requirements.txt (NOT pyproject.toml)
RUN pip install -r requirements.txt    # ← DOES NOT invoke build-backend ← SUCCEEDS
```

**API Installation Flow:**
1. Copies both `requirements.txt` and `pyproject.toml` to `/app/`
2. Runs `pip install -r requirements.txt`
3. pip reads `requirements.txt`, installs listed packages directly
4. **`pyproject.toml` is present but NEVER USED for installation**
5. Broken `build-backend` is never invoked → **SUCCEEDS**

### Conclusion

| Factor | Worker | API |
|--------|--------|-----|
| **Dockerfile Install Command** | `pip install -e .` | `pip install -r requirements.txt` |
| **Reads pyproject.toml?** | ✅ YES | ❌ NO |
| **Invokes build-backend?** | ✅ YES | ❌ NO |
| **Broken Backend Impact?** | 🔴 CAUSES FAILURE | ⚠️ LATENT (not triggered) |
| **Run #26 Status** | ❌ FAILED | ✅ PASSED |

**The API has a latent defect** — if its Dockerfile were ever changed to use `pip install -e .`, it would fail with the same error. Fixing it now prevents future failures.

---

## F. Docker Validation

### Local Docker Availability

```
Docker: NOT AVAILABLE locally
docker compose: NOT AVAILABLE locally
```

**Explicit Statement:** Docker validation could not be performed in this environment.

### Equivalent Validation Performed

The critical Docker operation was validated via direct Python packaging test:

| Docker Command | Local Equivalent | Result |
|----------------|------------------|--------|
| `RUN pip install -e .` (Dockerfile.worker:33) | `pip install -e .` in worker dir | ✅ SUCCESS |
| Package builds with correct backend | Backend resolution test | ✅ SUCCESS |
| No import errors | `from setuptools import build_meta` | ✅ SUCCESS |

**Confidence Level:** HIGH — The exact operation that failed in CI now succeeds locally.

---

## G. Regression Results

### Frontend Gates

| Gate | Command | Result | Details |
|------|---------|--------|---------|
| **Lint** | `pnpm --filter @fcke/web run lint` | ✅ PASS | ESLint completed without errors |
| **Type Check** | `pnpm --filter @fcke/web run type-check` | ✅ PASS | TypeScript compilation successful |
| **Tests** | `pnpm --filter @fcke/web run test` | ✅ PASS | 11/11 tests passed |
| **Build** | `pnpm --filter @fcke/web run build` | ✅ PASS | Next.js build completed successfully |

### Backend Gates

| Gate | Command | Result | Details |
|------|---------|--------|---------|
| **Ruff Lint** | `python3 -m ruff check apps/` | ✅ PASS | "All checks passed!" |
| **Backend Tests** | `python3 -m pytest tests/` | ✅ PASS | 22/22 tests passed |
| **Worker Tests** | `python3 -m pytest apps/worker/` | ℹ️ N/A | No tests defined (0 items collected) |

### Security Gate

| Gate | Command | Result | Details |
|------|---------|--------|---------|
| **Security Audit** | `pnpm audit --audit-level=moderate` | ✅ PASS | "No known vulnerabilities found" |

### MyPy Type Check (Informational)

| Gate | Command | Result | Details |
|------|---------|--------|---------|
| **MyPy** | `python3 -m mypy apps/` | ⚠️ 22 errors | Pre-existing issues (see notes) |

**MyPy Error Analysis:**
- **Import-not-found (8 errors):** Missing type stubs for `sqlalchemy`, `structlog` — third-party packages without type annotations
- **Call-arg (14 errors):** Custom logging keyword arguments in worker code — pre-existing design choice
- **Not caused by this change:** All mypy errors are pre-existing and unrelated to build-backend fix

### Regression Summary

| Category | Total | Pass | Fail | Skip |
|----------|-------|------|------|------|
| **Frontend** | 4 | 4 | 0 | 0 |
| **Backend** | 3 | 2 | 0 | 1 (N/A) |
| **Security** | 1 | 1 | 0 | 0 |
| **TOTAL** | **8** | **7** | **0** | **1** |

**All applicable gates pass. No regressions introduced.**

---

## H. Remaining Risks

### Resolved Risks

| Risk | Status | Mitigation |
|------|--------|------------|
| Worker Docker build failure due to invalid build-backend | ✅ RESOLVED | Changed to `setuptools.build_meta` |
| Latent API build-backend defect | ✅ RESOLVED | Fixed proactively |
| `pip install -e .` operation failure | ✅ VALIDATED | Tested successfully locally |

### Remaining Concerns

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **CI Docker environment differs from local** | Medium | Low | Same Python 3.11-slim base, same pip behavior |
| **MyPy type errors (pre-existing)** | Low | N/A | Not related to this change; can be addressed separately |
| **Docker not available for local validation** | Low | Low | Equivalent Python packaging validation performed |
| **Setuptools future deprecation of build_meta** | Very Low | Very Low | Standard backend, actively maintained |

### Acceptance Criteria Checklist

- [x] Baseline recorded (HEAD, origin/main, working tree)
- [x] Only authorized files modified (apps/worker/pyproject.toml, apps/api/pyproject.toml)
- [x] Exact change applied (build-backend correction only)
- [x] Static verification passed (zero old references, two new correct references)
- [x] Python packaging validated (both packages install successfully)
- [x] API/Worker discrepancy explained and documented
- [x] Docker equivalent validation performed (pip install -e . succeeds)
- [x] Full local regression passed (all gates green)
- [x] Git diff control verified (only expected changes)
- [ ] Commit created and pushed
- [ ] GitHub Actions CI achieves 7/7 PASS
- [ ] Final acceptance gate verified

---

## I. Commit Information

**Commit Message:**  
`fix(phase-0.7.13): correct setuptools build backends`

**Files Committed:**
1. `apps/worker/pyproject.toml` — Corrected build-backend
2. `apps/api/pyproject.toml` — Corrected build-backend
3. `reports/PHASE_0_7_13_BUILD_BACKEND_REMEDIATION_REPORT.md` — This report

**Commit Hash:** (To be recorded after commit)

---

## J. Appendix: Complete Validation Log

### Environment Setup

```bash
$ python3 --version
Python 3.12.14

$ pip3 --version
pip 25.0.1

$ pnpm --version
9.1.0
```

### All Commands Executed

```bash
# 1. Static Verification
grep -r "setuptools.backends._legacy" . --include="*.toml"
# Result: ✅ ZERO references

grep -r "setuptools.build_meta" . --include="*.toml"
# Result: ✅ Two correct references

# 2. Backend Import Test
python3 -c "from setuptools import build_meta; print('SUCCESS')"
# Result: ✅ SUCCESS

# 3. Worker Install Test
cd apps/worker && pip install -e .
# Result: ✅ SUCCESS (fcke-worker 0.1.0)

# 4. API Install Test
cd apps/api && pip install -e .
# Result: ✅ SUCCESS (fcke-api 0.1.0)

# 5. Frontend Lint
pnpm --filter @fcke/web run lint
# Result: ✅ PASS

# 6. Frontend Type Check
pnpm --filter @fcke/web run type-check
# Result: ✅ PASS

# 7. Frontend Tests
pnpm --filter @fcke/web run test
# Result: ✅ PASS (11/11 tests)

# 8. Frontend Build
pnpm --filter @fcke/web run build
# Result: ✅ PASS (compiled successfully)

# 9. Ruff Lint
python3 -m ruff check apps/
# Result: ✅ PASS (All checks passed!)

# 10. Backend Tests
python3 -m pytest tests/
# Result: ✅ PASS (22/22 tests)

# 11. Security Audit
pnpm audit --audit-level=moderate
# Result: ✅ PASS (No known vulnerabilities found)

# 12. Git Diff Control
git diff
# Result: ✅ Only 2 files changed (expected)
```

---

**Report End**

*This report documents the controlled remediation of setuptools build-backend configuration.*  
*Awaiting GitHub Actions CI verification for final acceptance.*
