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
const previousYearButton = document.getElementById('previousYear');
const nextYearButton = document.getElementById('nextYear');
const previousMonthButton = document.getElementById('previousMonth');
const nextMonthButton = document.getElementById('nextMonth');
const yearDisplay = document.getElementById('yearDisplay');
const monthDisplay = document.getElementById('monthDisplay');
const panel = document.getElementById('calendarPanel');
const title = document.getElementById('calendarTitle');
const calendarBody = document.getElementById('calendarBody');
const grid = document.getElementById('calendarGrid');

if (calendarConfig && previousYearButton && nextYearButton && previousMonthButton && nextMonthButton && yearDisplay && monthDisplay && panel && title && calendarBody && grid) {
    const ramalheteUrlTemplate = calendarConfig.dataset.ramalheteUrl;
    const calendarStatus = JSON.parse(calendarConfig.dataset.status);
    const minimumYear = 1900;
    const maximumYear = 2200;
    const now = new Date();
    let currentYear = now.getFullYear();
    let currentMonth = now.getMonth() + 1;

    function pad(value) {
        return String(value).padStart(2, '0');
    }

    function openRamalhete(year, month, day) {
        const date = `${year}-${pad(month)}-${pad(day)}`;
        window.location.href = ramalheteUrlTemplate.replace('0000-00-00', date);
    }

    function updateControls() {
        yearDisplay.value = currentYear;
        monthDisplay.value = monthNames[currentMonth - 1];
        previousYearButton.disabled = currentYear === minimumYear;
        nextYearButton.disabled = currentYear === maximumYear;
        previousMonthButton.disabled = currentYear === minimumYear && currentMonth === 1;
        nextMonthButton.disabled = currentYear === maximumYear && currentMonth === 12;
    }

    function animateCalendar(direction) {
        if (!direction) {
            return;
        }

        calendarBody.classList.remove('slide-left', 'slide-right');
        void calendarBody.offsetWidth;
        calendarBody.classList.add(direction === 'previous' ? 'slide-left' : 'slide-right');
    }

    function renderCalendar(direction) {
        const year = currentYear;
        const month = currentMonth;
        const firstDay = new Date(year, month - 1, 1).getDay();
        const daysInMonth = new Date(year, month, 0).getDate();
        const today = new Date();

        title.textContent = `${monthNames[month - 1]} de ${year}`;
        updateControls();
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
        animateCalendar(direction);
    }

    function changeYear(offset) {
        const nextYear = currentYear + offset;

        if (nextYear >= minimumYear && nextYear <= maximumYear) {
            currentYear = nextYear;
            renderCalendar(offset < 0 ? 'previous' : 'next');
        }
    }

    function changeMonth(offset) {
        const nextDate = new Date(currentYear, currentMonth - 1 + offset, 1);
        const nextYear = nextDate.getFullYear();

        if (nextYear >= minimumYear && nextYear <= maximumYear) {
            currentYear = nextYear;
            currentMonth = nextDate.getMonth() + 1;
            renderCalendar(offset < 0 ? 'previous' : 'next');
        }
    }

    previousYearButton.addEventListener('click', () => changeYear(-1));
    nextYearButton.addEventListener('click', () => changeYear(1));
    previousMonthButton.addEventListener('click', () => changeMonth(-1));
    nextMonthButton.addEventListener('click', () => changeMonth(1));

    renderCalendar();
}
