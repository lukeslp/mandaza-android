# Mandaza for Android

Animated hexagonal art, favorites, PNG export and a customizable ambient clock.
This source release covers the native phone/tablet app and core engine.
The F-Droid flavor is entirely on-device, with no account, analytics, direct
updater, Play Review runtime or Internet permission. Microphone response is
optional and starts off. Full-panel flip-cover behavior is not yet verified.

## Build

Use JDK 21, Android SDK 36/build-tools 36.0.0 and the checksum-pinned wrapper.
In a disposable clone, prepare and build the F-Droid flavor:

```sh
python3 fdroid/prepare-build.py --confirm-build-sandbox
cd android
./gradlew :core:testDebugUnitTest :app:testFdroidDebugUnitTest :app:lintFdroidRelease :app:assembleFdroidRelease
```

The preparation removes unused store-only sources/declarations. The release is
unsigned without private signing variables. The upstream F-Droid APK is signed
with Mandaza's existing direct-download identity; F-Droid reproduces the build
and copies those signatures. Play App Signing compatibility is not assumed.
The catalog build recipe is maintained in fdroiddata; the disabled recipe in
this source tree is a version/build template, not an official catalog listing.

## License and source

First-party code and supplied app artwork: MIT, copyright Luke Steuber.
The loop engine adapts Dillon (Dillo)'s MIT-licensed loop-construction family;
Mash ancestry includes Dillon, GRC/Steve Gibson and Johannes Baagoe.
See [all notices](THIRD_PARTY_NOTICES.md), [provenance](docs/FDROID_PROVENANCE.md)
and `LICENSES/`. Runtime components include Apache-2.0, BSD-3-Clause and
Boost-1.0 portions; this app's MIT license does not relicense them.

This export contains complete Android build inputs without private Git history,
Apple/TV/Wear build configurations, signing material or local machine settings.
`SOURCE_EXPORT.json` records the source revision, transformations and hashes.
Author: [Luke Steuber](https://lukesteuber.com/).
