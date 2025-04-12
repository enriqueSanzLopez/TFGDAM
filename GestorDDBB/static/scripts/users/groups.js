try {
    document.addEventListener('DOMContentLoaded', () => {
        let borrar = document.getElementsByClassName('borrar-group');
        for (let i = 0; i < borrar.length; i++) {
            borrar[i].addEventListener('click', (e) => {
                const id = e.target.id.split('borrar-group-')[1];
                const groupNameElement = document.getElementById('group-name-' + id);
                if (groupNameElement) {
                    document.getElementById('group_borrar_id').value = id;
                    document.getElementById('group-borrar-title').innerText = '¿Seguro que quieres eliminar el permiso ' + groupNameElement.value + '?';
                } else {
                    console.error('Elemento con ID group-name-' + id + ' no encontrado.');
                }
            });
        }
    });
} catch (e) { }