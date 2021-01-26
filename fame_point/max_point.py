import matplotlib.pyplot as plt

CAMPAIGN_DAYS = 14

boosts = (
    {'percent': 0.00, 'total_boost': 0, 'price': 0},
    {'percent': 0.05, 'total_boost': 5, 'price': 10},
    {'percent': 0.05, 'total_boost': 10, 'price': 50},
    {'percent': 0.10, 'total_boost': 20, 'price': 250},
    {'percent': 0.20, 'total_boost': 40, 'price': 1000},
    {'percent': 0.20, 'total_boost': 60, 'price': 2500},
    {'percent': 0.30, 'total_boost': 90, 'price': 5000},
    {'percent': 0.30, 'total_boost': 120, 'price': 20000},
    {'percent': 0.40, 'total_boost': 160, 'price': 30000},
    {'percent': 0.40, 'total_boost': 200, 'price': 40000},
    {'percent': 0.40, 'total_boost': 240, 'price': 50000},
)


def max_finder(base_points):
    final_sums = list()
    for i, boost in enumerate(boosts):
        print('-' * 20, i, boost, '-' * 20)
        income_points = base_points
        multiplier = 1
        total_points = 0
        step_counter = 0

        for day in range(CAMPAIGN_DAYS):
            total_points += income_points
            while step_counter <= i and total_points > boosts[step_counter]['price']:
                multiplier += boosts[step_counter]['percent']
                total_points -= boosts[step_counter]['price']
                income_points = int(base_points * multiplier)
                step_counter += 1
            print(f'day: {day + 1:<2} | total: {int(total_points):<5} | multiplier: {multiplier:<4.2f} | '
                  f'income: {income_points}')
        print(f'total: {total_points:<7}')
        final_sums.append(total_points)
    print(final_sums)

    return final_sums.index(max(final_sums))


if __name__ == '__main__':
    step = max_finder(1000)
    print(step, boosts[step]['total_boost'])
    base_points = [x for x in range(100 , 2000)]
    max_points = [max_finder(i) for i in base_points]

    y_range = [x for x in range(11)]
    y_labels = ['0 %', '5 %', '10 %', '20 %', '40 %', '60 %', '90 %', '120 %', '160 %', '200 %', '240 %']

    plt.plot(base_points, max_points, linewidth=5)
    plt.xlabel('average daily base fame points', labelpad=20, fontsize=18)
    plt.ylabel('optimum boost level', labelpad=20, fontsize=18)

    plt.xticks(fontsize=18)
    plt.yticks(y_range, y_labels, fontsize=18)

    plt.grid()

    plt.show()
