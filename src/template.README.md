<p align="center">
  <img src="src/play-store-icon.png" width="128"/>
</p>
<p align="center">
  <img alt="OS-Android" src="https://img.shields.io/badge/OS-Android-green?style=for-the-badge"/>
  <img alt="License" src="https://img.shields.io/github/license/petarov/google-app-ids?style=for-the-badge">
</p>

# Google Android Play Store Apps

A list of Google made Android apps (including Android System Apps) that can be found on the Play Store. Many of these come preinstalled on a new Android device.

  * v%%VERSION%%
  * Built on %%BUILD_TIMESTAMP%%
  * **%%APPS_COUNT%%** apps total

| Icon | Package Name | App Name | Genre | Privileged* |
| --- | --- | --- | --- | --- |
%%APPS%%

**Privileged*** - Privileged apps are system apps that are located in a **priv-app** directory on one of the system image partitions. [Documentation](https://source.android.com/devices/tech/config/perms-whitelist).

# Editing

To add or modify an app open and edit the [app-ids.csv](src/app-ids.csv) file.

You may now open a [pull request](https://github.com/petarov/google-app-ids/pulls), or preferably rebuild the dist files as described below and then open a PR.

# Building

Requires Python `3.x` and working Internet connection.

Install build dependencies:

    ./make

Run the `build.py` script in order to build all the `dist/` output files and a new `README.md` file. 

    ./build.py

# License

[MIT License](LICENSE)