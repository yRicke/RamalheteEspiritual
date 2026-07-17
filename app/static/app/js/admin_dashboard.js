const monthNames = [
    'Janeiro',
    'Fevereiro',
    'Março',
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

const adminConfig = document.getElementById('adminDashboardConfig');
const previousYearButton = document.getElementById('adminPreviousYear');
const nextYearButton = document.getElementById('adminNextYear');
const previousMonthButton = document.getElementById('adminPreviousMonth');
const nextMonthButton = document.getElementById('adminNextMonth');
const yearDisplay = document.getElementById('adminYearDisplay');
const monthDisplay = document.getElementById('adminMonthDisplay');
const summaryPeriod = document.getElementById('adminSummaryPeriod');
const summaryGrid = document.getElementById('adminSummaryGrid');
const summaryValues = document.querySelectorAll('[data-admin-summary-field]');

if (adminConfig && previousYearButton && nextYearButton && previousMonthButton && nextMonthButton && yearDisplay && monthDisplay && summaryPeriod && summaryGrid) {
    const summaryUrlTemplate = adminConfig.dataset.summaryUrl;
    const minimumYear = 1900;
    const maximumYear = 2200;
    const now = new Date();
    let currentYear = now.getFullYear();
    let currentMonth = now.getMonth() + 1;
    let latestRequest = 0;

    function updateControls() {
        yearDisplay.value = currentYear;
        monthDisplay.value = monthNames[currentMonth - 1];
        previousYearButton.disabled = currentYear === minimumYear;
        nextYearButton.disabled = currentYear === maximumYear;
        previousMonthButton.disabled = currentYear === minimumYear && currentMonth === 1;
        nextMonthButton.disabled = currentYear === maximumYear && currentMonth === 12;
    }

    function animateSummary(direction) {
        if (!direction) {
            return;
        }

        summaryGrid.classList.remove('slide-left', 'slide-right');
        void summaryGrid.offsetWidth;
        summaryGrid.classList.add(direction === 'previous' ? 'slide-left' : 'slide-right');
    }

    async function updateSummary(direction) {
        const requestNumber = latestRequest + 1;
        latestRequest = requestNumber;
        updateControls();
        summaryPeriod.textContent = `Carregando ${monthNames[currentMonth - 1]} de ${currentYear}...`;

        try {
            const url = summaryUrlTemplate.replace('0/0', `${currentYear}/${currentMonth}`);
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error('Falha ao carregar o resumo.');
            }

            const totals = await response.json();
            if (requestNumber !== latestRequest) {
                return;
            }

            summaryValues.forEach((element) => {
                element.textContent = Number(totals[element.dataset.adminSummaryField] || 0).toLocaleString('pt-BR');
            });
            summaryPeriod.textContent = `${monthNames[currentMonth - 1]} de ${currentYear}`;
            animateSummary(direction);
        } catch (error) {
            if (requestNumber === latestRequest) {
                summaryPeriod.textContent = 'Não foi possível carregar os totais.';
            }
        }
    }

    function changeYear(offset) {
        const nextYear = currentYear + offset;

        if (nextYear >= minimumYear && nextYear <= maximumYear) {
            currentYear = nextYear;
            updateSummary(offset < 0 ? 'previous' : 'next');
        }
    }

    function changeMonth(offset) {
        const nextDate = new Date(currentYear, currentMonth - 1 + offset, 1);
        const nextYear = nextDate.getFullYear();

        if (nextYear >= minimumYear && nextYear <= maximumYear) {
            currentYear = nextYear;
            currentMonth = nextDate.getMonth() + 1;
            updateSummary(offset < 0 ? 'previous' : 'next');
        }
    }

    previousYearButton.addEventListener('click', () => changeYear(-1));
    nextYearButton.addEventListener('click', () => changeYear(1));
    previousMonthButton.addEventListener('click', () => changeMonth(-1));
    nextMonthButton.addEventListener('click', () => changeMonth(1));

    updateSummary();
}

document.querySelectorAll('[data-password-toggle]').forEach((toggle) => {
    toggle.addEventListener('change', () => {
        const passwordInput = document.getElementById(toggle.dataset.passwordToggle);
        if (passwordInput) {
            passwordInput.type = toggle.checked ? 'text' : 'password';
        }
    });
});
