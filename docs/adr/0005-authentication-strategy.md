# ADR-0005: Authentication Strategy

## Status

**Planned (Phase 1)** | 2024-01-XX

## Context

The FCKE platform will need authentication and authorization to:
- Protect sensitive financial crime data
- Enable user-specific features
- Support compliance audit requirements
- Control access to different system capabilities

**Note**: Phase 0 does NOT implement authentication. This ADR documents the planned approach.

## Decision (Planned)

### Authentication: JWT-based with OAuth2/OIDC

#### Flow
1. User authenticates via identity provider (IdP)
2. IdP returns authorization code
3. Backend exchanges code for tokens
4. Returns access + refresh token to client
5. Client includes access token in Authorization header

#### Token Structure
```json
{
  "sub": "user-id",
  "email": "user@example.com",
  "roles": ["analyst", "admin"],
  "exp": 1704067200,
  "iat": 1704063600
}
```

### Authorization: Role-Based Access Control (RBAC)

#### Planned Roles
| Role | Permissions |
|------|-------------|
| viewer | Read-only access to public content |
| analyst | Read/write assessments, search knowledge |
| admin | Full access, user management, configuration |
| system | Service account for worker processes |

## Alternatives Considered

### Option A: Session-based Auth
- Simpler implementation
- Server-side state
- Not ideal for API-first architecture
- Rejected

### Option B: API Keys Only
- Simple for service-to-service
- No user context
- Insufficient for user-facing app
- Rejected as primary method

### Option C: OAuth2/OIDC with JWT (CHOSEN)
- Industry standard
- Scalable, stateless
- Supports SSO integration
- Good security properties

## Consequences

### Positive
- Standards-compliant authentication
- Supports enterprise SSO (Okta, Azure AD, Keycloak)
- Stateless scaling for API
- Clear permission model

### Negative
- Token refresh complexity
- Need secure key management
- Additional infrastructure for IdP

## Implementation Timeline
- **Phase 0**: No auth (current state)
- **Phase 1**: Basic JWT auth, role setup
- **Phase 2+:**: OIDC integration, fine-grained permissions

## Related Decisions

- [ADR-0004: API Design Standards](0004-api-design.md)
- [ADR-0010: Observability Strategy](0010-observability-strategy.md)
