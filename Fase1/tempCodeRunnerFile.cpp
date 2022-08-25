char *stringtochar(string s)
{

    char *char_arr;
    string str_obj(s);
    char_arr = &str_obj[0];
    return char_arr;
}