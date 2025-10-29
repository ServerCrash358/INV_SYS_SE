import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def add_item(stock_data, item="default", qty=0, logs=None):
    """Adds a specified quantity of an item to the stock data."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not item:
        logging.warning("Invalid item name: %s. Must be a non-empty string.",
                        item)
        return
    if not isinstance(qty, int):
        logging.warning("Invalid quantity for %s: %s. Must be an integer.",
                        item, qty)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    log_message = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_message)
    logging.info(log_message)


def remove_item(stock_data, item, qty):
    """Removes a specified quantity of an item from the stock data."""
    if not isinstance(item, str) or not item:
        logging.warning("Invalid item name: %s. Must be a non-empty string.",
                        item)
        return
    if not isinstance(qty, int):
        logging.warning("Invalid quantity for %s: %s. Must be an integer.",
                        item, qty)
        return

    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info("Removed %s from stock.", item)
    except KeyError:
        logging.warning("Attempted to remove non-existent item: %s", item)
    except TypeError:
        logging.error("Type error during removal of item %s with quantity %s.",
                      item, qty)


def get_qty(stock_data, item):
    """Retrieves the quantity of a specific item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Loads inventory data from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        logging.warning("Inventory file not found. "
                        "Starting with empty inventory.")
        return {}
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from %s. "
                      "Starting with empty inventory.", file)
        return {}


def save_data(stock_data, file="inventory.json"):
    """Saves the inventory data to a JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
            logging.info("Inventory data saved to %s", file)
    except IOError as e:
        logging.error("Could not save data to %s: %s", file, e)


def print_data(stock_data):
    """Prints a report of all items and their quantities."""
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")
    print("--------------------")


def check_low_items(stock_data, threshold=5):
    """Returns a list of items below a given stock threshold."""
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Main function to run the inventory system demo."""
    stock_data = load_data("inventory.json")
    my_logs = []

    add_item(stock_data, "apple", 10, my_logs)
    add_item(stock_data, "banana", 5, my_logs)

    add_item(stock_data, "banana", -2, my_logs)
    add_item(stock_data, 123, "ten", my_logs)

    remove_item(stock_data, "apple", 3)
    remove_item(stock_data, "orange", 1)

    print(f"Apple stock: {get_qty(stock_data, 'apple')}")
    print(f"Low items: {check_low_items(stock_data)}")

    print_data(stock_data)
    save_data(stock_data)


if __name__ == "__main__":
    main()
