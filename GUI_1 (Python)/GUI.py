import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import random
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load image safely
def load_image(path, size):

    try:
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)
    except:
        return None

# Play sound safely
def play_sound(path):
    try:
        pygame.mixer.Sound(path).play()
    except:
        pass

# Play background music
def play_music(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except:
        pass

# GUI Class
class TreasureHuntApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Ultimate Treasure Quest")
        self.root.geometry("1150x600")
        self.root.configure(bg="#0F0F1A")

        play_music("Sounds/mystery_theme.mp3")

        self.bg_image = load_image("Images/magic_land.jpg", (1150, 350))
        self.char_img = load_image("Images/pirate.png", (70, 70))
        self.treasure_img = load_image("Images/treasure.png", (70, 70))
        self.star_img = load_image("Images/star.png", (25, 25))

        self.canvas = tk.Canvas(root, width=1100, height=350, highlightthickness=0, bg="#1C1C2E")
        self.canvas.pack(pady=10)
        if self.bg_image:
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.star_animations = []
        self.animate_stars()

        self.positions = []
        self.rect_ids = []
        self.char_icon = None
        self.treasure_icon = None

        control_frame = tk.Frame(root, bg="#0F0F1A")
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Sorted List:", bg="#0F0F1A", fg="white", font=("Arial", 12)).grid(row=0, column=0)
        self.list_entry = tk.Entry(control_frame, width=60, font=("Arial", 12))
        self.list_entry.grid(row=0, column=1, padx=10)

        tk.Label(control_frame, text="Target:", bg="#0F0F1A", fg="white", font=("Arial", 12)).grid(row=1, column=0, pady=10)
        self.target_entry = tk.Entry(control_frame, width=60, font=("Arial", 12))
        self.target_entry.grid(row=1, column=1)

        tk.Button(control_frame, text="🔀 Random Data", bg="#6A5ACD", fg="white", font=("Arial", 11, "bold"), command=self.fill_random_data).grid(row=2, column=2, padx=10)

        tk.Button(control_frame, text="🎯 Brute Force", bg="#FF4500", fg="white", font=("Arial", 11, "bold"), command=self.run_brute_force).grid(row=2, column=0, pady=15)
        tk.Button(control_frame, text="🧠 Binary Search", bg="#32CD32", fg="white", font=("Arial", 11, "bold"), command=self.run_binary_search).grid(row=2, column=1, pady=15)

        self.result_label = tk.Label(root, text="", font=("Consolas", 14), bg="#0F0F1A", fg="#FFD700")
        self.result_label.pack(pady=10)

    def animate_stars(self):
        if self.star_img:
            for _ in range(12):
                x = random.randint(0, 1100)
                y = random.randint(0, 100)
                star = self.canvas.create_image(x, y, image=self.star_img)
                self.star_animations.append((star, random.uniform(0.5, 1.5)))
            self.twinkle()

    def twinkle(self):
        for star, speed in self.star_animations:
            x, y = self.canvas.coords(star)
            new_y = y + speed
            if new_y > 350:
                new_y = 0
                x = random.randint(0, 1100)
            self.canvas.coords(star, x, new_y)
        self.canvas.after(50, self.twinkle)

    def parse_input(self):
        try:
            arr = list(map(int, self.list_entry.get().split(',')))
            target = int(self.target_entry.get())
            return arr, target
        except:
            messagebox.showerror("Input Error", "Enter valid numbers.")
            return None, None

    def fill_random_data(self):
        arr = sorted(random.sample(range(1, 100), 11))
        target = random.choice(arr)
        self.list_entry.delete(0, tk.END)
        self.list_entry.insert(0, ",".join(map(str, arr)))
        self.target_entry.delete(0, tk.END)
        self.target_entry.insert(0, str(target))

    def draw_map(self, arr):
        self.canvas.delete("values")
        if self.bg_image:
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.positions.clear()
        self.rect_ids.clear()
        self.treasure_icon = None
        for i, val in enumerate(arr):
            x = 50 + i * 90
            frame = self.canvas.create_rectangle(x, 250, x + 60, 300, fill="#FFD700", outline="#FFD700", tags="values")
            label = self.canvas.create_text(x + 30, 275, text=str(val), font=("Courier New", 13, "bold"), fill="#2C2C54", tags="values")
            self.positions.append(x)
            self.rect_ids.append(frame)
        if self.char_img:
            self.char_icon = self.canvas.create_image(self.positions[0]+30, 220, image=self.char_img, tag="char")
        else:
            self.char_icon = self.canvas.create_oval(self.positions[0], 200, self.positions[0]+40, 240, fill="blue", tag="char")

    def update_character_position(self, x):
        self.canvas.coords(self.char_icon, x + 30, 220)

    def search_common(self, search_func):
        arr, target = self.parse_input()
        if arr is None: return
        self.draw_map(arr)
        start = time.time()
        index, comparisons = search_func(arr, target)
        elapsed = (time.time() - start) * 1000
        if index != -1:
            play_sound("Sounds/treasure_found.mp3")
            self.treasure_icon = self.canvas.create_image(self.positions[index]+30, 220, image=self.treasure_img)
        else:
            play_sound("Sounds/wrong_move.wav")
        return index, comparisons, elapsed

    def run_brute_force(self):
        def brute_force(arr, target):
            comparisons = 0
            for i in range(len(arr)):
                self.update_character_position(self.positions[i])
                play_sound("Sounds/step.wav")
                self.canvas.update()
                time.sleep(0.3)
                comparisons += 1
                if arr[i] == target:
                    return i, comparisons
            return -1, comparisons
    
        index, comp, elapsed = self.search_common(brute_force)
    
        if comp == 1:
            complexity = "O(1) - Best Case"
        else:
            complexity = f"O(n) - Worst Case ({comp} comparisons)"
    
        self.result_label.config(
            text=f"🎯 Brute Force: Index {index}, Comparisons {comp}, Time {elapsed:.2f}ms\n⏱️ Time Complexity: {complexity}"
        )
    
    def run_binary_search(self):
        def binary_search(arr, target):
            low, high = 0, len(arr) - 1
            comparisons = 0
            while low <= high:
                mid = (low + high) // 2
                self.update_character_position(self.positions[mid])
                play_sound("Sounds/step.wav")
                self.canvas.update()
                time.sleep(0.3)
                comparisons += 1
                if arr[mid] == target:
                    return mid, comparisons
                elif arr[mid] < target:
                    low = mid + 1
                else:
                    high = mid - 1
            return -1, comparisons
    
        index, comp, elapsed = self.search_common(binary_search)
    
        if comp == 1:
            complexity = "O(1) - Best Case"
        else:
            complexity = f"O(log n) - Approx. ({comp} comparisons)"
    
        self.result_label.config(
            text=f"🧠 Binary Search: Index {index}, Comparisons {comp}, Time {elapsed:.2f}ms\n⏱️ Time Complexity: {complexity}"
        )

# Run game
if __name__ == "__main__":
    root = tk.Tk()
    app = TreasureHuntApp(root)
    root.mainloop()
