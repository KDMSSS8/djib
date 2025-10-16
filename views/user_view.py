class UserView:
    def show_user_details(self, name, email):
        print("\nUser Details:")
        print(f"Name: {name}")
        print(f"Email: {email}")

    def get_user_input(self):
        name = input("Enter name: ")
        email = input("Enter email: ")
        return name, email