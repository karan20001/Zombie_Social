class UserConstant:
    REDIS_USER_KEY = "JWT"
    USER_DATA_NOT_FOUND = "User Data not found"

    class UserMarkingConstants:
        SUCCESSFULLY_MARKED = "User successfully marked"
        ALREADY_SUCCESSFULLY_MARKED = "User already marked"
        ALREADY_MARKED = "You have already marked this user"
        AWESOME_PERSON = "Thanks man, you are awesome !!"

    class UserLocationConstants:

        SUCCESSFULLY_UPDATED = "location updated successfully"
        PERMISSION_ERROR = "You are not allowed to change others location"


    class UserTradingConstants:

        SUCCESSFULLY_TRADED = "The trade was successfully executed"
        UNFAIR_TRADE = "The trade is not fair"
        UNAVAILABLE_ERROR = "inventory is unavailable"
        OFFERED = "Offered"
        REQUESTED = "Requested"



class InventoryConstant:
    INVENTORY_LIST = [
        "water",
        "foor",
        "medication",
        "ammunition"
    ]

    WATER = "water"
    FOOD = "food"
    MEDICATION = "medication"
    AMMUNITIONN = "ammunition"