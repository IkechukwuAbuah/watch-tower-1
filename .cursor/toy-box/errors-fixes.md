# Watch Tower Implementation - Errors & Fixes

## Purpose
Document all encountered errors and their solutions to avoid repeating mistakes and build institutional knowledge.

## Format Template
```markdown
### Error: [Brief description]
**Date**: [timestamp]
**Context**: [What you were trying to do]
**Error**: [Exact error message or behavior]
**Root Cause**: [Why it happened]
**Solution**: [How you fixed it]
**Prevention**: [How to avoid in future]
**Related Files**: [Files affected]
```

---

## Documented Errors

<!-- Errors will be added here as encountered -->

### Example: Import Error for Geography Type
**Date**: [To be filled when encountered]
**Context**: Updating Truck model to use PostGIS geography type
**Error**: `NameError: name 'Geography' is not defined`
**Root Cause**: Missing import from geoalchemy2
**Solution**: Add `from geoalchemy2 import Geography` to imports
**Prevention**: Always check PostGIS type imports when using geography fields
**Related Files**: `backend/models/__init__.py`

---

## Common Patterns to Watch

### PostGIS Related
- [ ] Geography type imports
- [ ] SRID specification (4326 for WGS84)
- [ ] Index creation for spatial queries
- [ ] Extension enabling in database

### Async SQLAlchemy
- [ ] Using async session correctly
- [ ] Await on all database operations
- [ ] Proper connection handling
- [ ] Transaction management

### External API Integration
- [ ] Rate limiting implementation
- [ ] Retry logic with backoff
- [ ] Error response handling
- [ ] Timeout configuration

### Pydantic Validation
- [ ] Field type compatibility
- [ ] Custom validators
- [ ] Serialization issues
- [ ] Optional vs required fields

---

## Lessons Learned

<!-- Add key learnings here -->

1. **Always test migrations**: Run both upgrade and downgrade before committing
2. **Check API limits early**: External services have quotas we must respect
3. **Use type hints**: Helps catch errors before runtime
4. **Document assumptions**: What seems obvious today won't be tomorrow

---

## Prevention Checklist

Before implementing a feature:
- [ ] Check if similar error documented here
- [ ] Verify all imports needed
- [ ] Review API documentation for limits
- [ ] Plan error handling strategy
- [ ] Consider rollback approach

After fixing an error:
- [ ] Document it here immediately
- [ ] Update relevant code comments
- [ ] Add test to prevent regression
- [ ] Share learning with team 