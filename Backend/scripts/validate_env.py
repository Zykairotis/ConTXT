#!/usr/bin/env python3
"""
Script to validate the environment configuration for the ConTXT document processing system.
This script checks if all required environment variables are set and validates their values.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import json
import re
from urllib.parse import urlparse

def colorize(text, color):
    """Add color to console output."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m",
        "bold": "\033[1m"
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def validate_api_key(key_name, key_value, check_pattern=True):
    """Validate an API key."""
    if not key_value or key_value.startswith("your_") or key_value == "":
        return False, f"{key_name} is not set"
    
    if check_pattern:
        # Check for common API key patterns
        patterns = {
            "XAI_API_KEY": r"^xai-[a-zA-Z0-9]+$",
            "OPENAI_API_KEY": r"^sk-[a-zA-Z0-9]+$",
            "ANTHROPIC_API_KEY": r"^sk-ant-[a-zA-Z0-9]+$",
            "PERPLEXITY_API_KEY": r"^pplx-[a-zA-Z0-9]+$"
        }
        if key_name in patterns and not re.match(patterns[key_name], key_value):
            return False, f"{key_name} does not match expected pattern"
    
    return True, None

def validate_url(url_str):
    """Validate a URL."""
    try:
        result = urlparse(url_str)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_json_array(json_str):
    """Validate a JSON array string."""
    try:
        data = json.loads(json_str)
        if isinstance(data, list):
            return True
        return False
    except:
        return False

def validate_env_config():
    """Validate the environment configuration."""
    load_dotenv()
    
    issues = []
    warnings = []
    
    # Required API keys (at least one must be set)
    api_keys = [
        "XAI_API_KEY", 
        "OPENAI_API_KEY", 
        "ANTHROPIC_API_KEY"
    ]
    
    # Check if at least one API key is set
    has_api_key = False
    for key in api_keys:
        is_valid, message = validate_api_key(key, os.getenv(key, ""))
        if is_valid:
            has_api_key = True
            break
    
    if not has_api_key:
        issues.append("At least one of these API keys must be set: XAI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY")
    
    # Check LLM configuration
    llm_provider = os.getenv("LLM_PROVIDER", "")
    if llm_provider:
        if llm_provider not in ["openai", "anthropic", "xai", "google"]:
            issues.append(f"LLM_PROVIDER value '{llm_provider}' is not supported")
        
        # Check if the corresponding API key is set
        if llm_provider == "openai" and not os.getenv("OPENAI_API_KEY", ""):
            issues.append("OPENAI_API_KEY is required when LLM_PROVIDER is set to 'openai'")
        elif llm_provider == "anthropic" and not os.getenv("ANTHROPIC_API_KEY", ""):
            issues.append("ANTHROPIC_API_KEY is required when LLM_PROVIDER is set to 'anthropic'")
        elif llm_provider == "xai" and not os.getenv("XAI_API_KEY", ""):
            issues.append("XAI_API_KEY is required when LLM_PROVIDER is set to 'xai'")
        elif llm_provider == "google" and not os.getenv("GOOGLE_API_KEY", ""):
            issues.append("GOOGLE_API_KEY is required when LLM_PROVIDER is set to 'google'")
    else:
        warnings.append("LLM_PROVIDER is not set, will use default")
    
    # Check database configurations
    neo4j_uri = os.getenv("NEO4J_URI", "")
    if not neo4j_uri:
        issues.append("NEO4J_URI is required")
    elif not neo4j_uri.startswith(("bolt://", "neo4j://", "neo4j+s://")):
        issues.append(f"NEO4J_URI value '{neo4j_uri}' does not have a valid protocol (bolt://, neo4j://, neo4j+s://)")
    
    vector_db_url = os.getenv("VECTOR_DB_URL", "")
    if not vector_db_url:
        issues.append("VECTOR_DB_URL is required")
    elif not validate_url(vector_db_url):
        issues.append(f"VECTOR_DB_URL value '{vector_db_url}' is not a valid URL")
    
    # Check environment configuration
    cors_origins = os.getenv("CORS_ORIGINS", "")
    if cors_origins and not validate_json_array(cors_origins):
        issues.append("CORS_ORIGINS must be a valid JSON array string, e.g., [\"http://localhost:3000\"]")
    
    # Check file paths
    upload_path = os.getenv("UPLOAD_PATH", "")
    if not upload_path:
        issues.append("UPLOAD_PATH is required")
    elif upload_path != "/app/uploads" and not Path(upload_path).exists():
        warnings.append(f"UPLOAD_PATH '{upload_path}' does not exist. It will need to be created.")
    
    # Check security settings
    secret_key = os.getenv("SECRET_KEY", "")
    if not secret_key:
        issues.append("SECRET_KEY is required")
    elif secret_key == "your-secret-key-here-make-it-long-and-random":
        issues.append("Default SECRET_KEY is being used. Generate a secure key.")
    elif len(secret_key) < 32:
        warnings.append("SECRET_KEY should be at least 32 characters long")
    
    # Detect environment inconsistencies
    if "localhost" in neo4j_uri and "neo4j:7687" in os.getenv("VECTOR_DB_URL", ""):
        warnings.append("Mixed environment configuration: NEO4J_URI uses localhost but VECTOR_DB_URL uses Docker service name")
    elif "neo4j:7687" in neo4j_uri and "localhost" in os.getenv("VECTOR_DB_URL", ""):
        warnings.append("Mixed environment configuration: NEO4J_URI uses Docker service name but VECTOR_DB_URL uses localhost")
    
    return issues, warnings

def main():
    """Run the validation."""
    print(colorize("=== ConTXT Environment Configuration Validator ===", "blue"))
    print()
    
    env_file = Path(".env")
    if not env_file.exists():
        print(colorize("Error: .env file not found!", "red"))
        print(colorize("Run ./scripts/setup_env.sh to create it.", "yellow"))
        sys.exit(1)
    
    issues, warnings = validate_env_config()
    
    # Print warnings
    if warnings:
        print(colorize("⚠️  Warnings:", "yellow"))
        for warning in warnings:
            print(f"  • {warning}")
        print()
    
    # Print issues
    if issues:
        print(colorize("❌ Configuration Issues:", "red"))
        for issue in issues:
            print(f"  • {issue}")
        print()
        print(colorize("Please fix these issues before starting the system.", "red"))
        sys.exit(1)
    else:
        # Print success message if no issues
        print(colorize("✅ Environment configuration is valid!", "green"))
        print()
        
        # Print detected environment
        if "localhost" in os.getenv("NEO4J_URI", ""):
            print(colorize("Environment: Local Development", "blue"))
        else:
            print(colorize("Environment: Docker", "blue"))
        
        print()
        print("Ready to start the system with:")
        print("  • ./scripts/docker_start.sh")

if __name__ == "__main__":
    main() 