#!/usr/bin/env sh

if uname -m | grep aarch64; then
  curl -o /tmp/ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz
  tar xvf /tmp/ffmpeg.tar.xz
  cp ffm*/ffprobe /ffprobe
elif uname -m | grep x86_64; then
  curl -o /tmp/ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
  tar xvf /tmp/ffmpeg.tar.xz
  cp ffm*/ffprobe /ffprobe
elif uname -m | grep armv7l; then
  curl -o /tmp/ffmpeg.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-armhf-static.tar.xz
  tar xvf /tmp/ffmpeg.tar.xz
  cp ffm*/ffprobe /ffprobe
fi