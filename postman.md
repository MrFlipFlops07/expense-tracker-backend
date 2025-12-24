############################################################
# FILE: postman.md
############################################################

# Postman API Testing Guide – Expense Tracker Backend

This document explains how to test all backend APIs using Postman.

## Authentication

Login via Cognito Hosted Login.
Copy the ID Token after login.

Required headers for ALL requests:

Authorization: Bearer <ID_TOKEN>  
Content-Type: application/json  

IMPORTANT: Always use the ID token, not the access token.

## Base API URL

https://vrczs1nnnh.execute-api.us-east-1.amazonaws.com/dev

## Expenses APIs

### Create Expense
POST /expenses

Body:
{
  "category": "Food",
  "amount": 250,
  "date": "2025-12-24",
  "note": "Lunch"
}

Expected Response:
{
  "message": "Expense added"
}

### List Expenses
GET /expenses

Expected Response:
[
  {
    "expenseId": "uuid",
    "category": "Food",
    "amount": 250,
    "date": "2025-12-24",
    "month": "2025-12",
    "note": "Lunch"
  }
]

### Update Expense
PUT /expenses/{expenseId}

Body:
{
  "amount": 300,
  "note": "Dinner"
}

Expected Response:
{
  "message": "Expense updated"
}

### Delete Expense
DELETE /expenses/{expenseId}

Expected Response:
{
  "message": "Expense deleted"
}

## Spending Limits APIs

### Set Monthly Limit
PUT /limits

Body:
{
  "month": "2025-12",
  "limit": 10000
}

Expected Response:
{
  "message": "Limit set"
}

### Get Monthly Limit
GET /limits

Expected Response:
{
  "month": "2025-12",
  "limit": 10000
}

If no limit exists:
{
  "month": "2025-12",
  "limit": null
}

## Common Errors

401 – Missing or expired token  
403 – Authorization failure  
404 – Invalid endpoint  
500 – Backend error (check CloudWatch logs)

## Notes for Frontend

- Always send ID token
- Never send userId
- expenseId comes from GET /expenses
- All data is scoped per user

## Testing Status

POST /expenses   OK  
GET /expenses    OK  
PUT /expenses    OK  
DELETE /expenses OK  
PUT /limits      OK  
GET /limits      OK  

