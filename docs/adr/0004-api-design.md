# ADR-0004: API Design Standards

## Status

**Accepted** | 2024-01-XX

## Context

We need to establish consistent API design standards for the FCKE platform that will guide all endpoint development.

## Decision

### RESTful API Conventions

#### URL Structure
```
Base: https://api.fcke.example.com/v1
```

| Pattern | Example | Description |
|---------|---------|-------------|
| Collection GET | `/v1/documents` | List with pagination |
| Single GET | `/v1/documents/{id}` | Get by ID |
| Create POST | `/v1/documents` | Create new resource |
| Update PUT | `/v1/documents/{id}` | Full update |
| Patch PATCH | `/v1/documents/{id}` | Partial update |
| Delete DELETE | `/v1/documents/{id}` | Soft delete |

#### Response Format
```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "has_next": true,
    "has_prev": false
  }
}
```

#### Error Response
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Document not found",
    "details": { ... }
  },
  "status": 404
}
```

### HTTP Status Codes
| Code | Usage |
|------|-------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (created) |
| 204 | Successful DELETE |
| 400 | Validation error |
| 401 | Not authenticated |
| 403 | Forbidden (authenticated but not authorized) |
| 404 | Resource not found |
| 409 | Conflict (duplicate) |
| 422 | Unprocessable entity |
| 429 | Rate limited |
| 500 | Internal server error |
| 502 | Bad gateway (upstream failure) |
| 503 | Service unavailable |

### Pagination
- Default page_size: 20
- Maximum page_size: 100
- Zero-indexed or one-indexed pages (choose one consistently)
- Include pagination metadata in response

## Alternatives Considered

### Option A: REST (CHOSEN)
- Industry standard, well-understood
- Good caching support
- Simple client implementation

### Option B: GraphQL
- Flexible queries
- Over-fetching/under-fetching control
- More complex setup and security considerations
- Rejected for Phase 0 - can add later via Apollo Federation

## Consequences

### Positive
- Consistent, predictable API
- Easy to document with OpenAPI/Swagger
- Good tooling ecosystem
- Standard patterns developers know

### Negative
- May need multiple requests for related data
- Versioning strategy needed for breaking changes

## Related Decisions

- [ADR-0005: Authentication Strategy](0005-authentication-strategy.md)
- [ADR-0006: Error Handling Approach](0006-error-handling.md)
