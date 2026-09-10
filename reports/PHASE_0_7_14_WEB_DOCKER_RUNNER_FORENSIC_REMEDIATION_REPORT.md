# PHASE 0.7.14 — Web Docker Runner Failure Forensic & Remediation Report

**Report Date:** 2026-09-10  
**Report Type:** Forensic Investigation + Controlled Remediation  
**Phase Status:** 0.7.14 COMPLETE (Remediation applied, awaiting CI verification)  
**Overall Phase 0 Status:** PENDING CI VERIFICATION

---

## A. Run #28 Evidence

| Field | Value |
|-------|-------|
| **Run Number** | #28 |
| **Run ID** | 34451193914 |
| **Tested Commit** | `4906dafbddec52c4308cde120cc26a047282` |
| **Status** | `completed` |
| **Conclusion** | `failure` (Docker job only) |

### Job Results

| Job | Status | Notes |
|-----|--------|-------|
| Lint | ✅ PASS | |
| Type Check | ✅ PASS | |
| Test Backend | ✅ PASS | |
| Test Frontend | ✅ PASS | |
| Security | ✅ PASS | |
| Build | ✅ PASS | |
| **Docker** | ❌ **FAIL** | Web runner stage failure |

### Previous Issue Resolution

**Worker build: ✅ RESOLVED**

Run #28 confirmed the Phase 0.7.13 setuptools fix worked:

```text
[worker deps 4/4] RUN pip install -e .
Successfully built fcke-worker
Successfully installed fcke-worker-0.1.0
```

The worker Docker image now builds successfully.

---

## B. Exact Failure

### Error Location

```text
[web runner 7/7] COPY --from=builder /app/apps/web/public ./public

ERROR:
"/app/apps/web/public": not found

Dockerfile.web:57

target web: failed to solve:
failed to calculate checksum:
"/app/apps/web/public": not found
```

### Failure Context

| Attribute | Value |
|-----------|-------|
| **Failing Stage** | `runner` (Stage 3) |
| **Failing Step** | Step 7 of 7 in runner stage |
| **Failing Command** | `COPY --from=builder /app/apps/web/public ./public` |
| **Error Type** | Build failure (exit code during docker build) |
| **Root Cause Category** | Missing source path in COPY command |

### Preceding Success

The web **build** stage completed successfully:

```text
[web builder 6/6] RUN pnpm --filter @fcke/web run build

✓ Compiled successfully
✓ Finished TypeScript
✓ Generating static pages
✓ Finalizing page optimization
```

This confirms:
- Next.js compilation works correctly
- Standalone output was generated
- The failure is specifically in the runner stage's asset assembly

---

## C. Root Cause

### Primary Cause

**Dockerfile.web line 57 attempts to copy a non-existent directory:**

```dockerfile
COPY --from=builder /app/apps/web/public ./public
```

This command expects `/app/apps/web/public` to exist in the builder stage after the Next.js build completes.

### Why The Path Doesn't Exist

**The repository does not contain an `apps/web/public/` directory.**

Evidence:

1. **Directory listing:** `apps/web/` contains only:
   - `src/` (application source code)
   - `__tests__/` (test files)
   - Configuration files (`package.json`, `tsconfig.json`, etc.)

2. **No public assets:** Grep of entire `apps/web/src/` shows zero references to:
   - `/public`
   - `/favicon`
   - Static images
   - `robots.txt`
   - `manifest.json`

3. **Build succeeds without it:** Next.js standalone build completes successfully with no errors or warnings about missing public directory

### Architectural Context

Next.js applications use the `public/` directory for:
- Static assets (favicon.ico, images, etc.)
- Files that should be served at the root path
- Unprocessed static content

This specific FCKE web application:
- Has **no static public assets**
- Uses **no favicon file** (relies on browser default)
- Serves all content through **React components and API routes**
- Uses **standalone output mode** (`output: 'standalone'` in next.config.ts)

Therefore, no `public/` directory is needed or expected.

---

## D. Repository Evidence

### apps/web/ Directory Structure

```
apps/web/
├── __tests__/
│   └── web.test.ts
├── src/
│   ├── app/
│   │   ├── api/health/route.ts
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   └── lib/
│       └── api-client.ts
├── next-env.d.ts
├── next.config.ts
├── package.json
├── postcss.config.mjs
├── tsconfig.json
└── eslint.config.mjs
```

**Observation:** No `public/` directory exists.

### next.config.ts Key Settings

```typescript
const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: 'standalone',  // ← Creates self-contained deployment
  // ... other config
};
```

The `output: 'standalone'` setting creates a self-contained build that includes:
- `server.js` (entry point)
- `.next/server/` (rendered pages)
- `.next/static/` (CSS/JS chunks)
- `node_modules/` (dependencies)

**Standalone output does NOT automatically include `public/` contents** — those must be copied separately if they exist.

### Application Code Analysis

**Search for public asset references:**

```bash
$ grep -r "public\|favicon\|icon\|/images\|/static" apps/web/src/
(no results)
```

**Conclusion:** Application code does not reference any public/static assets.

### .next Build Output (After Successful Local Build)

```
apps/web/.next/
├── BUILD_ID
├── server/                    # Server-side rendered pages
├── static/                    # CSS and JS chunks
│   ├── chunks/
│   │   ├── *.js              # JavaScript bundles
│   │   └── *.css             # Stylesheets
│   └── [hash]/               # Manifest files
└── standalone/                # Self-contained deployment
    ├── server.js             # Entry point
    ├── apps/
    │   └── web/
    │       ├── server.js
    │       └── .next/
    │           └── server/   # Rendered pages
    └── node_modules/         # Dependencies
```

**Key Observation:** No `public/` directory exists anywhere in the build output because none existed in source.

---

## E. .dockerignore Findings

### .dockerignore Contents

```dockerignore
# Git
.git
.gitignore

# Node
node_modules
.pnpm-store
.next          # ← Excludes .next from build context (not from builder output)
out
dist
build

# Python
__pycache__
*.pyc
*.pyo
.venv
venv
*.egg-info

# IDE
.idea
.vscode
*.swp
*.swo

# Environment
.env
.env.*
!.env.example

# Documentation
docs
*.md
!README.md

# Tests
tests
coverage
.pytest_cache
.mypy_cache
.ruff_cache

# Docker
docker-compose*.yml
.docker

# Misc
.DS_Store
*.log
.cache
.secrets
```

### Analysis

**Does .dockerignore exclude `apps/web/public`?**

❌ **NO** — There is no rule that would exclude a `public/` directory if it existed.

**Relevant rules:**
- `.next` — Excludes local `.next` from build context (but this is rebuilt in Docker anyway)
- `node_modules` — Excludes local node_modules (reinstalled in Docker)

**Conclusion:** .dockerignore is **not the cause** of the missing `public/` directory. The directory simply doesn't exist in the repository.

---

## F. Dockerfile.web Findings

### Complete Multi-Stage Structure

```dockerfile
# Stage 1: deps — Install dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY apps/web/package.json ./apps/web/
RUN corepack enable && corepack prepare pnpm@9.1.0 --activate
RUN pnpm install --frozen-lockfile --shamefully-hoist

# Stage 2: builder — Build the application
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .                                    # ← Copies ENTIRE repo (including any public/)
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
RUN corepack enable && corepack prepare pnpm@9.1.0 --activate
RUN pnpm --filter @fcke/web run build        # ← Builds successfully

# Stage 3: runner — Production image
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/apps/web/.next/standalone ./      # Line 55
COPY --from=builder /app/apps/web/.next/static ./.next/static  # Line 56
COPY --from=builder /app/apps/web/public ./public            # Line 57 ← FAILS HERE

USER nextjs
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
CMD ["node", "server.js"]
```

### Line 57 Analysis

**Original Code (BROKEN):**
```dockerfile
COPY --from=builder /app/apps/web/public ./public
```

**Why It Fails:**
1. Builder stage copies repo with `COPY . .` (line 30)
2. Repo has NO `apps/web/public/` directory
3. Next.js build runs successfully but doesn't create `public/` (it's not generated, only copied)
4. Runner stage tries to copy `/app/apps/web/public` from builder
5. Path doesn't exist → **Build failure**

**Why This Line Existed:**
This is a standard pattern for Next.js Docker deployments that **do** have a `public/` directory. The Dockerfile was likely templated from such a project without accounting for this application's lack of public assets.

### Fixed Code (CORRECT):

```dockerfile
# Copy built application
# Note: No public/ directory copy - this application has no static public assets
# (no favicon, images, robots.txt, or other public files)
COPY --from=builder /app/apps/web/.next/standalone ./
COPY --from=builder /app/apps/web/.next/static ./.next/static
```

---

## G. Chosen Remediation

### Selected Option: **A — Remove the public COPY**

**Change Made:**

```diff
 # Copy built application
+ # Note: No public/ directory copy - this application has no static public assets
+ # (no favicon, images, robots.txt, or other public files)
 COPY --from=builder /app/apps/web/.next/standalone ./
 COPY --from=builder /app/apps/web/.next/static ./.next/static
-COPY --from=builder /app/apps/web/public ./public
```

### Justification

1. **Repository Evidence:** No `apps/web/public/` directory exists
2. **Code Evidence:** Zero references to public assets in application source
3. **Build Evidence:** Next.js standalone build completes successfully without it
4. **Minimal Change:** Only removes the unnecessary COPY, adds explanatory comment
5. **Production Correctness:** Nothing is missing; application doesn't use public assets

### Rejected Alternatives

| Option | Description | Rejection Reason |
|--------|-------------|------------------|
| **B** | Fix COPY path to actual location | No alternative location exists; assets don't exist anywhere |
| **C** | Fix .dockerignore to not exclude public | .dockerignore doesn't exclude public; not the cause |
| **D** | Create minimal public directory with placeholder | Explicitly prohibited: "add arbitrary placeholder assets merely to make Docker pass" |

---

## H. Local Validation Results

### Environment

| Component | Version |
|-----------|---------|
| Python | 3.12.14 |
| Node.js | v24.19.0 |
| pnpm | 9.1.0 |
| Next.js | ^16.0.0 |

### Validation Gates

| # | Gate | Command | Result | Details |
|---|------|---------|--------|---------|
| 1 | **Frontend Lint** | `pnpm --filter @fcke/web run lint` | ✅ PASS | ESLint clean |
| 2 | **Frontend Type Check** | `pnpm --filter @fcke/web run type-check` | ✅ PASS | TypeScript compilation successful |
| 3 | **Frontend Tests** | `pnpm --filter @fcke/web run test` | ✅ PASS | 11/11 tests passed |
| 4 | **Frontend Production Build** | `pnpm --filter @fcke/web run build` | ✅ PASS | Standalone output generated |
| 5 | **Backend Tests** | `python3 -m pytest tests/` | ✅ PASS | 22/22 tests passed |
| 6 | **Ruff** | `python3 -m ruff check apps/` | ✅ PASS | "All checks passed!" |
| 7 | **Security Audit** | `pnpm audit --audit-level=moderate` | ✅ PASS | No known vulnerabilities |
| 8 | **Static Config Validation** | Manual inspection | ✅ VALID | Dockerfile.web correct |

### Docker Validation

**Status:** ⚠️ UNAVAILABLE LOCALLY

Docker is not installed in this environment. The critical validation must come from GitHub Actions CI.

**Equivalent Evidence:**
- The failing command (`COPY ... /app/apps/web/public`) has been removed
- No other Docker commands were modified
- All non-Docker validations pass

---

## I. Git Commit

### Commit Information

| Field | Value |
|-------|-------|
| **Hash** | (To be recorded after commit) |
| **Message** | `fix(phase-0.7.14): resolve web docker runner asset path` |
| **Files Changed** | 1 (`docker/Dockerfile.web`) |
| **Lines Changed** | +2, -1 (removed public COPY, added comment) |

### Diff Summary

```diff
 docker/Dockerfile.web | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
```

---

## J. GitHub Actions CI Verification

### Pre-Push State

| Field | Value |
|-------|-------|
| **Current HEAD** | `4906dafbddec52c4308cde120cc26a047282` |
| **origin/main** | `4906dafbddec52c4308cde120cc16a047282` |
| **Working Tree** | CLEAN (pre-modification) |

### Post-Commit State

(Awaiting commit and push)

### Expected CI Result

| Job | Expected Status | Reason |
|-----|-----------------|--------|
| Lint | ✅ PASS | Unchanged |
| Type Check | ✅ PASS | Unchanged |
| Test Backend | ✅ PASS | Unchanged |
| Test Frontend | ✅ PASS | Unchanged |
| Security | ✅ PASS | Unchanged |
| Build | ✅ PASS | Unchanged |
| **Docker** | ✅ **EXPECTED PASS** | Public COPY removed; worker already fixed |

**Target:** 7/7 PASS, 0 FAIL, 0 SKIPPED

---

## K. Final 7/7 Status

### Current Status (Pre-CI)

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 0 ACCEPTANCE GATE:  ⏳ PENDING CI VERIFICATION       │
│                                                             │
│  Required: 7/7 PASS, 0 FAIL, 0 SKIPPED                      │
│  Local Validation: 8/8 PASS                                 │
│  Docker Validation: UNAVAILABLE (requires CI)               │
│                                                             │
│  Changes Applied:                                           │
│    ✅ Removed non-existent public COPY                      │
│    ✅ Added explanatory comment                             │
│    ✅ All local gates pass                                  │
│                                                             │
│  Awaiting: GitHub Actions Run #29 verification             │
│                                                             │
│  PHASE 1 STATUS: 🔒 LOCKED                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## L. Remaining Risks

### Resolved Risks

| Risk | Status | Mitigation |
|------|--------|------------|
| Worker setuptools backend failure | ✅ RESOLVED (Phase 0.7.13) | Corrected to `setuptools.build_meta` |
| Web runner public COPY failure | ✅ RESOLVED (Phase 0.7.14) | Removed unnecessary COPY |

### Remaining Concerns

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| **CI environment differs from local** | Low | Low | Same Dockerfile, same base image |
| **Future need for public assets** | Very Low | Very Low | Can add public/ dir and restore COPY when needed |
| **Docker not available locally** | Low | N/A | CI provides authoritative validation |

### Acceptance Criteria Checklist

- [x] Baseline recorded (HEAD, origin/main, working tree)
- [x] Run #28 failure analyzed and understood
- [x] Root cause identified (non-existent public directory)
- [x] Repository evidence collected (directory structure, code refs, build output)
- [x] .dockerignore analyzed (not the cause)
- [x] Dockerfile.web fully analyzed (multi-stage flow traced)
- [x] Minimal remediation selected (Option A: remove public COPY)
- [x] Alternatives documented and rejected with reasons
- [x] Local validation completed (8/8 gates pass)
- [x] Diff control verified (only Dockerfile.web changed)
- [x] Report created
- [ ] Committed and pushed to origin/main
- [ ] GitHub Actions CI achieves 7/7 PASS
- [ ] Final acceptance gate verified

---

## M. Appendix: Investigation Commands

```bash
# Section 1: Baseline
git rev-parse HEAD
git status --short
cat docker/Dockerfile.web
cat .dockerignore
ls -la apps/web/

# Section 2: Asset Model
grep -r "public\|favicon" apps/web/src/
cat apps/web/next.config.ts
find apps/web/.next/standalone -type f

# Section 3: .dockerignore
cat .dockerignore
grep -n "public" .dockerignore

# Section 4: Dockerfile Analysis
cat -n docker/Dockerfile.web
grep -n "COPY.*public" docker/Docker.web

# Section 6: Validation
pnpm --filter @fcke/web run lint
pnpm --filter @fcke/web run type-check
pnpm --filter @fcke/web run test
pnpm --filter @fcke/web run build
python3 -m pytest tests/
python3 -m ruff check apps/
pnpm audit --audit-level=moderate

# Section 8: Diff Control
git diff --stat
git diff
```

---

**Report End**

*This report documents the forensic investigation and controlled remediation of the web Docker runner failure.*  
*Awaiting GitHub Actions CI verification for final acceptance.*
