import re
from datetime import datetime
from Intent_Recognizer import predict_intent
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
reservations = {}
from collections import deque
reservation_history = deque(maxlen=10)

# 队列存储预订历史记录，最多保存 10 条记录


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


# 发送邮件的功能
def send_confirmation_email(user_email, reservation_details):
    try:
        # 设置网易邮箱的SMTP服务器（例如使用网易 SMTP 服务器）
        smtp_server = "smtp.gmail.com"
        smtp_port = 465  # 选择465端口（SSL加密）
        sender_email = "yixinhou37@gmail.com"  # 发送者的网易邮箱地址
        sender_password = "yroejhojxxyzbnee"  # 发送者的邮箱密码（如果启用了2步验证，可以使用应用专用密码）

        # 创建邮件
        subject = "Your Reservation Confirmation"
        body = f"Thank you for your reservation!\n\n{reservation_details}"

        # 邮件内容
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = user_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # 连接SMTP服务器并发送邮件
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:  # 使用SSL加密
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, message.as_string())

        print("Chatbot: Your reservation details have been sent to your email!")

    except Exception as e:
        print(f"Chatbot: Failed to send email. Error: {e}")

def is_valid_reservation_time(input_time):
    try:
        # 尝试解析用户输入的时间为 DD/MM/YYYY 格式
        user_time = datetime.strptime(input_time, '%d/%m/%Y %I:%M %p')
    except ValueError:
        return False, "Invalid time format. Please use the format 'DD/MM/YYYY HH:MM AM/PM'."

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

def modify_reservation(reservation_id, new_name, new_party_size, new_date_time, new_contact_info):
    if reservation_id in reservations:
        reservations[reservation_id]["name"] = new_name
        reservations[reservation_id]["party_size"] = new_party_size
        reservations[reservation_id]["date_time"] = new_date_time
        reservations[reservation_id]["contact_info"] = new_contact_info  # 更新联系方式
        return f"Your reservation has been updated: {new_name} booked {new_party_size} people at {new_date_time}. Contact info: {new_contact_info}."
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


# 添加历史记录的函数
def add_to_reservation_history(reservation_details):
    reservation_history.append(reservation_details)

# 获取历史记录的函数
def get_reservation_history():
    if not reservation_history:
        return "No reservation history found. Please make a reservation first."
    return "\n".join(
        [f"Record {i+1}: {record}" for i, record in enumerate(reservation_history)]
    )

# Function to prompt the user for input
def prompt_for_input(prompt, name, restaurant_info):
    while True:
        print(f"Chatbot: {prompt}")
        user_input = input(f"{name}: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Exiting the reservation process. Thank you!")
            exit()

        # 检测意图
        intent = predict_intent(user_input)

        # 如果用户输入 "change"，处理修改名字逻辑
        if intent == "change":
            new_name = input("Chatbot: Please provide the new name: ").strip()
            if new_name:
                print(f"Chatbot: Got it! The name has been changed to {new_name}.")
                return new_name, True  # 返回新名字并标记为名字更新
            else:
                print("Chatbot: Name change canceled. Please try again.")
                continue

        # 验证其他输入类型
        if "name" in prompt.lower():
            if user_input:
                print(f"Chatbot: Got it! The new name is {user_input}.")
                return user_input, True  # 返回新名字并标记为名字更新
            else:
                print("Chatbot: Name cannot be empty. Please try again.")

        if "date" in prompt.lower() or "time" in prompt.lower():
            valid, error_message = is_valid_reservation_time(user_input)
            if valid:
                return user_input, False  # 返回有效时间，不标记为名字更新
            else:
                print(f"Chatbot: {error_message}")

        if "people" in prompt.lower():
            try:
                value = int(user_input)
                if 1 <= value <= 10:  # 限制人数范围
                    return value, False  # 返回人数，不标记为名字更新
                else:
                    print("Chatbot: The restaurant can only accommodate up to 10 guests at a time.")
            except ValueError:
                print("Chatbot: Please enter a valid number. For example: 3.")

        if "email" in prompt.lower() and is_valid_email(user_input):
            print(f"Chatbot: Got it! Your email is {user_input}.")
            return user_input, False  # 返回有效的邮箱，不标记为名字更新


        print("Chatbot: Invalid input. Please try again.")

def start_reservation_process(name, restaurant_info):
    while True:
        print(f"Chatbot: Hello, {name}! Let's proceed with your reservation.")

        # 询问人数
        while True:
            value, is_name_update = prompt_for_input(f"How many people will be in your party? (e.g., 3)", name, restaurant_info)
            if is_name_update:
                name = value  # 更新名字
                continue  # 重新开始
            else:
                party_size = value
                break

        # 询问日期时间
        while True:
            value, is_name_update = prompt_for_input(f"What date and time would you like to book? (eg: To book a reservation for 6:30 PM on December 15, 2024, please use the format: 15/12/2024 6:30 PM)", name, restaurant_info)
            if is_name_update:
                name = value  # 更新名字
                continue
            else:
                date_time = value
                break

        # 询问联系方式
        while True:
            value, is_name_update = prompt_for_input(f"Please provide your contact information (Email,eg:qweasd@gmail.com)", name, restaurant_info)
            if is_name_update:
                name = value  # 更新名字
                continue
            else:
                contact_info = value
                break

        # 确认用户输入的信息
        print("\nChatbot: Here is the information you provided:")
        print(f"  Name: {name}")
        print(f"  Party Size: {party_size}")
        print(f"  Date/Time: {date_time}")
        print(f"  Contact Info: {contact_info}")

        while True:
            print("Chatbot: Are you sure you want to book? (e.g., yes/yeah for Yes, no/nah for No)")
            user_input = input(f"{name}: ").strip().lower()

            # 基于规则的匹配
            if "yes" in user_input or "yeah" in user_input:
                print("Chatbot: Great! Your reservation is confirmed.")
                break
            elif "no" in user_input or "nah" in user_input:
                print("Chatbot: Let's re-enter your information.")
                return start_reservation_process(name, restaurant_info)
            elif "change" in user_input:
                name = input("Chatbot: Please provide the new name: ").strip()
                print(f"Chatbot: Got it! The name has been changed to {name}.")
            else:
                print("Chatbot: I'm sorry, I didn't understand that. Please respond with yes or no.")

        # 生成预订
        reservation_id, reservation_details = make_reservation(name, party_size, date_time, contact_info)
        print(f"Chatbot: Your reservation has been confirmed!\n{get_reservation_details(reservation_id)}")

        # 后续流程：修改、取消等
        while True:
            print("Chatbot: Would you like to [1] check the status, [2] modify, [3] cancel, or [4] confirm your reservation?")

            user_input = input(f"{name}: ").strip().lower()

            if user_input == "1":
                print(f"Chatbot: {get_reservation_details(reservation_id)}")
            elif user_input == "2":
                # 修改流程
                print("Chatbot: You can modify the following details:")
                print("0. Name")
                print("1. Party size")
                print("2. Date and time")
                print("3. Contact info")

                modify_choice = input("Chatbot: What would you like to modify? (0/1/2/3): ").strip()
                if modify_choice == "0":
                    new_name, _ = prompt_for_input("What's the new name? (e.g Patrick)", name, restaurant_info)
                    print(modify_reservation(reservation_id, new_name, party_size, date_time, contact_info))
                elif modify_choice == "1":
                    # 修改人数
                    new_party_size, is_name_update = prompt_for_input("How many people will be in your party? (e.g 3)", name, restaurant_info)
                    print(new_party_size)
                    print(modify_reservation(reservation_id, name, new_party_size, date_time, contact_info))
                elif modify_choice == "2":
                    # 修改日期时间
                    new_date_time ,is_name_update= prompt_for_input(
                        "What date and time would you like to book? (eg: To book a reservation for 6:30 PM on December 15, 2024, please use the format: 15/12/2024 6:30 PM)", name, restaurant_info)
                    print(new_date_time)
                    print(modify_reservation(reservation_id, name, party_size, new_date_time, contact_info))
                elif modify_choice == "3":
                    # 修改联系方式
                    new_contact_info,is_name_update = prompt_for_input("Please provide your new contact information (Email,eg:qweasd@gmail.com)",
                                                        name, restaurant_info)
                    print(modify_reservation(reservation_id, name, party_size, date_time, new_contact_info))
                else:
                    print("Chatbot: Invalid option, returning to main menu.")

            elif user_input == "3":
                print(cancel_reservation(reservation_id))
                break

            elif user_input == "4":
                # 确认预订并发送邮件
                reservation_details_text = get_reservation_details(reservation_id)
                print(f"Chatbot: Here is your reservation details:\n{reservation_details_text}")
                send_confirmation_email(contact_info, reservation_details_text)  # 发送邮件
                reservation_history.append(reservation_details_text)
                print(
                    "Chatbot: Your reservation has been saved to history and the details have been sent to your email. Thank you for using our system!")
                return True

        else:
                print("Chatbot: I'm sorry, I didn't understand that. Please choose a valid option.")

        return True
