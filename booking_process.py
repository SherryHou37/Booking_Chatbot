# booking_process.py
from restaurant_info import load_restaurant_info, handle_restaurant_query
import re
from datetime import datetime
from Intent_Recognizer import predict_intent
# Mock reservation system (to be integrated with the main chatbot system)
reservations = {}

# 假设餐厅的营业时间
restaurant_hours = {
    'Monday': ('12:00 PM', '10:00 PM'),
    'Tuesday': ('12:00 PM', '10:00 PM'),
    'Wednesday': ('12:00 PM', '10:00 PM'),
    'Thursday': ('12:00 PM', '10:00 PM'),
    'Friday': ('12:00 PM', '10:00 PM'),
    'Saturday': ('12:00 PM', '10:00 PM'),
    'Sunday': 'Closed'
}


def is_valid_reservation_time(input_time):
    try:
        # 将用户输入的时间解析成 datetime 对象
        user_time = datetime.strptime(input_time, '%m/%d/%Y %I:%M %p')
    except ValueError:
        return False, "Invalid time format. Please use the format 'MM/DD/YYYY HH:MM AM/PM'."

    # 检查用户输入的时间是否早于当前时间
    now = datetime.now()
    if user_time < now:
        return False, "The reservation time cannot be in the past. Please choose a future date and time."

    # 检查当天是否为关闭状态
    today = user_time.strftime('%A').strip()  # 获取用户输入的星期几
    if restaurant_hours.get(today) == 'Closed':
        return False, "Sorry, the restaurant is closed on that day."

    # 检查其他营业时间的逻辑（如果不是关闭状态，执行以下代码）
    try:
        open_time_str, close_time_str = restaurant_hours[today]
        open_time = datetime.strptime(open_time_str, '%I:%M %p').time()
        close_time = datetime.strptime(close_time_str, '%I:%M %p').time()

        # 检查用户时间是否在营业时间内
        if not (open_time <= user_time.time() <= close_time):
            return False, (f"Sorry, our operating hours on {today} are from "
                           f"{open_time.strftime('%I:%M %p')} to {close_time.strftime('%I:%M %p')}.")
    except ValueError:
        # 如果 restaurant_hours 中格式错误，提示异常
        return False, "Error with restaurant hours configuration."

    return True, "Valid time."



# Function to make a reservation
def make_reservation(name, party_size, date_time, contact_info):
    # Generate a unique reservation ID
    reservation_id = len(reservations) + 1
    reservations[reservation_id] = {
        "name": name,
        "party_size": party_size,
        "date_time": date_time,
        "status": "confirmed",
        "contact_info": contact_info  # 新增联系方式
    }
    return reservation_id, reservations[reservation_id]

# Function to get reservation details (for confirmation)
def get_reservation_details(reservation_id):
    if reservation_id in reservations:
        reservation = reservations[reservation_id]
        contact_info = reservation.get('contact_info', 'Not provided')
        return (f"Reservation ID: {reservation_id}\n"
                f"Name: {reservation['name']}\n"
                f"Party Size: {reservation['party_size']}\n"
                f"Date/Time: {reservation['date_time']}\n"
                f"Status: {reservation['status']}\n"
                f"Contact Info: {contact_info}")  # 显示联系方式
    else:
        return "Reservation not found."

# Function to check the reservation status
def check_status(reservation_id):
    if reservation_id in reservations:
        reservation = reservations[reservation_id]
        return f"Your reservation for {reservation['party_size']} people at {reservation['date_time']} is {reservation['status']}."
    else:
        return "Reservation not found."

# Function to cancel a reservation
def cancel_reservation(reservation_id):
    if reservation_id in reservations:
        reservations[reservation_id]["status"] = "canceled"
        return f"Your reservation for {reservations[reservation_id]['party_size']} people at {reservations[reservation_id]['date_time']} has been canceled."
    else:
        return "Reservation not found."

def modify_reservation(reservation_id, new_party_size, new_date_time, new_contact_info):
    if reservation_id in reservations:
        reservations[reservation_id]["party_size"] = new_party_size
        reservations[reservation_id]["date_time"] = new_date_time
        reservations[reservation_id]["contact_info"] = new_contact_info  # 更新联系方式
        return f"Your reservation has been updated: {new_party_size} people at {new_date_time}. Contact info: {new_contact_info}."
    else:
        return "Reservation not found."

def check_for_restaurant_query(user_input):
    restaurant_keywords = [
        'restaurant', 'location', 'place', 'name',  # 餐厅本身信息
        'menu', 'food', 'dish', 'items',  # 菜单信息
        'address', 'where',  # 地址信息
        'hours', 'operating hours', 'opening hours', 'time',  # 营业时间信息
        'offers', 'special offers', 'promotions', 'discounts'  # 优惠信息
    ]
    return any(keyword in user_input.lower() for keyword in restaurant_keywords)


# Function to prompt the user for input
def is_valid_email(input_str):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, input_str) is not None


# Function to check if user input is valid phone number
def is_valid_phone(input_str):
    phone_regex = r"^\+?[1-9]\d{1,14}$"
    return re.match(phone_regex, input_str) is not None

# Function to prompt the user for input
def prompt_for_input(prompt, name, restaurant_info):
    while True:
        print(f"Chatbot: {prompt}")  # 显示机器人提示
        user_input = input(f"{name}: ")  # 获取用户输入并加上用户的前缀

        if user_input in ["exit", "quit"]:
            print("Chatbot: Exiting the reservation process. Thank you!")
            print("Exiting the restaurant booking system. Have a nice day!")
            exit()
            
        # 如果用户询问餐厅信息，处理并继续
        if check_for_restaurant_query(user_input):
            handle_restaurant_query(user_input, restaurant_info)  # 调用查询函数提供信息
            continue  # 继续等待其他输入

        # 如果用户输入了日期时间，进行验证
        if "date" in prompt.lower() or "time" in prompt.lower():
            valid, error_message = is_valid_reservation_time(user_input)
            if valid:
                return user_input  # 返回有效的时间
            else:
                print(f"Chatbot: {error_message}")  # 提示日期时间错误

        # 处理人数输入（Party Size: <value>），确保是1到9之间的整数
        if "people" in prompt.lower():
            try:
                value = int(user_input)
                if value > 0 and value < 10:
                    return value
                else:
                    print("Chatbot: The restaurant can only accommodate up to 10 guests at a time.")  # 提示正确范围
            except ValueError:
                print("Chatbot: Please enter a valid number. For example: 3.")  # 提示用户输入有效数字

        # 如果用户输入了邮箱，并且格式有效，则直接返回邮箱
        if "email" in prompt.lower() and is_valid_email(user_input):
            print(f"Chatbot: Got it! Your email is {user_input}.")
            return user_input  # 返回有效的邮箱

        # 如果用户输入了电话号码，并且格式有效，则直接返回电话号码
        elif "phone" in prompt.lower() and is_valid_phone(user_input):
            print(f"Chatbot: Got it! Your phone number is {user_input}.")
            return user_input  # 返回有效的电话

        # 如果没有输入有效的邮箱或电话，提示用户重新输入
        if "email" in prompt.lower() or "phone" in prompt.lower():
            print("Chatbot: Please enter a valid email or phone number.")



# 更新 start_reservation_process 函数
def start_reservation_process(name, restaurant_info):
    print(f"Chatbot: Hello, {name}! Let's proceed with your reservation.")

    # 询问人数
    party_size = prompt_for_input(f"How many people will be in your party? (e.g  3)", name, restaurant_info)

    # 询问日期时间
    date_time = prompt_for_input(f"What date and time would you like to book? (e.g  08/09/2024 6:30 PM)", name, restaurant_info)

    # 询问联系方式
    contact_info = prompt_for_input(f"Please provide your contact information (Email or Phone)", name, restaurant_info)

    print("\nChatbot: Here is the information you provided:")
    print(f"  Party Size: {party_size}")
    print(f"  Date/Time: {date_time}")
    print(f"  Contact Info: {contact_info}")
    # 所有信息收集完成后进行预订
    while True:
        print("Chatbot: Are you sure you want to book? (e.g., yes/yeah for Yes, no/nah for No)")
        user_input = input(f"{name}: ").strip().lower()

        # 调用意图识别
        intent = predict_intent(user_input)

        if intent == "positive_responses":
            # 用户确认预订，跳出确认环节
            break
        elif intent == "negative_responses":
            # 用户拒绝，重新开始流程
            print("Chatbot: Let's re-enter your information.")
            return start_reservation_process(name, restaurant_info)
        else:
            print("Chatbot: I'm sorry, I didn't understand that. Please respond with yes or no.")

    # 生成预订
    reservation_id, reservation_details = make_reservation(name, party_size, date_time, contact_info)
    print(f"Chatbot: Your reservation has been confirmed!\n{get_reservation_details(reservation_id)}")

    # 后续流程：修改、取消等
    while True:
        print("Chatbot: Would you like to [1] check the status, [2] modify, [3] cancel, or [4] finish?")
        user_input = input(f"{name}: ").strip().lower()

        if user_input == "1":
            print(f"Chatbot: {get_reservation_details(reservation_id)}")
        elif user_input == "2":
            # 修改流程
            print("Chatbot: You can modify the following details:")
            print("1. Party size")
            print("2. Date and time")
            print("3. Contact info")

            modify_choice = input("Chatbot: What would you like to modify? (1/2/3): ").strip()

            if modify_choice == "1":
                # 修改人数
                new_party_size = prompt_for_input("How many people will be in your party? (e.g  3)", name, restaurant_info)
                print(modify_reservation(reservation_id, new_party_size, date_time, contact_info))
            elif modify_choice == "2":
                # 修改日期时间
                new_date_time = prompt_for_input("What date and time would you like to book? (e.g  08/09/2024 6:30 PM)", name, restaurant_info)
                print(modify_reservation(reservation_id, party_size, new_date_time, contact_info))
            elif modify_choice == "3":
                # 修改联系方式
                new_contact_info = prompt_for_input("Please provide your new contact information (Email or Phone)", name, restaurant_info)
                print(modify_reservation(reservation_id, party_size, date_time, new_contact_info))
            else:
                print("Chatbot: Invalid option, returning to main menu.")
        elif user_input == "3":
            print(cancel_reservation(reservation_id))
            break
        elif user_input == "4":
            print("Chatbot: Thank you for using our reservation system! You can always make a new reservation later.")
            break
        else:
            print("Chatbot: I'm sorry, I didn't understand that. Please choose a valid option.")

    return True