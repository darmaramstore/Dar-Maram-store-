#!/usr/bin/env python3
"""Validate the supplier CSV and generate real product cards for the Android WebView."""
import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlparse

COLUMNS = [
    "اسم المنتج", "الكود", "القسم", "السعر", "الوصف", "المقاس",
    "رابط أو اسم صورة المنتج",
]
CATEGORY_GROUPS = {
    "الطرح": "الطرح والإسكارفات والباندانات",
    "الإسكارفات": "الطرح والإسكارفات والباندانات",
    "الباندانات": "الطرح والإسكارفات والباندانات",
    "مكملات الحجاب": "الطرح والإسكارفات والباندانات",
    "الطرح والإسكارفات والباندانات": "الطرح والإسكارفات والباندانات",
    "الطرح والإسكارفات والباندانات ومكملات الحجاب": "الطرح والإسكارفات والباندانات",
    "الملابس الكاجوال": "الملابس الكاجوال",
    "الشالات": "الشيلان",
    "الشيلان": "الشيلان",
    "العبايات": "العبايات",
}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


class CatalogError(ValueError):
    pass


def clean(value):
    return str(value or "").strip()


def resolve_image(value, assets_dir, row_number):
    if value.startswith("https://"):
        parsed = urlparse(value)
        if not parsed.hostname or parsed.username or parsed.password or any(c.isspace() for c in value):
            raise CatalogError(f"Row {row_number}: invalid HTTPS image URL.")
        return value
    if value.startswith("http://"):
        raise CatalogError(f"Row {row_number}: image URLs must use HTTPS.")
    path = Path(value)
    if "\\" in value or value.startswith("/") or ".." in path.parts:
        raise CatalogError(f"Row {row_number}: unsafe image path.")
    relative = path if path.parts and path.parts[0] == "products" else Path("products") / path
    if len(relative.parts) != 2 or relative.parts[0] != "products":
        raise CatalogError(f"Row {row_number}: use a filename or products/<filename>.")
    if relative.suffix.lower() not in IMAGE_SUFFIXES:
        raise CatalogError(f"Row {row_number}: image must be JPG, PNG, or WEBP.")
    root = assets_dir.resolve()
    image_path = (root / relative).resolve()
    if root not in image_path.parents or not image_path.is_file():
        raise CatalogError(f"Row {row_number}: original image file not found: {relative.as_posix()}.")
    return relative.as_posix()


def load_catalog(csv_path, assets_dir):
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        missing = [c for c in COLUMNS if c not in headers]
        extra = [c for c in headers if c not in COLUMNS]
        if len(headers) != len(set(headers)) or missing or extra:
            detail = []
            if missing:
                detail.append("missing: " + "، ".join(missing))
            if extra:
                detail.append("unexpected: " + "، ".join(extra))
            raise CatalogError("CSV headings do not match the template. " + "; ".join(detail))

        products = []
        seen_codes = set()
        for row_number, row in enumerate(reader, start=2):
            values = {c: clean(row.get(c)) for c in COLUMNS}
            if not any(values.values()):
                continue
            name, code, category = values["اسم المنتج"], values["الكود"], values["القسم"]
            image = values["رابط أو اسم صورة المنتج"]
            if not name or not code or not category or not image:
                raise CatalogError(f"Row {row_number}: name, code, section, and original image are required.")
            if code in seen_codes:
                raise CatalogError(f"Row {row_number}: duplicate product code '{code}'.")
            if category not in CATEGORY_GROUPS:
                raise CatalogError(f"Row {row_number}: unknown section '{category}'.")
            seen_codes.add(code)
            products.append({
                "id": code,
                "name": name,
                "code": code,
                "category": category,
                "categoryGroup": CATEGORY_GROUPS[category],
                "price": values["السعر"],
                "description": values["الوصف"],
                "size": values["المقاس"],
                "image": resolve_image(image, assets_dir, row_number),
            })
    return products


def generated_javascript(products):
    payload = json.dumps(products, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    runtime = r"""
(function () {
  "use strict";
  const products = window.DAR_MARAM_PRODUCTS || [];
  const host = document.getElementById("productGrid");
  if (!host || !products.length) return;
  host.replaceChildren();

  products.forEach(function (item) {
    const card = document.createElement("article");
    card.className = "product";
    card.dataset.name = item.name;
    card.dataset.code = item.code;
    card.dataset.productId = item.id;
    card.dataset.category = item.categoryGroup;
    card.dataset.price = item.price || "";
    card.dataset.size = item.size || "";

    const image = document.createElement("img");
    image.src = item.image;
    image.alt = item.name;
    image.loading = "lazy";
    card.appendChild(image);

    const info = document.createElement("div");
    info.className = "info";
    const title = document.createElement("h3");
    title.textContent = item.name;
    info.appendChild(title);

    const code = document.createElement("small");
    code.className = "product-code";
    code.textContent = "الكود: " + item.code;
    info.appendChild(code);

    if (item.size) {
      const size = document.createElement("small");
      size.className = "product-size";
      size.textContent = "المقاس: " + item.size;
      info.appendChild(size);
    }
    if (item.description) {
      const description = document.createElement("p");
      description.className = "product-description";
      description.textContent = item.description;
      info.appendChild(description);
    }
    if (item.price) {
      const price = document.createElement("div");
      price.className = "price";
      price.textContent = item.price;
      info.appendChild(price);
    }
    card.appendChild(info);

    const fav = document.createElement("button");
    fav.type = "button";
    fav.className = "fav";
    fav.setAttribute("aria-label", "إضافة إلى المفضلة");
    fav.textContent = "♡";
    fav.addEventListener("click", function () {
      if (typeof window.favorite === "function") window.favorite(fav);
    });
    card.appendChild(fav);
    host.appendChild(card);
  });

  if (typeof window.productData === "function" && !window.__darMaramCatalogHooks) {
    const originalProductData = window.productData;
    window.productData = function (card) {
      const product = originalProductData(card);
      return product ? Object.assign({}, product, { size: card.dataset.size || "" }) : product;
    };
    window.addProductToCart = function (card) {
      const product = window.productData(card);
      if (!product) { toast("بيانات المنتج غير مكتملة؛ لم تتم إضافته"); return; }
      const existing = cartItems.find(function (entry) { return entry.id === product.id; });
      if (existing) existing.qty += 1;
      else cartItems.push({
        id: product.id, name: product.name, code: product.code,
        price: product.price, size: product.size, qty: 1
      });
      persistStoreState();
      renderCart();
      toast("تمت إضافة المنتج إلى السلة");
    };

    const originalRenderCart = window.renderCart;
    window.renderCart = function () {
      originalRenderCart();
      document.querySelectorAll("#cartContent .cart-item").forEach(function (row, index) {
        const item = cartItems[index];
        if (!item || !item.size) return;
        const size = document.createElement("small");
        size.className = "cart-item-meta";
        size.textContent = "المقاس: " + item.size;
        const main = row.querySelector(".cart-item-main");
        if (main) main.appendChild(size);
      });
    };

    window.checkoutCart = function () {
      if (!cartItems.length) { toast("السلة فارغة"); return; }
      const lines = cartItems.map(function (item) {
        return "- " + item.name +
          (item.code ? " (كود " + item.code + ")" : "") +
          (item.size ? " (المقاس " + item.size + ")" : "") +
          " × " + item.qty +
          (item.price ? " — السعر المسجل: " + item.price : "");
      }).join("\n");
      const message = "مرحبًا، أريد طلب المنتجات التالية من دار مرام ستور بنظام الدفع عند الاستلام:\n" +
        lines + "\nبرجاء تأكيد التوافر والسعر وتكلفة التوصيل.";
      window.location.href = "https://wa.me/201119301092?text=" + encodeURIComponent(message);
    };
    window.__darMaramCatalogHooks = true;
  }

  if (typeof window.syncProductCards === "function") window.syncProductCards();
  if (typeof window.renderCart === "function") window.renderCart();
  if (typeof window.filterProducts === "function") window.filterProducts();
})();
"""
    return "/* Generated from catalog/products.csv. Do not edit by hand. */\nwindow.DAR_MARAM_PRODUCTS = " + payload + ";\n" + runtime


def inject_script_tag(html_path):
    html = html_path.read_text(encoding="utf-8")
    tag = '<script src="catalog-generated.js"></script>'
    if tag in html:
        return
    if html.count("</body>") != 1:
        raise CatalogError("Could not safely locate the single </body> tag.")
    html_path.write_text(html.replace("</body>", tag + "\n</body>"), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--assets", type=Path, required=True)
    parser.add_argument("--html", type=Path, required=True)
    args = parser.parse_args()
    products = load_catalog(args.csv, args.assets)
    output = args.assets / "catalog-generated.js"
    output.write_text(generated_javascript(products), encoding="utf-8")
    inject_script_tag(args.html)
    print(f"Validated {len(products)} supplier product(s); generated {output}.")
    if not products:
        print("Empty template: no placeholder products or images were generated.")


if __name__ == "__main__":
    try:
        main()
    except CatalogError as error:
        raise SystemExit("Catalog import error: " + str(error))
