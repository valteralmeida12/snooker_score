# Snookerscore

## Introduction

This project aims to create a snooker score board that can be updated live. 
While streaming from a mobile device I struggled to showcase the score of the game. 
Luckly, streamlabs obs offers the chance to add a costum url to the stream, and that is how I got this idea.

With this project you'll be able to have your own snooker score board, and update it live using you mobile phone
or any other device with which you can access your webpage.

## Features

- Snooker scoreboard interface.
- Live updates.
- Easy accessibility.

## Getting Started

### Prerequisites

To set implement this project you'll need:

- sudo apt-get update
- sudo apt-get install python3 python3-pip
- sudo pip3 install flask flask-socketio

### Hardware 

- Host machine for you webpage (I used a rpi zero 2w with a costume and minimal linux distro)
- Portforward your the ports your machine is using, so the webpage is accessible outside your local network.

### How to activate your webpage

- pyhton3 snookerscore.py

## Demonstration

Demo: https://www.youtube.com/watch?v=vnkapi7iZTU