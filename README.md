
# IMPORTANT
## `HSS` is the original prototype.
## [`GSS`](https://github.com/unix2dossss/GSS) is the improved and actively maintained version.



<br>
<br>
<br>

### Home Security System

![Simple Camera Security System](HSS.png)

#### Inspiration
My parents were considering buying a security system for our garage, which is separate from the main house. Rather than spending money on a locked-down, subscription-based solution, I decided to design and build a simple camera security system myself using hardware we already had and tools I enjoy working with.

#### Overview
This project is a lightweight, self-hosted camera security system that runs 24/7 on my homelab.
It monitors a live camera feed, detects motion in real time, and reacts immediately when activity is detected.

The focus is on simplicity, reliability, and full local control.

#### Features

- Continuous camera monitoring  
- Real-time motion detection  
- Automatic video recording on motion  
- Instant Telegram notifications  
- Optional audible alert on detection  
- Fully headless operation (SSH-only)

#### High-level architecture

- USB camera connected to a homelab server  
- Python process continuously reading camera frames  
- Frames analysed using basic image statistics  
- Motion detected by comparing frame deltas  
- When motion is detected:
  - Recording starts
  - A notification is sent
  - An alert can be triggered
- System returns to idle monitoring once motion stops  

All processing happens locally on the server.

#### Tech stack

- Python 3
- OpenCV  
- NumPy  
- Telegram Bot API  
- Ubuntu Server

#### Deployment

The system runs on a headless Ubuntu server in my homelab with a USB webcam attached.  
Everything is managed remotely over SSH, making it suitable for always-on operation.

#### Why this project

- Practical, real-world use case  
- No recurring costs  
- Hands-on experience with computer vision basics  
- Experience designing a reliable, long-running system  
- Full ownership of data and behaviour
