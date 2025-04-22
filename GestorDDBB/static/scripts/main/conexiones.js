class ConnectionData {
    constructor(token, host, db_name, name) {
        this.id = this.generateId();
        this.token = token;
        this.host = host;
        this.db_name = db_name;
        this.name = name;
    }
};

export const Conexiones = {
    template: `
    <div class="d-flex flex-row justify-content-end align-items-center flex-wrap">
        <button type="button" class="btn btn-light btn-lg" data-bs-toggle="modal" data-bs-target="#conexion-modal"><i class="fa-solid fa-plug"></i></button>
        <!--<button type="button" class="btn btn-light"><i class="fa-solid fa-plug-circle-xmark"></i></button>-->
    </div>
    <ul>
        <li v-for="conexion in conexiones" :key="conexion.id">{{conexion.host}} - {{conexion.db_name}}</li>
    </ul>
    `,
    data() {
        return {
            conexionLoading: false,
            conexionError: false,
            conexiones: []
        };
    },
    methods: {
        async addConnection() {
            this.conexionLoading = true;
            this.conexionError = false;
            $.ajax({
                url: '/api/csrf',
                type: 'GET',
                success: function (response) {
                    if (response.status === 'success') {
                        const csrfToken = response.token;
                        console.log('Token CSRF recibido:', csrfToken);
                        const data = {
                            db_engine: document.getElementById('conexion-tipo').value,
                            db_name: document.getElementById('conexion-database').value,
                            user: document.getElementById('apid').value,
                            name: document.getElementById('conexion-name').value,
                            password: document.getElementById('conexion-password').value,
                            host: document.getElementById('conexion-host').value,
                            port: document.getElementById('conexion-port').value
                        };
                        $.ajax({
                            url: '/api/test-connection',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify(data),
                            beforeSend: function(xhr) {
                                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                            },
                            success: function(response) {
                                if (response.status === 'success') {
                                    console.log('Conexión exitosa. Token:', response.token);
                                    const nuevaConexion = new ConnectionData(response.token, data.host, data.db_name, data.name);
                                    this.conexiones.push(nuevaConexion);
                                } else {
                                    console.error('Error en la conexión:', response.message);
                                }
                            },
                            error: function(xhr, status, error) {
                                console.error('Error durante la solicitud:', error);
                            }
                        });
                    } else {
                        console.error('Error al recuperar el token CSRF:', response.message);
                        this.conexionError = true;
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Ocurrió un error durante la solicitud:', error);
                    this.conexionError = true;
                }
            });
        }
    }
};
