# This calculator calculates the final price after applying a discount
def calculate_discount(price, discount_percent):
    """
    Calculate the final price after applying a discount.
    
    Parameters:
    price (float): Original price of the item
    discount_percent (float): Discount percentage (0-100)
    
    Returns:
    float: Final price after discount (if applicable)
    """
    if discount_percent >= 20:
        # Apply the discount
        discount_amount = price * (discount_percent / 100)
        final_price = price - discount_amount
        return final_price
    else:
        # Return original price if discount is less than 20%
        return price

# Main program to interact with the user
def main():
    try:
        # Prompt user for input
        original_price = float(input("Enter the original price of the item: "))
        discount_percent = float(input("Enter the discount percentage: "))
        
        # Calculate final price
        final_price = calculate_discount(original_price, discount_percent)
        
        # Display the result
        if discount_percent >= 20:
            print(f"Original price: ${original_price:.2f}")
            print(f"Discount applied: {discount_percent}%")
            print(f"Final price after discount: ${final_price:.2f}")
        else:
            print(f"No discount applied (discount must be 20% or higher)")
            print(f"Final price: ${final_price:.2f}")
            
    except ValueError:
        print("Error: Please enter valid numbers for price and discount percentage.")

# Run the program
if __name__ == "__main__":
    main()