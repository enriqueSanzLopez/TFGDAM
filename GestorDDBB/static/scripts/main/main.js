import { Conexiones } from '/static/scripts/main/conexiones.js';
const main = {
    template: `
        <div id="main-principal">
            <div class="main-conexiones"><conexiones @buscar-tabla="handleBuscarTabla"></conexiones></div>
            <div class="d-flex flex-column justify-content-start align-items-center"></div>
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
        Conexiones
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
            //Mas codigo aqui...
        },
    },
    mounted() {
    }
};
document.addEventListener("DOMContentLoaded", () => {
    Vue.createApp(main).mount('#app');
});
