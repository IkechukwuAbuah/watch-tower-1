# Hallucination Verification Protocol

## 🚨 **MANDATORY PROCESS FOR ALL EXTERNAL INTEGRATIONS**

**Date Created**: 2024-12-28  
**Trigger**: After discovering massive LocoNav implementation hallucination  
**Purpose**: Prevent claiming completion without actual validation against documentation

---

## 📋 **VERIFICATION CHECKLIST**

Before marking ANY external integration as "complete", **MUST** complete:

### Phase 1: Documentation Analysis
- [ ] **Read actual API documentation** (not assumptions)
- [ ] **Verify authentication method** matches docs exactly
- [ ] **Check all endpoint URLs** against official docs
- [ ] **Confirm required parameters** and data formats
- [ ] **Identify any missing dependencies** or setup steps

### Phase 2: Implementation Review
- [ ] **Compare code against docs** line by line
- [ ] **Verify environment variables** match documented requirements
- [ ] **Check service class methods** match actual API endpoints
- [ ] **Validate request/response formats** against docs
- [ ] **Confirm error handling** covers documented error codes

### Phase 3: Validation Testing
- [ ] **Test with real credentials** (not placeholders)
- [ ] **Verify actual API responses** match expected format
- [ ] **Test error scenarios** documented in API docs
- [ ] **Validate rate limiting** and timeout handling
- [ ] **Document what actually works vs what was claimed**

---

## 🔍 **KNOWN HALLUCINATION PATTERNS**

### Pattern 1: Wrong Authentication
**Example**: LocoNav API
- **Claimed**: API key + secret pattern
- **Reality**: Single user token only
- **Red Flag**: Multiple auth fields for simple APIs

### Pattern 2: Wrong URLs
**Example**: LocoNav base URL
- **Claimed**: `https://api.loconav.com`
- **Reality**: `https://api.a.loconav.com`
- **Red Flag**: URLs that "look right" but are subtly wrong

### Pattern 3: Non-existent Features
**Example**: LocoNav webhook secrets
- **Claimed**: HMAC signature validation
- **Reality**: Not documented anywhere
- **Red Flag**: Security features that seem "obvious" but aren't documented

### Pattern 4: Wrong API Versions
**Example**: OpenAI API usage
- **Suspected**: Using Chat Completions instead of claimed Responses API
- **Red Flag**: API method names that don't match current documentation

---

## 🛠 **VERIFICATION TOOLS**

### 1. Documentation Sources
```bash
# Always check official docs first
/docs/[service]/[service]-docs.md
https://[service].com/api/docs
```

### 2. Quick Test Scripts
```bash
# Create simple test for each service
scripts/verify_[service].py
- Test authentication
- Test basic endpoint
- Validate response format
```

### 3. Environment Validation
```bash
# Check env vars match docs
scripts/env_verification.py
- Compare .env against docs
- Flag unknown variables
- Validate formats
```

---

## 📊 **VERIFICATION STATUS TRACKING**

| Service | Status | Verified Against | Last Check | Issues Found |
|---------|--------|------------------|------------|--------------|
| LocoNav | ✅ VERIFIED | Official docs | 2024-12-28 | Auth method, URL, webhook secrets |
| OpenAI | ❌ CRITICAL ISSUES | Official docs | 2024-12-28 | **EVAL() VULNERABILITY**, Wrong API, False claims |
| Google Sheets | ❌ NEEDS VERIFICATION | Official docs | - | Auth method unknown |
| Slack | ✅ VERIFIED | Test results | 2024-12-28 | Working correctly |
| Supabase | ❌ NEEDS VERIFICATION | Official docs | - | Configuration unknown |

---

## 🚨 **CRITICAL ACTIONS BEFORE AI SERVICE**

### Immediate Priorities:
1. **OpenAI API Verification** - Check if using wrong API version
2. **Google Sheets Verification** - Validate auth and endpoint methods
3. **Supabase Verification** - Confirm database connection methods

### Process:
1. Read official docs for each service
2. Compare against current implementation
3. Document discrepancies
4. Fix hallucinated implementations
5. Test with real credentials
6. Update all claims to reflect reality

---

## 📝 **LESSON LEARNED**

**Root Cause**: Implementing based on "common patterns" instead of reading actual documentation

**Impact**: Services appear complete but fail with real credentials

**Prevention**: This verification protocol MUST be followed for every external integration

**Success Metric**: Real credentials work on first try after reading docs

---

## 🎯 **NEXT VERIFICATIONS**

### OpenAI Service (HIGH PRIORITY)
- Check if using Chat Completions vs Responses API
- Verify function calling implementation
- Validate security (eval() usage)

### Google Sheets Service (MEDIUM PRIORITY)  
- Verify authentication method
- Check API version and endpoints
- Validate data sync approach

### Supabase Service (LOW PRIORITY)
- Confirm async client usage
- Validate connection configuration
- Check real-time features

**Remember**: No service is "complete" until it passes this verification protocol with real credentials.