def calculate_net_salary(gross_salary, tax_rate = 0.3):
    tax = gross_salary * tax_rate
    net_salary = gross_salary - tax
    return {
        "gross_salary": gross_salary,
        "tax": tax,
        "net_salary": net_salary
    }
