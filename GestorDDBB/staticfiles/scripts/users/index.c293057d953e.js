document.addEventListener('DOMContentLoaded', () => {
    const createUserBtn = document.getElementById('create-user');
    const saveChangesBtn = document.getElementById('save-changes');
    const changePasswordBtn = document.getElementById('change-password-button');

    const passwordInput = document.getElementById('password');
    const repeatPasswordInput = document.getElementById('repeat_password');
    const cambioPasswordInput = document.getElementById('cambio_password');
    const cambioRepeatInput = document.getElementById('cambio_repeat_password');

    const changePasswordTab = document.getElementById('change-password-tab');
    const formIdInput = document.getElementById('id');
    const cambioIdInput = document.getElementById('cambio_id');

    // CREAR USUARIO
    createUserBtn.addEventListener('click', () => {
        document.getElementById('create-user-form-tab').innerText = 'Crear usuario';
        formIdInput.value = 'new';
        cambioIdInput.value = 'new';

        document.getElementById('name').value = '';
        document.getElementById('real_name').value = '';
        document.getElementById('email').value = '';
        document.getElementById('group').selectedIndex = 0;

        passwordInput.style.display = 'block';
        repeatPasswordInput.style.display = 'block';
        passwordInput.value = '';
        repeatPasswordInput.value = '';

        changePasswordTab.style.display = 'none';

        saveChangesBtn.disabled = true;
    });

    // EDITAR USUARIO
    const ediciones = document.getElementsByClassName('editar');
    for (let btn of ediciones) {
        btn.addEventListener('click', (e) => {
            const id = e.currentTarget.id.split('editar-')[1];
            formIdInput.value = id;
            cambioIdInput.value = id;

            document.getElementById('create-user-form-tab').innerText = 'Editar usuario';
            document.getElementById('name').value = document.getElementById(`user-name-${id}`).value;
            document.getElementById('real_name').value = document.getElementById(`user-real_name-${id}`).value;
            document.getElementById('email').value = document.getElementById(`user-email-${id}`).value;
            document.getElementById('group').value = document.getElementById(`user-desc_group-${id}`).value;

            passwordInput.style.display = 'none';
            repeatPasswordInput.style.display = 'none';
            passwordInput.value = '';
            repeatPasswordInput.value = '';

            changePasswordTab.style.display = 'block';
            saveChangesBtn.disabled = false;
        });
    }

    // BORRAR USUARIO
    const borrarBtns = document.getElementsByClassName('borrar');
    for (let btn of borrarBtns) {
        btn.addEventListener('click', (e) => {
            const id = e.currentTarget.id.split('borrar-')[1];
            document.getElementById('borrar_id').value = id;
            document.getElementById('borrar-title').innerText = '¿Seguro que quieres eliminar a ' + document.getElementById(`user-name-${id}`).value + '?';
        });
    }

    // VALIDACIONES
    function validarUserForm() {
        const pwd = passwordInput.value;
        const rpt = repeatPasswordInput.value;
        saveChangesBtn.disabled = !(pwd && rpt && pwd === rpt);
    }

    function validarChangeForm() {
        const pwd = cambioPasswordInput.value;
        const rpt = cambioRepeatInput.value;
        changePasswordBtn.disabled = !(pwd && rpt && pwd === rpt);
    }

    passwordInput.addEventListener('input', validarUserForm);
    repeatPasswordInput.addEventListener('input', validarUserForm);
    cambioPasswordInput.addEventListener('input', validarChangeForm);
    cambioRepeatInput.addEventListener('input', validarChangeForm);
});
