<p align="center">
  <img src="src/play-store-icon.png" width="128"/>
</p>
<p align="center">
  <img alt="OS-Android" src="https://img.shields.io/badge/OS-Android-green?style=for-the-badge"/>
  <img alt="AppIds" src="https://img.shields.io/badge/Android-Package%20Names-green?style=for-the-badge"/>
  <img alt="License" src="https://img.shields.io/github/license/petarov/google-app-ids?style=for-the-badge">
</p>

# Google Android Play Store Apps

Built on: %%BUILD_TIMESTAMP%%

A list of Google made Android apps (a.k.a. Android System Apps) that can be found on the Play Store.

| Icon | Package Name | App Name | Privileged* |
| --- | --- | --- | --- |
%%APPS%%

**Privileged*** - Privileged apps are system apps that are located in a **priv-app** directory on one of the system image partitions. [Documentation](https://source.android.com/devices/tech/config/perms-whitelist).

# Editing & Building

To add or modify an app, please append a new entry to the [app-ids.csv](src/app-ids.csv) file.

Make sure you've got Python `2.7` or `3.x` and an active Internet connection.

Run the `build.py` script in order to build all the `dist/` output files and a new `README.md` file. 

    ./build.py

# License

[MIT License](LICENSE)