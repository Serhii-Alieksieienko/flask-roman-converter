import pytest
from main import app as flask_app
import converter


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class TestConverter:
    """Test the converter functions."""
    
    def test_number_to_roman_basic(self):
        """Test basic number to Roman conversion."""
        assert converter.number_to_roman(1) == "I"
        assert converter.number_to_roman(5) == "V"
        assert converter.number_to_roman(10) == "X"
        assert converter.number_to_roman(50) == "L"
        assert converter.number_to_roman(100) == "C"
        assert converter.number_to_roman(500) == "D"
        assert converter.number_to_roman(1000) == "M"
    
    def test_number_to_roman_complex(self):
        """Test complex number to Roman conversion."""
        assert converter.number_to_roman(4) == "IV"
        assert converter.number_to_roman(9) == "IX"
        assert converter.number_to_roman(40) == "XL"
        assert converter.number_to_roman(90) == "XC"
        assert converter.number_to_roman(400) == "CD"
        assert converter.number_to_roman(900) == "CM"
        assert converter.number_to_roman(1994) == "MCMXCIV"
        assert converter.number_to_roman(3999) == "MMMCMXCIX"
    
    def test_number_to_roman_invalid(self):
        """Test invalid inputs for number to Roman conversion."""
        with pytest.raises(ValueError):
            converter.number_to_roman(0)
        with pytest.raises(ValueError):
            converter.number_to_roman(4000)
        with pytest.raises(ValueError):
            converter.number_to_roman(-1)
    
    def test_roman_to_number_basic(self):
        """Test basic Roman to number conversion."""
        assert converter.roman_to_number("I") == 1
        assert converter.roman_to_number("V") == 5
        assert converter.roman_to_number("X") == 10
        assert converter.roman_to_number("L") == 50
        assert converter.roman_to_number("C") == 100
        assert converter.roman_to_number("D") == 500
        assert converter.roman_to_number("M") == 1000
    
    def test_roman_to_number_complex(self):
        """Test complex Roman to number conversion."""
        assert converter.roman_to_number("IV") == 4
        assert converter.roman_to_number("IX") == 9
        assert converter.roman_to_number("XL") == 40
        assert converter.roman_to_number("XC") == 90
        assert converter.roman_to_number("CD") == 400
        assert converter.roman_to_number("CM") == 900
        assert converter.roman_to_number("MCMXCIV") == 1994
        assert converter.roman_to_number("MMMCMXCIX") == 3999
    
    def test_roman_to_number_lowercase(self):
        """Test that lowercase input works."""
        assert converter.roman_to_number("mcmxciv") == 1994
    
    def test_roman_to_number_invalid(self):
        """Test invalid Roman numeral inputs."""
        with pytest.raises(ValueError):
            converter.roman_to_number("")
        with pytest.raises(ValueError):
            converter.roman_to_number("IIII")  # Invalid format
        with pytest.raises(ValueError):
            converter.roman_to_number("ABC")


class TestWebApp:
    """Test the Flask web application."""
    
    def test_home_page_get(self, client):
        """Test that a GET request to the home page is successful."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Roman Numeral Converter" in response.data
    
    def test_home_page_post_not_allowed(self, client):
        """Test that a POST request to the home page is not allowed."""
        response = client.post("/")
        assert response.status_code == 405
    
    def test_convert_number_to_roman(self, client):
        """Test converting number to Roman via web form."""
        response = client.post("/convert", data={
            "type": "to_roman",
            "number": "42"
        })
        assert response.status_code == 200
        assert b"XLII" in response.data
    
    def test_convert_roman_to_number(self, client):
        """Test converting Roman to number via web form."""
        response = client.post("/convert", data={
            "type": "to_number",
            "roman": "XLII"
        })
        assert response.status_code == 200
        assert b"42" in response.data
    
    def test_convert_invalid_number(self, client):
        """Test converting invalid number."""
        response = client.post("/convert", data={
            "type": "to_roman",
            "number": "5000"
        })
        assert response.status_code == 200
        assert b"must be an integer between 1 and 3999" in response.data
    
    def test_api_convert_number_to_roman(self, client):
        """Test API endpoint for number to Roman conversion."""
        response = client.post("/api/convert", 
                              json={"type": "to_roman", "value": 42})
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["result"] == "XLII"
    
    def test_api_convert_invalid(self, client):
        """Test API endpoint with invalid input."""
        response = client.post("/api/convert", 
                              json={"type": "to_roman", "value": 5000})
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"