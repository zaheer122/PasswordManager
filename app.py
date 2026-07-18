import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Password Manager")
app.geometry("900x600")

label = ctk.CTkLabel(
    app,
    text="Password Manager",
    font=("Arial", 28, "bold")
)

label.pack(pady=40)

app.mainloop()