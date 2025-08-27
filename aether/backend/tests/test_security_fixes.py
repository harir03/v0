"""
Test security fixes for critical vulnerabilities
"""
import pytest
from unittest.mock import patch
import os
import tempfile

def test_hardcoded_secrets_removed():
    """Test that hardcoded secrets are not present in config files"""
    
    # Check docker-compose.yml doesn't contain hardcoded secrets
    with open('/home/runner/work/v0/v0/aether/docker-compose.yml', 'r') as f:
        docker_compose_content = f.read()
    
    # Should not contain the old hardcoded password
    assert 'aether_password' not in docker_compose_content
    assert 'your-super-secret-key-change-in-production' not in docker_compose_content
    
    # Should use environment variables
    assert '${POSTGRES_PASSWORD' in docker_compose_content
    assert '${SECRET_KEY' in docker_compose_content

def test_database_port_not_exposed():
    """Test that database ports are not exposed to host"""
    
    with open('/home/runner/work/v0/v0/aether/docker-compose.yml', 'r') as f:
        docker_compose_content = f.read()
    
    # Database port should be commented out or not present
    lines = docker_compose_content.split('\n')
    postgres_section = False
    for line in lines:
        if 'postgres:' in line:
            postgres_section = True
        elif postgres_section and 'image:' in line:
            postgres_section = False
        elif postgres_section and '"5432:5432"' in line:
            # If the port is present, it should be commented out
            assert line.strip().startswith('#'), "PostgreSQL port should not be exposed to host"

def test_container_security_features():
    """Test that container security features are present"""
    
    with open('/home/runner/work/v0/v0/aether/docker-compose.yml', 'r') as f:
        docker_compose_content = f.read()
    
    # Should have security options
    assert 'security_opt:' in docker_compose_content
    assert 'no-new-privileges:true' in docker_compose_content
    assert 'cap_drop:' in docker_compose_content
    assert 'ALL' in docker_compose_content

def test_env_example_secure_defaults():
    """Test that .env.example has secure defaults"""
    
    with open('/home/runner/work/v0/v0/aether/backend/.env.example', 'r') as f:
        env_content = f.read()
    
    # Should not contain weak default passwords
    assert 'changeme' not in env_content
    assert 'aether_password' not in env_content
    assert 'your_super_secret_key_here' not in env_content
    
    # Should have secure-looking placeholders
    assert 'CHANGE_ME_IN_PRODUCTION' in env_content
    assert 'ACCESS_TOKEN_EXPIRE_MINUTES=1440' in env_content  # 24 hours, not 8 days

def test_production_compose_exists():
    """Test that production docker-compose file exists with enhanced security"""
    
    assert os.path.exists('/home/runner/work/v0/v0/aether/docker-compose.prod.yml')
    
    with open('/home/runner/work/v0/v0/aether/docker-compose.prod.yml', 'r') as f:
        prod_compose_content = f.read()
    
    # Should use Docker secrets
    assert 'secrets:' in prod_compose_content
    assert 'postgres_user' in prod_compose_content
    assert 'postgres_password' in prod_compose_content
    assert 'secret_key' in prod_compose_content
    
    # Should have internal networks
    assert 'networks:' in prod_compose_content
    assert 'aether-internal:' in prod_compose_content

def test_security_documentation_exists():
    """Test that security documentation is present"""
    
    assert os.path.exists('/home/runner/work/v0/v0/aether/SECURITY.md')
    
    with open('/home/runner/work/v0/v0/aether/SECURITY.md', 'r') as f:
        security_content = f.read()
    
    # Should contain critical security information
    assert 'Critical Security Checklist' in security_content
    assert 'MANDATORY CHANGES' in security_content
    assert 'Database Security' in security_content
    assert 'Container Security' in security_content

def test_token_expiration_reduced():
    """Test that JWT token expiration is set to 24 hours instead of 8 days"""
    
    # Check config.py
    with open('/home/runner/work/v0/v0/aether/backend/app/core/config.py', 'r') as f:
        config_content = f.read()
    
    # Should be 24 hours (60 * 24 = 1440 minutes)
    assert '60 * 24' in config_content
    assert '60 * 24 * 8' not in config_content

def test_https_enforcement_added():
    """Test that HTTPS enforcement is present in security middleware"""
    
    with open('/home/runner/work/v0/v0/aether/backend/app/middleware/security.py', 'r') as f:
        middleware_content = f.read()
    
    # Should have HTTPS enforcement
    assert 'x-forwarded-proto' in middleware_content
    assert 'https://' in middleware_content
    assert 'HTTP_301_MOVED_PERMANENTLY' in middleware_content

def test_enhanced_security_headers():
    """Test that enhanced security headers are present"""
    
    with open('/home/runner/work/v0/v0/aether/backend/app/middleware/security.py', 'r') as f:
        middleware_content = f.read()
    
    # Should have comprehensive security headers
    assert 'X-Content-Type-Options' in middleware_content
    assert 'X-Frame-Options' in middleware_content
    assert 'Content-Security-Policy' in middleware_content
    assert 'Permissions-Policy' in middleware_content
    assert 'preload' in middleware_content  # HSTS preload

def test_health_endpoint_minimal_disclosure():
    """Test that health endpoint doesn't leak sensitive information"""
    
    with open('/home/runner/work/v0/v0/aether/backend/main.py', 'r') as f:
        main_content = f.read()
    
    # Health endpoint should only return status
    assert '"status": "healthy"' in main_content
    # Should not contain service name that could help attackers
    assert '"service": "aether-agents-api"' not in main_content

if __name__ == "__main__":
    pytest.main([__file__, "-v"])