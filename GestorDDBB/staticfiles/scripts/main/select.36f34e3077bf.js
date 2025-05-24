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
            <button type="button" class="btn btn-primary btn-lg" @click="downloadJSON()">JSON <i class="fa-solid fa-download"></i></button>
            <button type="button" class="btn btn-primary btn-lg" @click="downloadCSV()">CSV <i class="fa-solid fa-download"></i></button>
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
                                    self.registers = response.data
                                } else {
                                    self.$emit('error', String(response.message));
                                }
                            },
                            error: function (xhr, status, error) {
                                self.$emit('error', String(error));
                            }
                        });
                    } else {
                        self.$emit('error', String(response.message));
                        this.conexionError = true;
                    }
                },
                error: function (xhr, status, error) {
                    self.$emit('error', String(error));
                    this.conexionError = true;
                }
            });
        },
        async downloadJSON() {
            if (!this.registers.length) {
                alert("No hay datos para exportar.");
                return;
            }

            const jsonData = JSON.stringify(this.registers, null, 2);
            const blob = new Blob([jsonData], { type: "application/json" });
            const url = URL.createObjectURL(blob);

            const a = document.createElement("a");
            a.href = url;
            a.download = `registros_${this.currentTable}.json`;
            a.click();

            URL.revokeObjectURL(url);
        },
        async downloadCSV() {
            if (!this.registers.length) {
                alert("No hay datos para exportar.");
                return;
            }

            const keys = Object.keys(this.registers[0]);
            const csvRows = [];
            csvRows.push(keys.join(','));
            for (const row of this.registers) {
                const values = keys.map(key => {
                    const val = row[key];
                    const escaped = String(val).replace(/"/g, '""');
                    return `"${escaped}"`;
                });
                csvRows.push(values.join(','));
            }

            const csvContent = csvRows.join('\n');
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = `registros_${this.currentTable}.csv`;
            a.click();

            URL.revokeObjectURL(url);
        }
    },
    mounted() {
        this.buscarRegistros();
    }
};