export const Busqueda = {
    props: {
        currentTable: {
            type: String,
            required: true
        },
        currentConnection: {
            type: [String, Number],
            required: true
        }
    },
    template: `
        <div class="acciones d-flex flex-row justify-content-between align-items-center">
            <button type="button" class="btn btn-success btn-lg" @click="buscarRegistros()"><i class="fa-solid fa-search"></i></button>
            <button type="button" class="btn btn-secondary btn-lg" @click="toggleFiltros"><i class="fa-solid fa-filter"></i></button>
            <button type="button" class="btn btn-primary btn-lg">JSON <i class="fa-solid fa-download"></i></button>
            <button type="button" class="btn btn-primary btn-lg">CSV <i class="fa-solid fa-download"></i></button>
        </div>
        <transition @enter="enter"
            @leave="leave">
            <div class="filtros mb-3" v-show="mostrarFiltros">
                <label>Columnas</label>
                <input type="text" class="form-control" v-model="columnas" placeholder="Columnas...">
                <label>Filtros</label>
                <input type="text" class="form-control" v-model="filtros" placeholder="Filtros...">
                <label>Orden</label>
                <input type="text" class="form-control" v-model="orden" placeholder="Orden...">
            </div>
        </transition>
        <div class="resultados d-flex flex-column flex-grow-1">
            <p>Resultados</p>
            <div class="result-registers flex-grow-1 overflow-auto">
                <table class="table table-bordered table-hover table-striped table-sm">
                    <thead v-if="registers.length">
                        <tr>
                            <th v-for="(value, key) in registers[0]" :key="key">
                                {{ key }}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(row, rowIndex) in registers" :key="rowIndex">
                            <td v-for="(value, key) in row" :key="key">
                                {{ value }}
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div v-if="!registers.length" class="text-muted text-center py-3">
                    No hay datos disponibles.
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            registers: [],
            columnas: '*',
            filtros: '',
            orden: '',
            mostrarFiltros: false,
        };
    },
    methods: {
        async toggleFiltros() {
            this.mostrarFiltros = !this.mostrarFiltros;
        },
        enter(el) {
            el.style.boxSizing = 'border-box';
            el.style.overflow = 'hidden';
            el.style.height = '0';
            el.style.opacity = '0';
            el.offsetHeight; // trigger reflow

            const height = el.scrollHeight + 'px';
            el.style.transition = 'height 0.3s ease, opacity 0.3s ease';
            el.style.height = height;
            el.style.opacity = '1';

            // Limpieza al terminar
            el.addEventListener('transitionend', function handler() {
                el.style.height = 'auto';
                el.style.overflow = '';
                el.removeEventListener('transitionend', handler);
            });
        },

        leave(el) {
            el.style.boxSizing = 'border-box';
            el.style.height = el.scrollHeight + 'px';
            el.style.opacity = '1';
            el.offsetHeight; // trigger reflow

            el.style.transition = 'height 0.3s ease, opacity 0.3s ease';
            el.style.height = '0';
            el.style.opacity = '0';
            el.style.overflow = 'hidden';
        },
        async buscarRegistros() {
            const self = this;
            $.ajax({
                url: '/api/csrf/',
                type: 'GET',
                success: function (response) {
                    if (response.status === 'success') {
                        const csrfToken = response.token;
                        const data = {
                            user: document.getElementById('apid').value,
                            columns: self.columnas,
                            filters: self.filtros,
                            ordering: self.orden,
                            connection_id: self.currentConnection,
                            table: self.currentTable
                        };
                        console.log('Datos a enviar a la API de registros', data);
                        $.ajax({
                            url: '/api/list-registers/',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify(data),
                            beforeSend: function (xhr) {
                                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                            },
                            success: function (response) {
                                if (response.status === 'success') {
                                    console.log('Resultados', response);
                                    self.registers = response.data
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
        }
    },
    mounted() {
        this.buscarRegistros();
    }
};