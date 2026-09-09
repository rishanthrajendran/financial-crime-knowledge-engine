# Contributing to Financial Crime Knowledge Engine

Thank you for your interest in contributing! This document outlines the process and standards for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Development Setup](#development-setup)
- [Branch Strategy](#branch-strategy)
- [Commit Conventions](#commit-conventions)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Be respectful, inclusive, and professional in all interactions.

## Development Setup

### Prerequisites

- Node.js >= 18.0.0
- pnpm >= 8.0.0
- Python >= 3.11
- Docker & Docker Compose
- uv (recommended) or pip

### Initial Setup

```bash
# Clone and navigate
git clone <repository-url>
cd financial-crime-knowledge-engine

# Install JavaScript/TypeScript dependencies
pnpm install

# Set up environment
cp .env.example .env
# Edit .env with your local configuration

# Start infrastructure services
docker compose up -d

# Run database migrations (when API is ready)
cd apps/api && alembic upgrade head
```

## Branch Strategy

We use a simplified Git flow:

```
main           # Production-ready code (protected)
  └── develop  # Integration branch (default for PRs)
       ├── feature/*    # New features
       ├── fix/*        # Bug fixes
       ├── docs/*       # Documentation changes
       └── refactor/*   # Refactoring work
```

### Branch Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<description>` | `feature/knowledge-ingestion` |
| Bug Fix | `fix/<description>` | `fix/health-check-timeout` |
| Documentation | `docs/<description>` | `docs/api-endpoints` |
| Refactor | `refactor/<description>` | `refactor/database-session` |

## Commit Conventions

We use [Conventional Commits](https://www.conventionalcommits.org/):

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting, semicolons) |
| `refactor` | Code refactoring |
| `perf` | Performance improvements |
| `test` | Adding or updating tests |
| `chore` | Build process, tooling, dependencies |
| `ci` | CI/CD configuration changes |

### Scopes

Common scopes: `web`, `api`, `worker`, `db`, `docs`, `infra`, `test`

### Examples

```bash
feat(api): add knowledge document CRUD endpoints
fix(web): resolve health check timeout issue
docs(readme): update installation instructions
test(api): add integration tests for health endpoint
chore(deps): update fastapi to 0.104.0
```

## Pull Request Process

1. **Create a branch** from `develop`
2. **Make your changes** following coding standards
3. **Test thoroughly** - ensure all tests pass
4. **Update documentation** if needed
5. **Submit PR** to `develop` branch with:
   - Clear title using conventional commit format
   - Description of what and why
   - Links to related issues
   - Screenshots for UI changes
6. **Address review feedback** promptly
7. **Maintainer merges** after approval

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New code has appropriate test coverage
- [ ] Documentation is updated
- [ ] No secrets or sensitive data committed
- [ ] Commit messages follow conventions

## Coding Standards

### TypeScript / Frontend

- Use strict TypeScript mode
- Prefer functional patterns over classes
- Use existing shadcn/ui components
- Follow React best practices (hooks, memoization)
- Export types for public APIs

### Python / Backend

- Follow PEP 8 style guide
- Use type hints everywhere
- Use async/await for I/O operations
- Follow Pydantic v2 patterns
- Document complex logic with docstrings

### API Design

- Use RESTful conventions
- Return proper HTTP status codes
- Include meaningful error messages
- Version APIs with `/v1/` prefix
- Document with OpenAPI schema

## Testing Requirements

### Test Types

| Type | Location | Coverage Goal |
|------|----------|---------------|
| Unit tests | `apps/*/tests/` | >80% core logic |
| Integration tests | `tests/integration/` | Critical paths |
| E2E tests | `tests/e2e/` | User workflows |
| Security tests | `tests/security/` | Auth, injection, secrets |

### Running Tests

```bash
# Frontend tests
pnpm --filter @fcke/web test

# Backend tests
cd apps/api && pytest

# All tests
pnpm test

# With coverage
pnpm test:coverage
```

## Getting Help

- Open an issue for bugs or feature requests
- Tag issues with appropriate labels
- Ask questions in discussions (if enabled)

## Recognition

Contributors will be recognized in:
- RELEASE notes for significant contributions
- CONTRIBUTORS.md file (to be added)

---

Thank you for contributing to Financial Crime Knowledge Engine!
