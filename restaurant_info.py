import pandas as pd


def load_restaurant_info():
    """
    读取餐厅信息并返回一个字典，包含基本信息、菜单、特价等内容。
    """
    # 读取Excel文件
    df_basic_info = pd.read_excel("data/restaurant_info.xlsx", sheet_name="Basic Info")
    df_menu = pd.read_excel("data/restaurant_info.xlsx", sheet_name="Menu")
    df_special_offers = pd.read_excel("data/restaurant_info.xlsx", sheet_name="Special Offers")

    # 提取基本信息
    restaurant_info = {
        "name": df_basic_info.iloc[0]["Restaurant Name"],
        "address": df_basic_info.iloc[0]["Address"],
        "phone": df_basic_info.iloc[0]["Phone"],
        "email": df_basic_info.iloc[0]["Email"],
        "website": df_basic_info.iloc[0]["Website"],
        "operating_hours": {
            "monday_to_friday": df_basic_info.iloc[0]["Monday to Friday Hours"],
            "saturday": df_basic_info.iloc[0]["Saturday Hours"],
            "sunday": df_basic_info.iloc[0]["Sunday Hours"]
        },
        "menu": df_menu.to_dict(orient="records"),
        "special_offers": df_special_offers.to_dict(orient="records")
    }

    return restaurant_info


def handle_restaurant_query(user_input, restaurant_info):
    """
    处理用户查询餐厅信息的请求，根据不同的查询，返回对应的信息。
    """
    # 转换用户输入为小写并查看查询类型
    user_input = user_input.lower()

    # 查询餐厅地址
    if any(keyword in user_input for keyword in ['address', 'location', 'where', 'place']):
        print(f"Chatbot: The restaurant is located at: {restaurant_info['address']}.")

    # 查询菜单
    elif any(keyword in user_input for keyword in ['menu', 'food', 'dish', 'items']):
        print("Chatbot: Here is the menu:")
        if restaurant_info["menu"]:
            for item in restaurant_info["menu"]:
                dish_name = item.get('Dish Name', 'Unknown Dish')
                price = f"${item.get('Price', 0):.2f}"  # 格式化价格为两位小数
                description = item.get('Description', 'No description available.')
                print(f"- {dish_name}: {price} ({description})")
        else:
            print("Chatbot: Sorry, the menu is currently unavailable.")

    # 查询营业时间
    elif any(keyword in user_input for keyword in ['hours', 'operating hours', 'opening hours', 'time']):
        print("Chatbot: Here are the operating hours:")
        operating_hours = restaurant_info['operating_hours']
        print(f"  Monday to Friday: {operating_hours['monday_to_friday']}")
        print(f"  Saturday: {operating_hours['saturday']}")
        print(f"  Sunday: {operating_hours['sunday']}")

    # 查询特殊优惠
    elif any(keyword in user_input for keyword in ['special offers', 'promotions', 'discounts','schedule']):
        print("Chatbot: Here are the current special offers:")
        if restaurant_info["special_offers"]:
            for offer in restaurant_info["special_offers"]:
                offer_name = offer.get('Offer Name', 'No name')
                description = offer.get('Description', 'No description available.')
                validity = offer.get('Validity', 'No validity info available.')
                print(f"- {offer_name}: {description} (Valid: {validity})")
        else:
            print("Chatbot: No special offers are currently available.")

    # 查询联系方式
    elif any(keyword in user_input for keyword in ['phone', 'contact', 'telephone']):
        print(f"Chatbot: You can reach us at {restaurant_info['phone']}.")

    # 查询电子邮件
    elif any(keyword in user_input for keyword in ['email', 'contact us']):
        print(f"Chatbot: You can contact us via email at {restaurant_info['email']}.")

    # 查询网站
    elif any(keyword in user_input for keyword in ['website', 'webpage', 'site']):
        print(f"Chatbot: You can visit our website at {restaurant_info['website']}.")

    # 查询餐厅名称
    elif any(keyword in user_input for keyword in ['name', 'restaurant name']):
        print(f"Chatbot: The name of the restaurant is {restaurant_info['name']}.")

    # 如果没有匹配的查询
    else:
        print("Chatbot: I'm sorry, I couldn't find that information. Could you be more specific?")
        print("Chatbot: For example, you can ask about the restaurant's 'address', 'menu', 'hours', 'special offers', 'contact', 'email', or 'website'.")

    return True


