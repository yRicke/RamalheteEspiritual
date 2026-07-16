const ramalheteForm = document.getElementById('ramalheteForm');

if (ramalheteForm) {
    const saveStatus = document.getElementById('saveStatus');
    const csrfToken = ramalheteForm.querySelector('[name=csrfmiddlewaretoken]').value;
    const inputs = ramalheteForm.querySelectorAll('input[type="number"]');
    const saveTimers = new Map();

    function updateStatus(message, hasError = false) {
        saveStatus.textContent = message;
        saveStatus.classList.toggle('error', hasError);
    }

    async function saveField(input) {
        const valor = input.value === '' ? 0 : Number(input.value);

        if (!Number.isInteger(valor) || valor < 0) {
            updateStatus('Informe um valor igual ou maior que zero.', true);
            return;
        }

        input.value = valor;
        updateStatus('Salvando...');

        try {
            const response = await fetch(ramalheteForm.dataset.saveUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
                body: new URLSearchParams({ campo: input.name, valor }),
            });

            if (!response.ok) {
                throw new Error('Falha ao salvar.');
            }

            updateStatus('Alteracoes salvas.');
        } catch (error) {
            updateStatus('Nao foi possivel salvar. Tente novamente.', true);
        }
    }

    function scheduleSave(input) {
        window.clearTimeout(saveTimers.get(input));
        updateStatus('Salvando...');
        saveTimers.set(input, window.setTimeout(() => saveField(input), 500));
    }

    inputs.forEach((input) => {
        input.addEventListener('input', () => scheduleSave(input));
        input.addEventListener('change', () => {
            window.clearTimeout(saveTimers.get(input));
            saveField(input);
        });
    });

    ramalheteForm.addEventListener('submit', (event) => event.preventDefault());
}
