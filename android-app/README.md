# Dar Maram Store — Android

The Android app opens its bundled Arabic RTL storefront directly from app/src/main/assets/index.html; it does not depend on the WordPress homepage to start. Product photos are loaded from the Dar Maram WordPress media library, so an internet connection is required for those images and for the website/WhatsApp links.

The app and website remain separate products. The app includes a link to the website:
https://darmaramstore.wordpress.com/

WhatsApp product orders open WhatsApp with the selected product name in the message. The app has no splash/intro screen.

## Build

Requires JDK 17, Android SDK platform 35, and Gradle 8.9:

    cd android-app
    gradle assembleDebug

APK output: app/build/outputs/apk/debug/app-debug.apk.

GitHub Actions builds a debug APK on pushes, pull requests, and manual workflow dispatch. Download the APK from the workflow run's Artifacts section.

## Release

A Play Store release still requires a release signing key, a signed Android App Bundle (AAB), Google Play Console access, store listing and policy declarations, and Google review. Do not commit signing credentials. A debug APK is not a Play Store release.
