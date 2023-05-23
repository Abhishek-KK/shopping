# Catalog of products
catalog = {
    "Product A": 20,
    "Product B": 40,
    "Product C": 50
}

# Discount rules
discount_rules = {
    "flat_10_discount": {"threshold": 200, "discount": 10},
    "bulk_5_discount": {"threshold": 10, "discount_percentage": 0.05},
    "bulk_10_discount": {"threshold": 20, "discount_percentage": 0.1},
    "tiered_50_discount": {"total_threshold": 30, "quantity_threshold": 15, "discount_percentage": 0.5}
}

# Fees
gift_wrap_fee = 1
shipping_fee_per_package = 5
max_units_per_package = 10

# Input quantities and gift wrap information for each product
quantities = {}
gift_wraps = {}

for product_name, _ in catalog.items():
    quantity = int(input(f"Enter the quantity of {product_name}: "))
    quantities[product_name] = quantity
    gift_wrap = input(
        f"Is {product_name} wrapped as a gift? (yes/no): ").lower() == "yes"
    if gift_wrap:
        gift_wraps[product_name] = quantity

# Calculate the subtotal
subtotal = 0
for product_name, price in catalog.items():
    subtotal += quantities[product_name] * price

# Apply the most beneficial discount rule
discount_applied = None
discount_amount = 0

for rule, rule_details in discount_rules.items():
    if rule == "flat_10_discount" and subtotal > rule_details["threshold"]:
        discount_applied = rule
        discount_amount = rule_details["discount"]
    elif rule == "bulk_5_discount":
        for product_name, quantity in quantities.items():
            if quantity > rule_details["threshold"]:
                discount_applied = rule
                discount_amount = catalog[product_name] * \
                    quantity * rule_details["discount_percentage"]
                break
    elif rule == "bulk_10_discount" and sum(quantities.values()) > rule_details["threshold"]:
        discount_applied = rule
        discount_amount = subtotal * rule_details["discount_percentage"]
    elif (
        rule == "tiered_50_discount"
        and sum(quantities.values()) > rule_details["total_threshold"]
        and any(quantity > rule_details["quantity_threshold"] for quantity in quantities.values())
    ):
        discount_applied = rule
        discount_amount = sum(
            (quantity - rule_details["quantity_threshold"]) *
            catalog[product_name] * rule_details["discount_percentage"]
            for product_name, quantity in quantities.items()
            if quantity > rule_details["quantity_threshold"]
        )

# Calculate shipping fee and gift wrap fee
total_units = sum(quantities.values())
shipping_fee = (total_units - 1) // max_units_per_package * \
    shipping_fee_per_package + shipping_fee_per_package
gift_wrap_fee_total = sum(gift_wraps.values()) * gift_wrap_fee

# Calculate the total amount
total = subtotal - discount_amount + shipping_fee + gift_wrap_fee_total

# Output the details
print("\n--- Order Details ---")
for product_name, quantity in quantities.items():
    print(
        f"{product_name}\t Quantity: {quantity}\t Total: {catalog[product_name] * quantity}")

print(f"\nSubtotal: {subtotal}")
if discount_applied:
    print(
        f"Discount applied: {discount_applied}\t Discount amount: {discount_amount}")
else:
    print("No applicable discounts")
print(f"Gift wrap fee: {gift_wrap_fee_total}")
print(f"Shipping fee: {shipping_fee}")
print(f"Total: {total}")
