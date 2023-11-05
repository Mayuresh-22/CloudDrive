# make scrollabel frame in customtkinter

import customtkinter as ctk

root = ctk.CTk()

frame = ctk.CTkFrame(root, width=500, height=500)
frame.pack()

scrollable_frame = ctk.CTkScrollableFrame(frame, width=500, height=500)

for i in range(50):
    ctk.CTkLabel(scrollable_frame, text=f"Label {i}").pack()

scrollable_frame.pack()

root.mainloop()
