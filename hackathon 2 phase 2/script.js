document.addEventListener('DOMContentLoaded', () => {
    const todoInput = document.getElementById('todo-input');
    const addTodoBtn = document.getElementById('add-todo-btn');
    const todoList = document.getElementById('todo-list');

    let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

    function saveTasks() {
        localStorage.setItem('tasks', JSON.stringify(tasks));
    }

    function renderTasks() {
        todoList.innerHTML = ''; // Clear current list

        tasks.forEach((task, index) => {
            const listItem = document.createElement('li');
            if (task.completed) {
                listItem.classList.add('completed');
            }

            const taskTextSpan = document.createElement('span');
            taskTextSpan.textContent = task.text;
            taskTextSpan.addEventListener('click', () => toggleComplete(index));

            const actionsDiv = document.createElement('div');
            actionsDiv.classList.add('actions');

            const completeBtn = document.createElement('button');
            completeBtn.classList.add('complete-btn');
            completeBtn.innerHTML = '&#10003;'; // Checkmark symbol
            completeBtn.title = task.completed ? 'Mark as Incomplete' : 'Mark as Complete';
            completeBtn.addEventListener('click', () => toggleComplete(index));

            const deleteBtn = document.createElement('button');
            deleteBtn.classList.add('delete-btn');
            deleteBtn.innerHTML = '&#10060;'; // Cross mark symbol
            deleteBtn.title = 'Delete Task';
            deleteBtn.addEventListener('click', () => deleteTask(index));

            actionsDiv.appendChild(completeBtn);
            actionsDiv.appendChild(deleteBtn);
            listItem.appendChild(taskTextSpan);
            listItem.appendChild(actionsDiv);
            todoList.appendChild(listItem);
        });
    }

    function addTask() {
        const taskText = todoInput.value.trim();
        if (taskText !== '') {
            tasks.push({ text: taskText, completed: false });
            todoInput.value = ''; // Clear input
            saveTasks();
            renderTasks();
        }
    }

    function toggleComplete(index) {
        tasks[index].completed = !tasks[index].completed;
        saveTasks();
        renderTasks();
    }

    function deleteTask(index) {
        tasks.splice(index, 1); // Remove 1 element at the given index
        saveTasks();
        renderTasks();
    }

    // Event Listeners
    addTodoBtn.addEventListener('click', addTask);
    todoInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            addTask();
        }
    });

    // Initial render
    renderTasks();
});
