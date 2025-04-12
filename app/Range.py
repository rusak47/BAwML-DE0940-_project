class Range:
    def __init__(self, name, number_min=None, number_max=None):
        self.name = name
        self.number_min = number_min
        self.number_max = number_max

    def get_condition_and_params(self):
        conditions = []
        params = []
        if self.number_min is not None:
            conditions.append(f"{self.name} >= %s")
            params.append(self.number_min)
        if self.number_max is not None:
            conditions.append(f"{self.name} <= %s")
            params.append(self.number_max)
        return " AND ".join(conditions), params

    def __str__(self):
        condition, _ = self.get_condition_and_params()
        return condition
    

if __name__ == "__main__":
    # Test Range class functionality
    print("Testing Range class...")

    # Test with only minimum value
    min_range = Range("test_field", number_min=10)
    condition, params = min_range.get_condition_and_params()
    print(f"\nRange with min=10:")
    print(f"Condition: {condition}")
    print(f"Params: {params}")
    print(f"String representation: {min_range}")

    # Test with only maximum value  
    max_range = Range("test_field", number_max=100)
    condition, params = max_range.get_condition_and_params()
    print(f"\nRange with max=100:")
    print(f"Condition: {condition}")
    print(f"Params: {params}")
    print(f"String representation: {max_range}")

    # Test with both min and max values
    min_max_range = Range("test_field", number_min=10, number_max=100)
    condition, params = min_max_range.get_condition_and_params()
    print(f"\nRange with min=10, max=100:")
    print(f"Condition: {condition}")
    print(f"Params: {params}")
    print(f"String representation: {min_max_range}")

    # Test with no values
    empty_range = Range("test_field")
    condition, params = empty_range.get_condition_and_params()
    print(f"\nRange with no values:")
    print(f"Condition: {condition}")
    print(f"Params: {params}")
    print(f"String representation: {empty_range}")