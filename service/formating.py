def transactions_format(transactions):
    if transactions:
        for transaction in transactions:
            transaction["format_amount"] = f"{transaction['amount']:,}"
            transaction["format_balance"] = f"{transaction['balance']:,}"
    return transactions

def summary_format(transactions_summary):
    total_balance = f"{transactions_summary['total_balance']:,}" if transactions_summary['total_balance'] is not None else 0
    income_sum = f"{transactions_summary['income_sum']:,}" if transactions_summary['income_sum'] is not None else 0
    expense_sum = f"{transactions_summary['expense_sum']:,}" if transactions_summary['expense_sum'] is not None else 0

    return {
        "total_balance" : total_balance,
        "income_sum" : income_sum,
        "expense_sum" : expense_sum
    }
