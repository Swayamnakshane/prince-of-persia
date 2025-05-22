
# 👑 Building a Prince of Persia-Inspired Platformer with Amazon Q CLI & Pygame on Linux

## 🎮 Introduction

As a child, few games captured imagination like **Prince of Persia**. From precise jumps to daring sword fights and timed traps, it wasn’t just a game—it was an adventure. Today, we’ll walk through building a simple 2D platformer inspired by Prince of Persia using **Python**, **Pygame**, and **Amazon Q CLI**, all developed natively on **Linux**.

But this isn't just about writing code. It’s about turning nostalgia into a working project using **AI-assisted development**.

---

## 🧒 A Personal Note: Where It All Began

When I was a kid, I used to watch my mother play games on her **Nokia 310**. The game “Snake” fascinated me.
**How did it move? How did it know when to turn or end?**

Back then, I didn’t have the answers. But today, I do—thanks to tools like **Amazon Q CLI**, which lets me build games by simply describing what I want to create.

Now, I’ve taken it a step further and started building **my own version of Prince of Persia**, with all the fun and challenge of the classic.

---

## ⚙️ Development Environment Setup (Linux)

### ✅ Tools Required

* **Amazon Q CLI** – AI code generation tool from AWS
* **Python 3.8+** – Core programming language
* **Pygame** – Game development library for Python
* **Linux OS** – Ubuntu/Debian-based preferred

---

## 📦 Step-by-Step Setup on Linux

### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
```

### 2. Install Pygame

```bash
pip3 install pygame
```

---

## 🤖 Install Amazon Q CLI on Linux

### Download and install the `.deb` package:

```bash
wget https://desktop-release.q.us-east-1.amazonaws.com/latest/amazon-q.deb
sudo dpkg -i amazon-q.deb
sudo apt-get install -f
```

### Verify installation and start:

```bash
q --version
q chat
```

---

## 🧠 Prompt-Driven Game Creation Using Amazon Q

With Amazon Q CLI, you don't need to write everything manually. You can describe your idea and let the tool generate functional code.
![Screenshot 2025-05-22 022325](https://github.com/user-attachments/assets/b8323d41-ce24-440c-9b39-7c47c23f33b9)

---

## 🧱 Step-by-Step Game Prompts

### 1. 🧍 Character Movement & Gravity

**Prompt**:

> Create a Pygame-based platformer with a main character that can run left/right, jump with gravity, and collide with platforms.

**Result**:

* Player movement with physics
* Platform collision detection
* Gravity and jumping

---

### 2. 🏰 Level Design

**Prompt**:

> Add basic level design with platforms at varying heights and a floor. Include a simple background.

**Result**:

* Static level with platforms
* Decorative background
* Expandable layout for more levels

---
![Screenshot 2025-05-22 232942](https://github.com/user-attachments/assets/947f8783-214c-4f9b-89a8-5844187d1d80)

### 3. ⚔️ Traps & Obstacles

**Prompt**:

> Add spike traps that reset the player's position if touched.

**Result**:

* Hazard detection logic
* Player reset or health mechanic

---

### 4. 🎯 Goal or Exit Door

**Prompt**:

> Add a door at the end of the level. When the player reaches it, show “You Win” and end the game.

**Result**:

* Goal object
* Victory screen

---

### 5. 🎵 Sound and Polish

**Prompt**:

> Add background music and jumping sound effects.

**Result**:

* Integrated audio playback
* Enhanced game feel

---

## 🧩 Feature Summary

| Feature             | Implemented via Amazon Q |
| ------------------- | ------------------------ |
| Player controls     | ✅                        |
| Platform collisions | ✅                        |
| Traps and obstacles | ✅                        |
| Win condition       | ✅                        |
| Audio & UI          | ✅                        |

---

## 👑 Why This Project Matters

This wasn’t just about building a game. It was about realizing a dream from childhood—understanding and building what once felt like magic.

With **Amazon Q CLI**, I could rapidly turn my thoughts into code, iterate on ideas, and focus on creativity instead of boilerplate.

![Screenshot 2025-05-22 233224](https://github.com/user-attachments/assets/138ce721-bcb4-403b-afac-fcebc6141043)





---


