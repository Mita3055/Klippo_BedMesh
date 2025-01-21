import pandas as pd
import numpy as np
import klippo
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

   
   
    ## make sure printer is hommed on slide surfase 
    ## restrict probe area to the slide
    ## create a 3d flat surface from the probe data
    ## using 3d surphase solve for Z offset for the print surface


class BedMesh:
    def __init__(self, originx, originy, stopx, stopy, stepx, stepy, printer):
        self.originx = originx
        self.originy = originy
        self.stopx = stopx
        self.stopy = stopy
        self.stepx = stepx
        self.stepy = stepy
        self.probeData = []
        self.meshData = None
        self.mesh = None
        self.printer = printer  # klippo_serial object
        
        mesh_table = self.probe_sequence()
        self.mesh = self.makeMesh(mesh_table)


    def parse_probe_response(response):
    #ask chatgbt how to do this part
        output = [] # Output is an array consisting of the cordinates of the bed mesh in [X, Y, Z1, Z2, Z3] format all in mm all floats values
        return output

    def probe_sequence(self):
        self.printer.home()
        self.printer.absolute()
    

        x_points = np.arange(self.originx, self.stopx + self.stepx, self.stepx)
        y_points = np.arange(self.originy, self.stopy + self.stepy, self.stepy)
        
        for x in x_points:
            for y in y_points:
                self.printer.moveTo(x, y, 0)
                response = self.probe()
                probeOut = self.parse_probe_response(response)
                self.probeData.append(probeOut)

        meshData = pd.DataFrame(self.probeData, columns=['X', 'Y', 'Z1', 'Z2', 'Z3'])

        return meshData
        

    def makeMesh(self, meshData):

        # Average Z1, Z2, Z3 to get a single Z value for each X, Y pair
        meshData['Z'] = meshData[['Z1', 'Z2', 'Z3']].mean(axis=1)
        
        # Create a pivot table to reshape the data for 3D surface plotting
        mesh_table = meshData.pivot_table(index='Y', columns='X', values='Z')
        # Create grid coordinates for interpolation
        x = mesh_table.columns.values
        y = mesh_table.index.values
        X, Y = np.meshgrid(x, y)
        Z = mesh_table.values

        # Interpolate to create a smooth surface
        xi = np.linspace(x.min(), x.max(), 100)
        yi = np.linspace(y.min(), y.max(), 100)
        XI, YI = np.meshgrid(xi, yi)
        ZI = griddata((X.flatten(), Y.flatten()), Z.flatten(), (XI, YI), method='cubic')

        # Plotting 3D surface
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(XI, YI, ZI, cmap='viridis')

        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        plt.show()

        return ZI
    
    def get_z_at(self, x, y):
        if self.mesh is None: ### 
            raise ValueError("Mesh data is not available. Please run probe_sequence first.")
        
        # Create grid coordinates for interpolation
        x_coords = self.mesh.columns.values
        y_coords = self.mesh.index.values
        X, Y = np.meshgrid(x_coords, y_coords)
        Z = self.mesh.values

        # Interpolate to find the Z value at the given (x, y) coordinates
        z_value = griddata((X.flatten(), Y.flatten()), Z.flatten(), (x, y), method='cubic')
        
        return z_value
    

    def save_mesh(self):
        if __name__ == "__main__":
            probeX = 10  # Define the number of probe points in X direction
            probeY = 10  # Define the number of probe points in Y direction

            bed_mesh = BedMesh(probeX, probeY)
            mesh_data = bed_mesh.probe_sequence()
            bed_mesh.mesh = mesh_data
            bed_mesh.save_mesh()
