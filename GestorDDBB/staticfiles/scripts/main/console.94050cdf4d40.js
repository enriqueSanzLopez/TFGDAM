export const Consola = {
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
        <button type="button" class="btn btn-primary btn-lg" @click="downloadJSON()">JSON <i class="fa-solid fa-download"></i></button>
        <button type="button" class="btn btn-primary btn-lg" @click="downloadCSV()">CSV <i class="fa-solid fa-download"></i></button>
    </div>
    <textarea v-model="consola" name="codigo" id="codigo" rows="10" class="form-control" placeholder="Código..."></textarea>
    <div class="resultados d-flex flex-column flex-grow-1">
        <p>Resultados</p>
        <div class="result-registers flex-grow-1 overflow-auto">
            <table v-if="responseType === 'select'" class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th v-for="(value, key) in registers[0]" :key="key">{{ key }}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in registers" :key="index">
                        <td v-for="(value, key) in item" :key="key">{{ value }}</td>
                    </tr>
                </tbody>
            </table>
            <pre v-else-if="responseType === 'command'" class="p-2 bg-light border rounded">
                {{ formatRegisters(registers) }}
            </pre>
        </div>
    </div>
    `,
    data() {
        return {
            registers: [],
            consola: '',
            mostrarFiltros: false,
            responseType: '',
        };
    },
    methods: {
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
                            query: self.consola,
                            connection_id: self.currentConnection,
                        };
                        $.ajax({
                            url: '/api/consola/',
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify(data),
                            beforeSend: function (xhr) {
                                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                            },
                            success: function (response) {
                                if (response.status === 'success') {
                                    self.registers = response.data
                                    self.responseType = response.type || (Array.isArray(response.data) ? 'select' : 'command');
                                } else {
                                    self.$emit('error', String(response.message));
                                }
                            },
                            error: function (xhr, status, error) {
                                self.$emit('error', String(error));
                            }
                        });
                    } else {
                        self.$emit('error', String(error));
                        this.conexionError = true;
                    }
                },
                error: function (xhr, status, error) {
                    self.$emit('error', String(error));
                    this.conexionError = true;
                }
            });
        },
        async formatRegisters(data) {
            if (typeof data === 'string') return data;
            try {
                return JSON.stringify(data, null, 2);
            } catch (e) {
                return String(data);
            }
        },
    },
    mounted() {
    }
};