from fastapi import FastAPI, Query
from salary import calculate_net_salary
from  loan import calculate_compound_interest, calculate_loan_payment
from enum import Enum

class PayFrequency(str, Enum):
    weekly = "weekly"
    semimonthly = "semi-monthly"
    monthly = "monthly" 

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Advanced Salary & Loan Calculator API"}

@app.get("/salary/")
def net_salary(gross_salary: int, tax_rate: float = 0.3):
    return calculate_net_salary(gross_salary, tax_rate)

@app.get("/loan/")
def loan_payment(principal: int, monthly_rate: float, months: int):
    return calculate_loan_payment(principal, months, monthly_rate)

@app.get("/compound-interest/")
def compound_interest(
    principal: float, 
    annual_rate: float, 
    years: float,
    compounds_per_year: int = Query(12)
):
    return calculate_compound_interest(principal, annual_rate, years, compounds_per_year)

# To run the FastAPI app, use the command:
# uvicorn main:app --reload