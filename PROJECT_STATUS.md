# Dar Maram Store — Android Project Status

Updated: 2026-11-21

## Repository safety
- Default branch: `main`.
- `main` remains unchanged at `815c0efaab4b46af9d85c6c5127e36f75cac78a2`.
- Android review work is isolated on `app-review/verified-release-20261121`.
- This branch is one commit ahead of `preview/functionality-pass-20261120`; the only source change is release-workflow checksum reporting.

## Verified Android build
- Android source exists under `android-app/` with Gradle Kotlin build files, `AndroidManifest.xml`, and `MainActivity.kt`.
- Package: `com.darmaram.store`; version name `1.0.2`; version code `3`; min SDK 23; target SDK 35.
- The app launches its bundled `assets/index.html` directly in a WebView; there is no splash/intro screen.
- Signed Release APK and Play Store AAB built successfully in GitHub Actions run [44899094384](https://github.com/darmaramstore/Dar-Maram-store-/actions/runs/44899094384).
- The workflow verified the APK with Android `apksigner`, generated SHA-256 checksums for APK and AAB, uploaded both binaries and the checksum artifact, and removed the temporary signing key.
- APK artifact: `dar-maram-store-signed-release-apk`.
- AAB artifact: `dar-maram-store-play-release-aab`.
- Checksum artifact: `dar-maram-store-release-checksums`.
- APK SHA-256: `4ebee3b81a50a215eef6e5b030cff0654f4d8c725cdee39034ff36e6d54cfaa1`.
- AAB SHA-256: `6e94edab36387aec523cda540580fd4ccae72643d2a54ca127c0027b1d3fc161`.

## Store requirements currently present
- Arabic RTL storefront styling using black, gold, and cream.
- Store categories include casual women's clothing, hijab/scarves/bandanas, shawls, and abayas.
- WhatsApp handoff link uses `201119301092`.
- Store address is present: 119 شارع خلوصي، شبرا مصر، الساحل، القاهرة.
- Cash on delivery is the only payment method shown.
- No Shopify integration, medical/pharmacy content, or returns/exchanges section was found in the bundled storefront HTML.

## Remaining functional gaps
- The product grid is deliberately empty with a message that approved products will be added later. No supplier-MS product photos or verified product-code catalogue were found in the Library files retrieved for this review; retrieved visual files were store mockups and screenshots.
- The bottom navigation entries for favorites, cart, and account currently show informational toast messages; they are not a persistent favorites/cart/account implementation.
- There is no configured product API, backend checkout, stock/price source, or end-to-end order submission. Do not represent the app as a complete ecommerce checkout yet.
- The APK signing certificate is self-issued under Dar Maram Store, not a Google Play-issued certificate. The Actions signature check succeeded, but sideloaded installation may still trigger Play Protect warnings.
- The AAB has not been uploaded to Google Play Console and the app has not been submitted to any store.

## Next work
1. Locate and import only the user's approved original product photos and verified product codes; do not substitute mockup imagery or invent product names/prices.
2. Implement and test real cart and order handoff behavior using verified product data; do not claim an order or payment succeeded unless a real service confirms it.
3. Test the Android app on devices and prepare Play Console declarations only after the app functionality and store data are complete.

No public release, deployment, domain connection, or store submission has been performed.
