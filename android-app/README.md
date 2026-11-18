# Dar Maram Store — Android

This is a standalone Android storefront. The Arabic RTL home screen is bundled locally in `app/src/main/assets/index.html`; the app opens directly to that screen and does not depend on WordPress or an internet-hosted storefront to launch.

The app and website remain separate products. The optional website link in the app points to:
https://darmaramstore.wordpress.com/

## Store behavior in this build

- Arabic right-to-left interface with the approved black, gold, and cream palette.
- Category tiles for veils/scarves/bandanas, casual clothing, shawls, and abayas.
- Floating WhatsApp contact button: `+20 111 930 1092`.
- Store address: `119 شارع خلوصي، شبرا مصر، الساحل، القاهرة، مصر`.
- Cash on delivery is the only payment option displayed.
- No demo products, invented prices, wallet/card payment methods, or returns/exchanges section are included. The product area remains empty until the store's approved real product photos and prices are added.

The current repository does not contain a connected catalogue-management backend or a customer order database. The WhatsApp contact is available for customer enquiries; this APK should not be described as a completed online checkout system.

## Build

Requires JDK 17 and Gradle 8.9:

```bash
gradle assembleDebug
```

APK output: `app/build/outputs/apk/debug/app-debug.apk`.

GitHub Actions builds a debug APK on pushes, pull requests, and manual workflow dispatch. Download it from the workflow run's Artifacts section.

## Release

A Play Store release still requires a release signing key, a signed Android App Bundle (AAB), Google Play Console access, store listing and policy declarations, and Google review. Do not commit signing credentials. A debug APK is installable for testing but is not a Play Store release.
