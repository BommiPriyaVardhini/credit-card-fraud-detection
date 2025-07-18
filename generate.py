import pandas as pd
import random

# Function to generate a random 12-digit credit card number
def generate_card_number():
    return "".join([str(random.randint(0, 9)) for _ in range(12)])

# Generate 1000 unique credit card numbers
card_numbers = set()
while len(card_numbers) < 1000:
    card_numbers.add(generate_card_number())

# Save to CSV
df = pd.DataFrame(list(card_numbers), columns=["CreditCardNumber"])
df.to_csv("credit_card_dataset.csv", index=False)

print("Dataset generated successfully: credit_card_dataset.csv")
