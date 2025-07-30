#!/usr/bin/env python3
"""
Simple test script to verify the configuration system works correctly.
"""

def test_config_import():
    """Test that the configuration can be imported successfully"""
    try:
        from app.config.settings import (
            OLLAMA_API_BASE, ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY,
            PREFERRED_PROVIDER, BIG_MODEL, SMALL_MODEL, MODEL_ALIAS_MAP,
            validate_configuration
        )
        print("✅ Configuration import successful")
        return True
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False

def test_validation():
    """Test the configuration validation function"""
    try:
        from app.config.settings import validate_configuration
        
        issues = validate_configuration()
        if issues:
            print("⚠️  Configuration validation found issues (expected without .env):")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def test_model_validation_import():
    """Test that the model validation can be imported"""
    try:
        from app.utils.model_validation import validate_and_map_model
        print("✅ Model validation import successful")
        return True
    except ImportError as e:
        print(f"❌ Model validation import failed: {e}")
        return False

def main():
    print("🧪 Testing Configuration System")
    print("=" * 40)
    
    # Test configuration import
    config_ok = test_config_import()
    
    # Test validation function
    validation_ok = test_validation()
    
    # Test model validation import
    model_validation_ok = test_model_validation_import()
    
    print("\n📊 Test Results:")
    print(f"Configuration Import: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"Validation Function: {'✅ PASS' if validation_ok else '❌ FAIL'}")
    print(f"Model Validation Import: {'✅ PASS' if model_validation_ok else '❌ FAIL'}")
    
    if all([config_ok, validation_ok, model_validation_ok]):
        print("\n🎉 All tests passed! Configuration system is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration setup.")

if __name__ == "__main__":
    main() 