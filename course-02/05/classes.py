class Car:
    created_cars  = 0

    def __init__(self, model, wheel_count, wheel_pressure):
        Car.created_cars += 1
        self.model = model
        self.wheel_count = wheel_count
        self.wheel_pressure = wheel_pressure

    def drive(self):
        print(f"{self.model} is driving")


class ElectricCar(Car):
    def __init__(self, model, wheel_count, wheel_pressure, battery_capacity):
        super().__init__(model, wheel_count, wheel_pressure)
        self.battery_capacity = battery_capacity

    def charge(self):
        print(f"{self.model} is charging its {self.battery_capacity} kWh battery")


toyota = Car("Toyota", 4, 2.2)
bmw = Car("BMW", 5, 2.3)
honda = Car("Honda", 6, 2.4)
print(toyota)
print(toyota.model)
print(toyota.wheel_count)
toyota.drive()

tesla = ElectricCar("Tesla", 4, 2.2, 100)
tesla.drive()
tesla.charge()


print(f"Created cars: {Car.created_cars}")
