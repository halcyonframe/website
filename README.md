# halcyonframe.com

The Halcyon Frame website, with a browser installer for the firmware. It's a static site deployed by GitHub
Pages (`.github/workflows/pages.yml`), which bundles the latest
[firmware release](https://github.com/halcyonframe/halcyonframe/releases) for the installer.

- Installer: [ESP Web Tools](https://github.com/esphome/esp-web-tools) 10.4.0 (Apache-2.0), in `vendor/`
- Fonts: Fraunces and Inter (SIL OFL 1.1), subset to Latin, in `fonts/`

Preview locally with `python3 -m http.server`. The installer needs https or localhost.
