"""
HiroComic2PDF:
Used for converting .cbz files to .pdf files but with an easier GUI format

README contains more information regarding this project.
"""
import tkinter as tk
import tkinter.messagebox as msgbox
import os
import zipfile
import shutil
from PIL import Image

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.images = []
        self.img_path = ""
        self.pack()
        self.cbz_path = ""

        self.entryBox = tk.Entry(justify="center")
        self.label = tk.Label(text="Please enter the file path for where your .cbz files:")
        self.label.pack()
        self.entryBox.pack()

        # Create the application variable.
        self.textEntryContent = tk.StringVar()
        # set 
        self.textEntryContent.set("Enter directory here")
        # Tell the entry widget to watch this variable.
        self.entryBox["textvariable"] = self.textEntryContent

        # When the user hits return on the entry box, the approproate variable is changed to track what they have entered
        self.entryBox.bind('<Key-Return>',
                             self.textEntryContent,set(self.entryBox["textvariable"]))

        # CONVERT BUTTON
        self.btnConvert = tk.Button(master, text = "Convert", command = self.convert, justify = "center")
        self.btnConvert.pack()

    def toZip(self, inFile, pathForPDF):
        zip_ref = zipfile.ZipFile(pathForPDF + f"\\{inFile}", 'r')
        new_dir = pathForPDF + f"\\temp\\" + inFile.replace('.cbz','').rstrip()
        zip_ref.extractall(path=new_dir)
        zip_ref.close()
        newPDF = pathForPDF + "\\" + inFile.replace('.cbz','.pdf')
        self.zip_to_pdf(newPDF,new_dir)

    def clean_dir(self):
        # clears out the temp file
        shutil.rmtree(self.cbz_path + "\\temp\\")

        cbzFiles = os.listdir(self.cbz_path)
        for file in cbzFiles:
            if '.cbz' in file:
                os.remove(self.cbz_path + f"\\{file}")

    def collect_images(self, path):
        for item in os.listdir(path):
            itempath = os.path.join(path, item)
            _, extn = os.path.splitext(item.lower())
            if os.path.isdir(itempath):
                yield from self.collect_images(itempath)
            elif extn in (".jpg", ".jpeg", ".png"):
                img = Image.open(itempath)
                img.save(itempath, dpi=(96, 96))
                print(f"{itempath} saved...")
                yield img

    def zip_to_pdf(self, newPDFName, extractedPath):
        print(f"New name for file: {newPDFName} Path to extracted: {extractedPath}")
        print("Resetting list of images and image paths...")
        print("Finding folder with images to compress into pdf...")
        for _ in os.listdir(extractedPath):
            # gets paths of where to find images
            self.img_path = self.find_images(extractedPath)
        new_images = [*self.collect_images(self.img_path)]
        
        print(f"Saving images to {newPDFName}...")
        new_images[0].save(newPDFName, "PDF", resolution=100.0, save_all=True, append_images=new_images[1:])

        # close the file pointers
        for image in self.images:
            image.close()
        self.images.clear()
        new_images.clear()
        
    
    def find_images(self,currentPath) -> str:
        currentFiles = os.listdir(currentPath)
        for file in currentFiles:
            if '.png' in file or '.jpg' in file:
                return currentPath
            else:
                return self.find_images(currentPath + f"\\{file}")
    

    def toPDF(self, files: list, pathForPDF):
        sorted_files = sorted(files)
        for file in sorted_files:
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
            # clean up directory after finishing conversions
            msgbox.showinfo(title="Cleaning", message = "Cleaning the directory...")
            self.clean_dir()
        else:
            # case where valid path was not entered        
            msgbox.showerror(title = "ERROR", message = "Please enter a valid file path.")
            self.clean_dir()
        return
        

# configures the window
window = tk.Tk()
window.title('CBZ to PDF')
window.geometry("400x100")

app = App(window)

""" Makes the window actually appear """
app.mainloop()