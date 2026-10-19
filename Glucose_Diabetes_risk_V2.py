class GD_risk:
    parameters = {
    'FG': (100, 126),
    'PMG': (140, 200)
}
    def __init__(self,FG,PMG):
        self.FG = FG
        self.PMG = PMG

    def FG_check(self):
        FG_range = self.parameters['FG'] 
        if FG_range[0] <= self.FG < FG_range[1]:
            return 'PreDiabetic'
        elif self.FG >= FG_range[0]:
            return 'Diabetic'
        else:
            return 'Normal'

    def PMG_check(self):
        PMG_range = self.parameters['PMG']
        if PMG_range[0] <= self.PMG < PMG_range[1]:
            return 'PreDiabetic'
        elif self.PMG >= PMG_range[0]:
            return 'Diabetic'
        else:
            return 'Normal'
                    
    def combined_risk(self):
       if self.FG_check() == "Diabetic" or self.PMG_check() == "Diabetic":
        return "Diabetic"
       if self.FG_check() == "PreDiabetic" or self.PMG_check() == "PreDiabetic":
        return "PreDiabetic"
       return "Normal"
    
if __name__ == "__main__":
    FG = float(input('Enter FG: '))
    PMG = float(input('Enter PMG: '))      
    patients = GD_risk(FG,PMG)
    print(patients.FG_check())
    print(patients.PMG_check()) 
    print(patients.combined_risk())
