quantity = []
abv = []

print("BAC (Blood Alcohol Content) Calculator")

sex = input("Enter your gender (M/F): ")
weight = float(input("Enter your weight in KG: "))
time = float(input("Enter the time since your first drink in hours: "))
question = int(input("How many different drinks did you have? (1/2/3/etc.): "))
for i in range(question):
    print("For drink number", i + 1)
    quantity.append(int(input("Enter the ml of the drink consumed: ")))
    abv.append(float(input("Enter the alcohol by volume (ABV) percentage of the drink: ")))

total_alcohol_grams = 0

for i in range(len(quantity)):
    alcohol_ml = quantity[i] * (abv[i] / 100)
    alcohol_grams = alcohol_ml * 0.789
    total_alcohol_grams += alcohol_grams

if sex.upper() == 'M':
    bwc = 0.68
else:
    bwc = 0.55

weight_grams = weight * 1000
bac = (total_alcohol_grams / (weight_grams * bwc)) * 100 - (0.015 * time)
bac_percentage = max(0, bac)
print(f"Your estimated BAC is: {bac_percentage:.2f}%")
sober = bac_percentage / 0.015
hours = int(sober)
minutes = int((sober - hours) * 60) % 60
print(f"Estimated time to sober up: {hours} hours and {minutes} minutes")


