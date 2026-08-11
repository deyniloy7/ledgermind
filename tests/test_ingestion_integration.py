from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_upload_valid_pdf_returns_200():
    # Arrange and act
    response = client.post(
        "/api/v1/invoices/upload",
        files={"file": ("invoice.pdf", b"fake pdf content", "application/pdf")},
    )

    # Assert
    assert response.status_code == 200


def test_invalid_file_type_returns_415():
    # Arrange and act
    response = client.post(
        "/api/v1/invoices/upload",
        files={"file": ("invoice.jar", b"fake pdf content", "application/jar")},
    )

    # Assert
    assert response.status_code == 415
    body = response.json()
    assert body["error"] == "INVALID_FILE_TYPE"
    assert "invoice.jar" in body["message"]


def test_empty_file_returns_400():
    # Arrange and act
    response = client.post(
        "/api/v1/invoices/upload",
        files={"file": ("invoice.pdf", b"", "application/pdf")},
    )

    # Assert
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "EMPTY_FILE"
    assert "invoice.pdf" in body["message"]


def test_large_file_type_413():
    # Arrange and act
    response = client.post(
        "/api/v1/invoices/upload",
        files={"file": ("invoice.pdf", b"x" * (11 * 1024 * 1024), "application/pdf")},
    )

    # Assert
    assert response.status_code == 413
    body = response.json()
    assert body["error"] == "FILE_TOO_LARGE"
    assert "invoice.pdf" in body["message"]
