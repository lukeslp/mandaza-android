# Mandaza Android release verification

Version 1.3.6 (10311), tag `fdroid-v1.3.6`, uses source commit
`f3645dd1fd2a5210eb3e060edbe34c1e3527562d`. The tag and signed APK are immutable.

The public Linux build in [run 42004282746](https://github.com/lukeslp/mandaza-android/actions/runs/42004282746)
built that exact commit. Its downloaded unsigned APK matches SHA-256
`4e9d12e0f63f1be7461f1f9c13925bc8136a715cd65dc34bf854ab77999c11b0`.
The release receipt's reference to private-source CI records an earlier check;
the public-source artifact was subsequently compared directly. Neither check
establishes official F-Droid builder acceptance.

The repeatable `Verify published F-Droid release` workflow checks out the
selected release tag, runs its build/tests/lint/APK verifier, and compares its
source commit and unsigned APK with the published receipt. The comparison gate
rejects a different source revision, tag or APK digest. It retains a JSON result
and the unsigned APK. This is an upstream check; F-Droid runs its own builder.

On November 5, the exact signed APK with SHA-256
`db95b1c95edeedd9426102a0ebebdf394985bace0df28e3231946dc47651425e`
was installed over 1.3.5 (10310) on a Pixel 9a and Pixel 10, both API 37. Both
retained the existing app identity, first-install record and credential-data
directory, resumed the release activity and ran without an observed app crash.
No uninstall or data reset was used. Individual personal favorites/history were
not extracted; retaining the data directory is distinct from checking each item.

The earlier seven-case Pixel runs used a separate debug-signed review app.
Those functional/ATF results remain separate from the exact-release upgrade and
launch checks. Full human TalkBack traversal, physical Fire/tablet/fold behavior
and 16KB-device checks are still not claimed.

[Official F-Droid MR !55922](https://gitlab.com/fdroid/fdroiddata/-/merge_requests/55922)
is submitted for review. Its account-gated fork CI has run zero jobs. Maintainer
CI, official reproduction, merge and catalog publication remain separate stages.

For future releases, choose a new phone version code above every code already
issued across direct, Play, Amazon and F-Droid builds, including private
candidates. A target channel with a lower code cannot update an installed newer
variant. A matching package and app signer are also required; Play/Amazon
store-delivered signing compatibility must be checked independently. The current
first F-Droid recipe intentionally uses manual updates. An automated tag/version
recipe needs review before it changes that third-party submission.
