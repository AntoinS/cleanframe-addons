# Add-on API 2 (CleanFrame 0.8.0)

`catalog.json` remains API 1 and is unchanged. New hosts read `catalog-v2.json`; it includes complete API 1 descriptors, so existing Spotify installations and declarative widget packages remain compatible. The API 2 catalog contains Spotify and the explicitly experimental iPhone Remote 0.1.0 package. Secure pairing, reconnection, navigation, Play/Pause and live Spotify text entry passed on the reference devices. Full lifecycle and cross-app compatibility remain pending; this is not a regular Apple TV compatibility release.

## Separate Android applications

Native code is installed by Android into its own app, never loaded into CleanFrame's WebView. API 2 currently admits the reviewed `apple-remote` identity only. Adding another executable identity requires a host change and review; putting an arbitrary APK URL in the catalog cannot grant access.

The schema is `native-package.schema.json`. This **non-installable template** illustrates the fields; replace placeholders with verified release facts after device acceptance:

```json
{
  "api": 2,
  "id": "apple-remote",
  "kind": "native",
  "name": "iPhone Remote",
  "description": "Control Android TV using the iPhone remote",
  "author": "CleanFrame",
  "license": "REPLACE_WITH_VERIFIED_SPDX_LICENSE",
  "version": "0.1.0",
  "versionCode": 1,
  "minHostVersion": "0.8.0",
  "packageName": "com.cleanframe.addon.appleremote",
  "serviceInterface": 1,
  "apkUrl": "https://github.com/AntoinS/cleanframe-addons/releases/download/RELEASE_TAG/VERIFIED_FILE.apk",
  "sha256": "REPLACE_WITH_REAL_APK_SHA256",
  "signerSha256": "REPLACE_WITH_APPROVED_CERTIFICATE_SHA256",
  "icon": "remote",
  "permissions": ["Local network", "Foreground receiver service", "Start after reboot"]
}
```

Only HTTPS release assets in this repository are accepted. The host verifies SHA-256, archive package identity, exact version name/code, minimum host version, and signer certificate before requesting installation. The certificate must also match the host certificate. Downloads are bounded to 64 MiB. Android asks for installation/removal confirmation; cancelling or a failed download retains the existing installation. Final success requires PackageManager verification. Installation does not activate a receiver. Native service packages do not use a home-widget slot.

## Service interface 1

Shared AIDL package `com.cleanframe.addonapi`:

```aidl
interface IRemoteAddon { String request(String json); }
```

The receiver component is `com.cleanframe.addon.appleremote/.RemoteService`. All visible setup is hosted by CleanFrame; the add-on app entry redirects there. The service requires signature permission `com.cleanframe.addon.permission.CONTROL` and checks the calling package and signing certificate. CleanFrame rechecks the installed APK certificate before binding and when connected. Request format is `{"api":1,"op":"status"}`; host operations are `status`, `setupStatus`, `enable`, `disable`, `philipsPairBegin`, `philipsPairFinish` (four digits in `code`), `applePairBegin`, and `unpair` (device `id`). Unknown commands or extra fields are rejected. `setupStatus` exposes only the visible PIN, expiry and device handles in addition to redacted status. Keys, account credentials and entered text remain private. There is no arbitrary shell, navigation injection, or executable WebView bridge.

`status` is read-only; binding must not enable the receiver. Status includes activation, runtime, Android connection, Apple connection, keyboard readiness and bounded redacted events. Never return keys, credentials, entered text, or raw protocol packets in diagnostics. Pairing PINs are restricted to the setup flow. Enable/disable may only follow an explicit user action. A separate app may be installed while its service is disabled, disconnected, or not yet paired.

## Host JavaScript bridge

`CleanFrameNative.addons(JSON.stringify({action, id}))` retains `state`, `refresh`, `install`, `remove` and `toggle`. Setup is a frontend route. `remoteState` asynchronously refreshes cached setup state; `remote` queues a bounded service request in `command`. `install` also updates an existing package. Actions return acceptance immediately; `cleanframe:addons` events carry actual changes.

State retains `installed` (ID-keyed descriptors), `catalog`, `busy`, `error`, and adds `api:2`, `runtime` (ID-keyed service status), and `pending`. A pending package operation has an `action`, `id`, and `status`: `permission-required`, `awaiting-confirmation`, `checking`, `cancelled`, or `failed`. Awaiting confirmation is not installed success. `runtime[id].enabled` is the receiver's activation state; `installed` records verified installation separately. The shared frontend renders setup. A host-owned translucent code sheet leaves the Philips system code visible. Android still owns installation and keyboard permission dialogs.

## Contribution and release

Submit source, license notices, exact dependency revisions, build instructions, protocol/security tests, and device acceptance evidence with a pull request. Do not include signing keys, paired identities, home-network addresses or account data. Release maintainers build and sign reviewed source, verify the artifact, and then add real immutable release metadata. Only an explicitly labeled experimental release with verified artifact facts may be offered before the full regular-release gate. Placeholder hashes and unreviewed test APKs are never catalog entries. API 1 catalog/package files are maintained independently for older hosts.
