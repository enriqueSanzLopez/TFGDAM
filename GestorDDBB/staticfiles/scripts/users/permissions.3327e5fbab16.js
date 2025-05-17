try {
    document.addEventListener('DOMContentLoaded', () => {
        document.getElementById('create-permission').addEventListener('click', () => {
            document.getElementById('create-permission-modal-title').innerText = 'Crear permiso';
            document.getElementById('permission_id').value = 'new';
            document.getElementById('permission_name').value = '';
            document.getElementById('permission_value').value = '';
            document.getElementById('permission_order').value = '';
        });

        let ediciones = document.getElementsByClassName('editar-permission');
        for (let i = 0; i < ediciones.length; i++) {
            ediciones[i].addEventListener('click', (e) => {
                const id = e.target.id.split('editar-permission-')[1];
                document.getElementById('create-permission-modal-title').innerText = 'Editar permiso';
                document.getElementById('permission_id').value = document.getElementById('permission-id-' + id).value;
                document.getElementById('permission_name').value = document.getElementById('permission-name-' + id).value;
                document.getElementById('permission_value').value = document.getElementById('permission-value-' + id).value;
                document.getElementById('permission_order').value = document.getElementById('permission-order-' + id).value;
            });
        }

        let borrar = document.getElementsByClassName('borrar-permission');
        for (let i = 0; i < borrar.length; i++) {
            borrar[i].addEventListener('click', (e) => {
                const id = e.target.id.split('borrar-permission-')[1];
                const permissionNameElement = document.getElementById('permission-name-' + id);
                if (permissionNameElement) {
                    document.getElementById('permission_borrar_id').value = id;
                    document.getElementById('permission-borrar-title').innerText = '¿Seguro que quieres eliminar el permiso ' + permissionNameElement.value + '?';
                } else {
                    console.error('Elemento con ID permission-name-' + id + ' no encontrado.');
                }
            });
        }
    });
} catch (e) { }