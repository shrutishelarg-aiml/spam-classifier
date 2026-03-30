import tkinter as tk
from tkinter import messagebox

# -----------------------------
# Data Structures & Logic Layer
# -----------------------------
class ShoppingCart:

    def __init__(self):
        self.cart = []          # List for items
        self.undo_stack = []    # Stack for undo
        self.item_map = {}      # Dictionary {item: {"price": x, "qty": y, "discount": z}}

    def add_item(self, item, price, qty=1, discount=0):
        """Add item with quantity & discount."""
        self.cart.append(item)
        self.item_map[item] = {"price": price, "qty": qty, "discount": discount}
        self.undo_stack.append(("add", item))

    def remove_item(self):
        """Remove last item."""
        if self.cart:
            removed_item = self.cart.pop()
            self.undo_stack.append(("remove", removed_item))
            self.item_map.pop(removed_item, None)
            return removed_item
        return None

    def undo(self):
        """Undo last action."""
        if self.undo_stack:
            action, item = self.undo_stack.pop()
            if action == "add" and item in self.cart:
                self.cart.remove(item)
                self.item_map.pop(item, None)
            elif action == "remove":
                # Re-add item if removed
                if item not in self.cart:
                    self.cart.append(item)

    def calculate_total(self):
        """Calculate total with discounts applied."""
        total = 0
        for item, details in self.item_map.items():
            price, qty, discount = details["price"], details["qty"], details["discount"]
            total += (price * qty) - discount
        return total

    def get_items(self):
        """Return items with details."""
        return [(item, details) for item, details in self.item_map.items()]


# -----------------------------
# GUI Layer (Tkinter)
# -----------------------------
class ShoppingCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛒 Shopping Cart System")
        self.root.configure(bg="#f0f8ff")  # Light blue background(hex code for alice Blue)

        # Connect to logic layer
        self.cart_system = ShoppingCart()

        # --- Input Fields ---
        tk.Label(root, text="Item Name:", bg="#f0f8ff", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.item_entry = tk.Entry(root, font=("Arial", 12))
        self.item_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Price:", bg="#f0f8ff", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(root, font=("Arial", 12))
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Quantity:", bg="#f0f8ff", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.qty_entry = tk.Entry(root, font=("Arial", 12))
        self.qty_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Discount:", bg="#f0f8ff", font=("Arial", 12, "bold")).grid(row=3, column=0, padx=5, pady=5)
        self.discount_entry = tk.Entry(root, font=("Arial", 12))
        self.discount_entry.grid(row=3, column=1, padx=5, pady=5)

        # --- Buttons ---
        tk.Button(root, text="➕ Add Item", command=self.add_item, bg="#32cd32", fg="white", font=("Arial", 12, "bold")).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(root, text="➖ Remove Item", command=self.remove_item, bg="#ff6347", fg="white", font=("Arial", 12, "bold")).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(root, text="↩ Undo", command=self.undo, bg="#ffa500", fg="white", font=("Arial", 12, "bold")).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(root, text="💳 Checkout", command=self.checkout, bg="#4682b4", fg="white", font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=2, pady=10)

        # --- Cart Display ---
        self.cart_display = tk.Listbox(root, width=50, height=10, font=("Courier New", 12))
        self.cart_display.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    # --- Event Handlers ---
    def add_item(self):
        item = self.item_entry.get()
        price = self.price_entry.get()
        qty = self.qty_entry.get()
        discount = self.discount_entry.get()

        if item and price.isdigit() and qty.isdigit() and discount.isdigit():
            self.cart_system.add_item(item, int(price), int(qty), int(discount))
            self.update_display()
        else:
            messagebox.showwarning("Input Error", "Enter valid item, price, quantity, and discount")

    def remove_item(self):
        removed = self.cart_system.remove_item()
        if removed:
            self.update_display()
        else:
            messagebox.showwarning("Cart Empty", "No items to remove")

    def undo(self):
        self.cart_system.undo()
        self.update_display()

    def checkout(self):
        total = self.cart_system.calculate_total()
        if total > 0:
            messagebox.showinfo("Checkout", f"🎉 Total Bill: ₹{total}")
        else:
            messagebox.showinfo("Checkout", "Cart is empty")

    def update_display(self):
        self.cart_display.delete(0, tk.END)
        for item, details in self.cart_system.get_items():
            self.cart_display.insert(
                tk.END,
                f"{item} | Price: ₹{details['price']} | Qty: {details['qty']} | Discount: ₹{details['discount']}"
            )


# -----------------------------
# Main Entry Point
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingCartApp(root)
    root.mainloop()
