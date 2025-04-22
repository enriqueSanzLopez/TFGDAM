import { Conexiones } from '/static/scripts/main/conexiones.js';
const main = {
    template: `
        <div id="main-principal">
            <div class="main-conexiones"><conexiones></conexiones></div>
            <div class="d-flex flex-column justify-content-start align-items-center"></div>
        </div>
    `,
    data() {
        return {
            mensaje: 'Hola, Vue.js!',
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
    },
    mounted() {
    }
};
document.addEventListener("DOMContentLoaded", () => {
    Vue.createApp(main).mount('#app');
});
