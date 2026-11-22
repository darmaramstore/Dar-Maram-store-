# Dar Maram Store — Android Project Status

Updated: 2026-11-22

## Repository safety
- Default branch: `main`.
- `main` remains unchanged at `815c0efaab4b46af9d85c6c5127e36f75cac78a2`.
- Current review branch: `app-review/cart-and-whatsapp-20261122`.
- Android work is isolated to this review branch. No merge, public release, domain connection, deployment, or app-store submission has been performed.

## Verified Android build
- Android source is under `android-app/`; the app is a standalone Android WebView shell that loads the bundled `assets/index.html` directly.
- Package: `com.darmaram.store`; version `1.0.2`; version code `3`; min SDK 23; target SDK 35.
- No splash/intro screen is shown; the bundled storefront is loaded directly.
- Latest signed Release APK and Play Store AAB were built successfully in GitHub Actions run [45017576031](https://github.com/darmaramstore/Dar-Maram-store-/actions/runs/45017576031) from review-branch commit `6e57fdcd795c54abca43566e151ece860f89a836`.
- The workflow checked that all four Android signing secrets exist, built APK and AAB, verified the APK with Android `apksigner`, generated SHA-256 checksums, uploaded all three artifacts, and removed the temporary signing key.
- APK SHA-256: `db8444eac4e5f2fb1b78b688a8038d7817ebdf732f5df3bb9d334fad9f8aa1fa`.
- AAB SHA-256: `64d95ed5ec16e795f993937903d9cb549abcce17954e3697dbc8aa7d4bb36b3c`.
- Signing certificate subject: `CN=Dar Maram Store, OU=Mobile, O=Dar Maram Store, L=Cairo, ST=Cairo, C=EG`.
- Signing certificate SHA-256: `3f2571040fe06bea618286bd1fbb26621133bb9643837e988655ad632592555a`. It matches the certificate used in the previous signed review build.

## Store requirements present
- Arabic RTL storefront styling using black, gold, and cream.
- Sections for hijabs/scarves/bandanas, casual women's clothing, shawls, and abayas.
- WhatsApp number: `201119301092`.
- Store address: 119 شارع خلوصي، شبرا مصر، الساحل، القاهرة، مصر.
- Cash on delivery is the only payment method shown.
- No Shopify integration, medical/pharmacy content, returns/exchanges section, or extra payment methods were added.
- WhatsApp links now use same-WebView navigation so the Android WebView client can route them to the WhatsApp app.

## Functionality and remaining gaps
- Cart state and favorites are persisted locally using browser local storage.
- Cart supports adding an available product, quantity changes, item removal, and a WhatsApp order-message handoff that states cash on delivery. The message asks the store to confirm stock, price, and delivery cost; sending it does not mean an order has been accepted.
- Favorites can be toggled and filtered locally.
- The product grid is intentionally empty until approved original products are added. A Library image search found design mockups and HTML previews, but no confirmed separate supplier-MS product photos or verified product-code catalogue. No replacement images, invented products, or prices were added.
- Because the grid is empty, cart/favorites/WhatsApp order flow cannot yet be exercised with real store products.
- There is no product API, inventory/price backend, customer account service, or server-side checkout/payment processing.
- The signing certificate is self-issued by the store, not a Google Play-issued certificate. `apksigner` verification succeeded, but sideloaded installation can still trigger Play Protect warnings; signature verification alone is not a malware-safety guarantee.
- The AAB has not been uploaded to Google Play Console and the app has not been submitted to any store.

## Next work
1. Import only the original supplier photos and verified product codes when the actual source files are available.
2. Populate product cards with verified names, codes, categories, and prices; then test cart, favorites, and WhatsApp order handoff against real product entries.
3. Perform device-level installation and navigation tests before any store submission.

No public release, deployment, domain connection, or store submission has been performed.
