"""
HiroComic2PDF:
Used for converting .cbz files to .pdf files but with an easier GUI format

README contains more information regarding this project.
"""
import tkinter as tk
import tkinter.messagebox as msgbox

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.entryBox = tk.Entry()
        self.label = tk.Label(text="Please enter the file path for where your .cbz files:")
        self.label.pack()
        self.entryBox.pack()

        # Create the application variable.
        self.textEntryContent = tk.StringVar()
        # set 
        self.textEntryContent.set("Enter directory here for conversion")
        # Tell the entry widget to watch this variable.
        self.entryBox["textvariable"] = self.textEntryContent

        # When the user hits return on the entry box, the approproate variable is changed to track what they have entered
        self.entryBox.bind('<Key-Return>',
                             self.textEntryContent,set(self.entryBox["textvariable"]))

        # CONVERT BUTTON

        self.btnConvert = tk.Button(master, text = "Convert", command = self.convert)
        self.btnConvert.pack()

    def convert(self):
        cbz_path = self.textEntryContent

        if (cbz_path is None or "Enter directory here for conversion"):
            msgbox.showerror(title = "ERROR", message = "Please enter a valid file path.")
        print(f"The button was pressed with cbz_path as {cbz_path}")

# configures the window
window = tk.Tk()
window.title('CBZ to PDF')
window.geometry("400x100")

app = App(window)

""" Makes the window actually appear """
app.mainloop()