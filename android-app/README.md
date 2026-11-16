# Dar Maram Store — Android

This Android application opens the existing Dar Maram Store storefront at https://darmaramstore.wordpress.com in an Android WebView, retaining the current live catalogue and checkout experience supplied by the website.

## Build
Requires JDK 17 and Gradle 8.9:
```bash
gradle assembleDebug
```
APK output: `app/build/outputs/apk/debug/app-debug.apk`.

A GitHub Actions workflow builds the debug APK on pushes, pull requests, and manual workflow dispatch. Download it from the workflow run's Artifacts section.

## Release
The debug APK is for installation/testing. A Play Store release requires a separately configured signing key, verified application identity, privacy/data-safety review, and a release AAB. Do not commit signing credentials.
