import csv
import tempfile
import unittest
from pathlib import Path

from import_catalog import COLUMNS, CatalogError, generated_javascript, inject_script_tag, load_catalog


class CatalogImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.assets = self.root / "assets"
        (self.assets / "products").mkdir(parents=True)
        self.csv_path = self.root / "products.csv"

    def tearDown(self):
        self.temp.cleanup()

    def row(self, **changes):
        item = {
            "اسم المنتج": "اسم مورد أصلي",
            "الكود": "MS-001",
            "القسم": "الملابس الكاجوال",
            "السعر": "",
            "الوصف": "",
            "المقاس": "M",
            "رابط أو اسم صورة المنتج": "sample.jpg",
        }
        item.update(changes)
        return item

    def write_csv(self, rows):
        with self.csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    def test_empty_template_has_no_products(self):
        self.write_csv([])
        self.assertEqual(load_catalog(self.csv_path, self.assets), [])
        self.assertIn("window.DAR_MARAM_PRODUCTS = [];", generated_javascript([]))

    def test_valid_original_local_image(self):
        (self.assets / "products" / "sample.jpg").write_bytes(b"image")
        self.write_csv([self.row()])
        products = load_catalog(self.csv_path, self.assets)
        self.assertEqual(products[0]["image"], "products/sample.jpg")
        self.assertEqual(products[0]["size"], "M")

    def test_https_image_url_is_preserved(self):
        self.write_csv([self.row(**{"رابط أو اسم صورة المنتج": "https://cdn.example.com/MS-001.jpg"})])
        self.assertEqual(
            load_catalog(self.csv_path, self.assets)[0]["image"],
            "https://cdn.example.com/MS-001.jpg",
        )

    def test_duplicate_code_is_rejected(self):
        (self.assets / "products" / "sample.jpg").write_bytes(b"image")
        self.write_csv([self.row(), self.row(**{"اسم المنتج": "اسم آخر"})])
        with self.assertRaisesRegex(CatalogError, "duplicate product code"):
            load_catalog(self.csv_path, self.assets)

    def test_missing_image_is_rejected(self):
        self.write_csv([self.row()])
        with self.assertRaisesRegex(CatalogError, "original image file not found"):
            load_catalog(self.csv_path, self.assets)

    def test_http_url_is_rejected(self):
        self.write_csv([self.row(**{"رابط أو اسم صورة المنتج": "http://example.com/a.jpg"})])
        with self.assertRaisesRegex(CatalogError, "must use HTTPS"):
            load_catalog(self.csv_path, self.assets)

    def test_path_traversal_is_rejected(self):
        self.write_csv([self.row(**{"رابط أو اسم صورة المنتج": "../secret.jpg"})])
        with self.assertRaisesRegex(CatalogError, "unsafe image path"):
            load_catalog(self.csv_path, self.assets)

    def test_unknown_category_is_rejected(self):
        self.write_csv([self.row(**{"القسم": "قسم غير معتمد"})])
        with self.assertRaisesRegex(CatalogError, "unknown section"):
            load_catalog(self.csv_path, self.assets)

    def test_script_tag_injection_is_idempotent(self):
        html = self.root / "index.html"
        html.write_text("<html><body>Store</body></html>", encoding="utf-8")
        inject_script_tag(html)
        inject_script_tag(html)
        self.assertEqual(html.read_text(encoding="utf-8").count("catalog-generated.js"), 1)


if __name__ == "__main__":
    unittest.main()
