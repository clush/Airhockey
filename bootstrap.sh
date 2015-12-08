#!/bin/bash
set -e

# update stuff
sudo apt-get update

# check natural dependencies
mkdir ~/opencv_dep && cd ~/opencv_dep
sudo aptitude build-dep -y libopencv-dev

# remove some packages
sudo aptitude purge -y libavcodec-dev libavformat-dev libswscale-dev
sudo aptitude purge -y libx264-dev x264

# setup dependencies
sudo aptitude install -y autoconf automake build-essential libass-dev libfreetype6-dev libgpac-dev libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libx11-dev libxext-dev libxfixes-dev pkg-config texi2html zlib1g-dev
sudo aptitude install -y yasm

# build x264
mkdir ~/ffmpeg_sources
cd ~/ffmpeg_sources
wget http://download.videolan.org/pub/x264/snapshots/last_x264.tar.bz2
tar xjvf last_x264.tar.bz2
cd x264-snapshot*
./configure --enable-shared --enable-pic
make

sudo make install

# build ffmpeg
cd ~/ffmpeg_sources
wget http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
tar xjvf ffmpeg-snapshot.tar.bz2
cd ffmpeg
./configure --extra-libs="-ldl" --enable-gpl --enable-libass --enable-libfreetype --enable-libtheora --enable-libvorbis --enable-libx264 --enable-nonfree --enable-x11grab --enable-shared --enable-pic
make

sudo make install

# clean up (standard hard disk is 10GB, free space for opencv build)
rm -rf ~/ffmpeg_sources

# build opencv

mkdir ~/opencv_sources
cd ~/opencv_sources
wget http://kent.dl.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.9/opencv-2.4.9.zip
unzip opencv-2.4.9.zip
cd opencv-2.4.9
mkdir release
cd release
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_NEW_PYTHON_SUPPORT=ON ..
make

sudo make install

# clean up
rm -rf ~/opencv_sources
rm -rf ~/opencv_dep

# install xfce4
sudo apt-get -y install xfce4

# edit config
sudo sed -i 's/allowed_users=console/allowed_users=anybody/g' /etc/X11/Xwrapper.config
