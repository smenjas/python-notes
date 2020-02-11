def get_max_unsecured_debt_ratio(income):
    """Return the maximum unsecured-debt-to-income ratio, based on income."""
    if not isinstance(income, (int, float)):
        raise TypeError("Expected a real number.")

    # Below this income, you should not have any unsecured debt.
    min_income = 40000
    if income <= min_income:
        return 0

    slope = 1 / 600000
    min_ratio = 0.1
    ratio = (slope * income) + min_ratio

    # The maximum unsecured-debt-to-income ratio, for any income.
    max_ratio = 0.4
    ratio = min(ratio, max_ratio)

    return ratio
