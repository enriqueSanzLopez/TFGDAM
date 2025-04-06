try {
    document.getElementById('create-user').addEventListener('click', () => {
        document.getElementById('create-user-form-tab').innerText = 'Crear usuario';
        document.getElementById('id').value = 'new';
        document.getElementById('name').value = '';
        document.getElementById('real_name').value = '';
        document.getElementById('email').value = '';
        document.getElementById('password').style.display = 'block';
        document.getElementById('repeat_password').style.display = 'block';
        document.getElementById('password').value = '';
        document.getElementById('repeat_password').value = '';
        document.getElementById('change-password-tab').style.display = 'none';
        document.getElementById('save-changes').disabled = true;
    });

    let ediciones = document.getElementsByClassName('editar');
    for (let i = 0; i < ediciones.length; i++) {
        ediciones[i].addEventListener('click', (e) => {
            const id = e.target.id.split('editar-')[1];
            document.getElementById('create-user-form-tab').innerText = 'Editar usuario';
            document.getElementById('id').value = document.getElementById('user-id-' + id).value;
            document.getElementById('cambio_id').value = document.getElementById('user-id-' + id).value;
            document.getElementById('name').value = document.getElementById('user-name-' + id).value;
            document.getElementById('real_name').value = document.getElementById('user-real_name-' + id).value;
            document.getElementById('email').value = document.getElementById('user-email-' + id).value;
            document.getElementById('group').value = document.getElementById('user-desc_group-' + id).value;
            document.getElementById('password').style.display = 'none';
            document.getElementById('repeat_password').style.display = 'none';
            document.getElementById('password').value = '';
            document.getElementById('repeat_password').value = '';
            document.getElementById('change-password-tab').style.display = 'block';
            document.getElementById('save-changes').disabled = false;
        });
    }

    let borrar = document.getElementsByClassName('borrar');
    for (let i = 0; i < borrar.length; i++) {
        borrar[i].addEventListener('click', (e) => {
            const id = e.target.id.split('borrar-')[1];
            document.getElementById('borrar_id').value = id;
            document.getElementById('borrar-title').innerText='¿Seguro que quieres eliminar a '+document.getElementById('user-name-'+id).value+'?';
        });
    }
} catch (e) { }

try {
    function validarUserForm() {
        if (document.getElementById('password').value == '') {
            document.getElementById('save-changes').disabled = true;
        }
        else if (document.getElementById('password').value == document.getElementById('repeat_password').value) {
            document.getElementById('save-changes').disabled = false;
        } else {
            document.getElementById('save-changes').disabled = true;
        }
    }
    function validarChangeForm() {
        if (document.getElementById('cambio_password').value == '') {
            document.getElementById('save-changes').disabled = true;
        }
        else if (document.getElementById('cambio_password').value == document.getElementById('cambio_repeat_password').value) {
            document.getElementById('change-password-button').disabled = false;
        } else {
            document.getElementById('change-password-button').disabled = true;
        }
    }
    document.getElementById('password').addEventListener('input', () => {
        validarUserForm();
    });
    document.getElementById('repeat_password').addEventListener('input', () => {
        validarUserForm();
    });
    document.getElementById('cambio_password').addEventListener('input', () => {
        validarChangeForm();
    });
    document.getElementById('cambio_repeat_password').addEventListener('input', () => {
        validarChangeForm();
    });
    validarChangeForm();
} catch (e) { }