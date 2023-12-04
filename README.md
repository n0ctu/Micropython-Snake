# Micropython-Snake
A simple snake game for MCUs with Micropython and Neopixel. I put this together to bring the [LuXeria Camp 2023 Badge](https://github.com/luxeria/campbadge2023/) to life.

## Hardware preparation

In this example, I'm using the [LuXeria Camp 2023 Badge](https://github.com/luxeria/campbadge2023/) with a 5 x 5 LED matrix on it and the [M5 STAMP-C3](https://docs.m5stack.com/en/core/stamp_c3).

todo
                        
## Installation

1. Clone this repository
2. Make a venv and install the dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Install Micropython on your MCU: [Official Download/Instructions](https://micropython.org/download/) / [LuXeria Instructions for M5 STAMP-C3](https://github.com/luxeria/campbadge2023/tree/main/MicroPython)
4. Copy the 'main.py' to your ESP32's root directory using mpremote, then reset it
```bash
mpremote cp main.py :.
mpremote reset
```

## Demo

[snake.gif](demo/snake.gif)
