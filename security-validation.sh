#!/bin/bash

# Security Validation Script for Aether Platform
# This script validates that critical security vulnerabilities have been addressed

echo "🔒 AETHER PLATFORM SECURITY VALIDATION"
echo "======================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track results
PASSED=0
FAILED=0
WARNINGS=0

check_pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
    ((WARNINGS++))
}

check_info() {
    echo -e "${BLUE}ℹ️  INFO${NC}: $1"
}

echo "🚨 CRITICAL SECURITY CHECKS"
echo "============================"

# 1. Check for hardcoded secrets
echo
echo "1. Checking for hardcoded production secrets..."

if grep -q "aether_password" aether/docker-compose.yml; then
    check_fail "Hardcoded database password found in docker-compose.yml"
else
    check_pass "No hardcoded database passwords in docker-compose.yml"
fi

if grep -q "your-super-secret-key-change-in-production" aether/docker-compose.yml; then
    check_fail "Hardcoded secret key found in docker-compose.yml"
else
    check_pass "No hardcoded secret keys in docker-compose.yml"
fi

if grep -q "changeme" aether/backend/.env.example; then
    check_fail "Weak default password 'changeme' found in .env.example"
else
    check_pass "No weak default passwords in .env.example"
fi

# 2. Check database port exposure
echo
echo "2. Checking database port exposure..."

if grep -A 20 "postgres:" aether/docker-compose.yml | grep -v "^[[:space:]]*#" | grep -q "5432:5432"; then
    check_fail "PostgreSQL port exposed to host (security risk)"
else
    check_pass "PostgreSQL port not exposed to host"
fi

if grep -A 15 "redis:" aether/docker-compose.yml | grep -v "^[[:space:]]*#" | grep -q "6379:6379"; then
    check_fail "Redis port exposed to host (security risk)"
else
    check_pass "Redis port not exposed to host"
fi

# 3. Check container security
echo
echo "3. Checking container security features..."

if grep -q "security_opt:" aether/docker-compose.yml && grep -q "no-new-privileges:true" aether/docker-compose.yml; then
    check_pass "Container security options configured"
else
    check_fail "Missing container security options"
fi

if grep -q "cap_drop:" aether/docker-compose.yml && grep -q "ALL" aether/docker-compose.yml; then
    check_pass "Container capabilities properly dropped"
else
    check_fail "Container capabilities not properly restricted"
fi

# 4. Check JWT token expiration
echo
echo "4. Checking JWT token security..."

if grep -q "60 \* 24 \* 8" aether/backend/app/core/config.py; then
    check_fail "JWT token expiration too long (8 days)"
elif grep -q "60 \* 24" aether/backend/app/core/config.py; then
    check_pass "JWT token expiration set to 24 hours (secure)"
else
    check_warn "Could not verify JWT token expiration time"
fi

# 5. Check security headers
echo
echo "5. Checking security headers implementation..."

if grep -q "Content-Security-Policy" aether/backend/app/middleware/security.py; then
    check_pass "Content Security Policy header implemented"
else
    check_fail "Missing Content Security Policy header"
fi

if grep -q "X-Frame-Options.*DENY" aether/backend/app/middleware/security.py; then
    check_pass "X-Frame-Options header properly configured"
else
    check_fail "X-Frame-Options header missing or misconfigured"
fi

if grep -q "preload" aether/backend/app/middleware/security.py; then
    check_pass "HSTS preload configured"
else
    check_warn "HSTS preload not configured"
fi

# 6. Check HTTPS enforcement
echo
echo "6. Checking HTTPS enforcement..."

if grep -q "x-forwarded-proto" aether/backend/app/middleware/security.py; then
    check_pass "HTTPS enforcement implemented"
else
    check_fail "HTTPS enforcement not implemented"
fi

# 7. Check production configuration
echo
echo "7. Checking production configuration..."

if [ -f "aether/docker-compose.prod.yml" ]; then
    check_pass "Production docker-compose configuration exists"
    
    if grep -q "secrets:" aether/docker-compose.prod.yml; then
        check_pass "Docker secrets configured for production"
    else
        check_fail "Docker secrets not configured for production"
    fi
    
    if grep -q "aether-internal:" aether/docker-compose.prod.yml; then
        check_pass "Internal network configured for production"
    else
        check_fail "Internal network not configured for production"
    fi
else
    check_fail "Production docker-compose configuration missing"
fi

# 8. Check security documentation
echo
echo "8. Checking security documentation..."

if [ -f "aether/SECURITY.md" ]; then
    check_pass "Security documentation exists"
    
    if grep -q "Critical Security Checklist" aether/SECURITY.md; then
        check_pass "Security documentation contains deployment checklist"
    else
        check_warn "Security documentation missing deployment checklist"
    fi
else
    check_fail "Security documentation missing"
fi

# 9. Check input validation
echo
echo "9. Checking input validation..."

if grep -q "validate_input" aether/backend/app/core/security.py; then
    check_pass "Input validation functions implemented"
else
    check_fail "Input validation functions missing"
fi

if grep -q "sanitized_value = re.sub" aether/backend/app/core/security.py; then
    check_pass "Input sanitization implemented"
else
    check_fail "Input sanitization missing"
fi

# 10. Check authentication system
echo
echo "10. Checking authentication system..."

if grep -q "def authenticate_user" aether/backend/app/api/v1/endpoints/auth.py; then
    check_pass "User authentication system implemented"
else
    check_fail "User authentication system missing"
fi

if grep -q "bcrypt" aether/backend/app/core/security.py; then
    check_pass "Secure password hashing (bcrypt) implemented"
else
    check_fail "Secure password hashing missing"
fi

# Summary
echo
echo "📊 SECURITY VALIDATION SUMMARY"
echo "==============================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All critical security checks passed!${NC}"
    echo "The platform is ready for production deployment."
    exit 0
elif [ $FAILED -le 2 ]; then
    echo -e "${YELLOW}⚠️  Some security issues found but manageable.${NC}"
    echo "Review failed checks before production deployment."
    exit 1
else
    echo -e "${RED}🚨 Critical security issues found!${NC}"
    echo "DO NOT deploy to production until all issues are resolved."
    exit 2
fi