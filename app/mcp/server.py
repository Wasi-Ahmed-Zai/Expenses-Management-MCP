from fastmcp import FastMCP

from app.services.expense_service import (
    add_expense,
    get_expense,
    list_expenses,
    update_expense,
    delete_expense,
)


class ExpenseMCPServer:
    """Expense Management MCP server."""

    def __init__(self):
        self.mcp = FastMCP(
            "Expense Management MCP",
        )

        self._register_tools()

    @staticmethod
    def _success(message: str, data=None) -> dict:
        """Create a successful tool response."""

        return {
            "success": True,
            "message": message,
            "data": data,
        }

    @staticmethod
    def _error(message: str) -> dict:
        """Create an error tool response."""

        return {
            "success": False,
            "message": message,
        }

    def _register_tools(self):
        """Register all MCP tools."""

        @self.mcp.tool
        def create_expense(
            amount: float,
            currency: str = "PKR",
            category: str | None = None,
            description: str | None = None,
            merchant: str | None = None,
            expense_date: str | None = None,
            payment_method: str | None = None,
            account: str | None = None,
            notes: str | None = None,
        ) -> dict:
            """
            Create a new expense in the Expense Management system.
            """

            try:
                expense = add_expense(
                    amount=amount,
                    currency=currency,
                    category=category,
                    description=description,
                    merchant=merchant,
                    expense_date=expense_date,
                    payment_method=payment_method,
                    account=account,
                    notes=notes,
                )

                return self._success(
                    f"Expense created successfully. "
                    f"Expense ID: {expense['id']}",
                    expense,
                )

            except ValueError as error:
                return self._error(str(error))

            except Exception:
                return self._error(
                    "We couldn't create the expense right now. "
                    "Please try again."
                )

        @self.mcp.tool
        def get_expense_by_id(
            expense_id: str,
        ) -> dict:
            """
            Get a single expense by its ID.
            """

            try:
                expense = get_expense(expense_id)

                return self._success(
                    f"Expense '{expense_id}' found.",
                    expense,
                )

            except ValueError as error:
                return self._error(str(error))

            except Exception:
                return self._error(
                    "We couldn't retrieve the expense right now. "
                    "Please try again."
                )

        @self.mcp.tool
        def get_expenses() -> dict:
            """
            Get all expenses from the Expense Management system.
            """

            try:
                expenses = list_expenses()

                return self._success(
                    f"Found {len(expenses)} expense(s).",
                    expenses,
                )

            except Exception:
                return self._error(
                    "We couldn't retrieve the expenses right now. "
                    "Please try again."
                )

        @self.mcp.tool
        def edit_expense(
            expense_id: str,
            amount: float | None = None,
            currency: str | None = None,
            category: str | None = None,
            description: str | None = None,
            merchant: str | None = None,
            expense_date: str | None = None,
            payment_method: str | None = None,
            account: str | None = None,
            notes: str | None = None,
        ) -> dict:
            """
            Update an existing expense.
            Only provided fields will be changed.
            """

            try:
                expense = update_expense(
                    expense_id=expense_id,
                    amount=amount,
                    currency=currency,
                    category=category,
                    description=description,
                    merchant=merchant,
                    expense_date=expense_date,
                    payment_method=payment_method,
                    account=account,
                    notes=notes,
                )

                return self._success(
                    f"Expense '{expense_id}' updated successfully.",
                    expense,
                )

            except ValueError as error:
                return self._error(str(error))

            except Exception:
                return self._error(
                    "We couldn't update the expense right now. "
                    "Please try again."
                )

        @self.mcp.tool
        def remove_expense(
            expense_id: str,
        ) -> dict:
            """
            Delete an expense by its ID.
            """

            try:
                result = delete_expense(expense_id)

                return self._success(
                    result["message"],
                    {
                        "expense_id": expense_id,
                    },
                )

            except ValueError as error:
                return self._error(str(error))

            except Exception:
                return self._error(
                    "We couldn't delete the expense right now. "
                    "Please try again."
                )

    def run(self):
        """Start the MCP server."""

        self.mcp.run(
            transport="streamable-http",
        )


server = ExpenseMCPServer()
mcp = server.mcp


if __name__ == "__main__":
    server.run()
