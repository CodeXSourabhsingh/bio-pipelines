class PK_Dosage:
    VD_TABLE = {
    'Warfarin':     0.14,
    'Digoxin':      7.0,
    'Theophylline': 0.5,
    'Gentamicin':   0.25,
    'Metformin':    1.0,
}
    def __init__ (self,weight,half_life,target_concentration,drug):
        self.weight = weight
        self.half_life = half_life
        self.target_concentration = target_concentration
        self.drug = drug
        if drug not in self.VD_TABLE:
            raise ValueError(f"drug '{drug}' not in the table ")
        
    def vd(self):
        vd = self.weight * self.VD_TABLE[self.drug]
        return vd
    def ld(self):
        ld = self.vd()*self.target_concentration
        return ld
    def md(self):
        k = 0.693/self.half_life
        md = k * self.vd() * self.target_concentration * 12
        return md
    def steady_state(self):
        ss = 5 * self.half_life
        return ss
    
if __name__ == "__main__":
    weight = float(input('Enter weight: '))
    half_life = float(input('Enter half_life: '))
    target_concentration = float(input('Enter target_concentration:  '))
    drug = input('Enter drug: ').strip().title()

    pk = PK_Dosage(weight,half_life,target_concentration,drug)

    print(f"VD: {pk.vd():.2F} L")
    print(f"ld: {pk.ld():.2f} mg")
    print(f"md: {pk.md():.2f} mg")
    print(f"steady_state: {pk.steady_state():.1f} h")
        
        
     
    

   


