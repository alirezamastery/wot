import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

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


def calculator(base_points):
    final_sums = list()
    for i, boost in enumerate(boosts):
        print('\n' + f'boost level: {i} -- boost percent: {boost["total_boost"]}% -- base points: {base_points}')
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
                  f'income: {income_points} | i: {i}  counter: {step_counter}')
        print(f'total: {total_points:<7}')

        if step_counter > i:
            final_sums.append(total_points)
        else:
            break

    print(final_sums)

    return final_sums


LEGEND_SIZE = 15
ANNOTATE_SIZE = 10
SHOW_PERCENT = False
if __name__ == '__main__':
    base_incomes = [x for x in range(500, 15000, 250)]
    multiple_final_sums = [calculator(base_income) for base_income in base_incomes]

    labels = ['0 %', '5 %', '10 %', '20 %', '40 %', '60 %', '90 %', '120 %', '160 %', '200 %', '240 %']

    figs, ax = plt.subplots(1, constrained_layout=True)
    for final_sums in multiple_final_sums:
        x_range = [x for x in range(len(final_sums))]
        x_labels = [label for label in labels[:len(final_sums)]]

        ax.plot(x_range, final_sums, '--o')

        for i in x_range:
            ax.annotate(f'{final_sums[i]:,}\n{boosts[i]["total_boost"] + "%" if SHOW_PERCENT else ""}',
                        (i, final_sums[i]),
                        xytext=(-1, 5), textcoords='offset points', fontsize=ANNOTATE_SIZE)

    plt.xlabel('boost level', labelpad=20, fontsize=18)
    plt.ylabel('total point at the end of campaign', labelpad=20, fontsize=18)
    plt.xticks([x for x in range(len(labels))], labels, fontsize=18)
    plt.yticks(fontsize=18)
    # plt.legend([f'Base daily Fame Points: {base_income:,}' for base_income in base_incomes],
    #            prop={'size': LEGEND_SIZE})

    plt.grid(True)

    plt.show()
