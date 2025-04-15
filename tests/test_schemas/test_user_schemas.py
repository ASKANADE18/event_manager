import pytest
from pydantic import ValidationError
from app.schemas.user_schemas import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    LoginRequest,
    UserRole
)
from uuid import uuid4


# Fixtures
@pytest.fixture
def user_base_data():
    return {
        "nickname": "john_doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe",
    }

@pytest.fixture
def user_response_data():
    return {
        "id": str(uuid4()),  # UUID as string
        "nickname": "john_doe",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile_pictures/john_doe.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe",
        "role": UserRole.AUTHENTICATED,
        "is_professional": True,
    }

@pytest.fixture
def user_update_data():
    return {
        "email": "updated.email@example.com",
        "bio": "Updated bio",
        "linkedin_profile_url": "https://linkedin.com/in/updated",
    }


# Test for UserBase
def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.nickname == user_base_data["nickname"]
    assert user.linkedin_profile_url == user_base_data["linkedin_profile_url"]
    assert user.github_profile_url == user_base_data["github_profile_url"]

def test_user_base_invalid_url(user_base_data):
    user_base_data["profile_picture_url"] = "invalid-url"
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)

# Test for UserResponse
def test_user_response_valid(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.role == UserRole.AUTHENTICATED
    assert user.is_professional is True

# Test for UserCreate
def test_user_create_valid(user_base_data):
    user_base_data["password"] = "StrongPassword123!"
    user = UserCreate(**user_base_data)
    assert user.password == "StrongPassword123!"

# Test for UserUpdate
def test_user_update_valid(user_update_data):
    user_update = UserUpdate(**user_update_data)
    assert user_update.email == user_update_data["email"]

def test_user_update_no_values():
    with pytest.raises(ValidationError) as exc_info:
        UserUpdate()
    assert "At least one field must be provided for the update" in str(exc_info.value)

# Test for Enum
def test_user_role_enum():
    assert UserRole.ANONYMOUS.value == "ANONYMOUS"
    assert UserRole.ADMIN.value == "ADMIN"

# URL Validation
@pytest.mark.parametrize("url", [
    "http://valid.com/profile.jpg",
    "https://valid.com/profile.png",
    None
])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url

@pytest.mark.parametrize("url", [
    "ftp://invalid.com/profile.jpg",
    "http//invalid",
    "https//invalid"
])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)
        