import tkinter as tk


MENU_BIG_FONTS = 'TkDefaultFont 14'

class Configuration(tk.Toplevel):
    def __init__(self, root):
        super(Configuration, self).__init__()
        root.gameTypeVar = tk.IntVar()
        root.shapeL = tk.IntVar()
        root.shapeO = tk.IntVar()
        root.shapeI = tk.IntVar()
        root.shapeS = tk.IntVar()
        root.shapeT = tk.IntVar()
        root.shapeZ = tk.IntVar()
        root.shapeJ = tk.IntVar()
        photoL = tk.PhotoImage(file='images/L.png')
        photoO = tk.PhotoImage(file='images/O.png')
        photoI = tk.PhotoImage(file='images/I.png')
        photoS = tk.PhotoImage(file='images/S.png')
        photoT = tk.PhotoImage(file='images/T.png')
        photoZ = tk.PhotoImage(file='images/Z.png')
        photoJ = tk.PhotoImage(file='images/J.png')


        # Toplevel window for configuration
        self.focus_set()
        self.grab_set()
        self.title='Configurations'


        # Dimensions frame
        self.dimensionsFrame = tk.Frame(self,
                                        borderwidth=2, relief=tk.GROOVE,
                                        padx=10, pady=10)
        self.dimensionsFrame.grid(row=0, column=0)
        self.dimensionLabel = tk.Label(self.dimensionsFrame,
                                       font=MENU_BIG_FONTS,
                                       text='Dimensions')
        self.dimensionLabel.grid(row=0, column=0, columnspan=2)
        self.heightLabel = tk.Label(self.dimensionsFrame, text='Height:')
        self.heightLabel.grid(row=1, sticky=tk.W)
        self.widthLabel = tk.Label(self.dimensionsFrame, text='Width:')
        self.widthLabel.grid(row=2, sticky=tk.W)
        self.boxSizeLabel= tk.Label(self.dimensionsFrame, text='Box Size:')
        self.boxSizeLabel.grid(row=3, sticky=tk.W)
        self.heightSpin = tk.Spinbox(self.dimensionsFrame, from_=10, to=40,
                                     width=3)
        self.heightSpin.grid(row=1, column=1)
        self.widthSpin = tk.Spinbox(self.dimensionsFrame, from_=6, to=30,
                                    width=3)
        self.widthSpin.grid(row=2, column=1)
        self.boxSizeSpin = tk.Spinbox(self.dimensionsFrame, from_=10, to=100,
                                      width=3)
        self.boxSizeSpin.grid(row=3, column=1)

        # Game type frame
        self.gameTypeFrame = tk.Frame(self,
                                      borderwidth=2, relief=tk.GROOVE,
                                      padx=10, pady=10)
        self.gameTypeFrame.grid(row=1, column=0)
        self.gameLabel = tk.Label(self.gameTypeFrame,
                                  font=MENU_BIG_FONTS,
                                  text='Game Type')
        self.gameLabel.grid(row=0)
        self.normalGameRadio = tk.Radiobutton(self.gameTypeFrame,
                                              text='Normal',
                                              variable=root.gameTypeVar,
                                              value=1)
        self.normalGameRadio.grid(row=1, sticky=tk.W)
        self.pausedGameRadio= tk.Radiobutton(self.gameTypeFrame,
                                              text='Paused',
                                              variable=root.gameTypeVar,
                                              value=2)
        self.pausedGameRadio.grid(row=2, sticky=tk.W)
        self.changeSpeedGameRadio= tk.Radiobutton(self.gameTypeFrame,
                                              text='Change Speed',
                                              variable=root.gameTypeVar,
                                              value=3)
        self.changeSpeedGameRadio.grid(row=3, sticky=tk.W)


        # Select shapes frame
        self.selectShapesFrame = tk.Frame(self,
                                          borderwidth=2, relief=tk.GROOVE,
                                          padx=10, pady=10)
        self.selectShapesFrame.grid(row=0, column=1, rowspan=2)
        self.selectLabel = tk.Label(self.selectShapesFrame,
                                    text='Select Shapes', font=MENU_BIG_FONTS)
        self.selectLabel.grid(row=0, column=0)

        self.L_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoL,
                                      variable=root.shapeL, onvalue=1,
                                      offvalue=0)
        self.L_check.image = photoL
        self.L_check.grid(row=1, column=0)

        self.J_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoJ,
                                      variable=root.shapeJ, onvalue=1,
                                      offvalue=0)
        self.J_check.image = photoJ
        self.J_check.grid(row=2, column=0)

        self.O_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoO,
                                      variable=root.shapeO, onvalue=1,
                                      offvalue=0)
        self.O_check.image = photoO
        self.O_check.grid(row=3, column=0)

        self.I_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoI,
                                      variable=root.shapeI, onvalue=1,
                                      offvalue=0)
        self.I_check.image = photoI
        self.I_check.grid(row=4, column=0)

        self.Z_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoZ,
                                      variable=root.shapeZ, onvalue=1,
                                      offvalue=0)
        self.Z_check.image = photoZ
        self.Z_check.grid(row=5, column=0)

        self.S_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoS,
                                      variable=root.shapeS, onvalue=1,
                                      offvalue=0)
        self.S_check.image = photoS
        self.S_check.grid(row=6, column=0)

        self.T_check = tk.Checkbutton(self.selectShapesFrame,
                                      image=photoT,
                                      variable=root.shapeT, onvalue=1,
                                      offvalue=0)
        self.T_check.image = photoT
        self.T_check.grid(row=7, column=0)

        # Submit button
        self.resultFrame = tk.Frame(self,
                                          borderwidth=2, relief=tk.GROOVE,
                                          padx=10, pady=10)
        self.resultFrame.grid(row=2, column=0, rowspan=2)
        cancelButton = tk.Button(self.resultFrame, text='Cancel',
                                 command=self.destroy)
        cancelButton.grid(column=0, row=0)
        submitButton = tk.Button(self.resultFrame, text='Submit',
                                      command=self.destroy)
        submitButton.grid(column=1, row=0)