import sys
import fitz
import requests
from PIL import Image
from pyzbar.pyzbar import decode
from urllib.parse import urlparse
from io import BytesIO

API_BASE = "https://api.myinvois.hasil.gov.my/admin/api/v1/public/documents"


def extract_qr_urls_from_pdf(pdf_path):
    urls = []
    doc = fitz.open(pdf_path)

    for page in doc:
        images = page.get_images(full=True)
        for img in images:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            img_pil = Image.open(BytesIO(image_bytes))
            decoded = decode(img_pil)

            for qr in decoded:
                urls.append(qr.data.decode("utf-8"))

    return urls


def extract_api_path(url):
    return urlparse(url).path


def fetch_json(api_path):
    url = f"{API_BASE}{api_path}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def extract_fields(data):
    return {
        "buyerName": data.get("buyerName"),
        "buyerTin": data.get("buyerTin"),
        "supplierName": data.get("supplierName"),
        "supplierTin": data.get("supplierTin"),
        "totalPayableAmount": data.get("totalPayableAmount"),
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: extract <pdf_file>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    qr_urls = extract_qr_urls_from_pdf(pdf_path)
    if not qr_urls:
        print("No QR code found")
        sys.exit(2)

    for url in qr_urls:
        api_path = extract_api_path(url)
        data = fetch_json(api_path)
        result = extract_fields(data)
        print(result)


if __name__ == "__main__":
    main()
