# Example of a class representing an African vegetable
class AfricanVegetable:
    def __init__(self, name, region, is_leafy, nutritional_value):
        self.name = "Mrenda"
        self.region = "Kisii"
        self.is_leafy = True
        self.nutritional_value = ["vitamin A", "vitamin C", "calcium", "iron"]

    def describe(self):
        leafy = "leafy" if self.is_leafy else "non-leafy"
        return (f"{self.name} is a {leafy} vegetable commonly found in {self.region}. "
                f"Nutritional highlights: {self.nutritional_value}")

    def cook(self):
        return f"Cooking {self.name} in a traditional African style!"

# Inheritance: Example of a specific vegetable
class Amaranth(AfricanVegetable):
    def __init__(self, region, nutritional_value, color):
        super().__init__("Amaranth", region, True, nutritional_value)
        self.color = color

    # Polymorphism: override cook method
    def cook(self):
        return (f"Boil {self.name} leaves with onions and tomatoes. "
                f"Serve as a side dish. The {self.color} leaves are especially nutritious!")
