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
        <button type="button" class="btn btn-light btn-lg" data-bs-toggle="modal" data-bs-target="#conexion-modal">
            <i class="fa-solid fa-plug"></i>
        </button>
    </div>

    <ul>
        <li
            v-for="conexion in conexiones"
            :key="conexion.id"
            @contextmenu.prevent.stop="mostrarMenu($event, conexion)"
        >
            {{ conexion.host }} - {{ conexion.db_name }}
            <ul>
                <li
                    v-for="table in tables.filter(t => t.id_conexion === conexion.id)"
                    :key="table.nombre_tabla"
                    @contextmenu.prevent.stop="mostrarTableMenu($event, table)"
                >
                    {{ table.nombre_tabla }}
                </li>
            </ul>
        </li>
    </ul>
    <div
        v-if="menuVisible"
        ref="menu"
        class="menu-contextual"
        :style="{ top: menuY + 'px', left: menuX + 'px' }"
        @click.stop
    >
        <button type="button" @click="deleteConexion(conexionSeleccionada)">
            Desconectar <i class="fa-solid fa-xmark" style="color: red;"></i>
        </button>
    </div>
    <div
        v-if="menuTableVisible"
        ref="menuTable"
        class="menu-contextual"
        :style="{ top: menuTableY + 'px', left: menuTableX + 'px' }"
        @click.stop
    >
        <button type="button" @click="buscarEnTabla">
            Buscar <i class="fa-solid fa-magnifying-glass" style="color: blue;"></i>
        </button>
        <button type="button" v-if="editarPermission === true">
            Consola <i class="fa-solid fa-code" style="color: blue;"></i></i>
        </button>
    </div>
    `,
    data() {
        return {
            conexionLoading: false,
            conexionError: false,
            conexiones: [],
            tables: [],
            menuVisible: false,
            menuX: 0,
            menuY: 0,
            conexionSeleccionada: null,
            menuTableVisible: false,
            menuTableX: 0,
            menuTableY: 0,
            editarPermission: false,
            tableSeleccionada: null
        };
    },
    methods: {
        async addConnection() {
            const self = this;
            this.conexionLoading = true;
            this.conexionError = false;
            $.ajax({
                url: '/api/csrf/',
                type: 'GET',
                success: function (response) {
                    if (response.status === 'success') {
                        const csrfToken = response.token;
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
                            url: '/api/test-connection/',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify(data),
                            beforeSend: function (xhr) {
                                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                            },
                            success: function (response) {
                                if (response.status === 'success') {
                                    self.listarConexiones();
                                } else {
                                    console.error('Error en la conexión:', response.message);
                                }
                            },
                            error: function (xhr, status, error) {
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
        },
        async listarConexiones() {
            const self = this;
            $.ajax({
                url: '/api/csrf/',
                type: 'GET',
                success: function (response) {
                    if (response.status === 'success') {
                        const csrfToken = response.token;
                        const data = {
                            user: document.getElementById('apid').value,
                        };
                        $.ajax({
                            url: '/api/list-connections/',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify(data),
                            beforeSend: function (xhr) {
                                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                            },
                            success: function (response) {
                                if (response.status === 'success') {
                                    console.log('Resultados', response);
                                    self.conexiones = response.conexiones;
                                    self.listarTablas();
                                } else {
                                    console.error('Error en la conexión:', response.message);
                                }
                            },
                            error: function (xhr, status, error) {
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
        },
        mostrarMenu(event, conexion) {
            this.menuTableVisible = false;
            this.menuVisible = true;
            this.menuX = event.clientX;
            this.menuY = event.clientY;
            this.conexionSeleccionada = conexion;
        },
        cerrarMenu(event) {
            if (this.menuVisible && this.$refs.menu && !this.$refs.menu.contains(event.target)) {
                this.menuVisible = false;
            }
        },
        async deleteConexion(id) {
            const fakeTarget = document.createElement('div');
            document.body.appendChild(fakeTarget);
            const fakeEvent = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            Object.defineProperty(fakeEvent, 'target', { value: fakeTarget });

            this.cerrarMenu(fakeEvent);

            document.body.removeChild(fakeTarget);
            const self = this;
            $.ajax({
                url: '/api/csrf/',
                type: 'GET',
                success: function (response) {
                    if (response.status === 'success') {
                        const csrfToken = response.token;
                        const data = {
                            user: document.getElementById('apid').value,
                            id: id.id
                        };
                        console.log(data);
                        $.ajax({
                            url: '/api/delete-connection/',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify(data),
                            beforeSend: function (xhr) {
                                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                            },
                            success: function (response) {
                                if (response.status === 'success') {
                                    self.listarConexiones();
                                    self.menuVisible = false;
                                } else {
                                    console.error('Error en la conexión:', response.message);
                                }
                            },
                            error: function (xhr, status, error) {
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
        },
        async listarTablas() {
            const self = this;
            $.ajax({
                url: '/api/csrf/',
                type: 'GET',
                success: function (response) {
                    if (response.status === 'success') {
                        const csrfToken = response.token;
                        const data = {
                            user: document.getElementById('apid').value,
                        };
                        $.ajax({
                            url: '/api/list-tables/',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify(data),
                            beforeSend: function (xhr) {
                                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                            },
                            success: function (response) {
                                if (response.status === 'success') {
                                    console.log('Resultados', response);
                                    self.tables = response.tables
                                } else {
                                    console.error('Error en la conexión:', response.message);
                                }
                            },
                            error: function (xhr, status, error) {
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
        },
        mostrarTableMenu(event, table) {
            this.menuVisible = false;
            this.menuTableVisible = true;
            this.menuTableX = event.clientX;
            this.menuTableY = event.clientY;
            this.tableSeleccionada = table;
        },
        cerrarTableMenu(event) {
            if (this.menuTableVisible && this.$refs.menuTable && !this.$refs.menuTable.contains(event.target)) {
                this.menuTableVisible = false;
            }
        },
        cerrarTodosLosMenus(event) {
            const fueraMenuConexion = this.menuVisible && this.$refs.menu && !this.$refs.menu.contains(event.target);
            const fueraMenuTabla = this.menuTableVisible && this.$refs.menuTable && !this.$refs.menuTable.contains(event.target);

            if (fueraMenuConexion) {
                this.menuVisible = false;
            }

            if (fueraMenuTabla) {
                this.menuTableVisible = false;
            }
        },
        async checkEdicionPermiso() {
            const self = this;
            $.ajax({
                url: '/api/csrf/',
                type: 'GET',
                success: function (response) {
                    if (response.status === 'success') {
                        const csrfToken = response.token;
                        const data = {
                            user: document.getElementById('apid').value,
                        };
                        $.ajax({
                            url: '/api/edicion-permission/',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify(data),
                            beforeSend: function (xhr) {
                                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                            },
                            success: function (response) {
                                if (response.status === 'success') {
                                    console.log('Resultados', response);
                                    self.editarPermission = response.edicion
                                } else {
                                    console.error('Error en la conexión:', response.message);
                                }
                            },
                            error: function (xhr, status, error) {
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
        },
        async buscarEnTabla() {
            const fakeTarget = document.createElement('div');
            document.body.appendChild(fakeTarget);
            const fakeEvent = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            Object.defineProperty(fakeEvent, 'target', { value: fakeTarget });

            this.cerrarTableMenu(fakeEvent);

            document.body.removeChild(fakeTarget);
            this.$emit('buscar-tabla', {
                connectionId: this.tableSeleccionada.id_conexion,
                tableName: this.tableSeleccionada.nombre_tabla,
                action: 'select'
            });
        }
    },
    mounted() {
        document.getElementById('add-connection').addEventListener('click', () => {
            this.addConnection();
        });
        document.addEventListener('click', this.cerrarTodosLosMenus);
        this.listarConexiones();
        this.checkEdicionPermiso();
    }
};
