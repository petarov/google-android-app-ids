<p align="center">
  <img src="src/play-store-icon.png" width="128"/>
</p>
<p align="center">
  <img alt="OS-Android" src="https://img.shields.io/badge/OS-Android-green?style=for-the-badge"/>
  <img alt="License" src="https://img.shields.io/github/license/petarov/google-app-ids?style=for-the-badge">
</p>

# Google Android Play Store Apps

Google-made Android apps that can be found on the Play Store. Many of these come preinstalled on Android devices.

Please note that currently only `English`-language apps in the `US` Google Play Store are listed.

  * **%%APPS_COUNT%%** apps - v%%VERSION%% - built on %%BUILD_TIMESTAMP%%

| Icon | App Name | Package Name | Genre |
| --- | --- | --- | --- |
%%APPS%%

# Installation

Install and update [using npm](https://github.com/petarov/google-android-app-ids/pull/1#issuecomment-809714435):

    npm install github:petarov/google-android-app-ids

Or just use the compiled `csv` and `json` files from `dist/`

# Contributing

To add or modify an app, open and edit the [app-ids.csv](src/app-ids.csv) file.

After that open a [pull request](https://github.com/petarov/google-app-ids/pulls) or preferably rebuild the `dist/` folder files as described below and then open a PR.

# Building

Requires Python `3.x` and working Internet connection.

Run the following to install dependencies, build all `dist/` files and generate a new `README.md` file:

    ./make

# License

[MIT License](LICENSE)