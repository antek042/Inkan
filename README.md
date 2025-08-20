# Inkan

<p align="center">
  <img src="https://i.imgur.com/Zw0svsu.png" alt="logo" with="150" height="150"/>
</p>
<br>

## 📌 Project Goal
**Inkan** aims to simplify the transition from Windows to Linux by helping users transfer files and applications.

## 🎯 Scope
- Transfer system wallpaper
- Transfer documents, photos, music, and videos
- Transfer selected applications

## 🛠️ Technologies
This project uses:
- [pyudev](https://pyudev.readthedocs.io/) – Linux device management
- [zstandard](https://facebook.github.io/zstd/) – fast data compression
- [pytest](https://docs.pytest.org/) – automated testing
- [GTK4](https://www.gtk.org/) – graphical user interface

## 🚦 Status
**Alpha** – the project is in a very early stage of development.

## ▶️ Running
Requirements:
- Python 3.10+
- Installed dependencies from `requirements.txt`

Instructions:
```bash
git clone https://github.com/antek5421/inkan.git
cd inkan
pip install -r requirements.txt
python main.py