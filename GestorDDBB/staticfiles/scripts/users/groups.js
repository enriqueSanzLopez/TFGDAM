try {
    document.addEventListener('DOMContentLoaded', () => {
        let borrar = document.getElementsByClassName('borrar-group');
        for (let i = 0; i < borrar.length; i++) {
            borrar[i].addEventListener('click', (e) => {
                const id = e.target.id.split('borrar-group-')[1];
                const groupNameElement = document.getElementById('group-name-' + id);
                if (groupNameElement) {
                    document.getElementById('group_borrar_id').value = id;
                    document.getElementById('group-borrar-title').innerText = '¿Seguro que quieres eliminar el grupo ' + groupNameElement.value + '?';
                } else {
                    console.error('Elemento con ID group-name-' + id + ' no encontrado.');
                }
            });
        }
        document.getElementById('create-group').addEventListener('click', () => {
            document.getElementById('create-group-modal-title').innerText = 'Crear grupo';
            document.getElementById('group_id').value = 'new';
            document.getElementById('group_name').value = '';
            const checkboxes = document.querySelectorAll('input[name="permissions"]');
            checkboxes.forEach(function (checkbox) {
                checkbox.checked = false;
            });
        });
        let editar = document.getElementsByClassName('editar-group');
        for (let i = 0; i < editar.length; i++) {
            editar[i].addEventListener('click', (e) => {
                const id = e.target.id.split('editar-group-')[1];
                document.getElementById('create-group-modal-title').innerText = 'Editar grupo';
                document.getElementById('group_id').value = id;
                document.getElementById('group_name').value = document.getElementById('group-name-' + id).value;
                const checkboxes = document.querySelectorAll('input[name="permissions"]');
                let permisos = document.getElementById('permissions-' + id).value.split(',');
                console.log(permisos)
                checkboxes.forEach(function (checkbox) {
                    checkbox.checked = false;
                    console.log(checkbox.value)
                    for (let j = 0; j < permisos.length; j++) {
                        if (permisos[j] == checkbox.value) {
                            checkbox.checked = true;
                        }
                    }
                });
            });
        }
    });
} catch (e) { }