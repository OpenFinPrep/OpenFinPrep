import argparse
import pandas as pd
import math
import numbers

parser = argparse.ArgumentParser(
    description="Find accounts"
)
parser.add_argument(
    "amount", type=int, help="Amount to find"
)
parser.add_argument(
    "--file", type=str, help="File with transactions (%(default)s)", default=""
)

args = parser.parse_args()

def find_missing_amount(transactions, target):
    result = []
    
    def backtrack(start, current_combination, current_sum):
        # If the current sum matches the target, store the combination
        if current_sum == target:
            result.append(list(current_combination))
            return

        if len(current_combination) > 4:
            return

        # Explore all options
        for i in range(start, len(transactions)):
            # Include the current number
            current_combination.append(transactions[i])
            backtrack(i + 1, current_combination, current_sum + transactions[i])
            
            # Include the current number negatively
            current_combination[-1] = -transactions[i]
            backtrack(i + 1, current_combination, current_sum - transactions[i])

            # Backtrack (undo choice)
            current_combination.pop()

    backtrack(0, [], 0)
    return result

labels = {}

if args.file.endswith(".csv"):
    df = pd.read_csv(args.file)
    for i, row in df.iterrows():
        amount = abs(row.iloc[1])
        if amount not in labels:
            labels[amount] = set()
        labels[amount].add(row.loc['concept'])
    amounts = list(set([a for a in list(df[df.columns[1]]) if not math.isnan(a) and a > 0]))

elif args.file.endswith(".json"):
    df = pd.read_json(args.file)
    d = df.iloc[0].to_dict()
    amounts = set()
    for k in d:
        if isinstance(d[k], numbers.Number) and not math.isnan(d[k]) and d[k] > 0:
            amount = abs(d[k])
            if amount not in labels:
                labels[amount] = set()
            labels[amount].add(k)
            amounts.add(amount)
    amounts = list(amounts)

combinations = find_missing_amount(amounts, args.amount)
print(f"{args.amount}: {combinations}")

for comb in combinations:
    parts = []
    for c in comb:
        sign = '+' if c >= 0 else '-'
        c = abs(c)
        parts.append(sign + ' ' + str(labels.get(c)))
    print(" ".join(parts))