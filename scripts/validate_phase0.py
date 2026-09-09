#!/usr/bin/env python3
"""Phase 0 Validation Script for Financial Crime Knowledge Engine."""

import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).parent.parent

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"

results: List[Dict] = []

def add_result(check_name: str, status: str, message: str):
    results.append({"check": check_name, "status": status, "message": message})
    if status == PASS:
        print(f"  [✓] {check_name}: {message}")
    elif status == WARN:
        print(f"  [!] {check_name}: {message}")
    else:
        print(f"  [✗] {check_name}: {message}")

def check_directory_structure():
    print(f"\n{Colors.BOLD}Checking Directory Structure (Phase 0)...{Colors.RESET}")
    
    required_dirs = [
        "apps/web/src/app",
        "apps/web/src/lib",
        "apps/api/app",
        "apps/api/app/models",
        "apps/api/app/schemas",
        "apps/api/app/api/v1",
        "apps/api/app/core",
        "apps/worker/worker",
        "database/migrations",
        "database/migrations/versions",
        "database/seeds",
        "database/schemas",
        "docs/architecture",
        "docs/adr",
        "docs/security",
        "docs/development",
        "docs/operations",
        ".github/workflows",
        "docker",
        "scripts",
        "apps/web/__tests__",
    ]
    
    found = 0
    missing = 0
    
    for dir_path in required_dirs:
        full_path = BASE_DIR / dir_path
        if full_path.is_dir():
            found += 1
        else:
            missing += 1
            add_result(f"Directory: {dir_path}", FAIL, "Directory does not exist")
    
    if missing == 0:
        add_result("Directory Structure", PASS, f"All {found} Phase 0 directories present")

def check_root_files():
    print(f"\n{Colors.BOLD}Checking Root Files...{Colors.RESET}")
    
    required_files = [
        ("package.json", "Root package.json"),
        ("pnpm-workspace.yaml", "pnpm workspace"),
        (".gitignore", "Git ignore"),
        (".env.example", "Env template"),
        ("README.md", "README"),
        ("LICENSE", "License"),
        ("alembic.ini", "Alembic config"),
        ("docker-compose.yml", "Docker Compose"),
        ("CONTRIBUTING.md", "Contributing"),
    ]
    
    for filename, desc in required_files:
        if (BASE_DIR / filename).exists():
            add_result(f"File: {filename}", PASS, desc)
        else:
            add_result(f"File: {filename}", FAIL, f"Missing: {desc}")

def check_web_app():
    print(f"\n{Colors.BOLD}Checking Web App...{Colors.RESET}")
    
    files = [
        ("apps/web/package.json", "Dependencies"),
        ("apps/web/next.config.ts", "Next.js config"),
        ("apps/web/tsconfig.json", "TypeScript config"),
        ("apps/web/postcss.config.mjs", "PostCSS config"),
        ("apps/web/eslint.config.mjs", "ESLint config"),
        ("apps/web/src/app/layout.tsx", "Root layout"),
        ("apps/web/src/app/page.tsx", "Landing page"),
        ("apps/web/src/app/globals.css", "Global styles"),
        ("apps/web/src/app/api/health/route.ts", "Health endpoint"),
        ("apps/web/src/lib/api-client.ts", "API client"),
        ("apps/web/__tests__/web.test.ts", "Tests"),
    ]
    
    for fp, desc in files:
        if (BASE_DIR / fp).exists():
            add_result(f"Web: {fp}", PASS, desc)
        else:
            add_result(f"Web: {fp}", FAIL, f"Missing: {desc}")

def check_api_app():
    print(f"\n{Colors.BOLD}Checking API App...{Colors.RESET}")
    
    files = [
        ("apps/api/pyproject.toml", "Project config"),
        ("apps/api/requirements.txt", "Requirements"),
        ("apps/api/app/__init__.py", "App init"),
        ("apps/api/app/main.py", "FastAPI app"),
        ("apps/api/app/config.py", "Config"),
        ("apps/api/app/database.py", "Database"),
        ("apps/api/app/models/__init__.py", "Models init"),
        ("apps/api/app/models/base.py", "Base model"),
        ("apps/api/app/schemas/__init__.py", "Schemas init"),
        ("apps/api/app/schemas/health.py", "Health schema"),
        ("apps/api/app/schemas/common.py", "Common schema"),
        ("apps/api/app/api/deps.py", "Deps"),
        ("apps/api/app/api/v1/router.py", "Router"),
        ("apps/api/app/api/v1/__init__.py", "V1 init"),
        ("apps/api/app/core/logging.py", "Logging"),
        ("apps/api/app/core/errors.py", "Errors"),
    ]
    
    for fp, desc in files:
        if (BASE_DIR / fp).exists():
            add_result(f"API: {fp}", PASS, desc)
        else:
            add_result(f"API: {fp}", FAIL, f"Missing: {desc}")

def check_worker():
    print(f"\n{Colors.BOLD}Checking Worker...{Colors.RESET}")
    
    files = [
        ("apps/worker/pyproject.toml", "Config"),
        ("apps/worker/worker/__init__.py", "Init"),
        ("apps/worker/worker/job_base.py", "Job base"),
        ("apps/worker/worker/registry.py", "Registry"),
        ("apps/worker/worker/executor.py", "Executor"),
    ]
    
    for fp, desc in files:
        if (BASE_DIR / fp).exists():
            add_result(f"Worker: {fp}", PASS, desc)
        else:
            add_result(f"Worker: {fp}", FAIL, f"Missing: {desc}")

def check_database():
    print(f"\n{Colors.BOLD}Checking Database...{Colors.RESET}")
    
    files = [
        ("database/migrations/env.py", "Alembic env"),
        ("database/migrations/script.py.mako", "Template"),
        ("database/migrations/versions/0001_initial_schema.py", "Migration"),
        ("database/schemas/knowledge_documents.sql", "Docs DDL"),
        ("database/schemas/knowledge_sources.sql", "Sources DDL"),
        ("database/schemas/audit_events.sql", "Audit DDL"),
        ("database/seeds/initial_data.sql", "Seed data"),
    ]
    
    for fp, desc in files:
        if (BASE_DIR / fp).exists():
            add_result(f"DB: {fp}", PASS, desc)
        else:
            add_result(f"DB: {fp}", FAIL, f"Missing: {desc}")

def check_docker():
    print(f"\n{Colors.BOLD}Checking Docker...{Colors.RESET}")
    
    files = [
        ("docker-compose.yml", "Compose"),
        ("docker/Dockerfile.web", "Web Dockerfile"),
        ("docker/Dockerfile.api", "API Dockerfile"),
        ("docker/Dockerfile.worker", "Worker Dockerfile"),
    ]
    
    for fp, desc in files:
        if (BASE_DIR / fp).exists():
            add_result(f"Docker: {fp}", PASS, desc)
        else:
            add_result(f"Docker: {fp}", FAIL, f"Missing: {desc}")

def check_ci():
    print(f"\n{Colors.BOLD}Checking CI/CD...{Colors.RESET}")
    
    if (BASE_DIR / ".github/workflows/ci.yml").exists():
        add_result("CI Workflow", PASS, "ci.yml exists")
    else:
        add_result("CI Workflow", FAIL, "ci.yml missing")

def check_docs():
    print(f"\n{Colors.BOLD}Checking Docs...{Colors.RESET}")
    
    docs = [
        "docs/architecture/SYSTEM_ARCHITECTURE.md",
        "docs/architecture/DOMAIN_MODEL.md",
        "docs/security/SECURITY_BASELINE.md",
        "docs/development/TESTING_STRATEGY.md",
        "CHANGELOG.md",
    ]
    
    for doc in docs:
        if (BASE_DIR / doc).exists():
            add_result(f"Doc: {doc}", PASS, "Exists")
        else:
            add_result(f"Doc: {doc}", WARN, "Missing (recommended)")

def check_secrets():
    print(f"\n{Colors.BOLD}Checking Secrets...{Colors.RESET}")
    
    patterns = [
        (r"password\s*=\s*[\"'][^\"']+[\"']", "Password"),
        (r"secret_key\s*=\s*[\"'][^\"']+[\"']", "Secret key"),
        (r"AKIA[0-9A-Z]{16}", "AWS Key"),
        (r"sk-[a-f0-9]{32}", "OpenAI key"),
    ]
    
    found = 0
    for pattern, desc in patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        for fp in BASE_DIR.rglob("*.{py,ts,tsx,js,yml,yaml}"):
            if any(x in str(fp) for x in ["node_modules", "__pycache__", ".git", "venv", "skills"]):
                continue
            try:
                content = fp.read_text(errors="ignore")
                if regex.search(content) and ".env.example" not in str(fp):
                    found += 1
                    add_result(f"Secret: {fp.name}", FAIL, f"{desc} found")
            except:
                pass
    
    if found == 0:
        add_result("Secrets Scan", PASS, "No secrets found")

def check_config():
    print(f"\n{Colors.BOLD}Checking Config...{Colors.RESET}")
    
    pkg = BASE_DIR / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text())
            add_result("package.json", PASS, f"Valid - {data.get('name')}")
        except:
            add_result("package.json", FAIL, "Invalid JSON")

def main():
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}FCKE - Phase 0 Validation{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    print(f"Base: {BASE_DIR}\n")
    
    check_directory_structure()
    check_root_files()
    check_web_app()
    check_api_app()
    check_worker()
    check_database()
    check_docker()
    check_ci()
    check_docs()
    check_secrets()
    check_config()
    
    print(f"\n{'='*60}")
    print(f"{Colors.BOLD}Summary{Colors.RESET}")
    print(f"{'='*60}\n")
    
    passes = sum(1 for r in results if r["status"] == PASS)
    fails = sum(1 for r in results if r["status"] == FAIL)
    warns = sum(1 for r in results if r["status"] == WARN)
    
    print(f"  Total: {len(results)}")
    print(f"  {Colors.GREEN}Passed:{Colors.RESET} {passes}")
    print(f"  {Colors.YELLOW}Warnings:{Colors.RESET} {warns}")
    print(f"  {Colors.RED}Failed:{Colors.RESET} {fails}\n")
    
    if fails > 0:
        print(f"{Colors.RED}{Colors.BOLD}FAILED{Colors.RESET}")
        return 1
    else:
        print(f"{Colors.GREEN}{Colors.BOLD}PASSED{Colors.RESET}")
        return 0

if __name__ == "__main__":
    sys.exit(main())
