# NOVA API Specification

## Base URL
- Local Development: `http://127.0.0.1:8000`
- OpenAPI Specification: `http://127.0.0.1:8000/api/docs`

---

## Endpoints

### 1. Health Check
`GET /api/health`

Returns the operational status, version, privacy settings, and security policy state of NOVA backend.

#### Response Example (200 OK):
```json
{
  "status": "ok",
  "service": "NOVA Workspace Assistant",
  "version": "0.1.0",
  "privacy_mode": "offline-strict",
  "qualcomm_isolation": "isolated-fallback",
  "environment": "development",
  "timestamp": "2026-09-24T13:51:51Z",
  "security_policy": {
    "shell_execution_blocked": true,
    "tool_registry_enforced": true,
    "user_confirmation_required": true,
    "audit_logging_active": true
  }
}
```

---

### 2. Root Welcome Endpoint
`GET /`

Returns service metadata and links to OpenAPI documentation and health endpoints.
