from models.inventory import Inventory

if __name__ == "__main__":
    
    inventory=Inventory()
    inventory.register_book("LORD OF THE RINGS", "J R R TOLKIEN", 1000, 50)
    inventory.register_book("THE HOBBIT", "J R R TOLKIEN", 500, 30)

    inventory.display_books()
    print("Current book quantity available:", inventory.current_book_quantity())