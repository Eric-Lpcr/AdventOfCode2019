

def compute_fuel(mass):
    return max(0, mass // 3 - 2)


def compute_fuel_for_fuel(mass):
    fuel = compute_fuel(mass)
    fuel_for_fuel = compute_fuel(fuel)
    while fuel_for_fuel > 0:
        fuel += fuel_for_fuel
        fuel_for_fuel = compute_fuel(fuel_for_fuel)
    return fuel


def main():
    with open('input.txt') as f:
        modules = [int(line) for line in f.readlines()]

    res = 0
    for m in modules:
        res += compute_fuel(m)
    print("Need", res, "fuel for modules")

    res = 0
    for m in modules:
        res += compute_fuel_for_fuel(m)
    print("Need", res, "fuel for modules and fuel")


if __name__ == '__main__':
    main()
