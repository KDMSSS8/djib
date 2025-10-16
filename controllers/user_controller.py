class UserController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def set_user_details(self):
        name, email = self.view.get_user_input()
        self.model.set_name(name)
        self.model.set_email(email)

    def update_view(self):
        name = self.model.get_name()
        email = self.model.get_email()
        self.view.show_user_details(name, email)