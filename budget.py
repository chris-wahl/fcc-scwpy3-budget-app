from typing import List, TypedDict

Ledger = TypedDict('Ledger', {
    'amount': float,
    'description': str
})


class Category:
    category: str
    ledger: List[Ledger]

    def __init__(self, category: str):
        self.category = category.title()
        self.ledger = []

    def get_balance(self) -> float:
        return sum([entry['amount'] for entry in self.ledger], 0)

    def check_funds(self, amount: float) -> bool:
        return self.get_balance() >= amount

    def deposit(self, amount: float, description: str = ''):
        self.ledger.append({
            'amount': amount,
            'description': description
        })

    def withdraw(self, amount: float, description: str = '') -> bool:
        if self.check_funds(abs(amount)):
            self.ledger.append({
                'amount': 0 - abs(amount),
                'description': description
            })
            return True
        return False

    def transfer(self, amount, category: 'Category') -> bool:
        if self.withdraw(amount, f'Transfer to {category.category}'):
            category.deposit(amount, f'Transfer from {self.category}')
            return True
        return False

    def __str__(self):
        total = self.get_balance()
        s = self.category.center(30, '*')

        ledger = '\n'.join([
            f"{entry['description'][:23]:<23}{entry['amount']:>7.2f}"
            for entry in self.ledger
        ])

        if ledger:
            s += f'\n{ledger}'
        s += f'\nTotal: {total}'

        return s


def create_spend_chart(categories: List[Category]):
    spend_per_category = [
        (abs(sum(
            [entry['amount'] for entry in category.ledger
             if entry['amount'] < 0], 0
        )), category.category) for category in categories
    ]

    total_spend = sum([e[0] for e in spend_per_category])
    # Reprocess spend_per_category into % of total
    spend_per_category = [(e[0] / total_spend * 100, e[1]) for e in spend_per_category]

    s = 'Percentage spent by category'
    for i in range(100, -1, -10):
        line = f'\n{i:>3}| '
        for amount, name in spend_per_category:
            if amount >= i:
                line += 'o  '
            else:
                line += ' ' * 3
        s += line

    # Set the lower `-------` bar
    s += '\n' + (' ' * 4) + '-' * (3 * len(categories) + 1)
    # Add in the category names
    max_name = max(len(e[1]) for e in spend_per_category)
    for i in range(max_name):
        line = '\n' + ' ' * 5
        for _, name in spend_per_category:
            line += (name[i:i + 1] or ' ') + '  '
        s += line

    return s
