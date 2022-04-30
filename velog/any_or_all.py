def any_or_all(p_list, value, type):
    if type == "any":
        if any(value == i for i in p_list):
            print(f"{value}이(가) 리스트에 존재함")
        else:
            print(f"{value}이(가) 리스트에 존재하지 않음")
    elif type == "all":
        if all(value == i for i in p_list):
            print(f"모든 리스트가 {value}")
        else:
            print(f"{value}이(가) 아닌 값이 존재")


temp_list = [1, 2, 3, 4, 5]
value = 3
any_or_all(temp_list, value, "any")

temp_list = [1, 2, 3, 4, 5]
value = 6
any_or_all(temp_list, value, "any")

temp_list = [3, 3, 3, 3, 3]
value = 3
any_or_all(temp_list, value, "all")

temp_list = [5, 5, 5, 5, 6]
value = 5
any_or_all(temp_list, value, "all")
