import tkinter as tk

from data_preprocessing import process_data

from models import rule_based_predict, svc_5_predict, svc_10_predict, phobert_no_pred_predict, phobert_5_pred_predict, phobert_10_pred_predict

model_dict = {
    "Rule-based": rule_based_predict, 
    "SVC_5_freq": svc_5_predict, 
    "SVC_10_freq": svc_10_predict, 
    "PhoBert_no_freq": phobert_no_pred_predict, 
    "PhoBert_5_freq": phobert_5_pred_predict, 
    "PhoBert_10_freq": phobert_10_pred_predict
}

tags_dict = {
    1: "Romance",
    2: "Drama",
    3: "Fantasy",
    4: "LGBT",
    5: "Comedy",
    6: "Modern",
    7: "Classics",
    8: "Novel"
}

def generate_output():
    title = title_box.get("1.0", "end-1c")  
    description = description_box.get("1.0", "end-1c") 

    combine = title + " " + description

    processed_text = process_data(combine)

    mode = mode_var.get()  # Get the selected mode
    mode_of_model = model_mode.get()

    output, threshold = model_dict[mode_of_model](processed_text)
    
    if mode == "Text Only":
        output_bool = [output_each >= threshold_each for output_each, threshold_each in zip(output, threshold)]
        output_list = [tags_dict[index + 1] for index, print_bool in enumerate(output_bool) if print_bool]
        # Display input text in the output textbox
        output_textbox.config(state=tk.NORMAL)  # Enable editing
        output_textbox.delete("1.0", tk.END)  # Clear previous output
        output_textbox.insert(tk.END, ", ".join(output_list))  # Insert input text
        output_textbox.config(state=tk.DISABLED)  # Disable editing
    elif mode == "Probability Only":
        for i in range(8):
            prob_textboxes[i].config(state=tk.NORMAL)  # Enable editing
            prob_textboxes[i].delete("1.0", tk.END)  # Clear previous output
            prob_textboxes[i].insert(tk.END, "Tag {}: {:.4f}".format(tags_dict[i + 1], output[i]))  # Insert new output
            prob_textboxes[i].config(state=tk.DISABLED)  # Disable editing

def change_layout(event):
    mode = mode_var.get()  # Get the selected mode

    if mode == "Text Only":
        output_textbox.pack()

        for i in range(8):
            prob_textboxes[i].pack_forget()
    elif mode == "Probability Only":
        output_textbox.pack_forget()

        for i in range(8):
            prob_textboxes[i].pack()

# Create main window
root = tk.Tk()
root.title("Output Mode Selector")

# Create input textbox
title_title = tk.Label(root, text = "Title")
title_title.pack()
title_box = tk.Text(root, height=1, width=50)
title_box.pack(pady=10)

description_title = tk.Label(root, text = "Description")
description_title.pack()
description_box = tk.Text(root, height=5, width=50)
description_box.pack(pady=10)

# Create mode selection option
mode_var = tk.StringVar()
mode_var.set("Text Only")  # Default mode
mode_option_menu = tk.OptionMenu(root, mode_var, "Text Only", "Probability Only", command=change_layout)
mode_option_menu.pack()

# Create model selection
model_mode = tk.StringVar()
model_mode.set("PhoBert_no_freq")  # Default mode
model_model_menu = tk.OptionMenu(root, model_mode, "PhoBert_no_freq", "PhoBert_5_freq", "PhoBert_10_freq")
model_model_menu.pack()

# Create submit button
submit_button = tk.Button(root, text="Submit", command=generate_output)
submit_button.pack()

# Create output textbox
output_textbox = tk.Text(root, height=5, width=50, state=tk.DISABLED)
output_textbox.pack(pady=10)

# Create output textboxes for probabilities
prob_textboxes = []
for i in range(8):
    prob_box = tk.Text(root, height=1, width=30, state=tk.DISABLED)
    #prob_box.pack(pady=5)
    prob_textboxes.append(prob_box)

# Run the GUI
root.mainloop()