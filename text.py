import tkinter as tk
from tkinter import messagebox, scrolledtext
from heapq import heappush, heappop, heapify
from collections import Counter

# ------------------- Node Class -------------------
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


# ------------------- Huffman Logic -------------------
class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.reverse_map = {}

    def build_tree(self, text):
        freq = Counter(text)
        heap = [Node(ch, fr) for ch, fr in freq.items()]
        heapify(heap)

        while len(heap) > 1:
            left = heappop(heap)
            right = heappop(heap)
            merged = Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heappush(heap, merged)

        return heap[0] if heap else None

    def generate_codes(self, node, current_code=""):
        if node is None:
            return
        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_map[current_code] = node.char
            return
        self.generate_codes(node.left, current_code + "0")
        self.generate_codes(node.right, current_code + "1")

    def encode(self, text):
        if not text:
            return "", None
        root = self.build_tree(text)
        self.generate_codes(root)
        encoded_text = "".join(self.codes[ch] for ch in text)
        return encoded_text, root

    def decode(self, encoded_text):
        if not encoded_text:
            return ""
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_map:
                decoded_text += self.reverse_map[current_code]
                current_code = ""
        return decoded_text


# ------------------- GUI Class -------------------
class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Text Compression & Decompression")
        self.root.geometry("850x650")
        self.huffman = HuffmanCoding()

        # --- GUI Elements ---
        tk.Label(root, text="Enter text to compress:", font=("Arial", 12, "bold")).pack(pady=10)
        self.text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=8, font=("Courier", 10))
        self.text_input.pack()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Compress", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white",
                  command=self.compress).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Decompress", font=("Arial", 11, "bold"), bg="#2196F3", fg="white",
                  command=self.decompress).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Clear Output", font=("Arial", 11, "bold"), bg="#f44336", fg="white",
                  command=self.clear_output).grid(row=0, column=2, padx=10)

        tk.Label(root, text="Output:", font=("Arial", 12, "bold")).pack(pady=10)
        self.output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=15, font=("Courier", 10))
        self.output_box.pack()

        # Internal variables
        self.encoded_text = ""
        self.decoded_text = ""

    # --- Button Functions ---
    def compress(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to compress.")
            return

        encoded_text, _ = self.huffman.encode(text)
        self.encoded_text = encoded_text

        # Calculate compression ratio
        if len(text) > 0:
            ratio = (1 - (len(encoded_text) / (len(text) * 8))) * 100
        else:
            ratio = 0

        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, f"Original Text:\n{text}\n\n")
        self.output_box.insert(tk.END, f"Huffman Codes:\n{self.huffman.codes}\n\n")
        self.output_box.insert(tk.END, f"Encoded Bitstring:\n{encoded_text}\n\n")
        self.output_box.insert(tk.END, f"Compression Ratio: {ratio:.2f}%\n\n")

        messagebox.showinfo("Compression Complete", "✅ Text compressed successfully!")

    def decompress(self):
        if not self.encoded_text:
            messagebox.showwarning("Warning", "Please compress text before decompressing.")
            return

        decoded_text = self.huffman.decode(self.encoded_text)
        self.decoded_text = decoded_text

        self.output_box.insert(tk.END, f"Decoded Text:\n{decoded_text}\n\n")
        messagebox.showinfo("Decompression Complete", "✅ Text decompressed successfully!")

    def clear_output(self):
        self.output_box.delete("1.0", tk.END)
        self.text_input.delete("1.0", tk.END)
        self.huffman = HuffmanCoding()
        self.encoded_text = ""
        self.decoded_text = ""
        messagebox.showinfo("Cleared", "🧹 All fields cleared successfully!")


# ------------------- Run Application -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
