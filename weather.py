from dataclasses import dataclass
from datetime import datetime
import os
import sys

class WeatherReading:
    date: datetime
    max_temp: int
    min_temp: int
    humidity: int
     
class WeatherFileParser:
    def __init__(self, directory):
        self.directory = directory
        
    def parse_files(self):
        readings = []
        
        for file in os.listdir(self.directory):
            if not file.endswith(".txt"):
                continue
            
            with open(os.path.join(self.directory, file)) as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) != 4:
                        continue
                    
                    date = datetime.strptime(parts[0], "%Y-%m-%d")
                    
                    readings.append(
                        WeatherReading(
                            date=date,
                            max_temp=int(parts[1]),
                            min_temp=int(parts[2]),
                            humidity=int(parts[3])
                        )
                    )
        return readings

class WeatherCalculator:
    def __init__(self, readings):
        self.readings = readings
        
    def yearly_extremes(self, year):
        year_data = [r for r in self.readings if r.date.year == year]

        highest = max(year_data, key=lambda x: x.max_temp)
        lowest = min(year_data, key=lambda x: x.min_temp)
        humid = max(year_data, key=lambda x: x.humidity)

        return highest, lowest, humid

def monthly_averages(self, year, month):
    data = [
        r for r in self.readings
        if r.date.year == year and r.date.month == month
    ]
    
    """
    if len(data) ==0:
        return 0,0,0
    """
    
    avg_high = sum(r.max_temp for r in data) // len(data)
    avg_low = sum (r.min_temp for r in data) // len(data)
    avg_hum = sum (r.humid for r in data) // len(data)
    return avg_high, avg_low,avg_hum

class WeatherReport:
    @staticmethod
    def yearly_report(high, low, humid):
        print(f"Highest: {high.max_temp}C on {high.date.strftime('%B %d')}")
        print(f"Lowest: {low.min_temp}C on {low.date.strftime('%B %d')}")
        print(f"Humidity: {humid.humidity}% on {humid.date.strftime('%B %d')}")
            
    @staticmethod   
    def monthly_report(avg_high, avg_low, avg_hum):
        print(f"Average Highest Temp: {avg_high}C")
        print(f"Average lowest Temp: {avg_low}C")
        print(f"Average Humid Temp: {avg_hum}%")
        
        
class WeatherChart:
    @staticmethod
    def draw(readings,year,month):
        print(f"\n{month}/{year}")
        
        for r in readings:
            if r.date.year == year and r.date.month == month:
                print(
                    f"{r.date.day:02d}"
                    f"\033[31m{'+' * r.max_temp}\033[0m "
                    f"{r.max_temp}C"
                )
                print(
                    f"{r.date.day:02d} "
                    f"\033[34m{'+' * abs(r.min_temp)}\033[0m "
                    f"{r.min_temp}C"
                )
                
def main():
    directory = sys.argv[1]
    option = sys.argv[2]
    value = sys.argv[3]
    
    parser = WeatherFileParser(directory)
    readings = parser.parse_files()
    calculator = WeatherCalculator(readings)

    if option == "-e":
        year = int(value)
        high, low, humid = calculator.yearly_extremes(year)
        WeatherReport.yearly_report(high, low, humid)
        
    elif option == "-a":
        year, month = map(int, value.split("/"))
        avg_high, avg_low, avg_humid = calculator.monthly_averages(year, month)
        WeatherReport.monthly_report(avg_high, avg_low, avg_humid)
        
    elif option == "-c":
        year, month = map(int, value.split("/"))
        WeatherChart.draw(readings, year, month)

if __name__ == "__main__":
    main()


    

    
    

        
        

 
     
        



   

 