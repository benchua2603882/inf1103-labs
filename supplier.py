class Supplier:
    """Store the details of a supplier independently of its products."""

    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        # Check that the supplier details are not left blank.
        if not isinstance(supplier_id, str) or not supplier_id.strip():
            raise ValueError("Supplier ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Supplier name cannot be empty.")
        if not isinstance(contact_email, str) or not contact_email.strip():
            raise ValueError("Contact email cannot be empty.")

        self.__supplier_id: str = supplier_id.strip().upper()
        self.__name: str = name.strip()
        self.__contact_email: str = contact_email.strip()

    @property
    def supplier_id(self) -> str:
        # Let other objects read the supplier ID.
        return self.__supplier_id

    @property
    def name(self) -> str:
        # Return the supplier's name.
        return self.__name

    @property
    def contact_email(self) -> str:
        # Return the email used to contact this supplier.
        return self.__contact_email

    def display_information(self) -> None:
        # Show the supplier details together.
        print(
            f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | "
            f"Email: {self.__contact_email}"
        )
