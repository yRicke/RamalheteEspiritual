const monthNames = [
    'Janeiro',
    'Fevereiro',
    'Marco',
    'Abril',
    'Maio',
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro'
];

const calendarConfig = document.getElementById('calendarConfig');
const form = document.getElementById('calendarForm');
const yearInput = document.getElementById('yearInput');
const monthInput = document.getElementById('monthInput');
const panel = document.getElementById('calendarPanel');
const title = document.getElementById('calendarTitle');
const grid = document.getElementById('calendarGrid');

if (calendarConfig && form && yearInput && monthInput && panel && title && grid) {
    const ramalheteUrlTemplate = calendarConfig.dataset.ramalheteUrl;
    const calendarStatus = JSON.parse(calendarConfig.dataset.status);

    function pad(value) {
        return String(value).padStart(2, '0');
    }

    function openRamalhete(year, month, day) {
        const date = `${year}-${pad(month)}-${pad(day)}`;
        window.location.href = ramalheteUrlTemplate.replace('0000-00-00', date);
    }

    function renderCalendar(year, month) {
        const firstDay = new Date(year, month - 1, 1).getDay();
        const daysInMonth = new Date(year, month, 0).getDate();
        const today = new Date();

        title.textContent = `${monthNames[month - 1]} de ${year}`;
        grid.innerHTML = '';

        for (let i = 0; i < firstDay; i += 1) {
            const emptyCell = document.createElement('div');
            emptyCell.className = 'day-cell empty';
            grid.appendChild(emptyCell);
        }

        for (let day = 1; day <= daysInMonth; day += 1) {
            const button = document.createElement('button');
            const date = `${year}-${pad(month)}-${pad(day)}`;
            const ramalheteStatus = calendarStatus[date] || '';
            const isToday = today.getFullYear() === Number(year) &&
                today.getMonth() === month - 1 &&
                today.getDate() === day;

            button.type = 'button';
            button.className = `day-cell${ramalheteStatus ? ` ${ramalheteStatus}` : ''}${isToday ? ' today' : ''}`;
            button.innerHTML = `<span class="day-number">${day}</span><span class="day-hint">${ramalheteStatus === 'complete' ? 'Preenchido' : ramalheteStatus === 'pending' ? 'Em branco' : 'Sem ramalhete'}</span>`;
            button.addEventListener('click', () => openRamalhete(year, month, day));
            grid.appendChild(button);
        }

        panel.hidden = false;
    }

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const year = Number(yearInput.value);
        const month = Number(monthInput.value);

        if (year && month) {
            renderCalendar(year, month);
        }
    });

    const now = new Date();
    yearInput.value = now.getFullYear();
    monthInput.value = now.getMonth() + 1;
    renderCalendar(now.getFullYear(), now.getMonth() + 1);
}
