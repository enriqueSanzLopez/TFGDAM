document.addEventListener('DOMContentLoaded', () => {
    const modalTitle = document.getElementById('create-permission-modal-title');
    const permissionIdInput = document.getElementById('permission_id');
    const permissionNameInput = document.getElementById('permission_name');
    const permissionValueInput = document.getElementById('permission_value');
    const permissionOrderInput = document.getElementById('permission_order');

    // CREAR PERMISO
    const createBtn = document.getElementById('create-permission');
    if (createBtn) {
        createBtn.addEventListener('click', () => {
            modalTitle.innerText = 'Crear permiso';
            permissionIdInput.value = 'new';
            permissionNameInput.value = '';
            permissionValueInput.value = '';
            permissionOrderInput.value = '';
        });
    }

    // EDITAR PERMISO
    const editarBtns = document.querySelectorAll('.editar-permission');
    editarBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = e.currentTarget.id.split('editar-permission-')[1];

            const idEl = document.getElementById(`permission-id-${id}`);
            const nameEl = document.getElementById(`permission-name-${id}`);
            const valueEl = document.getElementById(`permission-value-${id}`);
            const orderEl = document.getElementById(`permission-order-${id}`);

            if (idEl && nameEl && valueEl && orderEl) {
                modalTitle.innerText = 'Editar permiso';
                permissionIdInput.value = idEl.value;
                permissionNameInput.value = nameEl.value;
                permissionValueInput.value = valueEl.value;
                permissionOrderInput.value = orderEl.value;
            } else {
                console.error(`Alguno de los elementos del permiso con ID ${id} no fue encontrado.`);
            }
        });
    });

    // BORRAR PERMISO
    const borrarBtns = document.querySelectorAll('.borrar-permission');
    borrarBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = e.currentTarget.id.split('borrar-permission-')[1];
            const nameEl = document.getElementById(`permission-name-${id}`);
            const borrarIdInput = document.getElementById('permission_borrar_id');
            const borrarTitle = document.getElementById('permission-borrar-title');

            if (nameEl && borrarIdInput && borrarTitle) {
                borrarIdInput.value = id;
                borrarTitle.innerText = `¿Seguro que quieres eliminar el permiso ${nameEl.value}?`;
            } else {
                console.error(`Elemento de nombre del permiso con ID ${id} no encontrado.`);
            }
        });
    });
});
