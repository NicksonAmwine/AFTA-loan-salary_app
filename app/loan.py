import pandas as pd
import numpy as np

def calculate_loan_payment(principal, months, monthly_rate):
    monthly_rate = monthly_rate / 100
    if months <= 0 or principal <= 0:
        raise ValueError("Months and principal must be greater than zero.")
    if monthly_rate == 0:
        monthly_payment = principal / months
    else:
        monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -months)

    total_payment = monthly_payment * months

    return {
        "monthly_payment": round(monthly_payment, 2),
        "total_payment": round(total_payment, 2),
        "principal": principal,
        "interest_rate": monthly_rate,
        "duration_months": months
    }

def eligibility(gross_salary, pay_frequency, requested_amount):
    monthly_salary = convert_to_monthly(gross_salary, pay_frequency)
    max_advance = monthly_salary * 0.5

    is_eligible = requested_amount <= max_advance and monthly_salary >= 500000
    fee = round(requested_amount * 0.05, 2) if is_eligible else 0
    total_repayment = round(requested_amount + fee, 2) if is_eligible else 0

    if is_eligible:
        return {
            "is_eligible": is_eligible,
            "max_advance": round(max_advance, 2),
            "monthly_salary": round(monthly_salary, 2),
            "requested_amount": requested_amount,
            "reason": "Eligible for advance",
            "fee": fee,
            "total_repayment": total_repayment
        }

    return {
        "is_eligible": is_eligible,
        "max_advance": round(max_advance, 2),
        "monthly_salary": round(monthly_salary, 2),
        "requested_amount": requested_amount,
        "reason": "Amount exceeds maximum allowed",
        "fee": 0,
        "total_repayment": 0
    }

def convert_to_monthly(amount, frequency):
    if frequency == "weekly":
        return amount * 4
    elif frequency == "semi-monthly":
        return amount * 2
    else:
        return amount


def calculate_compound_interest(principal, annual_rate, years, compounds_per_year=12):
    rate = annual_rate / 100
    periods = years * compounds_per_year
    rate_per_period = rate / compounds_per_year

    schedule = pd.DataFrame({
        'period': range(1, periods + 1),
        'start_balance': 0.0,
        'payment': 0.0,
        'principal_payment': 0.0,
        'interest_payment': 0.0,
        'end_balance': 0.0
    })
    payment = principal * (rate_per_period * (1 + rate_per_period)**periods) / ((1 + rate_per_period)**periods - 1)
    
    remaining_balance = principal
    for i in range(periods):
        interest_payment = remaining_balance * rate_per_period
        principal_payment = payment - interest_payment
        
        schedule.loc[i, 'start_balance'] = remaining_balance
        schedule.loc[i, 'payment'] = payment
        schedule.loc[i, 'principal_payment'] = principal_payment
        schedule.loc[i, 'interest_payment'] = interest_payment
        
        remaining_balance -= principal_payment
        schedule.loc[i, 'end_balance'] = remaining_balance

    for col in ['start_balance', 'payment', 'principal_payment', 'interest_payment', 'end_balance']:
        schedule[col] = schedule[col].round(2)
    
    total_payment = payment * periods
    total_interest = total_payment - principal
    
    return {
        'principal': principal,
        'annual_rate': annual_rate,
        'years': years,
        'compounds_per_year': compounds_per_year,
        'payment_per_period': round(payment, 2),
        'total_payment': round(total_payment, 2),
        'total_interest': round(total_interest, 2),
        'completion_schedule': schedule.to_dict('records')
    }