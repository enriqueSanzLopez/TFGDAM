import { Conexiones } from '/static/scripts/main/conexiones.js';
import { Busqueda } from '/static/scripts/main/select.js';
import { Consola } from '/static/scripts/main/console.js';
const main = {
    template: `
        <div id="main-principal">
            <div class="main-conexiones"><conexiones @buscar-tabla="handleBuscarTabla" @consola-tabla="handleConsola"></conexiones></div>
            <div class="d-flex flex-column justify-content-start align-items-center main overflow-auto">
                <busqueda
                    v-if="action === 'select'"
                    :key="currentConnection + '_' + currentTable"
                    :currentTable="currentTable"
                    :currentConnection="currentConnection"
                />
                <consola
                    v-if="action === 'console'"
                    :key="currentConnection + '_' + currentTable"
                    :currentTable="currentTable"
                    :currentConnection="currentConnection"
                    @error="handleError"
                    />
            </div>
        </div>
        <div 
            v-if="errors.length" 
            class="error-list position-fixed bg-white border rounded p-2 shadow-sm"
            >
            <div 
                v-for="error in errors" 
                :key="error.id" 
                class="d-flex justify-content-between align-items-center mb-2"
                >
                <div class="error-message text-break">{{ error.error }}</div>
                <button 
                    type="button" 
                    class="btn btn-sm btn-danger ms-2" 
                    @click="eliminarError(error.id)" 
                    aria-label="Eliminar error"
                    title="Eliminar error"
                    >
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
        </div>
    `,
    data() {
        return {
            mensaje: 'Hola, Vue.js!',
            currentConnection: null,
            currentTable: null,
            action: null,
            errors: []
        };
    },
    components: {
        Conexiones,
        Busqueda,
        Consola
    },
    computed: {
    },
    watch: {
    },
    methods: {
        async handleBuscarTabla({ connectionId, tableName, action }) {
            this.currentConnection = connectionId;
            this.currentTable = tableName;
            this.action = action;
        },
        async handleConsola({ connectionId, tableName, action }) {
            this.currentConnection = connectionId;
            this.currentTable = tableName;
            this.action = action;
        },
        async handleError({ error }) {
            console.log('Se intenta manejar el error: '+error)
            this.agregarError(error)
        },
        async eliminarError(id) {
            this.errors = this.errors.filter(e => e.id !== id);
        },
        async agregarError(mensaje) {
            const idUnico = Date.now() + Math.random();
            this.errors.push({ id: idUnico, error: mensaje });
        },
    },
    mounted() {
    }
};
document.addEventListener("DOMContentLoaded", () => {
    Vue.createApp(main).mount('#app');
});
