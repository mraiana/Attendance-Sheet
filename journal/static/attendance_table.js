document.addEventListener('DOMContentLoaded', function() {
    const addRowButton = document.getElementById('add-row-button');
    const tableBody = document.getElementById('attendance-table-body');
    let newRowCount = 3; // Начинаем с индекса после начальных пустых строк

    addRowButton.addEventListener('click', function() {
        const newRow = tableBody.insertRow(-1);
        newRow.classList.add('new-student-row');

        let cellIndex = 0;

        // Ячейка для ФИО
        let nameCell = newRow.insertCell(cellIndex++);
        let nameInput = document.createElement('input');
        nameInput.type = 'text';
        nameInput.name = `new_student_name_${newRowCount}`;
        nameInput.placeholder = 'Имя Фамилия';
        nameCell.appendChild(nameInput);

        // Ячейка для Отсутствия
        let statusCell = newRow.insertCell(cellIndex++);
        let statusCheckbox = document.createElement('input');
        statusCheckbox.type = 'checkbox';
        statusCheckbox.name = `new_status_${newRowCount}`;
        statusCheckbox.value = 'absent';
        statusCell.appendChild(statusCheckbox);

        // Ячейка для Причины
        let reasonCell = newRow.insertCell(cellIndex++);
        let reasonInput = document.createElement('input');
        reasonInput.type = 'text';
        reasonInput.name = `new_reason_${newRowCount}`;
        reasonInput.placeholder = 'Введите причину';
        reasonCell.appendChild(reasonInput);

        // Ячейка для Опоздал
        let lateCell = newRow.insertCell(cellIndex++);
        let lateCheckbox = document.createElement('input');
        lateCheckbox.type = 'checkbox';
        lateCheckbox.name = `new_late_${newRowCount}`;
        lateCheckbox.value = 'late';
        lateCell.appendChild(lateCheckbox);

        // Ячейка для Времени опоздания
        let lateTimeCell = newRow.insertCell(cellIndex++);
        let lateTimeInput = document.createElement('input');
        lateTimeInput.type = 'number';
        lateTimeInput.name = `new_late_time_${newRowCount}`;
        lateTimeInput.placeholder = 'Время в минутах';
        lateTimeCell.appendChild(lateTimeInput);

        newRowCount++;
    });
});