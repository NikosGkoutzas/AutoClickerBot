def number(from_: int , to_: int , one_choice: int | None) -> list[str]:
    number_list = [
                    '①' , '②' , '③' , '④' , '⑤' , '⑥' , '⑦' , '⑧' , '⑨' , '⑩' , 
                    '⑪' , '⑫' , '⑬' , '⑭' , '⑮' , '⑯' , '⑰' , '⑱' , '⑲' , '⑳' , 
                    '㉑' , '㉒' , '㉓' , '㉔' , '㉕' , '㉖' , '㉗' , '㉘' , '㉙' , '㉚' , 
                    '㉛' , '㉜' , '㉝' , '㉞' , '㉟' , '㊱' , '㊲' , '㊳' , '㊴' , '㊵'
                  ]
    
    if(from_ is None and to_ is None):
        if(not isinstance(one_choice , int)):
            raise ValueError('3rd parameter of \'number\' function must be an integer.')
        
        if(one_choice is None):
            raise ValueError('3rd parameter of \'number\' function must be selected.')
        
        if(one_choice >=1 and one_choice <= 40):
            return list(number_list[one_choice - 1])
    
    if(from_ < to_ and from_ >= 1 and to_ <= 40):
        chosen_list = []
        for chosen_number in range(from_ , to_+1):
            chosen_list.append(number_list[chosen_number - 1])

        return chosen_list
    
    raise ValueError('Please select a valid range.')
    
