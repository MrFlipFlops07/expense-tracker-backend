# Expense Tracker – Backend

A fully serverless backend for an expense tracking application built using AWS services.

## 🚀 Tech Stack
- AWS Cognito (Authentication)
- API Gateway (REST APIs)
- AWS Lambda (Business Logic)
- DynamoDB (Single-table design)
- Postman (API testing)

---

## 🏗️ Architecture Overview

User → Cognito Hosted Login → API Gateway (Cognito Authorizer) → Lambda → DynamoDB

All APIs are secured using JWT tokens issued by Cognito.

---

## 🔐 Authentication

- Users authenticate via AWS Cognito Hosted / Managed Login
- Frontend sends the **ID Token** as a Bearer token

Authorization: Bearer <ID_TOKEN>

---

## 📡 API Endpoints

### Expenses
| Method | Endpoint | Description |
|------|--------|------------|
| POST | /expenses | Add expense |
| GET | /expenses | List expenses |
| PUT | /expenses/{id} | Update expense |
| DELETE | /expenses/{id} | Delete expense |

### Limits
| Method | Endpoint | Description |
|------|--------|------------|
| PUT | /limits | Set monthly limit |
| GET | /limits | Get monthly limit |

---

## 🗄️ DynamoDB Design

**Table:** ExpensesTable  

**Partition Key:** `userId`  
**Sort Key:** `itemKey`  

### Item Types
- Expense: `EXPENSE#<expenseId>`
- Limit: `LIMIT#YYYY-MM`

Single-table design ensures scalability and per-user isolation.

---

## 🧪 API Testing

All APIs were tested using Postman.

- Postman collection available in `/postman`
- Includes authenticated requests with Cognito ID token

---

## 🔒 Security Highlights

- No userId accepted from client
- Identity derived from JWT (`sub`)
- Cognito Authorizer on all routes
- Least-privilege IAM for Lambda

---

## 📄 Documentation

Detailed backend documentation and frontend handoff notes are available in `/docs`.

---

## ✅ Status

✔ Backend complete  
✔ All APIs tested  
✔ Ready for frontend integration
