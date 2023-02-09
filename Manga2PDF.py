"""
HiroComic2PDF:
Used for converting .cbz files to .pdf files but with an easier GUI format

README contains more information regarding this project.
"""
import tkinter as tk
import tkinter.messagebox as msgbox
import os, zipfile
import PIL

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

    def toZip(self, inFile, pathForPDF):
        zip_ref = zipfile.ZipFile(pathForPDF + f"\\{inFile}", 'r')
        new_dir = pathForPDF + f"\\temp\\{str(inFile[:-4]).rstrip()}\\"
        zip_ref.extractall(path=new_dir)
        zip_ref.close()
        newPDF = inFile.replace(inFile[:-4],".pdf")
        self.zipToPDF(newPDF,new_dir)
        # changes file extensions of new files
        #newFile = inFile.replace(inFile[-4:],'.pdf')


    def zipToPDF(self, newFileName, newPath):
        print(f"New name: {newFileName} New Path: {newPath}")
        chapters = os.listdir(newPath)

        for folder in chapters:
            for file in os.listdir(newPath + f"\\{folder}"):


    def toPDF(self, files: list, pathForPDF):
        for file in files:
            self.toZip(file, pathForPDF)
        


    def convert(self):
        cbz_path = self.textEntryContent.get()
        cbz_path.replace("/", "\\")
        print(f"cbz_path: {cbz_path}")
        print(os.path.exists(cbz_path))
        # tests if the path is valid
        if os.path.exists(cbz_path):
            msgbox.showinfo(title = "Success!", message = "Valid path selected! Verifying presence of cbz files...")
            fToConvert = 0

            for fname in os.listdir(cbz_path):
                if '.cbz' in fname: fToConvert += 1
            if fToConvert == 0:
                msgbox.showerror(title = "ERROR", message = f"No CBZ files to convert in {cbz_path}")
                return
            
            msgbox.showinfo(title = "Files Found!", message = f"{fToConvert} CBZ files found in {cbz_path}")
            # switches over to the file path where all the cbz files are located
            self.toPDF({file for file in os.listdir(cbz_path) if '.cbz' in file}, cbz_path)

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