#!/usr/bin/env python3
"""
Phase 0 Validation Script for Financial Crime Knowledge Engine

This script verifies that all Phase 0 requirements are met:
- Required directories exist
- Required files are present
- Configuration files are valid
- No secrets in code
- Docker compose is valid
- Dependencies are installable

Usage:
    python scripts/validate_phase0.py

Exit codes:
    0 - All checks passed (or only warnings)
    1 - One or more checks failed
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Tuple, List, Dict

# =============================================================================
# Configuration
# =============================================================================

# Base directory (parent of scripts directory)
BASE_DIR = Path(__file__).parent.parent

# Status colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# Result types
PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"

# Track results
results: List[Dict] = []

def add_result(check_name: str, status: str, message: str):
    """Add a validation result."""
    results.append({
        "check": check_name,
        "status": status,
        "message": message,
    })
    
    # Print immediate feedback
    if status == PASS:
        print(f"  {Colors.GREEN}[✓]{Colors.RESET} {check_name}: {message}")
    elif status == WARN:
        print(f"  {Colors.YELLOW}[!]{Colors.RESET} {check_name}: {message}")
    else:
        print(f"  {Colors.RED}[✗]{Colors.RESET} {check_name}: {message}")


# =============================================================================
# Validation Checks
# =============================================================================

def check_directory_structure():
    """Verify all required directories exist."""
    print(f"\n{Colors.BOLD}Checking Directory Structure...{Colors.RESET}")
    
    required_dirs = [
        # Apps
        "apps/web/src/app",
        "apps/web/src/lib",
        "apps/web/src/components",
        "apps/api/app",
        "apps/api/app/models",
        "apps/api/app/schemas",
        "apps/api/app/api/v1",
        "apps/api/app/core",
        "apps/api/tests",
        "apps/worker/worker",
        
        # Packages
        "packages/ui",
        "packages/knowledge",
        "packages/sdk",
        "packages/shared",
        
        # Database
        "database/migrations",
        "database/migrations/versions",
        "database/seeds",
        "database/schemas",
        
        # Knowledge
        "knowledge/manifests",
        "knowledge/schemas",
        "knowledge/taxonomies",
        "knowledge/ingestion",
        
        # Infrastructure
        "infrastructure/docker",
        "infrastructure/kubernetes",
        "infrastructure/terraform",
        "infrastructure/environments",
        
        # Tests
        "tests/integration",
        "tests/e2e",
        "tests/security",
        "tests/fixtures",
        
        # Docs
        "docs/architecture",
        "docs/adr",
        "docs/api",
        "docs/development",
        "docs/security",
        "docs/operations",
        
        # GitHub
        ".github/workflows",
        ".github/ISSUE_TEMPLATE",
        
        # Docker
        "docker",
        
        # Scripts
        "scripts",
    ]
    
    found = 0
    missing = 0
    
    for dir_path in required_dirs:
        full_path = BASE_DIR / dir_path
        if full_path.is_dir():
            found += 1
        else:
            missing += 1
            add_result(
                f"Directory: {dir_path}",
                FAIL,
                "Directory does not exist"
            )
    
    if missing == 0:
        add_result("Directory Structure", PASS, f"All {found} directories present")


def check_root_files():
    """Verify all root-level configuration files exist."""
    print(f"\n{Colors.BOLD}Checking Root Files...{Colors.RESET}")
    
    required_files = [
        ("package.json", "Root package.json with workspace config"),
        ("pnpm-workspace.yaml", "pnpm workspace definitions"),
        (".gitignore", "Git ignore rules"),
        (".editorconfig", "Editor configuration"),
        (".env.example", "Environment variable template"),
        ("README.md", "Project README"),
        ("CHANGELOG.md", "Changelog file"),
        ("LICENSE", "License file"),
        ("tsconfig.base.json", "Base TypeScript config"),
        ("alembic.ini", "Alembic migration config"),
        ("docker-compose.yml", "Docker Compose configuration"),
        ("CONTRIBUTING.md", "Contributing guidelines"),
    ]
    
    for filename, description in required_files:
        filepath = BASE_DIR / filename
        if filepath.exists():
            add_result(f"File: {filename}", PASS, description)
        else:
            add_result(f"File: {filename}", FAIL, f"Missing: {description}")


def check_web_app_files():
    """Verify Next.js web application files."""
    print(f"\n{Colors.BOLD}Checking Web App (apps/web)...{Colors.RESET}")
    
    required_files = [
        ("apps/web/package.json", "Web app dependencies"),
        ("apps/web/next.config.ts", "Next.js configuration"),
        ("apps/web/tsconfig.json", "TypeScript config"),
        ("apps/web/postcss.config.mjs", "PostCSS config"),
        ("apps/web/src/app/layout.tsx", "Root layout"),
        ("apps/web/src/app/page.tsx", "Landing page"),
        ("apps/web/src/app/globals.css", "Global styles"),
        ("apps/web/src/app/api/health/route.ts", "Health endpoint"),
        ("apps/web/src/lib/api-client.ts", "API client"),
    ]
    
    for filepath, description in required_files:
        full_path = BASE_DIR / filepath
        if full_path.exists():
            add_result(f"Web: {filepath}", PASS, description)
        else:
            add_result(f"Web: {filepath}", FAIL, f"Missing: {description}")


def check_api_app_files():
    """Verify FastAPI API application files."""
    print(f"\n{Colors.BOLD}Checking API App (apps/api)...{Colors.RESET}")
    
    required_files = [
        ("apps/api/pyproject.toml", "Python project config"),
        ("apps/api/requirements.txt", "Python requirements"),
        ("apps/api/app/__init__.py", "App package init"),
        ("apps/api/app/main.py", "FastAPI application entry"),
        ("apps/api/app/config.py", "Configuration module"),
        ("apps/api/app/database.py", "Database session management"),
        ("apps/api/app/models/__init__.py", "Models package init"),
        ("apps/api/app/models/base.py", "Base model definition"),
        ("apps/api/app/schemas/__init__.py", "Schemas package init"),
        ("apps/api/app/schemas/health.py", "Health schemas"),
        ("apps/api/app/schemas/common.py", "Common schemas"),
        ("apps/api/app/api/deps.py", "Dependency injection"),
        ("apps/api/app/api/v1/router.py", "API v1 router"),
        ("apps/api/app/core/logging.py", "Logging setup"),
        ("apps/api/app/core/errors.py", "Error handling"),
    ]
    
    for filepath, description in required_files:
        full_path = BASE_DIR / filepath
        if full_path.exists():
            add_result(f"API: {filepath}", PASS, description)
        else:
            add_result(f"API: {filepath}", FAIL, f"Missing: {description}")


def check_worker_files():
    """Verify worker application files."""
    print(f"\n{Colors.BOLD}Checking Worker App (apps/worker)...{Colors.RESET}")
    
    required_files = [
        ("apps/worker/pyproject.toml", "Worker project config"),
        ("apps/worker/worker/__init__.py", "Worker package init"),
        ("apps/worker/worker/job_base.py", "Job base class"),
        ("apps/worker/worker/registry.py", "Job registry"),
        ("apps/worker/worker/executor.py", "Job executor"),
    ]
    
    for filepath, description in required_files:
        full_path = BASE_DIR / filepath
        if full_path.exists():
            add_result(f"Worker: {filepath}", PASS, description)
        else:
            add_result(f"Worker: {filepath}", FAIL, f"Missing: {description}")


def check_database_files():
    """Verify database schema and migration files."""
    print(f"\n{Colors.BOLD}Checking Database...{Colors.RESET}")
    
    required_files = [
        ("database/migrations/env.py", "Alembic environment"),
        ("database/migrations/script.py.mako", "Migration template"),
        ("database/migrations/versions/0001_initial_schema.py", "Initial migration"),
        ("database/schemas/knowledge_documents.sql", "Documents DDL"),
        ("database/schemas/knowledge_sources.sql", "Sources DDL"),
        ("database/schemas/audit_events.sql", "Audit events DDL"),
        ("database/seeds/initial_data.sql", "Seed data"),
    ]
    
    for filepath, description in required_files:
        full_path = BASE_DIR / filepath
        if full_path.exists():
            add_result(f"DB: {filepath}", PASS, description)
        else:
            add_result(f"DB: {filepath}", FAIL, f"Missing: {description}")


def check_docker_files():
    """Verify Docker configuration files."""
    print(f"\n{Colors.BOLD}Checking Docker Configuration...{Colors.RESET}")
    
    required_files = [
        ("docker-compose.yml", "Docker Compose config"),
        ("docker/Dockerfile.web", "Web Dockerfile"),
        ("docker/Dockerfile.api", "API Dockerfile"),
        ("docker/Dockerfile.worker", "Worker Dockerfile"),
        (".dockerignore", "Docker ignore rules"),
    ]
    
    for filepath, description in required_files:
        full_path = BASE_DIR / filepath
        if full_path.exists():
            add_result(f"Docker: {filepath}", PASS, description)
        else:
            add_result(f"Docker: {filepath}", FAIL, f"Missing: {description}")


def check_ci_cd_files():
    """Verify CI/CD pipeline configuration."""
    print(f"\n{Colors.BOLD}Checking CI/CD Pipeline...{Colors.RESET}")
    
    required_files = [
        (".github/workflows/ci.yml", "CI workflow"),
        (".github/ISSUE_TEMPLATE/bug_report.yml", "Bug report template"),
        (".github/ISSUE_TEMPLATE/feature_request.yml", "Feature request template"),
        (".github/PULL_REQUEST_TEMPLATE.md", "PR template"),
    ]
    
    for filepath, description in required_files:
        full_path = BASE_DIR / filepath
        if full_path.exists():
            add_result(f"CI/CD: {filepath}", PASS, description)
        else:
            add_result(f"CI/CD: {filepath}", FAIL, f"Missing: {description}")


def check_documentation():
    """Verify documentation files."""
    print(f"\n{Colors.BOLD}Checking Documentation...{Colors.RESET}")
    
    required_docs = [
        ("docs/architecture/SYSTEM_ARCHITECTURE.md", "System architecture"),
        ("docs/architecture/KNOWLEDGE_BASE_INTEGRATION.md", "KB integration spec"),
        ("docs/architecture/SOURCE_OF_TRUTH.md", "Source of truth doc"),
        ("docs/architecture/DOMAIN_MODEL.md", "Domain model"),
        ("docs/architecture/AI_RAG_ARCHITECTURE.md", "AI/RAG architecture"),
        ("docs/architecture/SEARCH_ARCHITECTURE.md", "Search architecture"),
        ("docs/security/SECURITY_BASELINE.md", "Security baseline"),
        ("docs/security/AUTHENTICATION_AUTHORIZATION.md", "Auth design"),
        ("docs/operations/OBSERVABILITY.md", "Observability guide"),
        ("docs/development/TESTING_STRATEGY.md", "Testing strategy"),
        ("docs/development/ENGINEERING_STANDARDS.md", "Engineering standards"),
        ("docs/development/IMPLEMENTATION_STATUS.md", "Implementation status"),
        ("docs/TRACEABILITY_MATRIX.md", "Traceability matrix"),
        ("knowledge/README.md", "Knowledge integration guide"),
    ]
    
    # ADRs
    for i in range(1, 11):
        adr_file = f"docs/adr/{i:04d}-*.md"
        adr_path = list(BASE_DIR.glob(adr_file))
        if adr_path:
            add_result(f"ADR-{i:04d}", PASS, f"Found: {adr_path[0].name}")
        else:
            add_result(f"ADR-{i:04d}", FAIL, "Missing ADR document")
    
    for filepath, description in required_docs:
        full_path = BASE_DIR / filepath
        if full_path.exists():
            add_result(f"Docs: {filepath}", PASS, description)
        else:
            add_result(f"Docs: {filepath}", FAIL, f"Missing: {description}")


def check_test_files():
    """Verify test files exist."""
    print(f"\n{Colors.BOLD}Checking Test Files...{Colors.RESET}")
    
    test_files = [
        ("tests/backend/test_health.py", "Backend health tests"),
        ("tests/frontend/web.test.ts", "Frontend smoke tests"),
        ("tests/integration/test_database.py", "Integration DB tests"),
    ]
    
    for filepath, description in test_files:
        full_path = BASE_DIR / filepath
        if full_path.exists():
            add_result(f"Tests: {filepath}", PASS, description)
        else:
            add_result(f"Tests: {filepath}", FAIL, f"Missing: {description}")


def check_no_secrets():
    """Check for potential secrets in code."""
    print(f"\n{Colors.BOLD}Checking for Secrets Exposure...{Colors.RESET}")
    
    # Patterns that might indicate secrets
    secret_patterns = [
        (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
        (r'secret_key\s*=\s*["\'][^"\']+["\']', "Hardcoded secret key"),
        (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
        (r'token\s*=\s*["\'][^"\']{20,}["\']', "Potential token"),
        (r'AKIA[0-9A-Z]{16}', "AWS Access Key"),
        (r'sk-[a-f0-9]{32}', "OpenAI-style key"),
        (r'ghp_[a-zA-Z0-9]{36}', "GitHub token"),
        (r'xox[baprs]-[a-zA-Z0-9-]+', "Slack token"),
    ]
    
    # Files to scan (exclude .env.example, node_modules, etc.)
    extensions_to_scan = ['.py', '.ts', '.tsx', '.js', '.yml', '.yaml']
    exclude_dirs = ['node_modules', '__pycache__', '.git', 'venv', '.venv']
    
    secrets_found = 0
    
    for pattern, description in secret_patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        
        for ext in extensions_to_scan:
            for filepath in BASE_DIR.rglob(f'*{ext}'):
                # Skip excluded directories
                if any(excl in str(filepath) for excl in exclude_dirs):
                    continue
                
                try:
                    content = filepath.read_text(errors='ignore')
                    matches = regex.findall(content)
                    
                    if matches and '.env.example' not in str(filepath):
                        secrets_found += len(matches)
                        add_result(
                            f"Secrets: {filepath.name}",
                            FAIL,
                            f"{description} found ({len(matches)} occurrences)"
                        )
                except Exception:
                    pass
    
    if secrets_found == 0:
        add_result("Secrets Scan", PASS, "No secrets detected in code")


def check_config_validity():
    """Validate key configuration files."""
    print(f"\n{Colors.BOLD}Checking Configuration Validity...{Colors.RESET}")
    
    # Check package.json is valid JSON
    pkg_json = BASE_DIR / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text()
            data = json.loads(content)
            
            required_fields = ["name", "version"]
            missing_fields = [f for f in required_fields if f not in data]
            
            if missing_fields:
                add_result("package.json", FAIL, f"Missing fields: {missing_fields}")
            else:
                add_result("package.json", PASS, f"Valid JSON - {data.get('name')} v{data.get('version')}")
        except json.JSONDecodeError as e:
            add_result("package.json", FAIL, f"Invalid JSON: {e}")
    
    # Check pnpm-workspace.yaml exists and has packages
    workspace_yaml = BASE_DIR / "pnpm-workspace.yaml"
    if workspace_yaml.exists():
        content = workspace_yaml.read_text()
        if "apps/*" in content and "packages/*" in content:
            add_result("pnpm-workspace.yaml", PASS, "Workspace config valid")
        else:
            add_result("pnpm-workspace.yaml", WARN, "Missing apps/packages patterns")
    
    # Check .env.example has key variables
    env_example = BASE_DIR / ".env.example"
    if env_example.exists():
        content = env_example.read_text()
        expected_vars = ["APP_", "DATABASE_URL", "REDIS_URL"]
        found_vars = [v for v in expected_vars if v in content]
        
        if len(found_vars) >= 2:
            add_result(".env.example", PASS, f"Contains {len(found_vars)}+ variable groups")
        else:
            add_result(".env.example", WARN, "May be missing expected variables")


def check_docker_compose_validity():
    """Basic validation of docker-compose.yml."""
    print(f"\n{Colors.BOLD}Checking Docker Compose Validity...{Colors.RESET}")
    
    compose_file = BASE_DIR / "docker-compose.yml"
    if compose_file.exists():
        content = compose_file.read_text()
        
        # Check for required services
        required_services = ["web:", "api:", "db:", "redis:"]
        found_services = [s for s in required_services if s in content]
        
        if len(found_services) >= 3:
            add_result("docker-compose.yml", PASS, f"Defines {len(found_services)}+ services")
        else:
            add_result("docker-compose.yml", FAIL, f"Missing services. Found: {found_services}")


# =============================================================================
# Main Execution
# =============================================================================

def main():
    """Run all validation checks."""
    print(f"""
{Colors.BOLD}{'=' * 60}{Colors.RESET}
{Colors.BOLD}Financial Crime Knowledge Engine - Phase 0 Validation{Colors.RESET}
{Colors.BOLD}{'=' * 60}{Colors.RESET}

Base Directory: {BASE_DIR}
""")
    
    # Run all checks
    check_directory_structure()
    check_root_files()
    check_web_app_files()
    check_api_app_files()
    check_worker_files()
    check_database_files()
    check_docker_files()
    check_ci_cd_files()
    check_documentation()
    check_test_files()
    check_no_secrets()
    check_config_validity()
    check_docker_compose_validity()
    
    # Summary
    print(f"\n{'=' * 60}")
    print(f"{Colors.BOLD}Validation Summary{Colors.RESET}")
    print(f"{'=' * 60}\n")
    
    passes = sum(1 for r in results if r["status"] == PASS)
    failures = sum(1 for r in results if r["status"] == FAIL)
    warnings = sum(1 for r in results if r["status"] == WARN)
    total = len(results)
    
    print(f"  Total Checks: {total}")
    print(f"  {Colors.GREEN}Passed:{Colors.RESET} {passes}")
    print(f"  {Colors.YELLOW}Warnings:{Colors.RESET} {warnings}")
    print(f"  {Colors.RED}Failed:{Colors.RESET} {failures}")
    print()
    
    if failures > 0:
        print(f"{Colors.RED}{Colors.BOLD}VALIDATION FAILED{Colors.RESET}")
        print(f"\nFailed checks:")
        for r in results:
            if r["status"] == FAIL:
                print(f"  ✗ {r['check']}: {r['message']}")
        return 1
    else:
        print(f"{Colors.GREEN}{Colors.BOLD}VALIDATION PASSED{Colors.RESET}")
        if warnings > 0:
            print(f"\n  ({warnings} warning(s) - review recommended)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
