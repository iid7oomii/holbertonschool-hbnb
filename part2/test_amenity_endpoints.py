"""
Test script for Amenity endpoints
Run this after starting the Flask server with: python run.py
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/v1/amenities"


def test_create_amenity():
    """Test creating a new amenity"""
    print("\n=== Testing POST /api/v1/amenities/ ===")
    amenity_data = {
        "name": "WiFi"
    }

    response = requests.post(BASE_URL + "/", json=amenity_data)
    print(f"Status: {response.status_code}")
    print(
        f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

    if response.status_code == 201:
        return response.json()['id']
    return None


def test_create_multiple_amenities():
    """Test creating multiple amenities"""
    print("\n=== Creating multiple amenities ===")
    amenities = ["مسبح", "موقف سيارات", "مطبخ", "تكييف"]
    ids = []

    for amenity_name in amenities:
        amenity_data = {"name": amenity_name}
        response = requests.post(BASE_URL + "/", json=amenity_data)
        print(f"Creating '{amenity_name}': Status {response.status_code}")
        if response.status_code == 201:
            ids.append(response.json()['id'])

    return ids


def test_get_all_amenities():
    """Test getting all amenities"""
    print("\n=== Testing GET /api/v1/amenities/ ===")
    response = requests.get(BASE_URL + "/")
    print(f"Status: {response.status_code}")
    print(
        f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print(f"Total amenities: {len(response.json())}")


def test_get_amenity(amenity_id):
    """Test getting a specific amenity"""
    print(f"\n=== Testing GET /api/v1/amenities/{amenity_id} ===")
    response = requests.get(f"{BASE_URL}/{amenity_id}")
    print(f"Status: {response.status_code}")
    print(
        f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_update_amenity(amenity_id):
    """Test updating an amenity"""
    print(f"\n=== Testing PUT /api/v1/amenities/{amenity_id} ===")
    update_data = {
        "name": "WiFi سريع"
    }

    response = requests.put(f"{BASE_URL}/{amenity_id}", json=update_data)
    print(f"Status: {response.status_code}")
    print(
        f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_duplicate_name():
    """Test creating amenity with duplicate name"""
    print("\n=== Testing duplicate name (should fail) ===")
    amenity_data = {
        "name": "WiFi"  # Already exists
    }

    response = requests.post(BASE_URL + "/", json=amenity_data)
    print(f"Status: {response.status_code}")
    print(
        f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_invalid_name():
    """Test creating amenity with invalid name"""
    print("\n=== Testing invalid name (empty string, should fail) ===")
    amenity_data = {
        "name": ""
    }

    response = requests.post(BASE_URL + "/", json=amenity_data)
    print(f"Status: {response.status_code}")
    print(
        f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_name_too_long():
    """Test creating amenity with name exceeding max length"""
    print("\n=== Testing name too long (should fail) ===")
    amenity_data = {
        "name": "A" * 51  # 51 characters (max is 50)
    }

    response = requests.post(BASE_URL + "/", json=amenity_data)
    print(f"Status: {response.status_code}")
    print(
        f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def test_update_to_existing_name():
    """Test updating amenity to a name that already exists"""
    print("\n=== Testing update to existing name (should fail) ===")
    # First create two amenities
    amenity1 = {"name": "جيم"}
    amenity2 = {"name": "ساونا"}

    r1 = requests.post(BASE_URL + "/", json=amenity1)
    r2 = requests.post(BASE_URL + "/", json=amenity2)

    if r1.status_code == 201 and r2.status_code == 201:
        amenity1_id = r1.json()['id']
        # Try to update amenity1 to have the same name as amenity2
        response = requests.put(
            f"{BASE_URL}/{amenity1_id}", json={"name": "ساونا"})
        print(f"Status: {response.status_code}")
        print(
            f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("بدء اختبار Amenity Endpoints")
    print("=" * 60)

    try:
        # Create first amenity
        amenity_id = test_create_amenity()

        if amenity_id:
            # Get specific amenity
            test_get_amenity(amenity_id)

            # Update amenity
            test_update_amenity(amenity_id)

            # Get updated amenity
            test_get_amenity(amenity_id)

        # Create multiple amenities
        test_create_multiple_amenities()

        # Get all amenities
        test_get_all_amenities()

        # Test error cases
        test_duplicate_name()
        test_invalid_name()
        test_name_too_long()
        test_update_to_existing_name()

        print("\n" + "=" * 60)
        print("✅ اكتملت جميع الاختبارات")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ خطأ: لا يمكن الاتصال بالخادم")
        print("تأكد من تشغيل الخادم باستخدام: python run.py")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")


if __name__ == "__main__":
    run_all_tests()
