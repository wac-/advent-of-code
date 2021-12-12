population: list[int] = [0] * 9

with open('2021-12-06.txt') as f:
    initial_population_text = f.readline().strip()
    for lanternfish in initial_population_text.split(','):
        population[int(lanternfish)] += 1

print(population)

# Simulate each day.
for day in range(1,256 + 1):
    replicating_fish_count: int = population.pop(0)
    population[6] += replicating_fish_count
    population.append(replicating_fish_count)
    
    print('Day {}: {} = {}'.format(day, sum(population), population))

print(sum(population))
