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
        <div class="busqueda">
            <h3>Búsqueda en tabla</h3>
            <p>Tabla: {{ currentTable }}</p>
            <p>Conexión ID: {{ currentConnection }}</p>
            <!-- Aquí puedes añadir inputs, filtros, etc -->
        </div>
    `
};