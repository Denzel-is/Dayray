import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Данные задач проекта
tasks = [
    ('Планирование проекта', '2024-10-31', '2024-11-07'),
    ('Разработка базы данных', '2024-11-03', '2024-11-11'),
    ('Разработка серверной части', '2024-11-11', '2024-11-20'),
    ('Дизайн интерфейса', '2024-11-20', '2024-11-27'),
    ('Разработка админской части', '2024-11-27', '2024-12-06'),
    ('Написание документации', '2024-12-05', '2024-12-15'),
    ('Тестирование', '2024-12-15', '2024-12-22'),
    ('Презентация', '2024-12-24', '2024-12-28'),
]

# Преобразование строк в объекты datetime
tasks = [(task, datetime.strptime(start, '%Y-%m-%d'), datetime.strptime(end, '%Y-%m-%d')) for task, start, end in tasks]

# Создание графика
fig, ax = plt.subplots(figsize=(10, 6))

# Цвета для задач
colors = ['#ff6347', '#ff9a8b', '#f4a300', '#61c0bf', '#a7c7e7', '#5e81e7', '#c7d7e5', '#b8e994']  # Добавлен новый цвет

# Добавление данных на график
for i, (task, start, end) in enumerate(tasks):
    ax.barh(i, (end - start).days, left=start, height=0.6, color=colors[i], edgecolor='black', linewidth=1.2)
    ax.text(start, i, f" {task}", va='center', ha='left', color='white', fontsize=10, fontweight='bold')

# Форматирование оси времени
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
plt.xticks(rotation=45)
plt.xlabel('Дата', fontsize=11)
plt.ylabel('Задачи', fontsize=11)

# Настройки для лучшего отображения
plt.title('Диаграмма Ганта проекта с 31 октября по 25 декабря 2024', fontsize=16, fontweight='bold')
plt.tight_layout()

# Добавление сетки
ax.grid(True, axis='x', linestyle='--', alpha=0.6)

# Показ диаграммы
plt.show()
