
class RestaurantModelChoices:

    fssai: str = "FSSAI"
    fda: str = "FDA"

    FOOD_LICENSE_PROVIDER_CHOICES = (
        ("fssai", fssai),
        ("fda", fda)
    )



class RestaurantBranchMenuItemChoices:
    indian_rupee: str = "INR"
    great_british_pound: str = "GBP"
    us_dollar: str = "USD"
    chinese_yuan: str = "CNY"
    japanese_yen: str = "JPY"

    CURRENCY_CHOICES = (
        (indian_rupee, indian_rupee),
        (great_british_pound, great_british_pound),
        (us_dollar, us_dollar),
        (chinese_yuan, chinese_yuan),
        (japanese_yen, japanese_yen)
    )
