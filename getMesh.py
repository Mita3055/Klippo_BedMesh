import pandas as pd
import numpy as np
import klippo

probeX = [30, 30, 30, 30, 30, 30, 60, 60, 60, 60, 60, 60]
probeY = [30, 40, 50, 50, 70, 80, 30, 40, 50, 50, 70, 80]

class BedMesh:
    def __init__(self, probeX, probeY):
        self.probeX = probeX
        self.probeY = probeY
        self.mesh = None
        self.printer = klippo.klippo_serial(port='COM3')  # Replace 'COM3' with your printer's port
        self.printer.connect()


    def parse_probe_response(response):
    #ask chatgbt how to do this part
        output = [] # Output is an array consisting of the cordinates of the bed mesh in [X, Y, Z1, Z2, Z3] format all in mm all floats values
        return output

    def probe_sequence(self):
        self.printer.home()
        self.printer.absolute()
        data = []

        for x, y in zip(self.probeX, self.probeY):
            self.printer.moveTo(x, y, 0)
            response = self.probe()
            probeOut = self.parse_probe_response(response)
            data.append(probeOut)

        meshData = pd.DataFrame(data, columns=['X', 'Y', 'Z1', 'Z2', 'Z3'])
        return meshData
    

    def prosess_mesh(self):
        ## process the mesh data to get a 3d surface
        return 0
    
    
    ## make sure printer is hommed on slide surfase 
    ## restrict probe area to the slide
    ## create a 3d flat surface from the probe data
    ## using 3d surphase solve for Z offset for the print surface

    def save_mesh(self):
        self.mesh.to_csv('mesh.csv', index=False)
