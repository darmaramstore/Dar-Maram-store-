# Dar Maram Store — Android

The Android app is a standalone storefront. Its Arabic RTL home screen and interface are bundled locally in `app/src/main/assets/index.html`; it does not load WordPress or require the website to run.

The app and website are separate products. The app includes an optional external link to the website:
https://darmaram-store.darmaramstore.workers.dev/

The Android package also registers the optional `darmaram://store` handoff so a website link can open the installed app. The website must add that link separately; it is not automatically modified by this Android repository.

## Build

Requires JDK 17 and Gradle 8.9:

```bash
gradle assembleDebug
```

APK output: `app/build/outputs/apk/debug/app-debug.apk`.

GitHub Actions builds the debug APK on pushes, pull requests, and manual workflow dispatch. Download it from the workflow run's Artifacts section.

## Release

A Play Store release still requires a release signing key, a signed Android App Bundle (AAB), Google Play Console access, store listing and policy declarations, and Google review. Do not commit signing credentials. A debug APK is not a Play Store release.
