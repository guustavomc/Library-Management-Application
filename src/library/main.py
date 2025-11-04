from models.inventory import Inventory
from models.customer import Customer


if __name__ == "__main__":
    
    inventory=Inventory()
    inventory.register_book("LORD OF THE RINGS", "J R R TOLKIEN", 1000, 50)
    inventory.register_book("THE HOBBIT", "J R R TOLKIEN", 500, 30)

    inventory.display_books()

    inventory.available_books()

    customer=Customer("cliente 1", 10)
    inventory.lend_book("LORD OF THE RINGS", customer)

    inventory.available_books()


