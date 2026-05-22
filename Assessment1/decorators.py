"""Simple decorators used by the car rental CLI."""

# The decorators.py file contains simple decorators used by the car rental CLI to enforce access control and handle user input validation.
def admin_only(func):
    """Allow access only for logged-in admin users."""

    # The wrapper function checks if there is a current session and if the user's role is "admin". 
    # If either condition is not met, it prints an access denied message and returns without executing the decorated function. 
    # If the user is an admin, it proceeds to call the original function with the provided arguments.
    def wrapper(self, *args, **kwargs):
        if self.current_session is None or self.current_session.role != "admin":
            print("Access denied. Admin only.")
            return
        return func(self, *args, **kwargs)

    return wrapper
