# CleanFrame Add-ons

Public, reviewed add-ons for CleanFrame. API 1 keeps Spotify compatible with CleanFrame 0.7.0; API 2 adds the experimental iPhone Remote package for CleanFrame 0.8.0. The launcher and Mac editor are maintained separately in a private repository.

On Android TV open **Settings → Add-ons → Refresh catalog**. Download or update a package, enable/disable it, or uninstall it. Spotify is migrated automatically from existing CleanFrame installations. Removing its package removes the widget and stops observation; saved Spotify credentials and appearance preferences remain until the user explicitly signs out in Spotify settings.

## Contributing a widget

1. Copy an example from `examples/`. Choose a unique lowercase ID and a semantic version (`major.minor.patch`).
2. API 1 supports `text` (plain text), `clock` (optional IANA `timeZone`) and the reserved `spotify` provider. Packages are JSON data, not JavaScript, HTML, native binaries or network clients. New native capabilities require a host API update. No credentials belong in a package.
3. Supply `name`, `description`, `author`, `license`, `api`, `id`, `version`, `kind`. Metadata fields must be nonempty and at most 240 characters. Text is at most 500 characters. At most three additional widgets may be active; Spotify has its own player region.
4. Put the immutable package at `packages/ID/VERSION.json`. Add its metadata, relative `path` and SHA-256 digest to `catalog.json`. Never replace a published version; increase its version.
5. Open a pull request. Include a screenshot at 1080p and 720p, licensing details and a description of changes. A maintainer reviews it before merging into the downloadable catalog.

The TV only downloads from this repository over HTTPS, rejects redirects and oversized payloads, checks API/identity/checksum, and atomically saves changes. Interrupted or invalid downloads keep the previous installation. A checksum protects package integrity relative to the reviewed catalog; it is not a separate publisher signature. Offline installations remain usable. The catalog supports at most 32 entries in API 1.

The examples are SDK fixtures, not automatically installed or advertised in the catalog. Names/descriptions currently use the author's supplied language. CleanFrame management controls support German and English.

## Releases

Catalog releases use Git tags `vMAJOR.MINOR.PATCH` with a GitHub Release. Individual widgets keep independent versions. Release assets include the catalog and published JSON packages. The TV reads the current reviewed catalog from `main`; package paths remain immutable.

## Native add-ons (API 2)

See [API-2.md](API-2.md) for separately installed Android packages, the versioned service interface, review requirements and the new `catalog-v2.json`. The legacy `catalog.json` remains unchanged. iPhone Remote 0.1.0 is available as an experimental package. Setup is integrated into CleanFrame; supported device checks and remaining limitations are documented in [its README](addons/apple-remote/README.md). Source, dependency pins and the local builder are included. Signing keys and device configuration are not.
