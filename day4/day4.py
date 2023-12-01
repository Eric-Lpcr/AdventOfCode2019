from types import SimpleNamespace

doubles = [str(x)*2 for x in range(10)]


def check_password_rule1(password: str):
    if not any([double in password for double in doubles]):
        return False
    digits = [int(d) for d in str(password)]
    return all([digits[i] >= digits[i-1] for i in range(1, len(digits))])


def check_password_rule2(password: str):
    digits = [SimpleNamespace(digit=int(d), count=1, greater=True) for d in str(password)]
    for i in reversed(range(1, len(digits))):
        digits[i].greater = digits[i].digit >= digits[i-1].digit
        if digits[i].digit == digits[i-1].digit:
            digits[i-1].count += digits[i].count
            digits[i].count = 0
    digits = [d for d in digits if d.count > 0]

    return all([d.greater for d in digits]) and any([d.count == 2 for d in digits])


def main():
    input_text = "248345-746315"
    m, n = [int(s) for s in input_text.split('-')]

    res1 = res2 = 0
    for p in range(m, n+1):
        password = "00000" + str(p)
        password = password[-6:]
        if check_password_rule1(password):
            res1 += 1
        if check_password_rule2(password):
            res2 += 1

    print(f"Found {res1} different passwords meeting ruleset 1")
    print(f"Found {res2} different passwords meeting ruleset 2")


if __name__ == '__main__':
    main()
