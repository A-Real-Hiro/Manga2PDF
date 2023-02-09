"""
HiroComic2PDF:
Used for converting .cbz files to .pdf files but with an easier GUI format

README contains more information regarding this project.
"""
import tkinter as tk
import tkinter.messagebox as msgbox
import os, zipfile
from PIL import Image

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.cbz_path = ""

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

    def toZip(self, inFile, pathForPDF):
        zip_ref = zipfile.ZipFile(pathForPDF + f"\\{inFile}", 'r')
        new_dir = pathForPDF + f"\\temp\\" + inFile.replace('.cbz','').rstrip()
        zip_ref.extractall(path=new_dir)
        zip_ref.close()
        newPDF = pathForPDF + "\\" + inFile.replace('.cbz','.pdf')
        self.zipToPDF(newPDF,new_dir)


    def zipToPDF(self, newFileName, newPath):
        print(f"New name: {newFileName} New Path: {newPath}")
        
        chapter_folder = os.listdir(newPath)[0]
        chapters = os.listdir(newPath + f"\\{chapter_folder}")
        img_paths = []
        for folder in chapters:
            imgFileNames = [file for file in os.listdir(newPath + f"\\{chapter_folder}\\{folder}") if '.jpg' or '.png' in file]
            imgPath = newPath + f"\\{chapter_folder}\\{folder}"
            for file in imgFileNames:
                img_paths.append(imgPath + f"\\{file}")
        # sorts the images into order
        img_paths.sort()
        # opens the images in a list
        images = []
        images = [Image.open(img_path) for img_path in img_paths]
        images[0].save(newFileName, "PDF", resolution=100.0, save_all=True, append_images=images[1:])



    def toPDF(self, files: list, pathForPDF):
        for file in files:
            self.toZip(file, pathForPDF)
        


    def convert(self):
        self.cbz_path = self.textEntryContent.get()
        self.cbz_path.replace("/", "\\")
        print(f"cbz_path: {self.cbz_path}")
        print(os.path.exists(self.cbz_path))
        # tests if the path is valid
        if os.path.exists(self.cbz_path):
            msgbox.showinfo(title = "Success!", message = "Valid path selected! Verifying presence of cbz files...")
            fToConvert = 0

            for fname in os.listdir(self.cbz_path):
                if '.cbz' in fname: fToConvert += 1
            if fToConvert == 0:
                msgbox.showerror(title = "ERROR", message = f"No CBZ files to convert in {self.cbz_path}")
                return
            
            msgbox.showinfo(title = "Files Found!", message = f"{fToConvert} CBZ files found in {self.cbz_path}")
            # switches over to the file path where all the cbz files are located
            self.toPDF({file for file in os.listdir(self.cbz_path) if '.cbz' in file}, self.cbz_path)
            msgbox.showinfo(title="Success!", message = "All .cbz files in path were converted to PDFs! Happy reading!")

        else:
            # case where valid path was not entered        
            msgbox.showerror(title = "ERROR", message = "Please enter a valid file path.")
        
        return
        

# configures the window
window = tk.Tk()
window.title('CBZ to PDF')
window.geometry("400x100")

app = App(window)

""" Makes the window actually appear """
app.mainloop()