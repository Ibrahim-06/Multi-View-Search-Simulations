# استيراد المكتبات
import tkinter as tk
from tkinter import ttk, messagebox
import pygame
from PIL import Image, ImageTk
import threading
import time
import random
import math

# إعداد الصوت
def setup_sounds():
    pygame.mixer.init()
    pygame.mixer.music.load("Sounds/background_sound1.mp3")
    pygame.mixer.music.play(-1)

    global launch_sound, beep_sound, success_sound, lose_sound
    launch_sound = pygame.mixer.Sound("Sounds/rocket_sound.wav")
    beep_sound = pygame.mixer.Sound("Sounds/beep.wav")
    success_sound = pygame.mixer.Sound("Sounds/success.wav")
    lose_sound = pygame.mixer.Sound("Sounds/lose sound.wav")

# كلاس النجوم
class Star:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.reset_star()

    def reset_star(self):
        self.x = random.randint(0, self.width)
        self.y = random.randint(0, self.height)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 2)

    def move(self):
        self.y += self.speed
        if self.y > self.height:
            self.reset_star()

    def draw(self):
        self.canvas.create_oval(self.x, self.y, self.x + self.size, self.y + self.size, fill="white", outline="white", tags="star")

# التطبيق الأساسي
class SpaceSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("\U0001F680 Space Search Simulator")
        self.root.geometry("1300x820")
        self.root.configure(bg="black")

        self.canvas = tk.Canvas(root, width=1200, height=600, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.control_frame = tk.Frame(root, bg="black")
        self.control_frame.pack(pady=10)

        tk.Label(self.control_frame, text="Enter numbers (comma separated):", font=("Arial Rounded MT Bold", 12), bg="black", fg="white").grid(row=0, column=0, padx=5, pady=5)
        self.entry_data = tk.Entry(self.control_frame, width=50, font=("Arial", 12), bg="black", fg="white")
        self.entry_data.grid(row=0, column=1, padx=5)

        tk.Label(self.control_frame, text="\U0001FAE1\U0001FAE1\U0001FAE1\U0001FAE1 Target number: \U0001FAE1\U0001FAE1\U0001FAE1\U0001FAE1", font=("Arial Rounded MT Bold", 12), bg="black", fg="white").grid(row=1, column=0, padx=5, pady=5)
        self.entry_target = tk.Entry(self.control_frame, width=50, font=("Arial", 12), bg="black", fg="white")
        self.entry_target.grid(row=1, column=1, padx=5)

        self.buttons_frame = tk.Frame(self.control_frame, bg="black")
        self.buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.brute_button = tk.Button(self.buttons_frame, text="\U0001F680 Brute Force Search", font=("Arial Rounded MT Bold", 12), bg="#3498db", fg="black", width=20, command=lambda: self.start_search("Brute Force"))
        self.brute_button.pack(side="left", padx=10)

        self.binary_button = tk.Button(self.buttons_frame, text="\U0001F6F0\uFE0F Binary Search", font=("Arial Rounded MT Bold", 12), bg="#2ecc71", fg="black", width=20, command=lambda: self.start_search("Binary Search"))
        self.binary_button.pack(side="left", padx=10)

        self.random_button = tk.Button(self.buttons_frame, text="\U0001F3B2 Random Data", font=("Arial Rounded MT Bold", 12), bg="#f39c12", fg="black", width=20, command=self.generate_random_data)
        self.random_button.pack(side="left", padx=10)

        self.bg_img = ImageTk.PhotoImage(Image.open("background.png").resize((1200, 600)))
        self.planet_images = [ImageTk.PhotoImage(Image.open(f"planet{i+1}.png").resize((120, 120))) for i in range(10)]

        rocket_img = Image.open("rocket.png").resize((135, 135))
        self.rocket_img_right = ImageTk.PhotoImage(rocket_img)
        self.rocket_img_left = ImageTk.PhotoImage(rocket_img.transpose(Image.FLIP_LEFT_RIGHT))

        self.stars = [Star(self.canvas, 1200, 600) for _ in range(100)]

        self.offset = 0

        self.rocket_moving = False
        self.rocket_path = []
        self.rocket_target_index = 0
        self.rocket_dx = 0
        self.rocket_dy = 0
        self.rocket_steps_left = 0

        # تحميل فريمات الانفجار
        self.explosion_frames = [ImageTk.PhotoImage(Image.open(f"explosion{i}.png").resize((150, 150))) for i in range(1, 6)]

    def generate_random_data(self):
        random_data = [random.randint(1, 100) for _ in range(random.randint(8, 10))]
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, ",".join(map(str, random_data)))
        self.entry_target.delete(0, tk.END)
        self.entry_target.insert(0, str(random.choice(random_data)))

    def start_search(self, algo):
        try:
            data = list(map(int, self.entry_data.get().split(",")))
            target = int(self.entry_target.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers and target.")
            return

        self.algorithm = algo

        if algo == "Binary Search":
            sorted_pairs = sorted((val, idx) for idx, val in enumerate(data))
            self.sorted_data = [val for val, _ in sorted_pairs]
            self.original_indices = [idx for _, idx in sorted_pairs]
            self.data = self.sorted_data
        else:
            self.data = data

        self.target = target
        self.planets_pos = []
        spacing = 1300 // (len(self.data) + 1)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        total_width = spacing * (len(self.data) - 1)
        start_x = (1200 - total_width) // 2

        for i, value in enumerate(self.data):
            x = start_x + i * spacing
            y = 300
            self.planets_pos.append((x, y))
            self.canvas.create_image(x, y, image=self.planet_images[i % len(self.planet_images)], tags=f"planet{i}")
            self.canvas.create_text(x, y + 60, text=str(value), fill="white", font=("Arial Rounded MT Bold", 16), tags=f"planet_text{i}")

        self.rocket = self.canvas.create_image(self.planets_pos[0][0], 100, image=self.rocket_img_right, tags="rocket")

        threading.Thread(target=self.run_search, daemon=True).start()
        self.animate()

    def move_rocket_smooth(self, path_indices):
        if not path_indices:
            return
        self.rocket_path = path_indices
        self.rocket_target_index = 0
        self.prepare_next_move()

    def prepare_next_move(self):
        if self.rocket_target_index >= len(self.rocket_path):
            self.rocket_moving = False
            return

        idx = self.rocket_path[self.rocket_target_index]
        target_x, target_y = self.planets_pos[idx]
        current_x, current_y = self.canvas.coords(self.rocket)

        if target_x > current_x:
            self.canvas.itemconfig(self.rocket, image=self.rocket_img_right)
        else:
            self.canvas.itemconfig(self.rocket, image=self.rocket_img_left)

        distance = math.hypot(target_x - current_x, target_y - current_y)
        steps = max(1, int(distance // 4))

        self.rocket_dx = (target_x - current_x) / steps
        self.rocket_dy = (target_y - current_y) / steps
        self.rocket_steps_left = steps
        self.rocket_moving = True

    def finish_search(self, index, steps_taken):
        if steps_taken == 1:
            time_complexity = "O(1)"
        elif self.algorithm == "Brute Force":
            time_complexity = "O(n)"
        elif self.algorithm == "Binary Search":
            time_complexity = "O(log n)"
        else:
            time_complexity = "Unknown"

        x, y = self.planets_pos[index]
        self.show_explosion(x, y)

        message = f"\U0001F3AF Target Found, index = {index} | Time Complexity = {time_complexity}"
        self.canvas.create_text(600, 550, text=message, fill="gold", font=("Arial Rounded MT Bold", 20))

    def show_explosion(self, x, y, frame_index=0):
        if frame_index >= len(self.explosion_frames):
            return
        self.canvas.delete("explosion")
        self.canvas.create_image(x, y, image=self.explosion_frames[frame_index], tags="explosion")
        self.root.after(100, lambda: self.show_explosion(x, y, frame_index + 1))

    def run_search(self):
        if self.algorithm == "Brute Force":
            self.brute_force_search()
        elif self.algorithm == "Binary Search":
            self.binary_search()

    def brute_force_search(self):
        launch_sound.play()
        path = []
        for i, value in enumerate(self.data):
            path.append(i)
            if value == self.target:
                break
        self.move_rocket_smooth(path)
        while self.rocket_moving:
            time.sleep(0.01)
        if self.data[path[-1]] == self.target:
            success_sound.play()
            self.finish_search(path[-1], len(path))
        else:
            self.canvas.create_text(600, 550, text="\U0001F680 Target not found!", fill="red", font=("Arial Rounded MT Bold", 20))
            lose_sound.play()

    def binary_search(self):
        launch_sound.play()
        sorted_data = sorted((val, idx) for idx, val in enumerate(self.data))
        arr = [val for val, _ in sorted_data]
        indices = [idx for _, idx in sorted_data]

        left, right = 0, len(arr) - 1
        path = []
        while left <= right:
            mid = (left + right) // 2
            path.append(indices[mid])
            if arr[mid] == self.target:
                break
            elif arr[mid] < self.target:
                left = mid + 1
            else:
                right = mid - 1
        self.move_rocket_smooth(path)
        while self.rocket_moving:
            time.sleep(0.01)
        if arr[mid] == self.target:
            success_sound.play()
            self.finish_search(indices[mid], len(path))
        else:
            self.canvas.create_text(600, 550, text="\U0001F680 Target not found!", fill="red", font=("Arial Rounded MT Bold", 20))
            lose_sound.play()

    def animate(self):
        self.canvas.delete("star")
        for star in self.stars:
            star.move()
            star.draw()

        self.offset += 0.05
        for i in range(len(self.planets_pos)):
            x, y = self.planets_pos[i]
            dy = math.sin(self.offset + i) * 5
            self.canvas.coords(f"planet{i}", x, y + dy)
            self.canvas.coords(f"planet_text{i}", x, y + 70 + dy)

        if self.rocket_moving and self.rocket_steps_left > 0:
            self.canvas.move(self.rocket, self.rocket_dx, self.rocket_dy)
            self.rocket_steps_left -= 1
            if self.rocket_steps_left == 0:
                self.rocket_target_index += 1
                self.prepare_next_move()

        self.root.after(20, self.animate)

# تشغيل البرنامج
if __name__ == "__main__":
    setup_sounds()
    root = tk.Tk()
    app = SpaceSearchApp(root)
    root.mainloop()
