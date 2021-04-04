class TrafficSign:
    def __init__(self):
        self.trafficSignArray = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0]

    def printingAllSigns(self):
        print("NL: ", self.trafficSignArray[0], 
              "NR: ", self.trafficSignArray[1],
              "LF: ", self.trafficSignArray[2],
              "LR: ", self.trafficSignArray[3],
              "TL: ", self.trafficSignArray[4],
              "TR: ", self.trafficSignArray[5],
              "CL: ", self.trafficSignArray[6],
              "PI: ", self.trafficSignArray[7],
              "PO: ", self.trafficSignArray[8],
              "TLight: ", self.trafficSignArray[9],
              "ST: ", self.trafficSignArray[10])

    def notLeftStatus(self):
        return self.trafficSignArray[0]
    
    def notRightStatus(self):
        return self.trafficSignArray[1]
    
    def leftAndForwardStatus(self):
        return self.trafficSignArray[2]
    
    def rightAndForwardStatus(self):
        return self.trafficSignArray[3]

    def leftStatus(self):
        return self.trafficSignArray[4]
    
    def rightStatus(self):
        return self.trafficSignArray[5]
    
    def closeStatus(self):
        return self.trafficSignArray[6]

    def passengerInStatus(self):
        return self.trafficSignArray[7]
    
    def passengerOutStatus(self):
        return self.trafficSignArray[8]
    
    def trafficLightStatus(self):
        return self.trafficSignArray[9]
    
    def stopStatus(self):
        return self.trafficSignArray[10]

"""
0-Sola dönülmez
1-Sağa dönülmez
2-İleri ve sola mecburi yön
3-İleri ve sağa mecburi yön
4-Sola dön
5-Sağa Dön
6-Taşıt trafiğine kapalı yol
7-Durak bin
8-Durak in
9-Trafik lambası -1 yok 0-kırmızı 1-yeşil
10-Dur
"""