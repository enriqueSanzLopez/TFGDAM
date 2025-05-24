document.addEventListener('DOMContentLoaded', () => {
    const groupModalTitle = document.getElementById('create-group-modal-title');
    const groupIdInput = document.getElementById('group_id');
    const groupNameInput = document.getElementById('group_name');
    const groupSaveBtn = document.getElementById('group-save-changes');
    const permissionCheckboxes = document.querySelectorAll('input[name="permissions"]');

    // CREAR GRUPO
    const createGroupBtn = document.getElementById('create-group');
    if (createGroupBtn) {
        createGroupBtn.addEventListener('click', () => {
            groupModalTitle.innerText = 'Crear grupo';
            groupIdInput.value = 'new';
            groupNameInput.value = '';
            permissionCheckboxes.forEach(cb => cb.checked = false);
        });
    }

    // EDITAR GRUPO
    const editarBtns = document.querySelectorAll('.editar-group');
    editarBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = e.currentTarget.id.split('editar-group-')[1];
            const nameEl = document.getElementById(`group-name-${id}`);
            const permsEl = document.getElementById(`permissions-${id}`);

            if (nameEl && permsEl) {
                groupModalTitle.innerText = 'Editar grupo';
                groupIdInput.value = id;
                groupNameInput.value = nameEl.value;

                const permisos = permsEl.value.split(',').map(p => p.trim());
                permissionCheckboxes.forEach(cb => {
                    cb.checked = permisos.includes(cb.value);
                });
            } else {
                console.error(`No se encontraron elementos del grupo con ID ${id}`);
            }
        });
    });

    // BORRAR GRUPO
    const borrarBtns = document.querySelectorAll('.borrar-group');
    borrarBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = e.currentTarget.id.split('borrar-group-')[1];
            const nameEl = document.getElementById(`group-name-${id}`);
            if (nameEl) {
                document.getElementById('group_borrar_id').value = id;
                document.getElementById('group-borrar-title').innerText =
                    `¿Seguro que quieres eliminar el grupo ${nameEl.value}?`;
            } else {
                console.error(`Elemento con ID group-name-${id} no encontrado.`);
            }
        });
    });
});
