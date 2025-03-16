class RestaurantEmployeeChoices:

    server: str = "Server"
    cashier: str = "Cashier"
    cook: str = "Cook"
    host: str = "Host"
    manager: str = "Manager"

    RESTAURANT_ROLE_CHOICES = (
        ("server", server),
        ("cashier", cashier),
        ("cook", cook),
        ("host", host),
        ("manager", manager)
    )

    sunday: str = "Sunday"
    monday: str = "Monday"
    tuesday: str = "Tuesday"
    wednesday: str = "Wednesday"
    thursday: str = "Thursday"
    friday: str = "Friday"
    saturday: str = "Saturday"

    DAY_CHOICES = (
        (sunday, sunday),
        (monday, monday),
        (tuesday, tuesday),
        (wednesday, wednesday),
        (thursday, thursday),
        (friday, friday),
        (saturday, saturday)
    )