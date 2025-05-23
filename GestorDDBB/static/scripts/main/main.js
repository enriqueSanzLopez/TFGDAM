import { Conexiones } from '/static/scripts/main/conexiones.js';
import { Busqueda } from '/static/scripts/main/select.js';
import { Consola } from '/static/scripts/main/console.js';
import { ErrorList } from '/static/scripts/main/errors.js';
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
                    />
            </div>
        </div>
    `,
    data() {
        return {
            mensaje: 'Hola, Vue.js!',
            currentConnection: null,
            currentTable: null,
            action: null
        };
    },
    components: {
        Conexiones,
        Busqueda,
        Consola,
        ErrorList
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
    },
    mounted() {
    }
};
document.addEventListener("DOMContentLoaded", () => {
    Vue.createApp(main).mount('#app');
});
