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
        <button type="button" class="btn btn-success btn-lg"><i class="fa-solid fa-search"></i></button>
        <button type="button" class="btn btn-primary btn-lg" @click="downloadJSON()">JSON <i class="fa-solid fa-download"></i></button>
        <button type="button" class="btn btn-primary btn-lg" @click="downloadCSV()">CSV <i class="fa-solid fa-download"></i></button>
    </div>
    <textarea v-model="consola" name="codigo" id="codigo" rows="10" class="form-control" placeholder="Código..."></textarea>
    <div class="resultados d-flex flex-column flex-grow-1">
        <p>Resultados</p>
        <div class="result-registers flex-grow-1 overflow-auto"></div>
    </div>
    `,
    data() {
        return {
            registers: [],
            consola: '',
            mostrarFiltros: false,
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
                        console.log('Datos a enviar a la API de consola', data);
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
        },
    },
    mounted() {
    }
};