import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key

# DynamoDB setup
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("ExpensesTable")


# ---------- Helpers ----------

def decimal_to_float(obj):
    if isinstance(obj, list):
        return [decimal_to_float(i) for i in obj]
    if isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return float(obj)
    return obj


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(decimal_to_float(body))
    }


# ---------- Handlers ----------

def create_expense(user_id, event):
    body = json.loads(event["body"])

    expense_id = str(uuid.uuid4())
    date = body["date"]
    month = date[:7]  # YYYY-MM
    created_at = datetime.utcnow().isoformat()

    item = {
        "userId": user_id,
        "itemKey": f"EXPENSE#{expense_id}",
        "expenseId": expense_id,
        "category": body["category"],
        "amount": Decimal(str(body["amount"])),  # IMPORTANT
        "date": date,
        "month": month,
        "note": body.get("note", ""),
        "createdAt": created_at
    }

    table.put_item(Item=item)

    return response(201, {
        "message": "Expense added",
        "expense": item
    })

def update_expense(user_id, expense_id, event):
    body = json.loads(event["body"])

    update_expr = []
    expr_values = {}

    if "category" in body:
        update_expr.append("category = :c")
        expr_values[":c"] = body["category"]

    if "amount" in body:
        update_expr.append("amount = :a")
        expr_values[":a"] = Decimal(str(body["amount"]))

    if "date" in body:
        update_expr.append("date = :d")
        expr_values[":d"] = body["date"]
        expr_values[":m"] = body["date"][:7]
        update_expr.append("month = :m")

    if "note" in body:
        update_expr.append("note = :n")
        expr_values[":n"] = body["note"]

    table.update_item(
        Key={
            "userId": user_id,
            "itemKey": f"EXPENSE#{expense_id}"
        },
        UpdateExpression="SET " + ", ".join(update_expr),
        ExpressionAttributeValues=expr_values
    )

    return response(200, {"message": "Expense updated"})

def delete_expense(user_id, expense_id):
    table.delete_item(
        Key={
            "userId": user_id,
            "itemKey": f"EXPENSE#{expense_id}"
        }
    )

    return response(200, {"message": "Expense deleted"})

def set_limit(user_id, event):
    body = json.loads(event["body"])
    month = body["month"]
    limit = Decimal(str(body["limit"]))

    item = {
        "userId": user_id,
        "itemKey": f"LIMIT#{month}",
        "month": month,
        "limit": limit
    }

    table.put_item(Item=item)

    return response(200, {"message": "Limit set", "limit": item})


def get_limit(user_id):
    now_month = datetime.utcnow().strftime("%Y-%m")

    result = table.get_item(
        Key={
            "userId": user_id,
            "itemKey": f"LIMIT#{now_month}"
        }
    )

    if "Item" not in result:
        return response(200, {"month": now_month, "limit": None})

    return response(200, result["Item"])

def list_expenses(user_id):
    result = table.query(
        KeyConditionExpression=Key("userId").eq(user_id)
    )

    expenses = [
        item for item in result.get("Items", [])
        if item["itemKey"].startswith("EXPENSE#")
    ]

    return response(200, expenses)


# ---------- Main Lambda ----------

def lambda_handler(event, context):
    method = event["httpMethod"]
    resource = event["resource"]

    claims = event["requestContext"]["authorizer"]["claims"]
    user_id = claims["sub"]

    # ---------- Expenses ----------
    if resource == "/expenses" and method == "POST":
        return create_expense(user_id, event)

    if resource == "/expenses" and method == "GET":
        return list_expenses(user_id)

    if resource == "/expenses/{id}" and method == "PUT":
        expense_id = event["pathParameters"]["id"]
        return update_expense(user_id, expense_id, event)

    if resource == "/expenses/{id}" and method == "DELETE":
        expense_id = event["pathParameters"]["id"]
        return delete_expense(user_id, expense_id)

    # ---------- Limits ----------
    if resource == "/limits" and method == "PUT":
        return set_limit(user_id, event)

    if resource == "/limits" and method == "GET":
        return get_limit(user_id)

    return response(404, {"message": "Route not found"})
