class photometrics_ez():
    #############################
    # functions
    #############################
    
    def __init__(self, objective, binning = 1, overlap = 0.):
        # setup objective
        self.allowed_objectives = {'10x':self.objective_10x, '20x':self.objective_20x, '40x':self.objective_40x, 'custom':self.objective_custom}
        assert objective in self.allowed_objectives.keys()
        self._objective = self.allowed_objectives[objective]()
        
        self.height = int(1040 / binning)
        self.width = int(1392 / binning)
        
        self.overlap = overlap
        self.overlap_y_sign = -1
        self.overlap_x_sign = -1
        
        self.pixel_size = 6.45
        self.pixel_to_um = self.pixel_size / self._objective.magnification * binning
        
    @property
    def increment_y(self):
        return self.height * self.pixel_to_um / self._objective.correction_factor
    
    @property
    def increment_x(self):
        return self.width * self.pixel_to_um / self._objective.correction_factor
    
    @property
    def overlap_y(self):
        return self.increment_y * self.overlap_y_sign * self.overlap
    
    @property
    def overlap_x(self):
        return self.increment_x * self.overlap_x_sign * self.overlap
    
    @property
    def movement_correction_y(self):
        return self._objective.movement_correction_y * self.pixel_to_um
    
    @property
    def movement_correction_x(self):
        return self._objective.movement_correction_x * self.pixel_to_um
    
    def generate_stage_pos(self, x1, y1, z1, columns, rows, base_name = 'Port_', port_name = None):
        self.init_stg()
        
        # generates stage positions
        stage_pos=[]
        for row in range(rows):
            for column in range(columns):
                pos_info = base_name + port_name + "-" + str(row+1) + "-" + str(column+1)
                pos_x = str(round(x1 + column * (self.increment_x + self.overlap_x) + (row) * self.movement_correction_x, 2))
                pos_y = str(round(y1 + row * (self.increment_y + self.overlap_y) + (column) * self.movement_correction_y, 2))
                pos_z = str(round(z1, 2))
                stage_pos.append(self.pos_format.format(pos_info = pos_info, pos_x = pos_x, pos_y = pos_y, pos_z  = pos_z))
        
        self.write_stg(stage_pos, base_name = base_name, port_name = port_name)
                                     
                       
    def init_stg(self):
        self.header='"Stage Memory List", Version 6.0\n 0, 0, 0, 0, 0, 0, 0, "microns", "microns"\n 0\n{}\n'
        self.pos_format = '"{pos_info}", {pos_x}, {pos_y}, {pos_z}, 0, {pos_z}, FALSE, -9999, TRUE, TRUE, 0, -1, ""\n'
        
    def write_stg(self, stage_pos, base_name = 'Port_', port_name = None):
        num_pos = len(stage_pos)
        with open(base_name + port_name + '.stg','w') as text: 
            text.writelines(self.header.format(num_pos))
            text.writelines(stage_pos)
            text.close
    
    #############################
    # objective classes
    #############################
    
    class objective_10x():
        def __init__(self):
            self.magnification = 10
            self.movement_correction_y = -8 # in pixels
            self.movement_correction_x = -8 
            self.correction_factor = 0.992
        
    class objective_20x():
        def __init__(self):
            self.magnification = 20
            self.movement_correction_y = -8 # in pixels
            self.movement_correction_x = -8
            self.correction_factor = 0.992
            
    class objective_40x():
        def __init__(self):
            self.magnification = 40
            self.movement_correction_y = 0 # in pixels
            self.movement_correction_x = 0 
            self.correction_factor = 1
            
    class objective_custom():
        def __init__(self):
            self.magnification_factor = float(input("Please input the magnification of the lens: "))
            self.use_default_correction = input("Use default magnification correction of 1.0 (y/n): ")
            
            self.movement_correction_y = 0 # in pixels
            self.movement_correction_x = 0 
            
            if self.use_default_correction.lower() == "y":
                self.correction_factor = 1
                
            else:
                self.correction_factor = float(input("Please input the correction factor of the lens: "))
                