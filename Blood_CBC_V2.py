class CBC_Analyzer:
    parameters = {
    'hb': {'M': (13.5, 17.5), 'F': (12.0, 15.5)},
    'WBC': (4.0, 11.0),
    'Platelets': (150, 450)
}

    def __init__(self, sex, hb, WBC, Platelets):
        self.sex = sex
        self.hb = hb
        self.WBC = WBC
        self.Platelets = Platelets
    def hb_check(self):
        if self.sex in ['M', 'F']:
            hb_range = self.parameters['hb'][self.sex]
            if hb_range[0] <= self.hb <= hb_range[1]:
                return('hb: Normal range')
            elif self.hb < hb_range[0]:
                return('hb below low: Anemia')
            else:
                return('hb above high: Polycythemia')
               
    def WBC_check(self):
        wbc_range = self.parameters['WBC']
        if wbc_range[0] <= self.WBC <= wbc_range[1]:
            return('WBC: Normal range')
        elif self.WBC < wbc_range[0]:
            return('WBC below low: Leukopenia')
        else:
            return('WBC above high: Leukocytosis')
           
    def Platelets_check(self):
        platelets_range = self.parameters['Platelets']
        if platelets_range[0] <= self.Platelets <= platelets_range[1]:
            return('Platelets: Normal range')
        elif self.Platelets < platelets_range[0]:
            return('Platelets below low: Thrombocytopenia')
        else:
            return('Platelets above high: Thrombocytosis')

if __name__ == "__main__":

   sex = input('sex(M/F): ').upper().strip()
   hb = float(input('hb: '))
   WBC = float(input('WBC: '))
   Platelets = float(input('Platelets: '))

   patient = CBC_Analyzer(sex, hb, WBC, Platelets)
   print(patient.hb_check())
   print(patient.WBC_check())
   print(patient.Platelets_check())



