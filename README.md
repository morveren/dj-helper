# DJ helper 🔉 💿 <!-- omit in toc -->

This repo aims to make collecting and organising your tracks a little easier.

- [1. How to use this repo](#1-how-to-use-this-repo)
- [2. What does this repo do?...](#2-what-does-this-repo-do)


## 1. How to use this repo


1. Populate the .env file with the folders where you import your music to and the one you keep it in (see `.env_example` for details on variables)
2. Install Docker
3. Run `docker-compose up -d` in the terminal

that's basically it...the app will run in the background and migrate music that gets dumped into your selected folders

## 2. What does this repo do?...

1. Extracts metadata from a range of audio files
2. Converts any `.flac` files to `.aiff` files
3. Migrates files into a uniform file system in a specified location (ie. `<dj folder>/<artist>/<album>/<file>`