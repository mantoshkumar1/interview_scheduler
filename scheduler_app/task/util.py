def verify_rpc_value(user_dict):
    for key in user_dict:
        if type(user_dict[key]) == unicode or type(user_dict[key]) == str:
            continue
        else:
            raise ValueError('Value is not String')